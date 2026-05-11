# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog.

## [Unreleased]

### Added
- Docs: guía de hotfix para `PRTOUCH_PROBE_ZOFFSET` cuando `probe_result` es inmutable.
- Docs: agregado `HOSTS.md` con mapeo de impresoras/hosts (`se01`, `se02`, `ma01`) e IPs Tailscale.
- Docs: agregada sección de hosts de respaldo por IP directa en `HOSTS.md`.
- Docs: agregado `docs/future-plans-inmateriis.md` con plan semanal de mejoras (2026-05-08) para SE01, SE02 y MA01.
- Docs: agregado `docs/se01-dacai-special-plan.md` con plan individual de SE01 para caso especial de pantalla DACAI.

### Changed
- `config/printer.cfg`: sincronizado con se01 (agregado `[firmware_retraction]`, `pressure_advance` a `0.1`).
- `README.md`: actualizado para incluir `HOSTS.md` en la estructura del repo.
- `config/macros/tooling_macros.cfg`: agregado macro `EXTRAER_MATERIAL` (usa 70% de `SPOOLMAN_ACTIVE.nozzle_temp`).
- `docs/future-plans-inmateriis.md`: Semana 1 marcada como ejecutada y documentado alcance por impresora (SE01 por Mainsail; SE02/MA01 en display).

## [1.2.0] - 2026-03-12

### Added
- `v3se-config/btt_sfs_2.0.cfg`: configuración para el sensor de filamento BTT Smart Filament Sensor 2.0 (switch + encoder), con macros `SFS_ENABLE` / `SFS_DISABLE`.
- `v3se-config/printer-creality-ender3-v3-se-2023.cfg`: archivo de referencia con el pin mapping oficial de la placa Creality 4.2.2 (STM32F103).

### Changed
- `material_z_offset.cfg`: ajuste del offset Z para PLA de `+0.20` a `+0.05` (primera capa más pegada).
- `printer.cfg`: malla de cama (BED_MESH) recalibrada con nueva pasada de `BED_MESH_CALIBRATE`.

### Fixed
- Instalado symlink `mmu_server.py` de Happy-Hare en Moonraker (`moonraker/components/`), resolviendo el error `ModuleNotFoundError: No module named 'moonraker.components.mmu_server'`.
- Resuelto crash de Klipper `TypeError: 'probe_result' object does not support item assignment` en `prtouch.py` (incompatibilidad con el objeto `ProbeResult` namedtuple de Klipper). Se realizó `FIRMWARE_RESTART` para sacar al MCU de estado de shutdown.

## [1.1.0] - 2026-03-10

### Added
- Improved `README.md` with architecture, quick-start, and maintenance notes.
- Added `LICENSE` (MIT).
- Added GitHub repository topics and project description.

## [1.0.0] - 2026-03-10

### Added
- Initial public release of Ender 3 V3 SE Klipper configuration.
- Modular macro layout (`start_print`, `queue_and_finish`, `tooling_macros`, `spoolman_bridge`).
- Spoolman lane0 sync script and cron examples.
- Filament watchdog documentation and low-stock pause flow.

## [2026-05-10] - z_offset Hotfix for SE01

### Fixed
- **SE01 z_offset sync**: SE01 was running an outdated `spoolman_sync.py` that did not parse `z_offset` from Spoolman filament extras. Updated all 3 hosts (SE01/.1, SE02/.2, MA01/.3) with new version that includes:
  - New `_parse_float()` helper for robust parsing of numeric extras
  - New `_to_bool_int()` helper for boolean extras (fan_lock)
  - z_offset parsing: checks for `z_offset`, `z-offset`, `zoffset`, `material_z_offset` keys
  - fan_lock parsing: converts Spoolman boolean to Klipper integer (0/1)
  - Enhanced retry logic: attempts increased from 5 to 6

### Deployed
- `scripts/spoolman_sync.py` updated in all 3 printer hosts
- SE01 now correctly syncs `Z_OFFSET` parameter to `SYNC_SPOOLMAN_NOW` macro
- SE02/MA01 verified operational (no z_offset regression)

### Verification
- All 3 hosts report `Klippy state = ready`
- File deployment via Moonraker API successful on SE01/.1, SE02/.2, MA01/.3
- Manual test required: Verify SE01 `spoolman_sync.log` shows `z_offset=X.XX` in next sync cycle

