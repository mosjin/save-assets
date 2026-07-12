#!/usr/bin/env python3
"""
One-command installer for save-assets Claude Code skill.
Auto-patches ~/.claude/settings.json — no JSON editing needed.

  python install.py           # install
  python install.py --remove  # uninstall
"""
import json, os, sys, shutil
from pathlib import Path

MARKETPLACE_KEY = "save-assets"
PLUGIN_KEY      = "save-assets@save-assets"
SOURCE          = {"source": {"source": "github", "repo": "mosjin/save-assets"}}


def find_settings():
    for p in [Path.home() / ".claude/settings.json",
              Path(os.environ.get("APPDATA","")) / "Claude/settings.json"]:
        if p.exists():
            return p
    p = Path.home() / ".claude/settings.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("{}\n")
    return p


def install():
    path = find_settings()
    shutil.copy2(path, path.with_suffix(".json.bak"))
    data = json.loads(path.read_text(encoding="utf-8"))

    changed = False
    if MARKETPLACE_KEY not in data.setdefault("extraKnownMarketplaces", {}):
        data["extraKnownMarketplaces"][MARKETPLACE_KEY] = SOURCE
        print(f"✓ Marketplace registered: {MARKETPLACE_KEY}")
        changed = True
    if not data.setdefault("enabledPlugins", {}).get(PLUGIN_KEY):
        data["enabledPlugins"][PLUGIN_KEY] = True
        print(f"✓ Plugin enabled: {PLUGIN_KEY}")
        changed = True

    if changed:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("\nDone! Run  /reload-plugins  inside Claude Code, then use /save-assets")
    else:
        print("Already installed. Run /reload-plugins if skills are not showing.")


def remove():
    path = find_settings()
    data = json.loads(path.read_text(encoding="utf-8"))
    removed = []
    if MARKETPLACE_KEY in data.get("extraKnownMarketplaces", {}):
        del data["extraKnownMarketplaces"][MARKETPLACE_KEY]; removed.append("marketplace")
    if PLUGIN_KEY in data.get("enabledPlugins", {}):
        del data["enabledPlugins"][PLUGIN_KEY]; removed.append("plugin")
    if removed:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Removed: {', '.join(removed)}. Run /reload-plugins.")
    else:
        print("Nothing to remove.")


if __name__ == "__main__":
    remove() if "--remove" in sys.argv else install()
