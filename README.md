# MicroPython application

This application uses `micropy-system` as a pinned Git submodule.

## Common commands

```sh
# One-time local toolchain setup
tools/setup_build_env.sh

# Assemble and build app/version.txt for Pico 2 W
tools/build_firmware.sh

# Build an explicit version/model locally
tools/build_firmware.sh 1.0.1 pico2-w-rp2350

# Update the framework checkout; review and commit its pointer afterward
tools/update_framework.sh

# Trigger the GitHub release workflow by pushing a clean annotated tag
tools/release_github.sh 1.0.1
```

For a manual GitHub run, open **Actions → Build firmware release → Run
workflow** and enter a semantic version. The release workflow also runs when a
`vMAJOR.MINOR.PATCH` tag is pushed.

For MicroPico deployment, copy `system-config.example.json` to the ignored
`system-config.json`, edit it, run `python3 tools/assemble.py`, and configure
MicroPico's sync folder as `device`.
