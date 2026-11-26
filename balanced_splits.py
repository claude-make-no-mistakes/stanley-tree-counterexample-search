"""Seek exact Stanley collisions by matching deletion and rooted contraction at a balanced edge."""

import argparse
from collections import Counter
from functools import cache
from itertools import combinations
import json
from random import Random

import networkx as nx

from near_collisions import adjacency, join, signature
from search import distribution, expand, rooted_code


def component_trees(order, random_count, seed):
    for core_size in range(2, 6):
        for core in nx.nonisomorphic_trees(core_size):
            neighbors = adjacency(core)
            lower = tuple(2 if len(row) == 1 else 1 for row in neighbors)
            for weights in distribution(order, lower):
                yield expand(neighbors, weights)
    rng = Random(seed)
    for _ in range(random_count):
        yield nx.from_prufer_sequence([rng.randrange(order) for _ in range(order - 2)])


def branch_bags(tree, intern):
    @cache
    def branch(vertex, parent):
        code = tuple(sorted(branch(neighbor, vertex) for neighbor in tree[vertex] if neighbor != parent))
        return intern.setdefault(code, len(intern))

    positions = {}
    for vertex, neighbors in enumerate(tree):
        bag = tuple(sorted(branch(neighbor, vertex) for neighbor in neighbors))
        positions.setdefault(bag, vertex)
    branch.cache_clear()
    return positions


def validate_candidate(left, right, source, target):
    # The split edge in the joined tree is the unique edge with equally sized components.
    # In the first join, the contracted root sees exactly the same rooted branches as in the second.
    x, y = left
    u, v = right
    before = join((source, x), (target, v))[0]
    after = join((source, y), (target, u))[0]
    glued_before, root_before = join((source, x), (target, v), identify=True)
    glued_after, root_after = join((source, y), (target, u), identify=True)
    nx.set_node_attributes(glued_before, {root_before: True}, "is_root")
    nx.set_node_attributes(glued_after, {root_after: True}, "is_root")
    assert nx.is_isomorphic(glued_before, glued_after,
                            node_match=lambda a, b: a.get("is_root", False) == b.get("is_root", False))
    assert not nx.is_isomorphic(before, after)
    arrays = [adjacency(graph) for graph in (before, after)]
    assert signature(arrays[0]) == signature(arrays[1])
    return {"graph6": [nx.to_graph6_bytes(graph, header=False).decode().strip() for graph in (before, after)],
            "component_graph6": [nx.to_graph6_bytes(graph, header=False).decode().strip() for graph in (source, target)],
            "component_root_pairs": [left, right], "component_order": len(source)}


def scan(order, random_count, seed):
    known = set()
    inputs = []
    intern = {}
    seen_differences = {}
    trials = 0
    weights = (1,) * order
    for graph in component_trees(order, random_count, seed):
        tree = adjacency(graph)
        key = rooted_code(tree, weights)
        if key in known:
            continue
        known.add(key)
        positions = branch_bags(tree, intern)
        component = len(inputs)
        inputs.append(tree)
        for a, b in combinations(positions, 2):
            delta_a = tuple(sorted((Counter(a) - Counter(b)).elements()))
            delta_b = tuple(sorted((Counter(b) - Counter(a)).elements()))
            if delta_a < delta_b:
                pair = delta_a, delta_b
                roots = positions[a], positions[b]
            else:
                pair = delta_b, delta_a
                roots = positions[b], positions[a]
            trials += 1
            if pair in seen_differences:
                prev_component, prev_roots = seen_differences[pair]
                # Each unordered root-orbit pair is visited once per component.
                assert (prev_component, prev_roots) != (component, roots)
                previous = expand(inputs[prev_component], weights)
                return {"trials": trials, "witness": validate_candidate(prev_roots, roots, previous, graph)}
            seen_differences[pair] = component, roots
    return {"component_order": order, "target_order": 2 * order, "components": len(inputs),
            "root_pair_trials": trials, "distinct_branch_codes": len(intern), "witness": None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-order", type=int, default=15)
    parser.add_argument("--max-order", type=int, default=19)
    parser.add_argument("--random-count", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20261126)
    args = parser.parse_args()
    if not 8 <= args.min_order <= args.max_order or args.random_count < 0:
        parser.error("Expected component orders at least eight and a nonnegative random count")
    # A root pair exchange would recover known-infeasible small-order Stanley pairs here.
    assert scan(8, 50, seed=0)["witness"] is None
    for n in range(args.min_order, args.max_order + 1):
        result = scan(n, args.random_count, args.seed)
        print(json.dumps(result), flush=True)
        if result["witness"]:
            break
