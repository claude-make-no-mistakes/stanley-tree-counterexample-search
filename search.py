"""Compare exact spanning-forest partitions of leaf-decorated tree cores."""

import argparse
from collections import Counter
from itertools import combinations
import json
from math import comb

import networkx as nx


def forest_signature(adjacency, weights, max_components=None):
    """For each component-size partition, count edge subsets giving that partition."""
    limit = sum(weights) - 1 if max_components is None else max_components - 1
    if limit < 0:
        raise ValueError("Expected at least one component")

    def rooted(vertex, parent):
        leaves = weights[vertex] - 1
        states = {(leaves + 1 - cut, (1,) * cut): comb(leaves, cut) for cut in range(min(leaves, limit) + 1)}
        for child in adjacency[vertex]:
            if child == parent:
                continue
            combined = Counter()
            for (open_child, closed_child), right in rooted(child, vertex).items():
                for (open_parent, closed_parent), left in states.items():
                    closed_count = len(closed_parent) + len(closed_child)
                    if closed_count > limit:
                        continue
                    closed = closed_parent + closed_child
                    joined = tuple(sorted(closed))
                    combined[open_parent + open_child, joined] += left * right
                    if closed_count < limit:
                        separate = tuple(sorted(closed + (open_child,)))
                        combined[open_parent, separate] += left * right
            states = combined
        return states

    output = Counter()
    for (root_size, sizes), coefficient in rooted(0, -1).items():
        output[tuple(sorted(sizes + (root_size,)))] += coefficient
    return output


def distribution(total, lower):
    remainder = total - sum(lower)
    if remainder < 0:
        return
    for cuts in combinations(range(1, remainder + len(lower)), len(lower) - 1):
        yield tuple(lb + b - a - 1 for lb, a, b in
                    zip(lower, (0,) + cuts, cuts + (remainder + len(lower),)))


def cut_components(core):
    edges = list(core.edges())
    parts = []
    for how_many in (1, 2):
        groups = []
        for removed in combinations(edges, how_many):
            copy = core.copy()
            copy.remove_edges_from(removed)
            groups.append(tuple(tuple(sorted(part)) for part in nx.connected_components(copy)))
        parts.append(groups)
    return parts


def fingerprint(weights, one_cut, two_cuts):
    n = sum(weights)
    # The total number of pendant edges is fixed for this bucket.
    first = []
    second = Counter()
    for side, other in one_cut:
        a = sum(weights[v] for v in side)
        b = n - a
        first.append(min(a, b))
        if a > len(side):
            second[tuple(sorted((1, a - 1, b)))] += a - len(side)
        if b > len(other):
            second[tuple(sorted((1, a, b - 1)))] += b - len(other)
    for components in two_cuts:
        sizes = tuple(sorted(sum(weights[v] for v in part) for part in components))
        second[sizes] += 1
    return tuple(sorted(first)), tuple(sorted(second.items()))


def rooted_code(adjacency, weights):
    def encode(vertex, parent):
        return weights[vertex], tuple(sorted(encode(v, vertex) for v in adjacency[vertex] if v != parent))

    # Tree isomorphisms map the one or two centers to one another.
    degrees = list(map(len, adjacency))
    layer = [u for u, degree in enumerate(degrees) if degree <= 1]
    remaining = len(degrees)
    while remaining > 2:
        remaining -= len(layer)
        following = []
        for leaf in layer:
            for neighbor in adjacency[leaf]:
                degrees[neighbor] -= 1
                if degrees[neighbor] == 1:
                    following.append(neighbor)
        layer = following
    return min(encode(v, -1) for v in layer)


def expand(adjacency, weights):
    graph = nx.Graph()
    graph.add_nodes_from(range(len(weights)))
    graph.add_edges_from((v, u) for v, neighbors in enumerate(adjacency) for u in neighbors)
    for vertex, size in enumerate(weights):
        for _ in range(size - 1):
            graph.add_edge(vertex, len(graph))
    return graph


def validate():
    # Independent edge-cut enumeration, using Stanley's power-sum expansion.
    for n in range(2, 8):
        for tree in nx.nonisomorphic_trees(n):
            adjacency = tuple(tuple(tree[v]) for v in range(n))
            expected = Counter()
            for cuts in range(n):
                for edges in combinations(tree.edges(), cuts):
                    remains = tree.copy()
                    remains.remove_edges_from(edges)
                    sizes = tuple(sorted(map(len, nx.connected_components(remains))))
                    expected[sizes] += 1
            assert forest_signature(adjacency, (1,) * n) == expected
            assert forest_signature(adjacency, (1,) * n, max_components=3) == {
                sizes: count for sizes, count in expected.items() if len(sizes) <= 3}
            # Also validate the grouped-leaf path on the same tree.
            internal = [v for v in tree if tree.degree(v) > 1]
            if internal:
                labels = {v: i for i, v in enumerate(internal)}
                core = tuple(tuple(labels[nbr] for nbr in tree[v] if nbr in labels) for v in internal)
                weights = tuple(1 + sum(tree.degree(nbr) == 1 for nbr in tree[v]) for v in internal)
                assert forest_signature(core, weights) == expected
                assert forest_signature(core, weights, max_components=3) == {
                    sizes: count for sizes, count in expected.items() if len(sizes) <= 3}


def scan(n, core_order):
    buckets = {}
    raw_count = 0
    full_checks = 0
    for core in nx.nonisomorphic_trees(core_order):
        adjacency = tuple(tuple(core[v]) for v in range(core_order))
        one, two = cut_components(core)
        lower = tuple(2 if core.degree(v) == 1 else 1 for v in range(core_order))
        for weights in distribution(n, lower):
            raw_count += 1
            key = tuple(sorted(len(neighbors) + w - 1 for neighbors, w in zip(adjacency, weights))), fingerprint(weights, one, two)
            bucket = buckets.setdefault(key, [])
            if not bucket:
                bucket.append([adjacency, weights, None, None])
                continue
            code = rooted_code(adjacency, weights)
            for record in bucket:
                if record[2] is None:
                    record[2] = rooted_code(record[0], record[1])
            if any(record[2] == code for record in bucket):
                continue
            signature = forest_signature(adjacency, weights)
            full_checks += 1
            for record in bucket:
                if record[3] is None:
                    record[3] = forest_signature(record[0], record[1])
                    full_checks += 1
                if signature == record[3]:
                    pair = [expand(adjacency, weights), expand(record[0], record[1])]
                    assert not nx.is_isomorphic(*pair)
                    return {"n": n, "core_order": core_order,
                            "witness": [nx.to_graph6_bytes(g, header=False).decode().strip() for g in pair]}
            bucket.append([adjacency, weights, code, signature])
    return {"n": n, "core_order": core_order, "decorations": raw_count,
            "fingerprints": len(buckets), "full_checks": full_checks, "witness": None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-n", type=int, default=30)
    parser.add_argument("--max-n", type=int, default=32)
    parser.add_argument("--max-core", type=int, default=6)
    args = parser.parse_args()
    validate()
    for n in range(args.min_n, args.max_n + 1):
        for core_order in range(2, args.max_core + 1):
            result = scan(n, core_order)
            print(json.dumps(result), flush=True)
            if result["witness"]:
                return


if __name__ == "__main__":
    main()
