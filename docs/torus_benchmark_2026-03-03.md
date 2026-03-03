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

### New runs on 2026-03-03

| Nodes | Dims | Links | Setup Node (s) | Setup Link (s) | Setup Total (s) | Setup Wall (s) | Clean Node (s) | Clean Total (s) | Clean Wall (s) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1600 | 40x40 | 3200 | 5.68 | 45.66 | 51.35 | 54.46 | 1.63 | 1.64 | 3.67 |
| 4000 | 50x80 | 8000 | 17.14 | 175.97 | 198.00 | 200.08 | 4.13 | 4.13 | 6.17 |
| 8000 | 80x100 | 16000 | 48.35 | 862.20 | 911.29 | 913.35 | 9.13 | 9.14 | 11.19 |

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
- From 4k to 8k nodes, `setup total` grows from `198.00s` to `911.29s` (~4.60x).
- `clean` remains much smaller and closer to linear growth.

## Artifacts

- Summary TSV generated in this run: `infra/tmp/bench/torus_perf_2026-03-03.tsv`
- 8k archived logs:
  - `infra/tmp/bench/runs/2026-03-03_8k/setup_log.txt`
  - `infra/tmp/bench/runs/2026-03-03_8k/clean_log.txt`
