"""Check the two-edge and connected three-edge reconstruction theorems directly."""

import argparse
from itertools import combinations
import json

import networkx as nx


def rooted(tree, root, parent=None):
    return tree.nodes[root].get("weight", 1), tuple(sorted(
        (tree[root][child].get("marked", False), rooted(tree, child, root))
        for child in tree[root] if child != parent
    ))


def canonical(tree):
    return min(rooted(tree, v) for v in nx.center(tree))


def card(tree, specified, contracted):
    """Build the weighted forest directly from the connected contraction classes."""
    identifications = nx.Graph()
    identifications.add_nodes_from(tree)
    identifications.add_edges_from(contracted)
    result = nx.Graph()
    representative = {}
    for part in nx.connected_components(identifications):
        root = min(part)
        result.add_node(root, weight=len(part))
        representative.update((vertex, root) for vertex in part)
    removed = frozenset(map(frozenset, specified))
    result.add_edges_from((representative[u], representative[v]) for u, v in tree.edges()
                          if frozenset((u, v)) not in removed)
    return result


def two_edge_key(tree, specified):
    double = canonical(card(tree, specified, specified))
    mixed = []
    for edge in specified:
        forest = card(tree, specified, (edge,))
        mark = next(v for v in forest if forest.nodes[v]["weight"] == 2)
        mixed.append(rooted(forest, mark))
    return double, tuple(sorted(mixed))


def three_edge_key(tree, specified):
    layers = []
    for count in range(1, 4):
        codes = []
        for contracted in combinations(specified, count):
            forest = card(tree, specified, contracted)
            codes.append(tuple(sorted(canonical(forest.subgraph(part))
                                      for part in nx.connected_components(forest))))
        layers.append(tuple(sorted(codes)))
    return tuple(layers)


def check(order):
    two = {}
    three = {}
    pairs = triples = 0
    for index, tree in enumerate(nx.nonisomorphic_trees(order), 1):
        for count, table, key in ((2, two, two_edge_key), (3, three, three_edge_key)):
            for edges in combinations(tree.edges(), count):
                if count == 3 and len({v for edge in edges for v in edge}) != 4:
                    continue
                marked = tree.copy()
                nx.set_edge_attributes(marked, {edge: True for edge in edges}, "marked")
                source = canonical(marked)
                data = key(tree, edges)
                assert table.setdefault(data, source) == source
                if count == 2:
                    pairs += 1
                else:
                    triples += 1
    return {"order": order, "trees": index, "pairs": pairs, "connected_triples": triples,
            "distinct_pair_data": len(two), "distinct_triple_data": len(three)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, default=11)
    args = parser.parse_args()
    if args.max_order < 3:
        parser.error("Expected an order of at least three")
    for order in range(3, args.max_order + 1):
        print(json.dumps(check(order)), flush=True)
