#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]*\]\((https?://[^)\s]+)\)")
TIMEOUT = 12


def iter_urls() -> dict[str, set[str]]:
    urls: dict[str, set[str]] = {}
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for url in LINK.findall(text):
            urls.setdefault(url, set()).add(md.relative_to(ROOT).as_posix())
    return urls


def check(url: str) -> tuple[str, str]:
    headers = {"User-Agent": "GTS-AIRST-reference-audit/1.0"}
    request = urllib.request.Request(url, headers=headers, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            final = response.geturl()
            status = "REDIRECTED" if final != url else "LIVE"
            return status, final
    except urllib.error.HTTPError as exc:
        if exc.code in {403, 405, 429}:
            request = urllib.request.Request(url, headers=headers, method="GET")
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                    final = response.geturl()
                    status = "REDIRECTED" if final != url else "LIVE"
                    return status, final
            except Exception as nested:
                return "REVIEW_REQUIRED", f"{type(nested).__name__}: {nested}"
        if exc.code in {404, 410}:
            return "DEAD", f"HTTP {exc.code}"
        return "REVIEW_REQUIRED", f"HTTP {exc.code}"
    except Exception as exc:
        return "REVIEW_REQUIRED", f"{type(exc).__name__}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fail-on-dead", action="store_true")
    args = parser.parse_args()

    dead = 0
    for index, (url, files) in enumerate(sorted(iter_urls().items()), 1):
        status, detail = check(url)
        if status == "DEAD":
            dead += 1
        print(f"{status}\t{url}\t{','.join(sorted(files))}\t{detail}")
        if index % 20 == 0:
            time.sleep(0.5)

    print(f"REFERENCE_AUDIT dead={dead}")
    return 1 if args.fail_on_dead and dead else 0


if __name__ == "__main__":
    raise SystemExit(main())
