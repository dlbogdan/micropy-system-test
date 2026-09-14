#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK = ROOT / "vendor/micropy-system" / "src"
APP = ROOT / "app"
DEVICE = ROOT / "device"

if not FRAMEWORK.is_dir():
    raise SystemExit("Framework source is missing; initialize the Git submodule")
if not APP.is_dir():
    raise SystemExit("Application source directory is missing: app")

shutil.rmtree(DEVICE, ignore_errors=True)
shutil.copytree(FRAMEWORK, DEVICE, ignore=shutil.ignore_patterns(
    "__pycache__", "*.pyc", "system-config.json", "version.txt"))
shutil.copytree(APP, DEVICE, dirs_exist_ok=True, ignore=shutil.ignore_patterns(
    "__pycache__", "*.pyc"))

config = ROOT / "system-config.json"
if config.is_file():
    shutil.copy2(config, DEVICE / "system-config.json")

print(f"Assembled device filesystem at {DEVICE}")
