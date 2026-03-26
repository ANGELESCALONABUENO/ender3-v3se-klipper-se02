# Fix: `PRTOUCH_PROBE_ZOFFSET` internal error (`probe_result` is immutable)

## Síntoma
Al ejecutar `PRTOUCH_PROBE_ZOFFSET` (por ejemplo vía el macro `calibrar_punta`), Klipper entra en estado **shutdown** y muestra un error similar a:

- `Internal error on command:"PRTOUCH_PROBE_ZOFFSET"`
- `TypeError: 'probe_result' object does not support item assignment`

En los logs suele apuntar a:

- `/home/pi/klipper/klippy/extras/prtouch.py` cerca de la línea donde se hace `z_probe[2] = ...`

## Causa
En algunas versiones/entornos, `probe.run_single_probe(...)` devuelve un objeto tipo `probe_result` **inmutable**. El extra `prtouch.py` intenta modificarlo como si fuera una lista (`z_probe[2] = ...`), lo cual dispara el `TypeError`.

## Solución (parche)
En vez de asignar sobre `z_probe`, construir una lista mutable `[x, y, z]` y pasarla a `probe_calibrate_finalize(...)`.

## Cómo aplicar en la Raspberry (se01/ma01/etc.)
1) Respaldar el archivo:

```bash
cp -a /home/pi/klipper/klippy/extras/prtouch.py \
  /home/pi/klipper/klippy/extras/prtouch.py.bak-$(date +%Y%m%d-%H%M%S)
```

2) Editar el bloque dentro de `cmd_PRTOUCH_PROBE_ZOFFSET`.

Reemplazar:

```py
z_probe[2] = homing_origin[2] + z_adjust - start_z_offset
self.probe_calibrate_finalize(z_probe)
```

Por:

```py
# Newer Klipper versions may return an immutable probe_result object
# from run_single_probe. Build a mutable [x, y, z] list for finalize.
z_probe_z = homing_origin[2] + z_adjust - start_z_offset
z_probe_pos = [z_probe[0], z_probe[1], z_probe_z]
self.probe_calibrate_finalize(z_probe_pos)
```

3) Reiniciar Klipper para cargar el cambio:

- Ejecutar `FIRMWARE_RESTART` desde Mainsail/Fluidd.

## Notas
- Este repo mantiene configs/macros; el archivo `prtouch.py` vive en la instalación de Klipper del host.
- Si usas KIAUH o actualizas Klipper, el archivo puede sobrescribirse y tendrás que reaplicar el parche.
