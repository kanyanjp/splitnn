# Cloud Hypervisor VM Workflow

This document records the minimal workflow for running `splitnn` on Debian VMs started by `cloud-hypervisor`.

## Scope

- Host hypervisor: `cloud-hypervisor`
- Guest OS: Debian 12 cloud image
- Verified shape: 2 VMs on one host
- Verified guest IPs:
  - `192.168.249.11`
  - `192.168.249.12`
- Verified guest user:
  - user: `ccds`
  - password: `splitnn`

`splitnn` treats each VM as a `server`. The emulated topology nodes are still created inside each VM through namespaces, veth pairs, bridges, VXLAN devices, and `cctr`.

## Layout

Host-side helper files are stored under:

- `/home/ccds/vms/ch/setup_host_net.sh`
- `/home/ccds/vms/ch/build_seed_images.sh`
- `/home/ccds/vms/ch/launch_vm.sh`
- `/home/ccds/vms/ch/seed-data/`

Repository path on the host:

- `/home/ccds/work/splitnn`

Recommended repo path inside each guest:

- `/home/ccds/work/splitnn`

## Host Preparation

Install and verify `cloud-hypervisor` on the host:

```bash
mise use -g aqua:cloud-hypervisor/cloud-hypervisor
mise x -- cloud-hypervisor --version
```

Verify KVM access for the current user:

```bash
sg kvm -c 'id && [ -r /dev/kvm ] && [ -w /dev/kvm ] && echo kvm-ok'
```

Prepare the host bridge and tap devices:

```bash
/home/ccds/vms/ch/setup_host_net.sh
```

This creates:

- bridge: `chbr0`
- bridge IP: `192.168.249.1/24`
- tap devices: `chtap0`, `chtap1`

## Guest Image Preparation

Download the Debian cloud image once:

```bash
mkdir -p /home/ccds/vms/ch
cd /home/ccds/vms/ch
curl -fL --retry 3 -o debian-12-genericcloud-amd64.qcow2 \
  https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-genericcloud-amd64.qcow2
```

Create fresh overlay disks:

```bash
cd /home/ccds/vms/ch
qemu-img create -f qcow2 -F qcow2 -b debian-12-genericcloud-amd64.qcow2 vm1.qcow2
qemu-img create -f qcow2 -F qcow2 -b debian-12-genericcloud-amd64.qcow2 vm2.qcow2
```

Build cloud-init seed images:

```bash
/home/ccds/vms/ch/build_seed_images.sh
```

The current seed data configures:

- `splitnn-vm1` on `192.168.249.11/24`
- `splitnn-vm2` on `192.168.249.12/24`
- default gateway `192.168.249.1`
- `ccds/splitnn`
- password SSH enabled
- passwordless `sudo`

## Start VMs

Start VM1:

```bash
/home/ccds/vms/ch/launch_vm.sh vm1 vm1.qcow2 cidata-vm1.img chtap0
```

Start VM2:

```bash
/home/ccds/vms/ch/launch_vm.sh vm2 vm2.qcow2 cidata-vm2.img chtap1
```

Useful logs:

- `/home/ccds/vms/ch/vm1.serial.log`
- `/home/ccds/vms/ch/vm2.serial.log`
- `/home/ccds/vms/ch/vm1.ch.log`
- `/home/ccds/vms/ch/vm2.ch.log`

Verify connectivity from the host:

```bash
ping -c 1 192.168.249.11
ping -c 1 192.168.249.12
ssh ccds@192.168.249.11
ssh ccds@192.168.249.12
```

## Use China Mirrors In Guests

For guest package installation, use the Tsinghua mirror:

```bash
cat >/etc/apt/sources.list <<'EOF'
deb https://mirrors.tuna.tsinghua.edu.cn/debian bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
EOF
apt-get update
```

If the host builds `splitnn`, the guests only need runtime packages:

```bash
apt-get install -y iproute2 podman skopeo umoci sudo rsync bpftrace
```

If you also want to build inside the guest:

