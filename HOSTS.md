# Hosts del repositorio

Este repositorio corresponde operativamente a estas impresoras/hosts conectados por Tailscale.

## Mapeo principal

| Host | Equipo | IP Tailscale | Usuario SSH |
| --- | --- | --- | --- |
| se01 | Ender 3 V3 SE 01 | 100.100.53.1 | pi |
| se02 | Ender 3 V3 SE 02 | 100.100.53.2 | pi |
| ma01 | MA01 | 100.100.53.3 | pi |

## Uso rapido

```bash
ssh se01
ssh se02
ssh ma01
```

## Nota

- Estas IPs son de Tailscale.
- Este mapeo documenta a qué máquinas corresponde este repositorio.
- La configuración SSH local puede usar aliases `se01`, `se02` y `ma01` apuntando a esas IPs.
