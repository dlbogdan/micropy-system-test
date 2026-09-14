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

## Local application-to-Pico workflow

1. Put application code in `app`; `app/main.py` must expose `async def main()`.
2. Increment the semantic version in `app/version.txt`.
3. Ensure ignored `system-config.json` contains Wi-Fi credentials, the correct
   board model, `UPDATE_ON_BOOT: true`, and a trusted-LAN `DIRECT_BASE_URL` such
   as `http://192.168.1.10:8000/`.
4. Build the A/B application image:

   ```sh
   tools/build_firmware.sh
   # Explicit alternative:
   tools/build_firmware.sh 1.0.25 pico2-w-rp2350
   ```

5. In a separate terminal, serve the resulting `build` directory:

   ```sh
   tools/serve_update.sh 8000
   ```

6. Reset or power-cycle the Pico. It installs into the inactive slot and boots
   that slot as a candidate.
7. After application health checks and a short stable event-loop period, call
   `confirm_running_slot()` from the candidate. If it raises or does not
   confirm, the watchdog resets the board and the previous slot is restored.
8. Verify `/version.txt` and OTA state with `mpremote`, then commit the app source
   and version. `build` and `device` are generated and normally not committed.

For a blank Pico, run `python3 tools/assemble.py`, configure MicroPico to sync
only `device`, and upload that complete bootstrap tree once. Subsequent app
updates use OTA; do not synchronize the repository root.

The complete initialization, confirmation API, local OTA, rollback, and GitHub
release documentation lives in `vendor/micropy-system/README.md`.

For a manual GitHub run, open **Actions → Build firmware release → Run
workflow** and enter a semantic version. The release workflow also runs when a
`vMAJOR.MINOR.PATCH` tag is pushed.

For MicroPico deployment, copy `system-config.example.json` to the ignored
`system-config.json`, edit it, run `python3 tools/assemble.py`, and configure
MicroPico's sync folder as `device`.
