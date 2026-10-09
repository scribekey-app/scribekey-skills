"""Sends every case build.py wrote to an OpenAI-compatible chat endpoint, the way ScribeKey does.

Usage: python3 evals/run.py <prompts dir from build.py> <results.json> [repeats]
Environment: OPENAI_API_KEY; MODEL (default gpt-5-nano, ScribeKey's default); EFFORT (default
minimal, what ScribeKey sends to gpt-5 nano and mini); BASE_URL (default https://api.openai.com/v1).
Small models vary between runs, so repeat each case (3 is a useful default) and compare rates.
"""
import concurrent.futures
import glob
import json
import os
import sys
import time
import urllib.request

src, out = sys.argv[1], sys.argv[2]
repeats = int(sys.argv[3]) if len(sys.argv) > 3 else 3
model = os.environ.get("MODEL", "gpt-5-nano")
base = os.environ.get("BASE_URL", "https://api.openai.com/v1").rstrip("/")
cases = [c for f in sorted(glob.glob(f"{src}/*.json")) for c in json.load(open(f))]


def call(job):
    case, rep = job
    body = {"model": model, "messages": [
        {"role": "system", "content": case["system"]}, {"role": "user", "content": case["user"]}]}
    if model.startswith(("gpt-5", "o")):
        body["max_completion_tokens"] = 2048
        body["reasoning_effort"] = os.environ.get("EFFORT", "minimal")
    else:
        body["max_tokens"] = 2048
    request = urllib.request.Request(f"{base}/chat/completions", json.dumps(body).encode(), {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', '')}"})
    error = None
    for _ in range(3):
        try:
            start = time.time()
            reply = json.load(urllib.request.urlopen(request, timeout=120))
            return {"id": case["id"], "rep": rep, "seconds": round(time.time() - start, 2),
                    "output": reply["choices"][0]["message"].get("content")}
        except Exception as e:  # noqa: BLE001 - a failed case is recorded, not fatal
            error = str(e)
    return {"id": case["id"], "rep": rep, "error": error}


with concurrent.futures.ThreadPoolExecutor(8) as pool:
    results = list(pool.map(call, [(c, r) for c in cases for r in range(repeats)]))
json.dump(results, open(out, "w"), indent=1, ensure_ascii=False)
print(f"{len(results)} runs on {model}, {sum('error' in r for r in results)} errors")
