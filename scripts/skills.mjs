#!/usr/bin/env node
// Validates every skill and builds index.json, the listing the ScribeKey app reads.
//
//   node scripts/skills.mjs check [--base <git ref>]   validate; fail if index.json is stale
//   node scripts/skills.mjs build                       rewrite index.json
//
// No dependencies: the frontmatter accepted here is a deliberate subset of YAML (plain, quoted and
// folded `>-` scalars, one nested `metadata` map) that every Agent Skills client reads the same way.

import { execFileSync } from "node:child_process";
import { readFileSync, readdirSync, statSync, writeFileSync, existsSync } from "node:fs";
import { join, relative } from "node:path";

const REPO = "scribekey-app/scribekey-skills";
const BRANCH = "main";
const ROOT = new URL("..", import.meta.url).pathname;
const SKILLS_DIR = join(ROOT, "skills");
const INDEX = join(ROOT, "index.json");

// Limits the app enforces on import (enhancement/presets/SkillImport.kt and SkillPackage.kt).
const MAX_NAME = 64;
const MAX_DESCRIPTION = 1024;
const MAX_BODY = 20000;
const MAX_FILES_CHARS = 200000;
const NAME = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const SEMVER = /^\d+\.\d+\.\d+$/;
const PACKAGE = /^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)+$/;
const TOP_KEYS = new Set(["name", "description", "license", "compatibility", "metadata", "allowed-tools"]);
const SCRIBEKEY_KEYS = new Set(["scribekey-title", "scribekey-apps", "scribekey-categories"]);
// Kinds of app ScribeKey can find on a phone (AppCategory in enhancement/presets/SkillImport.kt).
const CATEGORIES = new Set(["email", "messaging"]);
const KEPT_FOLDERS = ["references/", "assets/"];

/** Splits a SKILL.md into its frontmatter lines and body; throws on a missing fence. */
function split(text) {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  if (lines[0] !== "---") throw new Error("must start with a --- line");
  const end = lines.indexOf("---", 1);
  if (end < 0) throw new Error("frontmatter is never closed with ---");
  return { front: lines.slice(1, end), body: lines.slice(end + 1).join("\n").trim() };
}

