import metis
import shutil
import argparse
import time
import numpy as np
from .fmt_util import *
from scipy.sparse import lil_matrix


def create_metis_adjacency_list(nodes, adjacency_list):
    """Converts the adjacency list to METIS format where indices must be contiguous."""
    node_to_index = {node: idx for idx, node in enumerate(nodes)}
    index_to_node = {idx: node for node, idx in node_to_index.items()}
    metis_adjacency_list = []

    start_time = time.time()
    neighbor_count = 0
    for node in nodes:
        # Convert the node's neighbors from IDs to indices
        # neighbors_with_weight = [(node_to_index[neighbor], 1) for neighbor in adjacency_list[node]]  # Add default weight 1
        # metis_adjacency_list.append(neighbors_with_weight)
        neighbors = [node_to_index[neighbor] for neighbor in adjacency_list[node]]  # Add default weight 1
        metis_adjacency_list.append(neighbors)
        neighbor_count += 1
        # if neighbor_count % 1000 == 0:
        #     print(f"Neighbor count: {neighbor_count}")
    # print("Adjacency list conversion completed. Time-cost: ", time.time() - start_time)

    return metis_adjacency_list, node_to_index, index_to_node


def evaluate_partition_balance(nodes, adjacency_list, parts, num_partitions):
    """Score a partition using the same edgeSum notion used by generated sub-topologies."""
    node_to_index = {node: idx for idx, node in enumerate(nodes)}
    internal_edges = [0] * num_partitions
    dangling_edges = [0] * num_partitions
    for u in nodes:
        for v in adjacency_list[u]:
            if u >= v:
                continue
            u_part = parts[node_to_index[u]]
            v_part = parts[node_to_index[v]]
            if u_part == v_part:
                internal_edges[u_part] += 1
            else:
                dangling_edges[u_part] += 1
                dangling_edges[v_part] += 1
    edge_sum = [
        internal_edges[i] + dangling_edges[i] for i in range(num_partitions)
    ]
    avg_edge_sum = sum(edge_sum) / num_partitions
    imbalance_pct = 0.0
    if avg_edge_sum > 0:
        imbalance_pct = (max(edge_sum) - min(edge_sum)) / avg_edge_sum * 100
    return {
        "edge_sum": edge_sum,
        "imbalance_pct": imbalance_pct,
        "max_edge_sum": max(edge_sum),
    }


def get_fat_tree_metis_candidates():
    """Candidate METIS option sets tuned for 4-way fat-tree partitioning."""
    return [
        {
            "name": "default_recursive",
            "opts": {
                "recursive": True,
                "niter": 20,
            },
        },
        {
            "name": "fat_tree_recursive_balance",
            "opts": {
                "recursive": True,
                "ctype": "rm",
                "iptype": "grow",
                "rtype": "fm",
                "ncuts": 8,
                "niter": 40,
                "ufactor": 30,
                "seed": 1,
            },
        },
    ]


def run_metis_partition(metis_adjacency_list, num_partitions, random=False, **opts):
    while True:
        try:
            local_opts = dict(opts)
            if random and "seed" not in local_opts:
                local_opts["seed"] = int(np.random.randint(0, 100))
            return metis.part_graph(
                metis_adjacency_list, nparts=num_partitions, **local_opts
            )
        except metis.METIS_InputError as e:
            print(f"METIS Input Error: {e}")
            print("Retrying with a different seed...")
            continue


def partition_graph_across_vm(nodes, adjacency_list, num_partitions, acc_server_num, random=False, topo_hint=None):
    """Partitions the graph into num_partitions using METIS and writes each subgraph."""
    node2serverid = {}
    if num_partitions == 1:
        server_id = acc_server_num
        for node in nodes:
            node2serverid[node] = server_id
        return node2serverid

    # Convert adjacency list to METIS format with correct indices
    start_time = time.time()
    metis_adjacency_list, node_to_index, index_to_node = create_metis_adjacency_list(nodes, adjacency_list)

    # Partition the graph into num_partitions parts using METIS.
    if topo_hint == "clos" and num_partitions == 4:
        best_result = None
        for candidate in get_fat_tree_metis_candidates():
            objval, parts = run_metis_partition(
                metis_adjacency_list, num_partitions, random=random, **candidate["opts"]
            )
            balance = evaluate_partition_balance(
                nodes, adjacency_list, parts, num_partitions
            )
            result = {
                "name": candidate["name"],
                "objval": objval,
                "parts": parts,
                **balance,
            }
            if best_result is None or (
                result["imbalance_pct"],
                result["max_edge_sum"],
                result["objval"],
            ) < (
                best_result["imbalance_pct"],
                best_result["max_edge_sum"],
                best_result["objval"],
            ):
                best_result = result
        print(
            "Selected fat-tree METIS options:",
            best_result["name"],
            f"edgeSum={best_result['edge_sum']}",
            f"imbalance={best_result['imbalance_pct']:.2f}%",
        )
        parts = best_result["parts"]
    else:
        _, parts = run_metis_partition(
            metis_adjacency_list, num_partitions, random=random, niter=20, recursive=True
        )
    # print("Partitioning completed. Time-cost: ", time.time() - start_time)

    for idx, part in enumerate(parts):
        node = index_to_node[idx]  # Convert index back to original node ID
        server_id = part + acc_server_num
        node2serverid[node] = server_id

    return node2serverid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A script to generate positions and events')
    parser.add_argument('-f', '--input-file', type=str, required=True, help='Input file name')
    parser.add_argument('-n', '--num-partition', type=int, required=True, help='# of partitions')
    args = parser.parse_args()

    input_filepath = args.input_file
    num_partitions = args.num_partition

    partition_graph_across_vm(input_filepath, num_partitions)
