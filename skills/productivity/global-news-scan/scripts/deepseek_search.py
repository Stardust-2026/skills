#!/usr/bin/env python3
"""Discover public news sources through DeepSeek Search."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

SEARCH_URL = "https://api.deepseek.com/v1/tools/search"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Keep the bearer credential on the configured API host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queries", nargs="+", help="Public search queries")
    parser.add_argument("--count", type=int, default=8, choices=range(1, 51),
                        metavar="1–50")
    args = parser.parse_args()
    queries = [query.strip() for query in args.queries]
    if any(not 1 <= len(query) <= 128 for query in queries):
        parser.error("Each query must contain 1–128 characters.")

    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        print("DeepSeek Search is unavailable: DEEPSEEK_API_KEY is unset.",
              file=sys.stderr)
        return 2

    opener = urllib.request.build_opener(NoRedirect())
    batches = []
    for query in queries:
        request = urllib.request.Request(
            SEARCH_URL,
            data=json.dumps({"query": query, "count": args.count}).encode("utf-8"),
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with opener.open(request, timeout=15) as response:
                payload = json.load(response)
            results = payload.get("results") if isinstance(payload, dict) else None
            if not isinstance(results, list):
                raise ValueError("Unexpected result shape")
        except urllib.error.HTTPError as error:
            print(f"DeepSeek Search stopped at HTTP {error.code}.", file=sys.stderr)
            break
        except (OSError, ValueError):
            print("DeepSeek Search stopped after a connection or response error.",
                  file=sys.stderr)
            break
        batches.append({"query": query, "results": results})

    print(json.dumps(batches, ensure_ascii=False, indent=2))
    return 0 if len(batches) == len(queries) else 1


if __name__ == "__main__":
    sys.exit(main())
