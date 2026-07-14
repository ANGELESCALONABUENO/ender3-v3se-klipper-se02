# SE02 - Ender 3 V3 SE 02

**Máquina:** Ender 3 V3 SE (Unidad 02)  
**IP Tailscale:** 100.100.53.2  
**Usuario SSH:** pi  
**Repositorio:** https://github.com/ANGELESCALONABUENO/ender3-v3se-klipper-se02

## Configuración específica de SE02

- Puerto serie: /dev/ttyAMA0
- Sensor: BLTouch/CRTouch
- Motherboard: Creality 4.2.2 (STM32F103)
- Pantalla: Display integrado (si aplica)

## Actualizar configuración

```bash
# En SE02:
cd /home/pi/printer_data/config
git pull origin master
```

O vía webhook en Moonraker para actualizaciones automáticas.
