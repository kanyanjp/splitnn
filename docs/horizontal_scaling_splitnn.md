# SplitNN Remote Benchmark Guide

This document is the shortest practical path for running remote benchmarks on multiple cloned servers.

## Scope

- one control host
- multiple remote Linux servers or VMs
- password SSH
- remote `setup/clean` driven by `driver/batch_test.py`

## What Actually Runs

- control host runs `driver/batch_test.py`
- each remote machine is one `server`
- each remote machine runs `infra/bin/topo_setup_test`
- logs are written under remote `infra/tmp/`
- results are collected back to `driver/raw_results/`

## Remote Machine Requirements

Each remote machine needs:

- the repo at the same path
- `sudo`
- `git`
- `go`
- `gcc`
- `make`
- `python3`
- `iproute2`
- `podman`
- `skopeo`
- `umoci`
- `bpftrace`

Recommended repo path:

- `/home/ecs-user/splitnn`

Recommended runtime path:

- `/home/ecs-user/splitnn/infra/tmp`

## Shared SSH Setup

Use one shared account and one shared password on all cloned machines.

The current remote driver uses Paramiko password SSH, so each machine should allow:

- same `user`
- same `password`
- `PasswordAuthentication yes`

## Required Config

Edit [server_config.json](/home/ecs-user/splitnn/driver/server_config.json).

Important fields:

- `ipAddr`
- `user`
- `password`
- `phyIntf`
- `infraWorkDir`
- `runtimeDir`
- `phyicalMachineId`

Recommended values for cloned servers:

- `phyIntf`: `eth0`
- `infraWorkDir`: `/home/ecs-user/splitnn/infra`
- `runtimeDir`: `/home/ecs-user/splitnn/infra/tmp`

## Important Code Reality

Current [batch_test.py](/home/ecs-user/splitnn/driver/batch_test.py) does more than just run remote setup:

- it calls `./sync_code.sh master`
- it runs remote `make`
- it pulls the container image remotely

So remote machines must be able to build, not just execute.

Also note:

- `var_options["t"]` in [batch_test.py](/home/ecs-user/splitnn/driver/batch_test.py) is not pre-filled for your benchmark cases
- `b` in [batch_test.py](/home/ecs-user/splitnn/driver/batch_test.py) is not set to the benchmark values by default
- `-p > 0` is currently buggy in parallel link setup and should not be used for benchmark runs

For stable benchmark runs, keep:

- `p = 0`

## Minimal Remote Benchmark Workflow

1. prepare all remote machines with the same repo path and dependencies
2. edit [server_config.json](/home/ecs-user/splitnn/driver/server_config.json)
3. edit `var_options` in [batch_test.py](/home/ecs-user/splitnn/driver/batch_test.py)
4. run the driver from the control host
5. collect results from `driver/raw_results/`

## Typical `batch_test.py` Changes

Set the topologies you actually want in `var_options["t"]`.

Examples:

- torus: `["grid", "40", "50"]`
- torus: `["grid", "50", "80"]`
- fat-tree: `["clos", "20"]`
- fat-tree: `["clos", "24"]`

Set the benchmark `b` values you want in `var_options["b"]`.

Examples:

- torus: `48`
- fat-tree: `48`

Do not enable the commented `p` list for benchmark runs.

## Run

From the control host:

```bash
cd /home/ecs-user/splitnn/driver
python3 batch_test.py
```

## Results

Collected results are stored under:

```bash
driver/raw_results/result-<server_num>-servers/
```

Typical files per server:

- `setup_log.txt`
- `clean_log.txt`
- `link_log.txt`
- `setup_cpu_mem_usage.txt`
- `clean_cpu_mem_usage.txt`

## Current Validated Four-Server Set

The latest validated set used for the recorded benchmark docs is:

- `47.87.129.103`
- `8.220.75.44`
- `8.209.103.4`
- `47.87.132.233`

## Current Recorded Results

See:

- [torus_benchmark_2026-03-03.md](/home/ecs-user/splitnn/docs/torus_benchmark_2026-03-03.md)
- [fat_tree_benchmark_2026-03-11.md](/home/ecs-user/splitnn/docs/fat_tree_benchmark_2026-03-11.md)
