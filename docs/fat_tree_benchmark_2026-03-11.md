# Fat-Tree Benchmark Report (2026-03-11)

## Scope

- Repository: `splitnn`
- Topology generator: `driver/scripts/topo/generate_clos_topo.py`
- Generator note: `clos` is used as the current fat-tree topology generator in this repo
- Remote mode: 4-server remote driver workflow
- Runtime flags: `-a naive -d 0 -N cctr -l ntlbr`

## Remote Server Set

The current validated four-server set is:

- `8.211.30.34`
- `47.245.148.67`
- `47.87.129.89`
- `47.245.151.90`

## Current Verified Results

Only completed and validated runs are recorded below.

| Topology | b | Best Setup Wall (s) | Notes |
|---|---:|---:|---|
| `k=20` | 48 | 47.00 | current best verified result |
| `k=20` | 128 | 56.35 | slower than `b=48` |
| `k=24` | 48 | 89.08 | current best verified result |

## Latest k=20 Result (`b=48`)

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `8.211.30.34` | 1960 | 1.60 | 42.52 | 31.18 | 44.46 |
| `47.245.148.67` | 1827 | 1.65 | 44.29 | 34.81 | 46.24 |
| `47.87.129.89` | 1901 | 1.72 | 44.96 | 34.36 | 47.00 |
| `47.245.151.90` | 1831 | 1.70 | 41.35 | 30.59 | 43.36 |

## Latest k=20 Result (`b=128`)

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `8.211.30.34` | 1960 | 1.62 | 43.68 | 32.24 | 54.89 |
| `47.245.148.67` | 1827 | 1.60 | 44.49 | 34.96 | 55.32 |
| `47.87.129.89` | 1901 | 1.67 | 45.13 | 34.42 | 56.35 |
| `47.245.151.90` | 1831 | 1.64 | 42.03 | 31.20 | 52.70 |

## Latest k=24 Result (`b=48`)

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `8.211.30.34` | 3240 | 2.77 | 77.09 | 57.19 | 79.99 |
| `47.245.148.67` | 3034 | 2.74 | 70.66 | 51.53 | 73.52 |
| `47.87.129.89` | 3240 | 2.93 | 78.58 | 57.79 | 81.64 |
| `47.245.151.90` | 3448 | 2.98 | 85.99 | 64.40 | 89.08 |

## Notes

- `Node setup time` is small in these runs; the dominant cost is `Link setup time`.
- `ExternalLinkOp time` is much larger than in torus runs, which is the main reason fat-tree is slower.
- `k=26` and `k=30` are not recorded yet in this document because there is no completed, validated rerun on the current four-server set.
