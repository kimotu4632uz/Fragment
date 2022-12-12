#!/usr/bin/env python

from pathlib import Path
import shutil
import mimetypes
import io

from PIL import Image, ImageChops
import img2pdf
import requests
from bs4 import BeautifulSoup


def filter_url(url):
    mime, code = mimetypes.guess_type(url)
    return mime == "image/jpeg" or mime == "image/png"


def filter_image(byte):
    img = Image.open(io.BytesIO(byte))
    return img.height > 700


def get(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text)

    urls = [x["src"] for x in soup.find_all("img") if "src" in x.attrs]
    + [x["href"] for x in soup.find_all("a") if "href" in x.attrs]

    urls = [x for x in urls if filter_url(x)]
    for url in urls:
        resp = requests.get(url)
        resp.raise_for_status()
        if filter_image(resp.content):
            (Path.cwd() / url.split("/")[-1]).write_bytes(resp.content)


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

        bg_img = Image.new("RGB", img.size, img.getpixel((0, 0)))
        diff_img = ImageChops.difference(img, bg_img)
        img_out = img.crop(diff_img.convert("RGB").getbbox())
        img_out.save(file)


def genpdf():
    files = sorted([str(x) for x in Path.cwd().glob("*.png")])
    (Path.cwd() / f"{Path.cwd().name}.pdf").write_bytes(
        img2pdf.convert(files, rotation=img2pdf.Rotation.ifvalid)
    )


command_dict = {
    "backup": (backup, [], "backup files"),
    "trim": (trim, [], "trim pictures"),
    "genpdf": (genpdf, [], "generate pdf from pictures"),
    "get": (get, ["URL"], "get image from URL")
}


def help():
    print("commands:")
    print("  quit: exit command")
    print("  help: show help")

    for key, val in command_dict.items():
        if not val[1]:
            print(f"  {key}: {val[2]}")
        else:
            print(f"  {key} {' '.join(val[1])}: {val[2]}")

    print()


def main():
    help()
    print(Path.cwd())

    while True:
        try:
            cmd = input("> ").strip().split()
        except EOFError:
            print()
            break

        if cmd[0] == "quit":
            break
        elif cmd[0] == "help":
            help()
        elif cmd[0] in command_dict:
            if not command_dict[cmd[0]][1]:
                command_dict[cmd[0]][0]()
            else:
                command_dict[cmd[0]][0](cmd[1:])
        else:
            print(f"no such command: {cmd}")


if __name__ == "__main__":
    main()
