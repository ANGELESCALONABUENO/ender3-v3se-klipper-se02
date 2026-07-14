# README Printer Setup

## Resumen
Configuracion de Klipper para Ender 3 V3 SE con macros externas en `macros/*.cfg` e integracion con Spoolman.

## Fork de Klipper (importante)
Esta instalacion NO usa el Klipper oficial de forma directa.
Usa este fork para soportar `prtouch` (sensor de presion/load-cell para calibracion en la punta):

- Repo: `https://github.com/0xD34D/klipper_ender3_v3_se`
- Ruta local: `/home/pi/klipper`
- Rama actual: `master`
- Commit verificado: `a4dc9078`

## Que es un fork
Un fork es una copia de un proyecto original donde se agregan cambios propios.
En este caso, el fork agrega soporte especifico para hardware de Ender 3 V3 SE que no siempre esta igual en el upstream.

## Archivos principales
- Config base: `/home/pi/printer_data/config/printer.cfg`
- Probing V3 SE: `/home/pi/printer_data/config/v3se-config/prtouch.cfg`
- Macros: `/home/pi/printer_data/config/macros/*.cfg`
- Sync Spoolman (canonico): `/home/pi/sync_lane0/sync_lane0_from_spoolman.sh`

## Nota para mantenimiento
Si se migra a Klipper oficial, validar primero compatibilidad de `prtouch` y macros relacionadas (`PRTOUCH_PROBE_ZOFFSET`) antes de actualizar.
