#!/usr/bin/env python3
"""Claude Code status line: model, cwd, and context usage.

Context usage is derived from the most recent main-chain assistant message's
token usage (input + cache creation + cache read = tokens sent to the model).
"""
import json
import os
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    model = (data.get("model") or {}).get("display_name") or "Claude"
    cwd = (data.get("workspace") or {}).get("current_dir") or data.get("cwd") or os.getcwd()
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]
    cwd_short = os.path.basename(cwd.rstrip("/")) or cwd

    # Context window: 200k standard, 1M when the flag is set.
    limit = 1_000_000 if data.get("exceeds_200k_tokens") else 200_000

    used = context_tokens(data.get("transcript_path"))

    parts = [f"\033[36m{model}\033[0m", f"\033[90m{cwd_short}\033[0m"]

    if used is not None:
        pct = used / limit * 100
        # Color by pressure: green < 50%, yellow < 80%, red otherwise.
        color = "32" if pct < 50 else ("33" if pct < 80 else "31")
        used_k = used / 1000
        limit_k = limit // 1000
        parts.append(f"\033[{color}m{used_k:.0f}k/{limit_k}k ({pct:.0f}%)\033[0m")

    sys.stdout.write("  ".join(parts))


def context_tokens(transcript_path):
    """Return total context tokens from the last main-chain assistant message."""
    if not transcript_path or not os.path.exists(transcript_path):
        return None
    last = None
    try:
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                if entry.get("type") != "assistant" or entry.get("isSidechain"):
                    continue
                usage = (entry.get("message") or {}).get("usage")
                if usage:
                    last = usage
    except Exception:
        return None
    if not last:
        return None
    return (
        last.get("input_tokens", 0)
        + last.get("cache_creation_input_tokens", 0)
        + last.get("cache_read_input_tokens", 0)
    )


if __name__ == "__main__":
    main()
