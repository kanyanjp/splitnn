# SplitNN

SplitNN is a virtual network construction framework used to benchmark large-scale emulation setup/cleanup performance.

## Key Directories

- `infra/`: core executor (`topo_setup_test`) that performs network setup/cleanup on one machine/VM.
- `driver/`: experiment orchestrator for multi-machine and batch runs.
- `dataproc/`: plotting and result post-processing scripts.

## Quick Start (Single-Machine Benchmark)

Use this for fast local benchmarking.

1. Build `infra` binary:

```bash
cd infra
make
```

2. Use local config:

- `infra/server_config_local.json` should point `infraWorkDir` to your local repo path.
- Topology files are in `infra/tmp/topo/` (for example `grid_20_25.txt`, `grid_25_40.txt`, `grid_40_50.txt`, `grid_50_80.txt`).

3. Run one setup test:

```bash
cd infra
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

4. Cleanup immediately after each run:

```bash
cd infra
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

5. Read timing results:

- `infra/tmp/setup_log.txt`: `Node setup time`, `Link setup time`, `Network operation time`
- `infra/tmp/clean_log.txt`: cleanup timing

## Minimal Benchmark Playbook

- For `b` scan: run fixed topology (for example `grid_20_25`) with varying `-b`, compare `Network operation time`.
- For scaling test: keep flags fixed and run `500 -> 1k -> 2k -> 4k`.
- Recommended between runs: cleanup, optional `sleep 10`, then next setup.

## Full Local Benchmark Guide

See [docs/local_benchmark.md](docs/local_benchmark.md) for:

- exact commands
- residual resource cleanup commands
- reproducibility checklist
- table template for recording results
