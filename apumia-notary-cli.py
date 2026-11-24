#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

NODE = os.environ.get("NOTARY_NODE_URL", "https://apumia.space").rstrip("/")
KEY = os.environ.get("NOTARY_API_KEY", "")


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def req(url: str, method: str = "GET", payload: dict | None = None, token: str = "") -> dict:
    if not url.startswith(("https://", "http://")):
        sys.exit("Error: Only http:// and https:// schemes are permitted.")
    headers = {"Accept": "application/json", "User-Agent": "apumia-notary-cli/1.0"}
    data = json.dumps(payload).encode("utf-8") if payload else None
    if data:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=15) as r:  # nosec B310
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')}")


def main() -> None:
    p = argparse.ArgumentParser(description="Notary AI Zero-Dependency CLI")
    p.add_argument("--node", default=NODE)
    sub = p.add_subparsers(dest="cmd", required=True)
    h_p = sub.add_parser("hash")
    h_p.add_argument("target")
    h_p.add_argument("--text", action="store_true")
    s_p = sub.add_parser("stamp")
    s_p.add_argument("target")
    s_p.add_argument("--agent-id", default="cli-agent")
    s_p.add_argument("--outcome", default="executed")
    s_p.add_argument("--api-key", default=KEY)
    v_p = sub.add_parser("verify")
    v_p.add_argument("query")
    sub.add_parser("head")
    a = p.parse_args()
    n = a.node.rstrip("/")
    if a.cmd == "hash":
        print(hashlib.sha256(a.target.encode("utf-8")).hexdigest() if a.text else sha256_file(a.target))
    elif a.cmd == "stamp":
        if not a.api_key:
            sys.exit("Error: --api-key or NOTARY_API_KEY required")
        d = a.target.lower() if len(a.target) == 64 else sha256_file(a.target)
        res = req(f"{n}/api/stamp", "POST", {"sha256": d, "agent_id": a.agent_id, "outcome": a.outcome}, a.api_key)
        print(json.dumps(res, indent=2))
    elif a.cmd == "verify":
        q = urllib.parse.quote(a.query.strip())
        print(json.dumps(req(f"{n}/api/verify?q={q}"), indent=2))
    elif a.cmd == "head":
        print(json.dumps(req(f"{n}/api/head"), indent=2))


if __name__ == "__main__":
    main()
