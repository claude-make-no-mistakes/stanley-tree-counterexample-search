"""Check deletion and contraction pairs on all unlabeled trees through a given order."""

import argparse
import json

import networkx as nx


def encode(tree, root, parent=None):
    return tuple(sorted(encode(tree, child, root) for child in tree[root] if child != parent))


def unrooted_code(tree):
    return min(encode(tree, center) for center in nx.center(tree))


def check(order):
    pairs = {}
    unmarked_pairs = {}
    unmarked_example = None
    unmarked_tree_changes = 0
    marked_edges = 0
    for index, tree in enumerate(nx.nonisomorphic_trees(order)):
        graph6 = nx.to_graph6_bytes(tree, header=False).decode("ascii").strip()
        labels = {vertex: label for label, vertex in enumerate(tree)}
        for left, right in tree.edges():
            # These rooted halves uniquely encode the source tree with its edge marked.
            source = tuple(sorted((encode(tree, left, right), encode(tree, right, left))))
            deleted = tree.copy()
            deleted.remove_edge(left, right)
            forest = tuple(sorted(unrooted_code(deleted.subgraph(component))
                                  for component in nx.connected_components(deleted)))
            contracted = nx.contracted_nodes(tree, left, right, self_loops=False)
            key = forest, encode(contracted, left)
            assert pairs.setdefault(key, source) == source
            marked_edges += 1

            key = forest, unrooted_code(contracted)
            edge = [labels[left], labels[right]]
            previous, first_graph, first_edge = unmarked_pairs.setdefault(key, (index, graph6, edge))
            if previous != index:
                unmarked_tree_changes += 1
                if unmarked_example is None:
                    unmarked_example = [[first_graph, first_edge], [graph6, edge]]

    return {"order": order, "trees": index + 1, "marked_edges": marked_edges,
            "marked_keys": len(pairs), "unmarked_tree_changes": unmarked_tree_changes,
            "unmarked_example": unmarked_example}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, default=14)
    args = parser.parse_args()
    if args.max_order < 2:
        parser.error("Expected an order of at least two")
    for order in range(2, args.max_order + 1):
        print(json.dumps(check(order)), flush=True)
