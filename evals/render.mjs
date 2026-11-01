// Renders every diagram output in a run.py results file with Pele, as ScribeKey does, and
// measures how it would read on a phone.
//
// Usage: node evals/render.mjs <results.json> <out dir>
// Setup, once: npm ci --prefix evals (pins pele 1.13.0, the app's bundled copy, and resvg for PNGs)
// Writes <out dir>/rendered.json (one record per run) and <out dir>/png/<id>-<rep>.png, drawn at a
// 360dp phone width and 3x density, as DocumentDiagram fits it. Exits 1 when a fixture renders other than its `render` says.
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import * as pele from 'pele';
import { Resvg } from '@resvg/resvg-js';

const [resultsPath, out] = process.argv.slice(2);
if (!resultsPath || !out) {
  console.error('Usage: node evals/render.mjs <results.json> <out dir>');
  process.exit(2);
}

// app/src/main/java/app/scribekey/render/mermaid/MermaidRenderer.kt, peleOptionsJson and precheck.
const MAX_SOURCE_CHARS = 50_000;
const OPTIONS = { links: false, images: false, limit: MAX_SOURCE_CHARS, maxEdges: 5_000, outputLimit: 2_000_000,
  // Not passed by the app today; set PELE_MAX_WIDTH=360 to see what Pele's reflow would change.
  ...(process.env.PELE_MAX_WIDTH ? { maxWidth: Number(process.env.PELE_MAX_WIDTH) } : {}) };
// DocumentDiagram.kt fits the drawing to the page's width, scaling it up or down, so a wide
// diagram's text shrinks with it; a phone page is about 360dp.
const PHONE_DP = 360;
const MIN_SP = 11;

const skillsDir = join(dirname(fileURLToPath(import.meta.url)), '..', 'skills');
const diagramSkills = new Set(readdirSync(skillsDir).filter((s) => {
  try { return /scribekey-presentation:\s*diagram/.test(readFileSync(join(skillsDir, s, 'SKILL.md'), 'utf8')); }
  catch { return false; }
}));

const skillOf = (id) => id.replace(/-\d+$/, '');
const longest = (labels) => Math.max(0, ...labels.map((l) => [...String(l).trim()].length));

// Longest path (in nodes) and widest fan-out of a directed graph; a cycle is cut where it closes.
function graphShape(ids, edges) {
  const next = new Map(ids.map((i) => [i, []]));
  for (const [a, b] of edges) (next.get(a) ?? next.set(a, []).get(a)).push(b);
  const memo = new Map();
  const depth = (n, seen) => {
    if (memo.has(n)) return memo.get(n);
    if (seen.has(n)) return 0;
    seen.add(n);
    const d = 1 + Math.max(0, ...(next.get(n) ?? []).map((m) => depth(m, seen)));
    seen.delete(n);
    memo.set(n, d);
    return d;
  };
  return {
    depth: Math.max(0, ...[...next.keys()].map((n) => depth(n, new Set()))),
    branching: Math.max(0, ...[...next.values()].map((v) => v.length)),
  };
}

function shape(model) {
  if (model.type === 'flowchart') {
    const nodes = [...model.nodes.values()];
    const edges = model.edges.map((e) => [e.start, e.end]);
    return { nodes: nodes.length, edges: edges.length, maxLabel: longest([...nodes.map((n) => n.text ?? ''), ...model.edges.map((e) => e.text)]),
      ...graphShape(nodes.map((n) => n.id), edges) };
  }
  if (model.type === 'mindmap') {
    const root = model.nodes[0];
    const all = [];
    const walk = (n, level) => { all.push({ n, level }); n.children.forEach((c) => walk(c, level + 1)); };
    if (root) walk(root, 1);
    return { nodes: all.length, edges: Math.max(0, all.length - 1), maxLabel: longest(all.map((a) => a.n.descr)),
      depth: Math.max(0, ...all.map((a) => a.level)), branching: Math.max(0, ...all.map((a) => a.n.children.length)) };
  }
  if (model.type === 'timeline') {
    const events = model.periods.flatMap((p) => p.events);
    return { nodes: events.length, edges: Math.max(0, model.periods.length - 1),
      maxLabel: longest([model.title ?? '', ...model.periods.map((p) => p.text), ...events]),
      depth: model.periods.length, branching: Math.max(0, ...model.periods.map((p) => p.events.length)) };
  }
  return {};
}

