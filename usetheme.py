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

def waybar_enabled(data):
    return

def rofi_enabled(data):
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
