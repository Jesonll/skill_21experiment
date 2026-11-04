#!/usr/bin/env python3
"""Export every PDF page as a numbered JPG using Poppler (no Python dependencies)."""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Final report PDF")
    parser.add_argument("--out", type=Path, help="Default: photos/ beside the PDF (use a separate output workspace for raw input photos)")
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--overwrite", action="store_true", help="Replace a folder containing only page-NNN.jpg exports")
    args = parser.parse_args()
    if args.dpi <= 0:
        parser.error("--dpi must be positive")
    if not args.pdf.is_file():
        parser.error(f"PDF not found: {args.pdf}")
    for tool in ("pdfinfo", "pdftoppm"):
        if not shutil.which(tool):
            parser.error(f"{tool} is required; install Poppler utilities")
    out = args.out or args.pdf.with_name("photos")
    if out.is_symlink() or (out.exists() and not out.is_dir()):
        parser.error(f"Output must be a regular directory: {out}")
    old = list(out.iterdir()) if out.exists() else []
    if old and not args.overwrite:
        parser.error(f"Output is not empty: {out}; use --overwrite to refresh exported JPGs")
    if any(p.is_symlink() or not p.is_file() or not re.fullmatch(r"page-\d{3,}\.jpg", p.name) for p in old):
        parser.error("Refusing to replace a folder containing anything other than exported page-NNN.jpg files")
    try:
        info = subprocess.run(["pdfinfo", str(args.pdf)], check=True, capture_output=True, text=True).stdout
        match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.MULTILINE)
        if not match or int(match[1]) < 1:
            parser.error("Cannot determine PDF page count")
        count = int(match[1])
        out.parent.mkdir(parents=True, exist_ok=True)
        # Render and validate before touching an existing export.
        with tempfile.TemporaryDirectory(prefix=".pdf-pages-", dir=out.parent) as tmp:
            staging = Path(tmp)
            subprocess.run(["pdftoppm", "-r", str(args.dpi), "-jpeg", "-jpegopt", "quality=95",
                            str(args.pdf), str(staging / "render")], check=True)
            pages = {}
            for image in staging.glob("render-*.jpg"):
                number = int(image.stem.split("-")[-1])
                with image.open("rb") as stream:
                    if stream.read(2) != b"\xff\xd8":
                        parser.error(f"Invalid JPEG output for page {number}")
                pages[number] = image
            if set(pages) != set(range(1, count + 1)):
                parser.error("Rendered JPG page numbers do not match the PDF")
            out.mkdir(exist_ok=True)
            for image in old:
                image.unlink()
            for number, image in sorted(pages.items()):
                image.replace(out / f"page-{number:03d}.jpg")
        print(f"Exported {count} pages at {args.dpi} dpi to {out}")
    except subprocess.CalledProcessError as error:
        parser.exit(1, f"PDF export failed: {error}\n{error.stderr or ''}")


if __name__ == "__main__":
    main()
