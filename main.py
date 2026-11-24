"""Ridiculous at First Glance, Real by the Second.

Writes one pitch sentence (1-200 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The pitch: church pews as coworking desks. Bizarre on first glance
(working from a church), sound on the second (churches sit empty six
days a week; freelancers pay real money for quiet, beautiful space).
The sentence is built from three parts so the pitch lands its turn:
the odd thing sold, who pays for it, and why the logic holds together.
"""

import os
import sys

# The three beats of the pitch, joined into a single sentence.
ODD_THING = "We rent out empty church pews as coworking desks"
WHO_PAYS = "freelancers pay $15 a day for silence, stained glass and Wi-Fi"
WHY_IT_HOLDS = "churches sit empty six days a week"

PITCH = f"{ODD_THING} \u2014 {WHO_PAYS}, because {WHY_IT_HOLDS}."

MAX_CHARS = 200


def validate(text: str) -> str:
    """Enforce the sealed scorer's gate: UTF-8 text, 1-200 chars, one line."""
    cleaned = " ".join(text.split())
    if not cleaned:
        raise ValueError("pitch is empty")
    if len(cleaned) > MAX_CHARS:
        raise ValueError(f"pitch is {len(cleaned)} chars, over {MAX_CHARS}")
    if cleaned.count(".") > 1:
        raise ValueError("pitch must be a single sentence")
    return cleaned


def main() -> int:
    text = validate(PITCH)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)
    # Round-trip check: what the judge reads must be exactly what we wrote.
    with open(path, "r", encoding="utf-8") as fh:
        if fh.read() != text:
            raise ValueError("entry.txt round-trip mismatch")
    print(text)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
