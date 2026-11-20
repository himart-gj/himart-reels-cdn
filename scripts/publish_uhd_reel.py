#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assemble staged `.b64` chunks or `.mp4` files in `staging/` into verified Ultra-HD 1080x1920 MP4s
in `dist_uhd/` ready for 2GB-capable Public GitHub Release hosting.
"""
import argparse
import base64
import json
import re
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--staging-dir", default="staging")
    ap.add_argument("--out-dir", default="dist_uhd")
    ap.add_argument("--tag", default="reels-uhd-latest")
    args = ap.parse_args()

    st_dir = Path(args.staging_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not st_dir.exists():
        print("Staging dir does not exist yet; nothing to assemble.")
        return

    for mp4 in sorted(st_dir.glob("*.mp4")):
        shutil.copy2(mp4, out_dir / mp4.name)

    groups = {}
    for bf in sorted(st_dir.glob("*_p*.b64")):
        m = re.match(r"^(.+)_p(\d+)\.b64$", bf.name)
        if m:
            groups.setdefault(m.group(1), {})[int(m.group(2))] = "".join(bf.read_text(encoding="utf-8").split())

    for stem, parts in sorted(groups.items()):
        raw = base64.b64decode("".join(parts[k] for k in sorted(parts)))
        fname = stem if stem.endswith(".mp4") else f"{stem}.mp4"
        (out_dir / fname).write_bytes(raw)

    manifest = []
    for mp4 in sorted(out_dir.glob("*.mp4")):
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate:stream=width,height,r_frame_rate", "-of", "json", str(mp4)],
            capture_output=True, text=True, check=True,
        )
        info = json.loads(res.stdout)
        manifest.append({
            "filename": mp4.name,
            "public_url": f"https://github.com/himart-gj/himart-reels-cdn/releases/download/{args.tag}/{mp4.name}",
            "probe": info,
        })
    (out_dir / "uhd_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
