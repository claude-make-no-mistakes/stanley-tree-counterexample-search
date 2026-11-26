"""Check whether pruning a published near collision preserves its restricted U-polynomial."""

import argparse
from collections import defaultdict
import json

import networkx as nx

from near_collisions import adjacency, degree_and_cuts, near_pair, signature
from search import expand, rooted_code


def prune_one(graphs):
    unique = {}
    for graph in graphs:
        for leaf, degree in graph.degree():
            if degree != 1:
                continue
            smaller = nx.convert_node_labels_to_integers(graph.subgraph(set(graph) - {leaf}))
            tree = adjacency(smaller)
            code = rooted_code(tree, (1,) * len(tree))
            unique.setdefault(code, smaller)
    return list(unique.values())


def compare(left, right, cap):
    def encode(graph):
        return nx.to_graph6_bytes(graph, header=False).decode().strip()

    buckets = defaultdict(list)
    n = len(left[0])
    for graph in left:
        tree = adjacency(graph)
        buckets[degree_and_cuts(tree)[1:]].append((rooted_code(tree, (1,) * n), tree))
    compared = 0
    for graph in right:
        tree = adjacency(graph)
        code = rooted_code(tree, (1,) * n)
        alternatives = [other for key, other in buckets.get(degree_and_cuts(tree)[1:], ()) if key != code]
        if not alternatives:
            continue
        target = signature(tree, cap)
        for other in alternatives:
            compared += 1
            if target != signature(other, cap):
                continue
            assert not nx.is_isomorphic(graph, expand(other, (1,) * n))
            return {"n": n, "restricted_u_index": cap - 1, "distinct_trees_compared": compared,
                    "restricted_collision_graph6": [encode(graph), encode(expand(other, (1,) * n))],
                    "full_collision": signature(tree) == signature(other)}
    return {"n": n, "restricted_u_index": cap - 1, "left_prunings": len(left), "right_prunings": len(right),
            "distinct_trees_compared": compared, "restricted_collision_graph6": None}


def scan(k, l, levels):
    y, z = near_pair(k, l)
    cap = k + l + 3
    left, right = ([nx.convert_node_labels_to_integers(graph)] for graph in (y, z))
    control = compare(left, right, cap)
    assert control["restricted_collision_graph6"] and not control["full_collision"]
    for _ in range(levels):
        left, right = (prune_one(graphs) for graphs in (left, right))
        result = compare(left, right, cap)
        print(json.dumps(result), flush=True)
        if result["restricted_collision_graph6"]:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--levels", type=int, choices=range(1, 5), default=4)
    args = parser.parse_args()
    scan(1, 2, args.levels)
