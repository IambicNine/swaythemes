"""
args:
    (str) : Name of theme
"""

import argparse
import os
import re
import subprocess
import tomllib

THEME_DIR = "./themes/"

def update_sway(data):
    config_file = os.path.expanduser(os.path.expandvars(data["config_dir"]))
    print(f"Editing {config_file}")
    if not os.path.isfile(config_file):
        print(f"Sway config file does not exist")
        exit(0)

    with open(config_file, "r") as file:
        lines = file.readlines()
        file.close()

    f = data["client"]["focused"]
    focused_str = f"client.focused\t\t{f['border']} {f['background']} {f['text']} {f['indicator']} {f['child_border']}\n"
    for i in range(len(lines)):
        if re.search(r"\bclient.focused\b", lines[i]):
            lines[i] = focused_str

    with open(config_file, "w") as file:
        file.write("".join(lines))
        file.close()

    # Reload sway config
    subprocess.run("swaymsg reload", shell=True)
    return

def update_waybar(data):
    config_file = os.path.expanduser(os.path.expandvars(data["config_dir"]))
    if not os.path.isfile(config_file):
        print(f"waybar style.css does not exist")
        exit(0)

    with open(config_file, "r") as file:
        lines = file.readlines()
        file.close()

    work = f"@define-color work\t{data['work']};\n"
    window = f"@define-color window\t{data['window']};\n"
    process = f"@define-color process\t{data['process']};\n"
    border = f"@define-color border\t{data['border']};\n"

    re_work = r"@define-color work"
    re_window = r"@define-color window"
    re_process = r"@define-color process"
    re_border = r"@define-color border"

    for i in range(len(lines)):
        if re.search(re_work, lines[i]):
            lines[i] = work
        elif re.search(re_window, lines[i]):
            lines[i] = window
        elif re.search(re_process, lines[i]):
            lines[i] = process
        elif re.search(re_border, lines[i]):
            lines[i] = border

    with open(config_file, "w") as file:
        file.write("".join(lines))
        file.close()

    # Restart waybar
    subprocess.run("pkill waybar && waybar &", shell=True)
    return

def update_rofi(data):
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="swaythemes",
        description="Color theme switcher for sway"
    )
    parser.add_argument("theme_name")
    args = parser.parse_args()

    # Check that theme exists
    filename = f"{args.theme_name}.toml"
    theme_path = f"{THEME_DIR}{filename}"
    if not os.path.isfile(theme_path):
        print(f"No such file exists in {THEME_DIR}")
        exit(0)
    print(f"Found {filename}")

    try:
        with open(theme_path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError:
        print("Invalid TOML file")
        exit(0)

    sway_enabled = data["sway"]["enable"]
    waybar_enabled = data["waybar"]["enable"]
    rofi_enabled = data["rofi"]["enable"]

    if sway_enabled:
        update_sway(data["sway"])
    if waybar_enabled:
        update_waybar(data["waybar"])
    if rofi_enabled:
        update_rofi(data["rofi"])
