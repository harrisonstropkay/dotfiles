#!/usr/bin/env python3
"""Claude Code status line: model, cwd, and context usage.

All values come strictly from Claude Code's JSON input. Any missing or
malformed field shows an error instead of a guessed value.
"""
import json
import os
import sys


def require(d, *keys):
    cur = d
    path = []
    for k in keys:
        path.append(k)
        if not isinstance(cur, dict) or cur.get(k) is None:
            raise ValueError(f"missing {'.'.join(path)}")
        cur = cur[k]
    return cur


def render(data):
    model = require(data, "model", "display_name")
    cwd = require(data, "workspace", "current_dir")
    limit = require(data, "context_window", "context_window_size")
    used = require(data, "context_window", "total_input_tokens")

    if not isinstance(limit, int) or limit <= 0:
        raise ValueError(f"bad context_window_size: {limit!r}")
    if not isinstance(used, int) or used < 0:
        raise ValueError(f"bad total_input_tokens: {used!r}")

    cwd_short = os.path.basename(cwd.rstrip("/")) or cwd
    pct = used / limit * 100
    # Color by pressure: green < 50%, yellow < 80%, red otherwise.
    color = "32" if pct < 50 else ("33" if pct < 80 else "31")
    if limit >= 1_000_000:
        limit_s = f"{limit / 1_000_000:g}m"
    else:
        limit_s = f"{limit // 1000}k"
    return "  ".join([
        f"\033[36m{model}\033[0m",
        f"\033[90m{cwd_short}\033[0m",
        f"\033[{color}m{used / 1000:.0f}k/{limit_s} ({pct:.0f}%)\033[0m",
    ])


def main():
    try:
        out = render(json.load(sys.stdin))
    except Exception as e:
        out = f"\033[31mstatusline error: {e}\033[0m"
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
