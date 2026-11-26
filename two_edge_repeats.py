"""Search two-edge expansions whose three deletion components are copies of one tree."""

import argparse
from collections import Counter
from functools import cache
from itertools import combinations_with_replacement, product
import json

import networkx as nx

from near_collisions import adjacency, signature


def arrangement_keys(tree):
    intern = {}

    @cache
    def side(vertex, parent):
        bag = tuple(sorted(side(child, vertex) for child in tree[vertex] if child != parent))
        return intern.setdefault(bag, len(intern))

    bags = {vertex: tuple(sorted(side(child, vertex) for child in tree[vertex])) for vertex in tree}
    roots = {}
    for vertex, bag in bags.items():
        roots.setdefault(bag, vertex)
    root_types = {vertex: roots[bag] for vertex, bag in bags.items()}
    representatives = tuple(roots.values())
    seen_paths = set()
    for a, b in combinations_with_replacement(tree, 2):
        path = nx.shortest_path(tree, a, b)
        path_bags = []
        for index, vertex in enumerate(path):
            off_path = set(tree[vertex]) - set(path[max(0, index - 1):index + 2])
            path_bags.append(tuple(sorted(side(child, vertex) for child in off_path)))
        path_bags = tuple(path_bags)
        reverse_bags = path_bags[::-1]
        path_type = min(path_bags, reverse_bags)
        if path_type in seen_paths:
            continue
        seen_paths.add(path_type)
        for left, right in product(representatives, repeat=2):
            # Each mixed term is determined by the two rooted types at the contracted edge.
            pair_left = tuple(sorted((root_types[a], left)))
            pair_right = tuple(sorted((root_types[b], right)))
            mixed = tuple(sorted((pair_left, pair_right)))
            if a == b:
                contraction = (tuple(sorted(path_bags[0] + bags[left] + bags[right])),)
            else:
                first = tuple(sorted(path_bags[0] + bags[left]))
                last = tuple(sorted(path_bags[-1] + bags[right]))
                contraction = (first, *path_bags[1:-1], last)
            # Exactly the two joining edges split off one whole copy, so their unordered
            # rooted attachments and the central path suffice to encode the unrooted tree.
            source = min((path_bags, left, right), (reverse_bags, right, left))
            yield source, mixed, min(contraction, contraction[::-1]), (a, b, left, right)


def scan(tree):
    fingerprints = {}
    arrangements = 0
    for source, mixed, contraction, mark in arrangement_keys(tree):
        fingerprint = mixed, contraction
        old_source, old_mark = fingerprints.setdefault(fingerprint, (source, mark))
        arrangements += 1
        if old_source != source:
            return arrangements, len(fingerprints), (old_mark, mark)
    return arrangements, len(fingerprints), None


def joined_tree(tree, mark):
    labels = {vertex: i for i, vertex in enumerate(tree)}
    a, b, left, right = (labels[v] for v in mark)
    order = len(tree)
    result = nx.disjoint_union_all((tree, tree, tree))
    result.add_edges_from(((a, order + left), (b, 2 * order + right)))
    return result


def scan_cancellations(tree):
    """Search different mixed expansions with the same deletion and double contraction."""
    counts = Counter(arrangements=0, structural_pairs=0, same_degrees=0,
                     same_two_parts=0, same_three_parts=0, same_five_parts=0)

    @cache
    def joined(mark):
        return joined_tree(tree, mark)

    @cache
    def invariant(mark, parts):
        graph = joined(mark)
        if parts == 1:
            return tuple(sorted(degree for _, degree in graph.degree()))
        return signature(adjacency(graph), parts)

    buckets = {}
    for source, _, contraction, mark in arrangement_keys(tree):
        counts["arrangements"] += 1
        bucket = buckets.setdefault(contraction, {})
        if source in bucket:
            continue
        for prior in bucket.values():
            counts["structural_pairs"] += 1
            for parts, label in ((1, "same_degrees"), (2, "same_two_parts"),
                                 (3, "same_three_parts"), (5, "same_five_parts")):
                if invariant(mark, parts) != invariant(prior, parts):
                    break
                counts[label] += 1
            else:
                if invariant(mark, None) == invariant(prior, None):
                    first, second = joined(prior), joined(mark)
                    assert not nx.is_isomorphic(first, second)
                    return counts, [nx.to_graph6_bytes(graph, header=False).decode().strip()
                                    for graph in (first, second)]
        bucket[source] = mark
    return counts, None


def cancellations(order):
    totals = Counter()
    for index, tree in enumerate(nx.nonisomorphic_trees(order), 1):
        counts, candidate = scan_cancellations(tree)
        totals.update(counts)
        if candidate is not None:
            break
    return {"component_order": order, "trees": index, **totals, "candidate": candidate}


def check(order):
    arrangements = 0
    expansions = 0
    for index, tree in enumerate(nx.nonisomorphic_trees(order), 1):
        count, keys, witness = scan(tree)
        arrangements += count
        expansions += keys
        if witness is not None:
            labels = {vertex: label for label, vertex in enumerate(tree)}
            return {"component_order": order, "trees": index, "arrangements": arrangements, "expansions": expansions,
                    "candidate": {"component": nx.to_graph6_bytes(tree, header=False).decode().strip(),
                                  "attachments": [[labels[v] for v in mark] for mark in witness]}}
    return {"component_order": order, "trees": index, "arrangements": arrangements,
            "expansions": expansions, "candidate": None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-order", type=int, default=2)
    parser.add_argument("--max-order", type=int, default=11)
    parser.add_argument("--search-mixed-cancellation", action="store_true")
    args = parser.parse_args()
    if not 2 <= args.min_order <= args.max_order:
        parser.error("Expected a component-order range starting at least at two")
    for order in range(args.min_order, args.max_order + 1):
        result = cancellations(order) if args.search_mixed_cancellation else check(order)
        print(json.dumps(result), flush=True)
        if result["candidate"] is not None:
            break