// resvg has no CSS custom properties; inline them the way the app's sandbox path does
// (MermaidSvgDrawing.inlineCssVariables), and take color-mix's first colour.
function inlineCss(svg) {
  const declared = new Map();
  for (const m of svg.matchAll(/(?<![\w-])(--[\w-]+)\s*:\s*([^;"}]+)/g)) if (!declared.has(m[1])) declared.set(m[1], m[2].trim());
  for (let i = 0; i < 4; i++) {
    const next = svg.replace(/var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*))?\)/g, (_, n, fb) => declared.get(n) ?? (fb ?? '').trim());
    if (next === svg) break;
    svg = next;
  }
  return svg.replace(/color-mix\(in \w+,\s*([^,\s]+)[^)]*\)/g, '$1');
}

function renderOne(source) {
  if (source.length > MAX_SOURCE_CHARS) return { ok: false, code: 'limit', error: 'source over the size limit' };
  try {
    const r = pele.render(source, OPTIONS);
    const [, , w, h] = r.svg.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);
    const fontPx = Number(r.svg.match(/font:(\d+(?:\.\d+)?)px/)?.[1] ?? 16);
    const scale = PHONE_DP / w;
    const textSp = +(fontPx * scale).toFixed(1);
    return { ok: true, type: r.type, svg: r.svg, width: w, height: h, aspect: +(w / h).toFixed(2), textSp,
      smallText: textSp < MIN_SP, tall: h * scale > 2 * 640, ...shape(pele.parse(source, OPTIONS)) };
  } catch (e) {
    return { ok: false, code: e?.code ?? 'error', error: String(e?.message ?? e) };
  }
}

const runs = JSON.parse(readFileSync(resultsPath, 'utf8')).filter((r) => diagramSkills.has(skillOf(r.id)) && !r.error);
mkdirSync(join(out, 'png'), { recursive: true });
const records = [];
let mismatches = 0;
for (const run of runs) {
  const { svg, ...rec } = renderOne((run.output ?? '').trim());
  if (svg) {
    const zoom = (3 * PHONE_DP) / rec.width;
    const png = new Resvg(inlineCss(svg), { fitTo: { mode: 'zoom', value: zoom }, background: '#ffffff',
      font: { loadSystemFonts: true, sansSerifFamily: 'Helvetica' } }).render().asPng();
    rec.png = join(out, 'png', `${run.id}-${run.rep}.png`);
    writeFileSync(rec.png, png);
  }
  if ('render' in run && run.render !== rec.ok) {
    mismatches++;
    console.log(`MISMATCH ${run.id}-${run.rep}: expected render ${run.render}, got ${rec.ok}${rec.error ? ` (${rec.error})` : ''}`);
  }
  records.push({ id: run.id, rep: run.rep, ...rec });
}
writeFileSync(join(out, 'rendered.json'), JSON.stringify(records, null, 1));

const bySkill = {};
for (const r of records) {
  const s = (bySkill[skillOf(r.id)] ??= { runs: 0, ok: 0, smallText: 0, tall: 0, over25: 0 });
  s.runs++;
  if (r.ok) { s.ok++; s.smallText += r.smallText; s.tall += r.tall; s.over25 += r.nodes > 25; }
}
console.log('RENDER  skill: rendered  small text <11sp  taller than 2 screens  over 25 nodes');
for (const [s, v] of Object.entries(bySkill)) console.log(`  ${s}: ${v.ok}/${v.runs}  ${v.smallText}  ${v.tall}  ${v.over25}`);
const failed = records.filter((r) => !r.ok);
if (failed.length) console.log('render fails:', failed.map((r) => `${r.id}-${r.rep} (${r.code}: ${r.error.split('\n')[0].slice(0, 80)})`).join('; '));
console.log(`PNGs in ${join(out, 'png')}`);
process.exit(mismatches ? 1 : 0);
