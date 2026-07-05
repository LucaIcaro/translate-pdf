Checks that DejaVu Sans is available on the system.

DejaVu Sans is included with most Linux distributions and is used
for rendering IAST transliteration text in the output PDF.
"""

import os
import sys


FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def main():
    if os.path.exists(FONT_PATH):
        print(f"Found DejaVu Sans at {FONT_PATH}")
        return

    alt_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/local/share/fonts/dejavu/DejaVuSans.ttf",
    ]
    for p in alt_paths:
        if os.path.exists(p):
            print(f"Found DejaVu Sans at {p}")
            return

    print(
        "DejaVu Sans not found. Install it with:\n"
        "  sudo apt install fonts-dejavu-core   (Debian/Ubuntu)\n"
        "  sudo dnf install dejavu-sans-fonts  (Fedora)\n"
        "Or download from https://dejavu-fonts.github.io/",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
