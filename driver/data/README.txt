AS Topology Data (trimmed set)

This repository keeps only small AS topology subsets for single-machine tests:

- `jp_kr_topo.txt`   (~1.5K nodes)
- `cn_sea_topo.txt`  (~5.1K nodes)

The selectable presets are defined in `driver/data/as_topo_config.json`:

- `small`  -> `jp_kr_topo.txt`
- `medium` -> `cn_sea_topo.txt`

Provenance

These topologies are derived from CAIDA AS-relationship data processing
workflows used by this project. For source dataset terms and citation guidance,
refer to CAIDA's acceptable use and dataset pages:

- https://www.caida.org/about/legal/aua/public_aua/
- https://www.caida.org/catalog/datasets/as-relationships/

Note

Large raw AS datasets are intentionally excluded from this repository to keep
repository size manageable.
