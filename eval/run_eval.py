from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Iterable, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def read_jsonl(path: str) -> Iterable[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Invalid JSON at {path}:{line_no} -> {e}") from e


def write_jsonl(path: str, obj: Dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def http_post_json(url: str, payload: Dict[str, Any], timeout_sec: float) -> Tuple[int, Dict[str, Any]]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = Request(
        url=url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(req, timeout=timeout_sec) as resp:
            status = resp.status
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                data = {"_raw": raw}
            return status, data

    except HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace") if e.fp else ""
        try:
            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            data = {"_raw": raw}
        return e.code, data

    except URLError as e:
        return 0, {"error": {"code": "NETWORK_ERROR", "message": str(e)}}


def now_ms() -> int:
    return int(time.time() * 1000)

def detect_lang_simple(text: str) -> str:
    for ch in text:
        if "\uac00" <= ch <= "\ud7a3":
            return "ko"
    return "en"

def contains_all(text: str, terms: list[str]) -> bool:
    t = text.lower()
    return all(term.lower() in t for term in terms)

def contains_any(text: str, terms: list[str]) -> bool:
    t = text.lower()
    return any(term.lower() in t for term in terms)

@dataclass
class EvalItem:
    id: str
    prompt: str
    template: Optional[str] = None
    version: Optional[int] = None
    system: Optional[str] = None
    vars: Optional[Dict[str, Any]] = None
    expect_lang: Optional[str] = None
    must_contain: Optional[list[str]] = None
    must_not_contain: Optional[list[str]] = None

def parse_item(row: Dict[str, Any]) -> EvalItem:
    if "id" not in row or "prompt" not in row:
        raise RuntimeError("Each jsonl row must include: id, prompt")

    return EvalItem(
        id=str(row["id"]),
        prompt=str(row["prompt"]),
        template=row.get("template"),
        version=row.get("version"),
        system=row.get("system"),
        vars=row.get("vars"),
        expect_lang=row.get("expect_lang"),
        must_contain=row.get("must_contain"),
        must_not_contain=row.get("must_not_contain"),
    )


def run_eval(
    *,
    input_path: str,
    output_path: str,
    api_base: str,
    timeout_sec: float,
) -> None:
    url = api_base.rstrip("/") + "/v1/llm/chat"

    total = 0
    ok_cnt = 0
    err_cnt = 0

    for row in read_jsonl(input_path):
        item = parse_item(row)
        total += 1

        req_payload: Dict[str, Any] = {
            "prompt": item.prompt,
        }
        if item.template is not None:
            req_payload["template"] = item.template
        if item.version is not None:
            req_payload["version"] = item.version
        if item.system is not None:
            req_payload["system"] = item.system
        if item.vars is not None:
            req_payload["vars"] = item.vars

        t0 = now_ms()
        status, resp_json = http_post_json(url, req_payload, timeout_sec=timeout_sec)
        t1 = now_ms()

        latency_ms = t1 - t0

        is_ok = (status == 200) and ("reply" in resp_json)
        reply_text = resp_json.get("reply", "") if isinstance(resp_json, dict) else ""
        checks = {}
        passed = is_ok

        if item.expect_lang:
            actual_lang = detect_lang_simple(reply_text)
            checks["lang"] = {"expect": item.expect_lang, "actual": actual_lang, "ok": (actual_lang == item.expect_lang)}
            passed = passed and checks["lang"]["ok"]

        if item.must_contain:
            ok = contains_all(reply_text, item.must_contain)
            checks["must_contain"] = {"terms": item.must_contain, "ok": ok}
            passed = passed and ok

        if item.must_not_contain:
            ok = not contains_any(reply_text, item.must_not_contain)
            checks["must_not_contain"] = {"terms": item.must_not_contain, "ok": ok}
            passed = passed and ok
        if is_ok:
            ok_cnt += 1
            result = {
                "id": item.id,
                "ok": True,
                "http_status": status,
                "latency_ms": latency_ms,
                "template": resp_json.get("template"),
                "version": resp_json.get("version"),
                "provider": resp_json.get("provider"),
                "reply": resp_json.get("reply"),
                "checks": checks,
                "pass": passed,
            }
        else:
            err_cnt += 1
            result = {
                "id": item.id,
                "ok": False,
                "http_status": status,
                "latency_ms": latency_ms,
                "checks": checks,
                "pass": False,
                "error": resp_json.get("error", resp_json),
                "request": {
                    "template": item.template,
                    "version": item.version,
                },
            }

        write_jsonl(output_path, result)

    summary = {
        "total": total,
        "ok": ok_cnt,
        "error": err_cnt,
        "ok_rate": (ok_cnt / total) if total else 0.0,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input_path", required=True, help="input jsonl path")
    parser.add_argument("--out", dest="output_path", required=True, help="output jsonl path")
    parser.add_argument("--api", dest="api_base", default="http://127.0.0.1:8000", help="API base url")
    parser.add_argument("--timeout", dest="timeout_sec", type=float, default=30.0, help="per-request timeout seconds")
    args = parser.parse_args()

    run_eval(
        input_path=args.input_path,
        output_path=args.output_path,
        api_base=args.api_base,
        timeout_sec=args.timeout_sec,
    )


if __name__ == "__main__":
    main()