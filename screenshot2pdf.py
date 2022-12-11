#!/usr/bin/env python

import sys
from pathlib import Path
import shutil

from PIL import Image, ImageChops
import img2pdf


def backup():
    (Path.cwd() / "backup").mkdir(exist_ok=True)
    for file in Path.cwd().iterdir():
        if file.is_file():
            shutil.copy2(file, (file.parent / "backup" / file.name))


def trim():
    for file in Path.cwd().glob("*.png"):
        img = Image.open(file)
        if img.mode == "RGBA":
            img = img.convert("RGB")

        bg_img = Image.new("RGB", img.size, img.getpixel((0,0)))
        diff_img = ImageChops.difference(img, bg_img)
        img_out = img.crop(diff_img.convert("RGB").getbbox())
        img_out.save(file)


def genpdf():
    files = sorted([str(x) for x in Path.cwd().glob("*.png")])
    (Path.cwd() / f"{Path.cwd().name}.pdf").write_bytes(img2pdf.convert(files, rotation=img2pdf.Rotation.ifvalid))


command_dict = {
    "backup": (backup, "backup files"),
    "trim": (trim, "trim pictures"),
    "genpdf": (genpdf, "generate pdf from pictures")
}


def help():
    print("commands:")
    print("  quit: exit command")
    print("  help: show help")

    for key, val in command_dict.items():
        print(f"  {key}: {val[1]}")

    print()


def main():
    help()
    print(Path.cwd())

    while True:
        try:
            cmd = input("> ").strip()
        except EOFError:
            print()
            break

        if cmd == "quit":
            break
        elif cmd == "help":
            help()
        elif cmd in command_dict:
            command_dict[cmd][0]()
        else:
            print(f"no such command: {cmd}")


if __name__ == "__main__":
    main()

