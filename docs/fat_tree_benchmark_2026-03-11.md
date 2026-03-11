# Fat-Tree Benchmark Report (2026-03-11)

## Scope

- Repository: `splitnn`
- Topology generator: `driver/scripts/topo/generate_clos_topo.py`
- Generator note: `clos` is used as the current fat-tree topology generator in this repo
- Remote mode: 4-server remote driver workflow
- Runtime flags: `-a naive -d 0 -N cctr -l ntlbr`

## Remote Server Set

The latest validated four-server set is:

- `47.87.129.103`
- `8.220.75.44`
- `8.209.103.4`
- `47.87.132.233`

## Current Verified Results

Only completed and validated runs are recorded below.

| Topology | b | Best Setup Wall (s) | Notes |
|---|---:|---:|---|
| `k=20` | 48 | 47.00 | current best verified result |
| `k=20` | 128 | 56.35 | slower than `b=48` |
| `k=24` | 48 | 89.08 | fastest recorded result; later rerun reproduced `89.11s` |
| `k=26` | 48 | 117.95 | current best verified result |
| `k=28` | 48 | 171.19 | fastest recorded result on the latest server set |
| `k=30` | 48 | 195.60 | stable rerun result on the current server set |

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
| `8.211.30.34` | 3240 | 2.81 | 77.21 | 57.47 | 80.14 |
| `47.245.148.67` | 3034 | 2.77 | 70.39 | 51.52 | 73.28 |
| `47.87.129.89` | 3240 | 2.91 | 78.44 | 57.78 | 81.46 |
| `47.245.151.90` | 3448 | 2.99 | 86.01 | 64.74 | 89.11 |

## Latest k=26 Result (`b=48`)

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `8.211.30.34` | 4009 | 3.80 | 100.13 | 74.30 | 104.11 |
| `47.245.148.67` | 3780 | 3.46 | 91.04 | 66.08 | 94.67 |
| `47.87.129.89` | 4426 | 3.90 | 113.88 | 83.14 | 117.95 |
| `47.245.151.90` | 4266 | 3.85 | 112.70 | 83.98 | 116.73 |

## Latest k=30 Result (`b=48`)

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `8.211.30.34` | 6780 | 5.99 | 189.30 | 139.30 | 195.60 |
| `47.245.148.67` | 5605 | 5.78 | 147.96 | 105.69 | 154.05 |
| `47.87.129.89` | 6467 | 6.46 | 186.98 | 129.49 | 193.76 |
| `47.245.151.90` | 6467 | 6.51 | 188.00 | 130.71 | 194.83 |

## Latest k=28 Result (`b=48`)

| Server | edgeSum | Node Setup (s) | Link Setup (s) | ExternalLinkOp (s) | Setup Total (s) |
|---|---:|---:|---:|---:|---:|
| `47.87.129.103` | 5566 | 4.76 | 148.32 | 105.36 | 153.33 |
| `8.220.75.44` | 4168 | 4.94 | 113.16 | 80.76 | 118.37 |
| `8.209.103.4` | 4726 | 4.62 | 126.91 | 95.59 | 131.78 |
| `47.87.132.233` | 6142 | 4.69 | 166.24 | 124.43 | 171.19 |

## Notes

- `Node setup time` is small in these runs; the dominant cost is `Link setup time`.
- `ExternalLinkOp time` is much larger than in torus runs, which is the main reason fat-tree is slower.
- `k=26`, `k=28`, and `k=30` all have completed reruns and are recorded above.
