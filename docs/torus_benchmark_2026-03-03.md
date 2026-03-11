# Torus Benchmark Report (2026-03-03)

## Scope

- Repository: `splitnn`
- Date: 2026-03-03
- Topology generator: `driver/scripts/topo/generate_grid_topo.py`
- Generator note: script generates toroidal wrap-around edges (torus).
- Node manager: `cctr`
- Link manager: `ntlbr`
- Flags: `-a naive -d 0 -N cctr -l ntlbr -s server_config_local.json -i 0`

## Tested Topology Scales

### Historical baseline (from `infra/tmp/bench/torus_perf.tsv`)

| Nodes | Dims | Links | Setup Total (s) | Clean Total (s) |
|---:|---|---:|---:|---:|
| 500 | 20x25 | 1000 | 13.44 | 0.47 |
| 1000 | 25x40 | 2000 | 59.63 | 1.02 |
| 2000 | 40x50 | 4000 | 161.61 | 2.08 |
| 4000 | 50x80 | 8000 | 653.11 | 3.91 |

### New runs on 2026-03-03 (current comparison set)

| Nodes | Dims | Links | Setup Node (s) | Setup Link (s) | Setup Total (s) | Setup Wall (s) | Clean Node (s) | Clean Total (s) | Clean Wall (s) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1000 | 25x40 | 2000 | 3.22 | 25.15 | 29.75 | 31.78 | 0.97 | 0.98 | 3.01 |
| 2000 | 40x50 | 4000 | 6.93 | 61.19 | 68.31 | 106.76 | 2.00 | 2.01 | 4.05 |
| 4000 | 50x80 | 8000 | 16.71 | 178.24 | 195.31 | 197.36 | 4.47 | 4.47 | 6.51 |
| 8000 | 80x100 | 16000 | 48.35 | 862.20 | 911.29 | 913.35 | 9.13 | 9.14 | 11.19 |

## Remote Four-Server Practice (2026-03-11)

These runs were executed through the remote driver workflow on four cloned servers.

- Control host runs `driver/batch_test.py`
- Runtime flags: `-a naive -d 0 -N cctr -l ntlbr`
- `b = 48`
- Only torus results are recorded below

### Best Current Torus Results

Use the best verified complete setup wall time seen for each scale so far.

| Nodes | Dims | Best Setup Wall (s) | Notes |
|---:|---|---:|---|
| 2000 | 40x50 | 15.08 | corrected 4-server re-run on the new host set |
| 4000 | 50x80 | 28.76 | corrected 4-server re-run on the new host set |
| 6000 | 75x80 | 49.14 | corrected 4-server re-run on the new host set |
| 8000 | 80x100 | 74.74 | corrected 4-server re-run on the new host set |

### Latest 40x50 Remote Result

Corrected server set:

- `8.211.30.34`
- `47.245.148.67`
- `47.87.129.89`
- `47.245.151.90`

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `8.211.30.34` | 1055 | 1.28 | 13.19 | 4.64 | 14.71 |
| `47.245.148.67` | 1049 | 1.24 | 12.80 | 4.20 | 14.27 |
| `47.87.129.89` | 1054 | 1.36 | 13.48 | 4.65 | 15.08 |
| `47.245.151.90` | 1050 | 1.31 | 13.29 | 4.35 | 14.84 |

### Latest 50x80 Remote Result

Corrected server set:

- `8.211.30.34`
- `47.245.148.67`
- `47.87.129.89`
- `47.245.151.90`

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `8.211.30.34` | 2052 | 2.70 | 24.34 | 4.50 | 27.22 |
| `47.245.148.67` | 2060 | 2.60 | 25.11 | 5.43 | 27.87 |
| `47.87.129.89` | 2054 | 2.80 | 25.63 | 4.88 | 28.59 |
| `47.245.151.90` | 2058 | 2.84 | 25.75 | 5.06 | 28.76 |

### Latest 80x100 Remote Result

Corrected server set:

- `8.211.30.34`
- `47.245.148.67`
- `47.87.129.89`
- `47.245.151.90`

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `8.211.30.34` | 4098 | 6.09 | 59.33 | 9.58 | 65.60 |
| `47.245.148.67` | 4093 | 5.82 | 57.76 | 9.09 | 63.76 |
| `47.87.129.89` | 4097 | 6.62 | 67.93 | 9.58 | 74.74 |
| `47.245.151.90` | 4092 | 6.47 | 68.08 | 9.02 | 74.72 |

### Latest 75x80 Remote Result

Corrected server set:

- `8.211.30.34`
- `47.245.148.67`
- `47.87.129.89`
- `47.245.151.90`

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `8.211.30.34` | 3086 | 4.35 | 40.98 | 8.02 | 45.67 |
| `47.245.148.67` | 3092 | 4.18 | 41.29 | 8.56 | 45.78 |
| `47.87.129.89` | 3086 | 4.44 | 44.37 | 8.31 | 49.14 |
| `47.245.151.90` | 3089 | 4.58 | 44.19 | 8.42 | 49.09 |

## Commands Used

### Topology generation

```bash
python3 driver/scripts/topo/generate_grid_topo.py 40 40 infra/runtime/topo/grid_40_40.txt
python3 driver/scripts/topo/generate_grid_topo.py 50 80 infra/runtime/topo/grid_50_80.txt
python3 driver/scripts/topo/generate_grid_topo.py 80 100 infra/runtime/topo/grid_80_100.txt
```

### Setup/Clean command template

```bash
sudo ./bin/topo_setup_test \
  -o <setup|clean> \
  -t runtime/topo/<topo_file>.txt \
  -b 24 \
  -a naive \
  -d 0 \
  -N cctr \
  -l ntlbr \
  -s server_config_local.json \
  -i 0
```

## Key Observations

- `setup` is dominated by `Link setup time` at larger scales.
- From 4k to 8k nodes, `setup total` grows from `195.31s` to `911.29s` (~4.67x).
- `clean` remains much smaller and closer to linear growth.
- 4k row above uses the latest re-run on 2026-03-03.
- In remote multi-server practice, use the best complete setup wall time per scale as the current summary figure.
- The old remote `75x80` number `94.48s` was superseded by the corrected re-run result `49.14s`.
- The old remote `50x80` number `29.04s` was superseded by the corrected re-run result `28.76s`.
- The old remote `80x100` number `86.10s` was superseded by the corrected re-run result `74.74s`.

## Artifacts

- Summary TSV generated in this run: `infra/tmp/bench/torus_perf_2026-03-03.tsv`
- 8k archived logs:
  - `infra/tmp/bench/runs/2026-03-03_8k/setup_log.txt`
  - `infra/tmp/bench/runs/2026-03-03_8k/clean_log.txt`
