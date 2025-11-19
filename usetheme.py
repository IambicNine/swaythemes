"""
args:
    (str) : Name of theme
"""

import argparse
import math
import os
import re
import subprocess
import tomllib

THEME_DIR = "./themes/"
filename = ""


def update_sway(data):
    config_file = os.path.expanduser(os.path.expandvars(data["config_file"]))
    print(f"Editing {config_file}")
    if not os.path.isfile(config_file):
        print(f"Sway config file does not exist")
        exit(0)

    with open(config_file, "r") as file:
        lines = file.readlines()
        file.close()

    print("Updating sway config")

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
    config_file = os.path.expanduser(os.path.expandvars(data["config_file"]))
    if not os.path.isfile(config_file):
        print(f"waybar style.css does not exist")
        exit(0)

    with open(config_file, "r") as file:
        lines = file.readlines()
        file.close()
    
    print("Updating waybar config")

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
    config_file = os.path.expanduser(os.path.expandvars(data["config_file"]))
    if not os.path.isfile(config_file):
        print ("Rofi config file does not exist")
        exit(0)

    with open(config_file, "r") as file:
        lines = file.readlines()
        file.close()

    print("Updating rofi config")
    re_active_foreground = r"^active-foreground:\s+rgba"
    re_selected_active_background = r"selected-active-background:\s+rgba"
    re_alternate_active_background = r"alternate-active-background:\s+rgba"
    re_lightfg = r"lightfg:\s+rgba"
    re_lightbg = r"lightbg:\s+rgba"
    re_accent_color = r"accent-color:\s+rgba"
    re_border_color = r"border-color:\s+rgba"
    
    af_hex = data["active-foreground"]
    sab_hex = data["selected-active-background"]
    aab_hex = data["alternate-active-background"]
    lfg_hex = data["lightfg"]
    lbg_hex = data["lightbg"]
    ac_hex = data["accent-color"]
    bc_hex = data["border-color"]

    af_rgba = hex_to_rgba(af_hex)
    sab_rgba = hex_to_rgba(sab_hex)
    aab_rgba = hex_to_rgba(aab_hex)
    lfg_rgba = hex_to_rgba(lfg_hex)
    lbg_rgba = hex_to_rgba(lbg_hex)
    ac_rgba = hex_to_rgba(ac_hex)
    bc_rgba = hex_to_rgba(bc_hex)

    af_str = f"\tactive-foreground:\trgba({af_rgba[0]}, {af_rgba[1]}, {af_rgba[2]}, {af_rgba[3]}%);\n"
    sab_str = f"\tselected-active-background:\trgba({sab_rgba[0]}, {sab_rgba[1]}, {sab_rgba[2]}, {sab_rgba[3]}%);\n"
    aab_str = f"\talternate-active-background:\trgba({aab_rgba[0]}, {aab_rgba[1]}, {aab_rgba[2]}, {aab_rgba[3]}%);\n"
    lfg_str = f"\tlightfg:\trgba({lfg_rgba[0]}, {lfg_rgba[1]}, {lfg_rgba[2]}, {lfg_rgba[3]}%);\n"
    lbg_str = f"\tlightbg:\trgba({lbg_rgba[0]}, {lbg_rgba[1]}, {lbg_rgba[2]}, {lbg_rgba[3]}%);\n"
    ac_str = f"\taccent-color:\trgba({ac_rgba[0]}, {ac_rgba[1]}, {ac_rgba[2]}, {ac_rgba[3]}%);\n"
    bc_str = f"\tborder-color:\trgba({bc_rgba[0]}, {bc_rgba[1]}, {bc_rgba[2]}, {bc_rgba[3]}%);\n"

    for i in range(len(lines)):
        if re.search(re_active_foreground, lines[i]):
            lines[i] = af_str
        elif re.search(re_selected_active_background, lines[i]):
            lines[i] = sab_str
        elif re.search(re_alternate_active_background, lines[i]):
            lines[i] = aab_str
        elif re.search(re_lightfg, lines[i]):
            lines[i] = lfg_str
        elif re.search(re_lightbg, lines[i]):
            lines[i] = lbg_str
        elif re.search(re_accent_color, lines[i]):
            lines[i] = ac_str
        elif re.search(re_border_color, lines[i]):
            lines[i] = bc_str

    with open(config_file, "w") as file:
        file.write("".join(lines))
        file.close()

    return


def check_hex(color_str):
    preample = f"{filename} has invalid entries ({color_str})"
    # Check that first character of string is an octothorpe
    if type(color_str) is not str:
        print(f"{preample}(Was expecting RGB hex string of the format #XXXXXXXX)")
        return False
    if color_str[0] != '#':
        print(f"{preample}(Color string does not start with '#')")
        return False
    hex_num = color_str[1:]
    l = len(hex_num)
    if l != 8:
        print(f"{preamble}Color string is {l} and not 8")
        return False
    for i in range(l):
        if not re.search("[0-9A-Fa-f]", hex_num):
            print(f"{preamble}Color string is an invalid hex number.")
            return False
    return True


def hex_to_rgba(color_str):
    if not check_hex(color_str):
        exit(0)
    red_val_x = color_str[1:3]
    gre_val_x = color_str[3:5]
    blu_val_x = color_str[5:7]
    alp_val_x = color_str[7:9]
    red_val_d = int(red_val_x, 16)
    gre_val_d = int(gre_val_x, 16)
    blu_val_d = int(blu_val_x, 16)
    alp_val_d = int(alp_val_x, 16)
    alp_percent = math.floor((alp_val_d / 255) * 100)
    # print(f"{color_str} --> ({red_val_d}, {gre_val_d}, {blu_val_d}, {alp_percent}%)")
    output = (red_val_d, gre_val_d, blu_val_d, alp_percent)
    return output


def main():
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


if __name__ == "__main__":
    main()
