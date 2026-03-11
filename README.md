# SplitNN

SplitNN is a virtual network construction framework for benchmarking large-scale emulation setup and cleanup performance across one or more Linux servers or VMs.

## Recommended Usage

The current recommended path is remote benchmark on multiple cloned servers:

1. prepare one Linux server or VM as the base environment
2. install runtime and build dependencies there
3. clone that base image horizontally into multiple machines
4. keep the same repo path, username, and password on all machines
5. edit `driver/server_config.json`
6. edit `driver/batch_test.py` benchmark options
7. run `driver/batch_test.py` from one control host

This matches the current codebase because:

- `driver/` is the real remote orchestration entry
- each remote machine is treated as one `server`
- result collection is wired around remote `infra/tmp/`
- cleanup is optimized around process kill plus namespace deletion
- benchmark docs in `docs/` already reflect this workflow

## Key Files

If you only want the important entry points, start here:

- `driver/batch_test.py`
  Remote multi-server test entry. Connects to each guest, prepares topology, runs `setup`/`clean`, and collects results.

- `driver/server_config.json`
  Multi-server configuration file. Set guest IPs, shared SSH credentials, NIC name, `infraWorkDir`, `runtimeDir`, and `phyicalMachineId` here.

- `infra/bin/topo_setup_test`
  Core runtime binary executed on each server or guest.

- `infra/server_config_local.json`
  Single-machine or single-guest local config for direct `infra` testing.

- `infra/code/network/netManage.go`
  Main setup/clean orchestration logic.

- `infra/code/network/ntlBrManager.go`
  Link manager implementation for bridges, veths, and VXLAN handling.

- `infra/code/network/cctrManager.go`
  Node/container manager used by the current workflow.

- `docs/horizontal_scaling_splitnn.md`
  Concise remote benchmark guide for cloned multi-server setups.

- `docs/torus_benchmark_2026-03-03.md`
  Current torus benchmark summary, including the latest four-server remote practice results.

- `docs/fat_tree_benchmark_2026-03-11.md`
  Current fat-tree benchmark summary on the validated four-server remote setup.

- `docs/local_benchmark.md`
  Single-machine benchmark workflow.

## Directory Layout

- `infra/`
  Core executor that performs actual network setup and cleanup on one machine or VM.

- `driver/`
  Remote orchestration, topology generation, partitioning, and result collection.

- `dataproc/`
  Plotting and result post-processing scripts.

## Remote Multi-Guest Workflow

Use this when you have multiple cloned VMs or servers and want to operate them remotely from one control node.

### 1. Prepare each remote machine

Install runtime dependencies on every guest:

- `iproute2`
- `podman`
- `skopeo`
- `umoci`
- `bpftrace`
- `sudo`

Remote benchmark with the current `driver/batch_test.py` also needs remote build capability:

- `git`
- `golang`
- `gcc`
- `make`
- `python3`

### 2. Keep one shared SSH credential

`driver/util/remote.py` uses Paramiko password SSH. The simplest scalable setup is:

- one shared guest username
- one strong shared password
- password SSH enabled on all cloned guests

Only IP addresses need to differ.

### 3. Configure remote servers

Edit `driver/server_config.json`.

Important fields:

- `ipAddr`
- `user`
- `password`
- `phyIntf`
- `infraWorkDir`
- `runtimeDir`
- `phyicalMachineId`

Recommended setting:

- `runtimeDir` should be `.../infra/tmp`

This matches the current remote result collection behavior in `driver/batch_test.py`.

### 4. Edit Benchmark Options

Before running, update `driver/batch_test.py`:

- set `var_options["t"]` to the topology list you want
- set `var_options["b"]` to the benchmark value you want
- keep `p = 0`

Do not use `-p > 0` for benchmark runs. The current parallel link setup path is buggy.

### 5. Run the remote batch driver

From the control host:

```bash
cd driver
python3 batch_test.py
```

The driver will:

- connect to all configured guests
- run `sync_code.sh`
- run remote `make`
- send `server_config.json`
- generate and partition topology
- send each sub-topology to the target guest
- run remote `setup`
- run remote `clean`
- collect logs back into `driver/raw_results/`

### 6. Read remote results

Collected outputs are stored under:

```bash
driver/raw_results/result-<server_num>-servers/
```

Typical files per server:

- `setup_log.txt`
- `clean_log.txt`
- `link_log.txt`
- `setup_cpu_mem_usage.txt`
- `clean_cpu_mem_usage.txt`

## Single-Machine Workflow

Use this when you want to test one machine or one guest directly without the remote driver.

### 1. Install dependencies

- `go`
- `gcc`
- `make`
- `python3`
- `iproute2`
- `podman`
- `skopeo`
- `umoci`
- `bpftrace`

### 2. Build

```bash
cd infra
make
```

### 3. Fix local config

Update `infra/server_config_local.json` so that:

- `infraWorkDir` points to your local `infra/`
- `runtimeDir` points to a writable in-repo runtime path
- `phyIntf` matches the local NIC name

### 4. Generate a torus topology

Example `20x20` torus:

```bash
mkdir -p infra/runtime/topo
python3 driver/scripts/topo/generate_grid_topo.py 20 20 infra/runtime/topo/grid_20_20.txt
```

The current `grid` generator wraps dimensions, so it behaves as a torus generator in practice.

### 5. Run setup and clean

```bash
cd infra
sudo ./bin/topo_setup_test \
  -o setup \
  -t runtime/topo/grid_20_20.txt \
  -b 24 \
  -a naive \
  -d 0 \
  -N cctr \
  -l ntlbr \
  -s server_config_local.json \
  -i 0

sudo ./bin/topo_setup_test \
  -o clean \
  -t runtime/topo/grid_20_20.txt \
  -b 24 \
  -a naive \
  -d 0 \
  -N cctr \
  -l ntlbr \
  -s server_config_local.json \
  -i 0
```

Logs:

- `infra/runtime/setup_log.txt`
- `infra/runtime/clean_log.txt`

## Cleanup Model

The current normal cleanup path is intentionally simple:

- kill node/container processes
- delete SplitNN-created backbone namespaces (`bbns*`)
- rely on kernel namespace teardown to reclaim veth, bridge, and VXLAN devices

This behavior is implemented in:

- `infra/code/network/netManage.go`
- `infra/code/network/cctrManager.go`
- `infra/code/network/ntlBrManager.go`

Important current behavior:

- cleanup no longer deletes every network namespace on the machine
- backbone cleanup is limited to SplitNN-created namespaces
- explicit per-link deletion is not part of the normal fast cleanup path

## More Detailed Docs

- `docs/local_benchmark.md`
- `docs/horizontal_scaling_splitnn.md`