function scalar(raw) {
  const v = raw.trim();
  if (v.startsWith('"')) {
    if (!v.endsWith('"') || v.length < 2) throw new Error(`unclosed quote: ${v}`);
    return JSON.parse(v);
  }
  if (v.startsWith("'")) {
    if (!v.endsWith("'") || v.length < 2) throw new Error(`unclosed quote: ${v}`);
    return v.slice(1, -1).replace(/''/g, "'");
  }
  if (/\s#/.test(v)) throw new Error(`comments are not allowed in values: ${v}`);
  if (/: /.test(v)) throw new Error(`quote a value that contains ": ": ${v}`);
  return v;
}

/** Reads `key: value` lines at [indent], with `>-` folded blocks and one nested map. */
function parseMap(lines, start, indent) {
  const out = {};
  let i = start;
  while (i < lines.length) {
    const line = lines[i];
    if (line.trim() === "") { i++; continue; }
    const lead = line.length - line.trimStart().length;
    if (lead < indent) break;
    if (lead > indent) throw new Error(`unexpected indent: "${line}"`);
    const m = /^([A-Za-z0-9_-]+):(?: (.*))?$/.exec(line.trim());
    if (!m) throw new Error(`expected "key: value": "${line}"`);
    const [, key, rest = ""] = m;
    if (key in out) throw new Error(`duplicate key: ${key}`);
    i++;
    if (rest.trim() === ">-" || rest.trim() === ">") {
      const block = [];
      while (i < lines.length && (lines[i].trim() === "" || lines[i].length - lines[i].trimStart().length > indent)) {
        block.push(lines[i].trim());
        i++;
      }
      out[key] = block.filter(Boolean).join(" ");
    } else if (rest.trim() === "") {
      const child = parseMap(lines, i, indent + 2);
      out[key] = child.map;
      i = child.next;
    } else {
      out[key] = scalar(rest);
    }
  }
  return { map: out, next: i };
}

function parseSkill(text) {
  const { front, body } = split(text);
  const { map, next } = parseMap(front, 0, 0);
  if (next < front.length) throw new Error("unreadable frontmatter");
  return { fields: map, body };
}

function packages(value) {
  return (value ?? "").split(/[\s,]+/).filter(Boolean);
}

function files(dir) {
  return readdirSync(dir).flatMap((entry) => {
    const path = join(dir, entry);
    return statSync(path).isDirectory() ? files(path) : [path];
  });
}

function isText(buffer) {
  if (buffer.includes(0)) return false;
  try {
    new TextDecoder("utf-8", { fatal: true }).decode(buffer);
    return true;
  } catch {
    return false;
  }
}

function semverGreater(a, b) {
  const pa = a.split(".").map(Number);
  const pb = b.split(".").map(Number);
  for (let i = 0; i < 3; i++) if (pa[i] !== pb[i]) return pa[i] > pb[i];
  return false;
}

function gitShow(ref, path) {
  try {
    return execFileSync("git", ["show", `${ref}:${path}`], { cwd: ROOT, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
  } catch {
    return null;
  }
}

/** Every problem with one skill folder, as lines; empty when it is fine. */
function validate(folder, base) {
  const problems = [];
  const dir = join(SKILLS_DIR, folder);
  const skillPath = join(dir, "SKILL.md");
  if (!existsSync(skillPath)) return { problems: ["has no SKILL.md"] };
  let skill;
  try {
    skill = parseSkill(readFileSync(skillPath, "utf8"));
  } catch (e) {
    return { problems: [`SKILL.md: ${e.message}`] };
  }
  const { fields, body } = skill;
  const meta = typeof fields.metadata === "object" ? fields.metadata : {};
  for (const key of Object.keys(fields)) if (!TOP_KEYS.has(key)) problems.push(`unknown top-level key "${key}"`);
  if (fields.metadata !== undefined && typeof fields.metadata !== "object") problems.push("metadata must be a map");
  for (const [key, value] of Object.entries(meta)) {
    if (typeof value !== "string") problems.push(`metadata.${key} must be a string`);
    if (key.startsWith("scribekey-") && !SCRIBEKEY_KEYS.has(key)) problems.push(`unknown ScribeKey key metadata.${key}`);
  }

  const name = fields.name;
  if (!name) problems.push("name is missing");
  else {
    if (name.length > MAX_NAME) problems.push(`name is longer than ${MAX_NAME} characters`);
    if (!NAME.test(name)) problems.push("name must be lowercase letters, digits and single hyphens");
    if (name !== folder) problems.push(`name "${name}" must match its folder "${folder}"`);
  }
  const description = fields.description ?? "";
  if (!description.trim()) problems.push("description is missing");
  if (description.length > MAX_DESCRIPTION) problems.push(`description is longer than ${MAX_DESCRIPTION} characters`);
  if (!body) problems.push("the body has no instructions");
  if (body.length > MAX_BODY) problems.push(`the body is longer than ${MAX_BODY} characters`);
  if (fields.license !== "MIT") problems.push('license must be "MIT"');
  if (!SEMVER.test(meta.version ?? "")) problems.push('metadata.version must be "MAJOR.MINOR.PATCH"');
  for (const pkg of packages(meta["scribekey-apps"])) {
    if (!PACKAGE.test(pkg)) problems.push(`"${pkg}" in metadata.scribekey-apps is not an Android package name`);
  }
  for (const category of packages(meta["scribekey-categories"])) {
    if (!CATEGORIES.has(category)) {
      problems.push(`"${category}" in metadata.scribekey-categories is not one of: ${[...CATEGORIES].join(", ")}`);
    }
  }

  const extra = files(dir).map((p) => relative(dir, p)).filter((p) => p !== "SKILL.md");
  let textChars = 0;
  for (const path of extra) {
    if (!KEPT_FOLDERS.some((f) => path.startsWith(f))) {
      problems.push(`${path}: only SKILL.md, references/ and assets/ are allowed (ScribeKey never runs scripts)`);
      continue;
    }
    const buffer = readFileSync(join(dir, path));
    if (!isText(buffer)) problems.push(`${path}: only UTF-8 text files are allowed`);
    textChars += buffer.toString("utf8").length;
  }
  if (textChars > MAX_FILES_CHARS) problems.push(`bundled files are over ${MAX_FILES_CHARS} characters`);

  // A changed skill needs a higher version, or nobody is offered the update.
  if (base && SEMVER.test(meta.version ?? "")) {
    const changed = [ "SKILL.md", ...extra ].some((p) => {
      const before = gitShow(base, `skills/${folder}/${p}`);
      return before !== null && before !== readFileSync(join(dir, p), "utf8");
    }) || [...gitFiles(base, folder)].some((p) => !extra.includes(p) && p !== "SKILL.md");
    const before = gitShow(base, `skills/${folder}/SKILL.md`);
    if (changed && before !== null) {
      let oldVersion = null;
      try { oldVersion = parseSkill(before).fields.metadata?.version ?? null; } catch { /* unreadable before: any version is new */ }
      if (oldVersion && !semverGreater(meta.version, oldVersion)) {
        problems.push(`changed since ${base} but metadata.version is still ${meta.version}; bump it above ${oldVersion}`);
      }
    }
  }
  return { problems, fields, meta, extra };
}

function gitFiles(base, folder) {
  try {
    const out = execFileSync("git", ["ls-tree", "-r", "--name-only", base, `skills/${folder}/`], { cwd: ROOT, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
    return new Set(out.split("\n").filter(Boolean).map((p) => p.slice(`skills/${folder}/`.length)));
  } catch {
    return new Set();
  }
}

function folders() {
  return readdirSync(SKILLS_DIR).filter((f) => statSync(join(SKILLS_DIR, f)).isDirectory()).sort();
}

function buildIndex(results) {
  const skills = results.map(({ folder, fields, meta, extra }) => {
    const entry = {
      name: fields.name,
      title: meta["scribekey-title"] ?? humanise(fields.name),
      description: fields.description,
      version: meta.version,
      // A lone SKILL.md is one raw request; a folder with files goes through the folder link.
      url: extra.length === 0
        ? `skills/${folder}/SKILL.md`
        : `https://github.com/${REPO}/tree/${BRANCH}/skills/${folder}`,
    };
    const apps = packages(meta["scribekey-apps"]);
    if (apps.length) entry.apps = apps;
    const categories = packages(meta["scribekey-categories"]);
    if (categories.length) entry.categories = categories;
    return entry;
  });
  return JSON.stringify({ name: "ScribeKey skills", skills }, null, 2) + "\n";
}

function humanise(name) {
  const words = name.replace(/-/g, " ");
  return words.charAt(0).toUpperCase() + words.slice(1);
}

function main() {
  const [command, ...args] = process.argv.slice(2);
  const baseAt = args.indexOf("--base");
  const base = baseAt >= 0 ? args[baseAt + 1] : null;
  if (command !== "check" && command !== "build") {
    console.error("usage: node scripts/skills.mjs check [--base <ref>] | build");
    process.exit(2);
  }
  const results = folders().map((folder) => ({ folder, ...validate(folder, command === "check" ? base : null) }));
  let failed = false;
  for (const { folder, problems } of results) {
    for (const problem of problems) {
      console.error(`skills/${folder}: ${problem}`);
      failed = true;
    }
  }
  if (failed) process.exit(1);
  const index = buildIndex(results);
  if (command === "build") {
    writeFileSync(INDEX, index);
    console.log(`Wrote index.json with ${results.length} skills`);
    return;
  }
  const current = existsSync(INDEX) ? readFileSync(INDEX, "utf8") : "";
  if (current !== index) {
    console.error("index.json is out of date. Run: node scripts/skills.mjs build");
    process.exit(1);
  }
  console.log(`${results.length} skills OK`);
}

main();
