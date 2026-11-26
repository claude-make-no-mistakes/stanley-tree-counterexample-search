"""Search two-edge expansions whose three deletion components are copies of one tree."""

import argparse
from functools import cache
from itertools import combinations_with_replacement, product
import json

import networkx as nx


def scan(tree):
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
    fingerprints = {}
    arrangements = 0
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
            fingerprint = mixed, min(contraction, contraction[::-1])
            # Exactly the two joining edges split off one whole copy, so their unordered
            # rooted attachments and the central path suffice to encode the unrooted tree.
            source = min((path_bags, left, right), (reverse_bags, right, left))
            mark = a, b, left, right
            old_source, old_mark = fingerprints.setdefault(fingerprint, (source, mark))
            arrangements += 1
            if old_source != source:
                return arrangements, len(fingerprints), (old_mark, mark)
    return arrangements, len(fingerprints), None


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
    parser.add_argument("--max-order", type=int, default=11)
    args = parser.parse_args()
    if args.max_order < 2:
        parser.error("Expected a maximum component order of at least two")
    for order in range(2, args.max_order + 1):
        result = check(order)
        print(json.dumps(result), flush=True)
        if result["candidate"] is not None:
            break
