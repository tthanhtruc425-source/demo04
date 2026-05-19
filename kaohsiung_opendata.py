#!/usr/bin/env python3
"""
Download and display Kaohsiung City tourism events from the open data URL.

Usage:
  python kaohsiung_opendata.py [URL]

If no URL is provided, the script uses the default dataset URL.
"""
import sys
import requests
import io
import csv
import json
from typing import List, Dict, Any

DEFAULT_URL = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"


def download(url: str) -> bytes:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.content


def try_parse_json(content: bytes):
    try:
        return json.loads(content.decode("utf-8-sig"))
    except Exception:
        return None


def parse_csv(content: bytes) -> List[Dict[str, Any]]:
    text = content.decode("utf-8-sig")
    f = io.StringIO(text)
    reader = csv.reader(f)
    rows = list(reader)
    if not rows:
        return []
    header = rows[0]
    data_rows = rows[1:]
    result = []
    for r in data_rows:
        # pad shorter rows
        if len(r) < len(header):
            r += [""] * (len(header) - len(r))
        result.append({h: v for h, v in zip(header, r)})
    return result


def print_table(rows: List[Dict[str, Any]], max_rows: int = 20):
    if not rows:
        print("No records found.")
        return
    headers = list(rows[0].keys())
    try:
        from tabulate import tabulate
        print(tabulate([ [r.get(h, "") for h in headers] for r in rows[:max_rows] ], headers=headers, tablefmt="github"))
    except Exception:
        # fallback: simple column widths
        col_widths = {h: max(len(str(h)), *(len(str(r.get(h, ""))) for r in rows[:max_rows])) for h in headers}
        # header
        hdr = " | ".join(h.ljust(col_widths[h]) for h in headers)
        sep = "-+-".join("-" * col_widths[h] for h in headers)
        print(hdr)
        print(sep)
        for r in rows[:max_rows]:
            line = " | ".join(str(r.get(h, "")).ljust(col_widths[h]) for h in headers)
            print(line)


def main(argv):
    url = argv[1] if len(argv) > 1 else DEFAULT_URL
    print(f"Downloading from: {url}")
    content = download(url)

    # Try JSON first
    parsed_json = try_parse_json(content)
    if parsed_json is not None:
        # Normalize to a list of dicts
        if isinstance(parsed_json, dict):
            # find the first list value if present
            list_values = [v for v in parsed_json.values() if isinstance(v, list)]
            rows = list_values[0] if list_values else []
        elif isinstance(parsed_json, list):
            rows = parsed_json
        else:
            rows = []
        print(f"Parsed JSON with {len(rows)} records")
        if rows and isinstance(rows[0], dict):
            print_table(rows)
        else:
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        return

    # Fallback to CSV
    try:
        rows = parse_csv(content)
        print(f"Parsed CSV with {len(rows)} records")
        print_table(rows)
        return
    except Exception as e:
        print("Failed to parse content as CSV:", e)

    # Last resort: print raw text
    txt = content.decode("utf-8", errors="replace")
    print("Raw content (first 2000 chars):")
    print(txt[:2000])


if __name__ == "__main__":
    main(sys.argv)
