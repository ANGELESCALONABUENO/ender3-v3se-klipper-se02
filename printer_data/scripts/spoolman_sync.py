#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.request
import urllib.error


LOG_PATH = "/home/pi/printer_data/logs/spoolman_sync.log"


def _log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass


def _http_json(url: str, method: str = "GET", body: dict | None = None, timeout_s: float = 10.0) -> dict:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def _post_gcode_with_retry(moonraker: str, script: str, attempts: int = 6) -> None:
    last_err: Exception | None = None
    for i in range(attempts):
        try:
            _http_json(
                f"{moonraker}/printer/gcode/script",
                method="POST",
                body={"script": script},
                timeout_s=8.0,
            )
            return
        except urllib.error.HTTPError as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(0.4 + (i * 0.4))
                continue
            raise
        except Exception as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(0.4 + (i * 0.4))
                continue
            raise
    if last_err is not None:
        raise last_err


def _to_bool_int(val) -> int:
    if isinstance(val, bool):
        return 1 if val else 0
    if val is None:
        return 0
    s = str(val).strip().lower()
    if s in ("1", "true", "yes", "on", "si", "sí"):
        return 1
    return 0


def _parse_float(extra: dict, keys: tuple[str, ...], default=None):
    for k in keys:
        v = extra.get(k)
        if v not in (None, ""):
            try:
                return float(str(v).strip())
            except Exception:
                continue
    return default


def main() -> int:
    spoolman_server = os.environ.get("SPOOLMAN_SERVER", "http://100.100.10.1:7912").rstrip("/")
    moonraker = os.environ.get("MOONRAKER", "http://127.0.0.1:7125").rstrip("/")

    _log(f"start moonraker={moonraker} spoolman={spoolman_server}")

    # Durante impresion solo saltar si ya estamos sincronizados; si synced=0, intentar recuperar.
    try:
        ps = _http_json(
            f"{moonraker}/printer/objects/query?print_stats=state&gcode_macro%20SPOOLMAN_ACTIVE=synced"
        )
        status = ps.get("result", {}).get("status", {})
        print_state = status.get("print_stats", {}).get("state", "")
        synced = int(status.get("gcode_macro SPOOLMAN_ACTIVE", {}).get("synced", 0))
        if print_state in ("printing", "paused") and synced == 1:
            _log(f"skip: state={print_state} synced={synced}")
            print(f"spoolman_sync: skip (state={print_state}, synced={synced})")
            return 0
    except Exception as e:
        _log(f"warn: no se pudo verificar estado/synced: {e!r}")

    status = _http_json(f"{moonraker}/server/spoolman/status")
    spool_id = (status.get("result") or {}).get("spool_id")
    if spool_id in (None, "", "None"):
        _log("no active spool_id")
        print("spoolman_sync: no active spool_id")
        return 0

    spool = _http_json(f"{spoolman_server}/api/v1/spool/{spool_id}")
    filament = spool.get("filament") or {}
    spool_extra = spool.get("extra") or {}
    filament_extra = filament.get("extra") or {}

    remaining_g = spool.get("remaining_weight")
    nozzle_temp = filament.get("settings_extruder_temp")
    bed_temp = filament.get("settings_bed_temp")

    pa = _parse_float(filament_extra, ("pressure_advance", "advance", "pa", "pressureAdvance", "pressure-advance"), default=0.1)
    z_offset = _parse_float(filament_extra, ("z_offset", "z-offset", "zoffset", "material_z_offset"), default=None)
    fan_lock = _to_bool_int(filament_extra.get("fan_lock", 0))
    initial_purge_distance = _parse_float(
        spool_extra,
        ("initial_purge_distance", "initial_purge_mm", "purge_distance", "startup_purge_distance"),
        default=None,
    )
    if initial_purge_distance is None:
        initial_purge_distance = _parse_float(
            filament_extra,
            ("initial_purge_distance", "initial_purge_mm", "purge_distance", "startup_purge_distance"),
            default=None,
        )
    if initial_purge_distance is not None:
        try:
            initial_purge_distance = float(initial_purge_distance)
            if initial_purge_distance < 0.0:
                initial_purge_distance = 0.0
            if initial_purge_distance > 300.0:
                initial_purge_distance = 300.0
        except Exception:
            initial_purge_distance = None

    script = "SYNC_SPOOLMAN_NOW"
    try:
        if nozzle_temp not in (None, ""):
            script += f" NOZZLE={float(nozzle_temp)}"
    except Exception:
        pass
    try:
        if bed_temp not in (None, ""):
            script += f" BED={float(bed_temp)}"
    except Exception:
        pass
    try:
        if remaining_g not in (None, ""):
            script += f" REMAINING_G={float(remaining_g)}"
    except Exception:
        pass

    if pa is not None:
        script += f" PRESSURE_ADVANCE={float(pa)}"
    if z_offset is not None:
        script += f" Z_OFFSET={float(z_offset)}"
    script += f" FAN_LOCK={int(fan_lock)}"
    if initial_purge_distance is not None:
        script += f" INITIAL_PURGE_DISTANCE={float(initial_purge_distance)}"

    _post_gcode_with_retry(moonraker, script, attempts=6)

    _log(
        "ok "
        + f"spool_id={spool_id} noz={nozzle_temp!r} bed={bed_temp!r} pa={pa!r} z_offset={z_offset!r} fan_lock={fan_lock} purge_mm={initial_purge_distance!r} "
        + f"posted={script!r}"
    )
    print(
        f"spoolman_sync: ok spool_id={spool_id} noz={nozzle_temp!r} bed={bed_temp!r} "
        + f"pa={pa!r} z_offset={z_offset!r} fan_lock={fan_lock} purge_mm={initial_purge_distance!r}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        _log(f"error: {e!r}")
        print(f"spoolman_sync: error: {e}", file=sys.stderr)
        raise SystemExit(1)
