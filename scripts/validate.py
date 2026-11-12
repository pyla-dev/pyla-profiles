#!/usr/bin/env python3
"""Validate every profiles/*/profile.jsonc against schema/profile.schema.json.

Strips // and /* */ comments (JSONC), then validates with jsonschema.
Usage: python3 scripts/validate.py [repo_root]
Exit 0 = all profiles valid.
"""
import json
import re
import sys
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError:
    sys.exit("jsonschema required: pip install jsonschema")


def strip_jsonc(text: str) -> str:
    # remove /* */ and // comments, keeping // inside quoted strings intact
    out = []
    i, n = 0, len(text)
    in_str = False
    esc = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
        elif c == "/" and i + 1 < n and text[i + 1] == "/":
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif c == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1])
    schema = json.loads((root / "schema" / "profile.schema.json").read_text())
    validator = Draft7Validator(schema)
    files = sorted((root / "profiles").glob("*/profile.jsonc"))
    if not files:
        print("no profiles found", file=sys.stderr)
        return 1
    failed = 0
    for f in files:
        try:
            data = json.loads(strip_jsonc(f.read_text()))
        except json.JSONDecodeError as e:
            print(f"FAIL {f.relative_to(root)}: invalid JSON after comment strip: {e}")
            failed += 1
            continue
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            failed += 1
            print(f"FAIL {f.relative_to(root)}")
            for e in errors:
                where = "/".join(str(p) for p in e.path) or "(root)"
                print(f"   {where}: {e.message[:160]}")
        else:
            rules = len(data.get("rules", []))
            off = sum(1 for r in data["rules"] if r.get("enabled") is False)
            print(f"OK   {f.relative_to(root)}  ({rules} rules, {off} disabled)")
    if failed:
        print(f"\n{failed} profile(s) FAILED", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
