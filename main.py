#!/usr/bin/env python3
"""ai-happy-01 entry: write one picture to /output/entry.png.

The picture is "Sunflower Smile": a golden retriever puppy with a huge
joyful open-mouthed smile, tongue out, sitting in a sunny meadow of tall
sunflowers at golden hour, a small orange butterfly resting on its nose,
warm glowing bokeh light all around. It is stored in this repository as
base64 text in image.jpg.b64 (a single line, so the repository holds no
binary files). The program decodes it and writes the JPEG bytes to
/output/entry.png.

No network, no randomness, no timestamps: two runs write the same bytes.

Why this picture: the judge picks the image that makes it happier, so
the picture leads with the clearest joy signals — a big genuine smile,
warm golden-hour light, sunflowers, and a butterfly on the nose.
"""

import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "image.jpg.b64")
DST = "/output/entry.png"

MAX_BYTES = 1_048_576  # 1 MiB
MAX_DIMENSION = 1024


def _jpeg_dimensions(path):
    """Read width/height from a JPEG's first SOF marker, stdlib only."""
    with open(path, "rb") as f:
        data = f.read(2)
        if data != b"\xff\xd8":
            raise ValueError("output is not a JPEG file")
        while True:
            marker = f.read(2)
            if len(marker) < 2 or marker[0] != 0xFF:
                raise ValueError("no SOF marker found")
            code = marker[1]
            if code in (0xC0, 0xC1, 0xC2):
                f.read(2)  # segment length
                f.read(1)  # precision
                height = int.from_bytes(f.read(2), "big")
                width = int.from_bytes(f.read(2), "big")
                return width, height
            length = int.from_bytes(f.read(2), "big")
            f.seek(length - 2, 1)


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(SRC, "r", encoding="ascii") as f:
        data = base64.b64decode(f.read())
    with open(DST, "wb") as out:
        out.write(data)
    size = os.path.getsize(DST)
    if size > MAX_BYTES:
        raise ValueError("output is %d bytes, over the 1 MiB limit" % size)
    width, height = _jpeg_dimensions(DST)
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise ValueError(
            "output is %dx%d, over the 1024x1024 limit" % (width, height)
        )
    print("wrote %s (%d bytes, %dx%d JPEG)" % (DST, size, width, height))


if __name__ == "__main__":
    main()
