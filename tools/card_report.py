"""Report the memory card state for a SpongeBobRecomp user directory.

Host-side only: reads files, opens no window, launches nothing.

    python tools\\card_report.py                     # %LOCALAPPDATA%\\SpongeBobRecomp
    python tools\\card_report.py "<user dir>"
    python tools\\card_report.py "<user dir>" --json

Prints the SlotA/SlotB device, the raw card size and SHA-256, and every
directory entry (game code, company, file name, block count) from both
directory blocks. Use it on a support report: it shows whether a save is
really on the card and whether the game is still using the folder device.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import struct
import sys

HEADER_BYTES = 0x2000
DIRECTORY_BYTES = 0x2000
ENTRY_BYTES = 0x40
MAX_ENTRIES = 127

DEVICE_NAMES = {
    0: "Dummy (not a memory card - broken)",
    1: "MemoryCard (raw) - expected",
    2: "MaskROM",
    5: "Ethernet",
    6: "Baseboard",
    7: "Gecko",
    8: "MemoryCardFolder (GCI folder) - legacy",
    255: "None - expected for slot B",
}


def default_user_directory() -> pathlib.Path:
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return pathlib.Path(local) / "SpongeBobRecomp"
    return pathlib.Path.cwd()


def read_ini_slots(path: pathlib.Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    section = ""
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        if section.lower() != "core":
            continue
        match = re.match(r"(Slot[AB])\s*=\s*(.*)", line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


def parse_entries(block: bytes) -> list[dict]:
    entries = []
    for index in range(MAX_ENTRIES):
        entry = block[index * ENTRY_BYTES:(index + 1) * ENTRY_BYTES]
        if len(entry) < ENTRY_BYTES:
            break
        if entry[0:4] in (b"\xff\xff\xff\xff", b"\x00\x00\x00\x00"):
            continue
        name = entry[8:0x28].split(b"\x00")[0]
        entries.append({
            "index": index,
            "game_code": entry[0:4].decode("latin-1", "replace"),
            "company": entry[4:6].decode("latin-1", "replace"),
            "file": name.decode("latin-1", "replace"),
            "blocks": struct.unpack(">H", entry[0x38:0x3A])[0],
        })
    return entries


def report(user_directory: pathlib.Path) -> dict:
    result: dict = {"user_directory": str(user_directory)}
    ini = user_directory / "Config" / "Dolphin.ini"
    slots = read_ini_slots(ini)
    result["dolphin_ini"] = str(ini)
    result["dolphin_ini_exists"] = ini.is_file()
    result["slot_a"] = slots.get("SlotA")
    result["slot_b"] = slots.get("SlotB")
    result["slot_a_device"] = DEVICE_NAMES.get(int(slots["SlotA"]), "unknown") \
        if slots.get("SlotA", "").isdigit() else "unset (Dolphin default: GCI folder)"
    result["slot_b_device"] = DEVICE_NAMES.get(int(slots["SlotB"]), "unknown") \
        if slots.get("SlotB", "").isdigit() else "unset (Dolphin default: None)"

    gc_root = user_directory / "GC"
    result["gc_directories"] = sorted(p.name for p in gc_root.iterdir()
                                      if p.is_dir()) if gc_root.is_dir() else []

    cards = []
    if gc_root.is_dir():
        for candidate in sorted(gc_root.glob("MemoryCardA.*.raw")):
            data = candidate.read_bytes()
            entry = {
                "path": str(candidate),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest().upper(),
                "expected_bytes": 16 * 1024 * 1024,
                "entries": {},
            }
            for label, offset in (("directory_1", HEADER_BYTES),
                                  ("directory_2", HEADER_BYTES + DIRECTORY_BYTES)):
                block = data[offset:offset + DIRECTORY_BYTES]
                found = parse_entries(block) if len(block) == DIRECTORY_BYTES else []
                if found:
                    entry["entries"][label] = found
            cards.append(entry)
    result["cards"] = cards

    folder_saves = []
    if gc_root.is_dir():
        for card_directory in sorted(gc_root.glob("*/Card A")):
            folder_saves.extend(
                {"path": str(p), "bytes": p.stat().st_size}
                for p in sorted(card_directory.glob("*.gci"))
            )
    result["legacy_folder_saves"] = folder_saves
    return result


def print_text(data: dict) -> None:
    print(f"user directory : {data['user_directory']}")
    ini_state = "present" if data["dolphin_ini_exists"] else "MISSING"
    print(f"Dolphin.ini    : {ini_state}")
    print(f"slot A         : {data['slot_a'] or 'unset'} ({data['slot_a_device']})")
    print(f"slot B         : {data['slot_b'] or 'unset'} ({data['slot_b_device']})")
    print(f"GC/ directories: {', '.join(data['gc_directories']) or '(none)'}")
    if not data["cards"]:
        print("raw cards      : none (the game has not opened a raw card yet)")
    for card in data["cards"]:
        size_note = "ok" if card["bytes"] == card["expected_bytes"] else \
            f"UNEXPECTED (expected {card['expected_bytes']})"
        print(f"raw card       : {pathlib.Path(card['path']).name} "
              f"{card['bytes']} bytes ({size_note})")
        print(f"  sha256       : {card['sha256']}")
        if not card["entries"]:
            print("  entries      : none (blank card, or no save written yet)")
        for label, entries in card["entries"].items():
            print(f"  {label}:")
            for entry in entries:
                print(f"    [{entry['index']}] {entry['game_code']} "
                      f"company={entry['company']} '{entry['file']}' "
                      f"blocks={entry['blocks']}")
    if data["legacy_folder_saves"]:
        print("legacy GCI files still present (kept as backup):")
        for save in data["legacy_folder_saves"]:
            print(f"  {save['path']} {save['bytes']} bytes")
    else:
        print("legacy GCI files: none")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("user_directory", nargs="?",
                        help="SpongeBobRecomp user directory")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args()
    directory = pathlib.Path(args.user_directory) if args.user_directory \
        else default_user_directory()
    if not directory.is_dir():
        print(f"not a directory: {directory}", file=sys.stderr)
        return 2
    data = report(directory)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print_text(data)
    healthy = (
        data["slot_a"] == "1"
        and data["slot_b"] == "255"
        and any(card["bytes"] == card["expected_bytes"] for card in data["cards"])
    )
    return 0 if healthy else 1


if __name__ == "__main__":
    raise SystemExit(main())