# Local Benchmark Guide

This document records the single-machine benchmark workflow used in recent tests.

## Scope

- Machine: local host
- Binary: `infra/bin/topo_setup_test`
- Config: `infra/server_config_local.json`
- Topologies:
  - `infra/tmp/topo/grid_20_25.txt` (500 nodes, 1000 edges)
  - `infra/tmp/topo/grid_25_40.txt` (1000 nodes, 2000 edges)
  - `infra/tmp/topo/grid_40_50.txt` (2000 nodes, 4000 edges)
  - `infra/tmp/topo/grid_50_80.txt` (4000 nodes, 8000 edges)

## Fixed Flags

Unless explicitly testing other options, keep:

- `-a naive`
- `-d 0`
- `-N cctr`
- `-l ntlbr`
- `-s server_config_local.json`
- `-i 0`

Only vary:

- topology file (`-t`)
- BBNS number (`-b`)

## One-Test Procedure

Run setup:

```bash
cd /home/ecs-user/work/splitnn/infra
sudo ./bin/topo_setup_test \
  -o setup \
  -t tmp/topo/grid_25_40.txt \
  -b 24 \
  -a naive \
  -d 0 \
  -N cctr \
  -l ntlbr \
  -s server_config_local.json \
  -i 0
```

Extract key timings:

```bash
cd /home/ecs-user/work/splitnn/infra
rg -n "edgeSum|Node setup time|Bbns setup time|Link setup time|Network operation time" tmp/setup_log.txt
```

Run cleanup:

```bash
cd /home/ecs-user/work/splitnn/infra
sudo ./bin/topo_setup_test \
  -o clean \
  -t tmp/topo/grid_25_40.txt \
  -b 24 \
  -a naive \
  -d 0 \
  -N cctr \
  -l ntlbr \
  -s server_config_local.json \
  -i 0
```

## Recommended Multi-Run Order

For scale test with fixed `b`:

1. 500 (`grid_20_25`)
2. 1k (`grid_25_40`)
3. 2k (`grid_40_50`)
4. 4k (`grid_50_80`)

Between tests:

1. run `clean`
2. `sleep 10`
3. run next `setup`

## Residual Cleanup (When Needed)

If a run is interrupted or results look unstable, clean residual resources:

```bash
cd /home/ecs-user/work/splitnn/infra
sudo pkill -f topo_setup_test || true
sudo ip -all netns del || true
sudo ip link del group 1 || true
sudo pkill -f "monitor_kern_func.sh|monitor_cctr_time.sh|monitor_cpu_mem_usage.py|bpftrace" || true
```

Verify clean state:

```bash
ip netns list
ip -d -o link show | rg "group 1|vxlan|bbns|probe-dummy" || true
pgrep -af "topo_setup_test|monitor_kern_func.sh|monitor_cctr_time.sh|monitor_cpu_mem_usage.py|bpftrace|cctr|goctr" || true
```

## Result Table Template

Use this format to track runs:

| Size | Topology | b | edgeSum | Node(s) | Bbns(s) | Link(s) | Network(s) | Wall(s) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 500 | grid_20_25 | 24 | 1000 |  |  |  |  |  |
| 1k | grid_25_40 | 24 | 2000 |  |  |  |  |  |
| 2k | grid_40_50 | 24 | 4000 |  |  |  |  |  |
| 4k | grid_50_80 | 24 | 8000 |  |  |  |  |  |

## Notes on Variance

- `Network operation time` is the main metric.
- Large variance can occur after interrupted runs or leftover monitor/netns state.
- If variance is high, run residual cleanup before retesting.