```bash
apt-get install -y git golang gcc make python3 python3-pip
```

## Recommended SplitNN Workflow

The simplest workflow is:

1. Build on the host.
2. Generate topology on the host.
3. Sync the repo or `infra/` subtree to the guest.
4. Run `topo_setup_test` inside the guest.

This avoids installing the full build toolchain in every VM.

## Build On Host

```bash
cd /home/ccds/work/splitnn/infra
make
```

This produces:

- `infra/bin/cctr`
- `infra/bin/goctr`
- `infra/bin/topo_setup_test`

## Generate 30x30 Torus

Use the existing `grid` generator. It already wraps both dimensions, so it is a torus generator in practice.

```bash
cd /home/ccds/work/splitnn
mkdir -p infra/runtime/topo
python3 driver/scripts/topo/generate_grid_topo.py 30 30 infra/runtime/topo/grid_30_30.txt
```

## Sync To Guest

Example sync to VM1:

```bash
rsync -av /home/ccds/work/splitnn/ ccds@192.168.249.11:/home/ccds/work/splitnn/
```

Sync to VM2 if needed:

```bash
rsync -av /home/ccds/work/splitnn/ ccds@192.168.249.12:/home/ccds/work/splitnn/
```

## Guest Config For Single-VM Infra Test

Inside the guest, adjust the local config to match the guest interface and path. A minimal example:

```json
{
  "servers": [
    {
      "ipAddr": "127.0.0.1",
      "user": "ccds",
      "password": "",
      "phyIntf": "ens3",
      "infraWorkDir": "/home/ccds/work/splitnn/infra",
      "runtimeDir": "/home/ccds/work/splitnn/infra/runtime",
      "dockerImageName": "public.ecr.aws/docker/library/alpine:3.23",
      "kernFuncsToMonitor": [
        ["setup", "cctr", "chroot_fs_refs"],
        ["setup", "topo_setup_test", "wireless_nlevent_flush"],
        ["setup", "topo_setup_test", "fib6_clean_tree"],
        ["clean", "", "br_vlan_flush"]
      ],
      "server_best_bbns_factor": 2.353,
      "phyicalMachineId": 0,
      "phyicalMachineNodeCapacity": 15000
    }
  ]
}
```

Important field:

- `phyIntf` must be `ens3` in these VMs, not `eth0`

## Run 30x30 Torus In One Guest

Setup:

```bash
cd /home/ccds/work/splitnn/infra
sudo ./bin/topo_setup_test \
  -o setup \
  -t runtime/topo/grid_30_30.txt \
  -b 24 \
  -a naive \
  -d 0 \
  -N cctr \
  -l ntlbr \
  -s server_config_local.json \
  -i 0
```

Inspect timing:

```bash
cd /home/ccds/work/splitnn/infra
rg -n "edgeSum|Node setup time|Bbns setup time|Link setup time|Network operation time|Error:" runtime/setup_log.txt
```

Cleanup:

```bash
cd /home/ccds/work/splitnn/infra
sudo ./bin/topo_setup_test \
  -o clean \
  -t runtime/topo/grid_30_30.txt \
  -b 24 \
  -a naive \
  -d 0 \
  -N cctr \
  -l ntlbr \
  -s server_config_local.json \
  -i 0
```

## Multi-VM Driver Use

For `driver/server_config.json`, set the VM addresses and guest NIC name:

- VM1: `192.168.249.11`
- VM2: `192.168.249.12`
- `user`: `ccds`
- `password`: `splitnn`
- `phyIntf`: `ens3`

If both VMs run on the same host and you do not want to model multiple physical machines, set:

- `phyicalMachineId: 0`

for both entries.

## Current Known State

This setup has already verified:

- `cloud-hypervisor` boots Debian guests correctly
- KVM acceleration is in use
- guest networking works
- password SSH works
- `sudo` works
- `splitnn` torus topology generation for `30x30` is available

The remaining operational work is only guest package installation plus the final `topo_setup_test` run.
