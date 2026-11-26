"""Enumerate identical-fringe completions of a fixed rooted branch."""

import argparse
from collections import Counter
from functools import cache
import json

import networkx as nx

from balanced_splits import component_trees, validate_candidate
from near_collisions import adjacency
from search import expand, rooted_code


def tree_completions(tree, prune_automorphisms=False):
    intern = {}

    def intern_bag(branches):
        key = tuple(sorted(branches))
        return intern.setdefault(key, len(intern))

    @cache
    def branch(vertex, parent):
        return intern_bag(branch(v, vertex) for v in tree[vertex] if v != parent)

    seen_roots = set()
    for root in range(len(tree)):
        original = branch(root, -1)
        if original in seen_roots:
            continue
        seen_roots.add(original)
        parent = {root: -1}
        order = [root]
        for step in order:
            for vertex in tree[step]:
                if vertex != parent[step]:
                    parent[vertex] = step
                    order.append(vertex)
        orbit = {root: ()}
        seen_ends = set()
        for endpoint in order[1:]:
            fringe = branch(endpoint, parent[endpoint])
            if prune_automorphisms:
                # Equal sequences of branch types describe the same endpoint orbit.
                orbit[endpoint] = (*orbit[parent[endpoint]], fringe)
                if orbit[endpoint] in seen_ends:
                    continue
                seen_ends.add(orbit[endpoint])
            moved_tail = fringe
            child = endpoint
            vertex = parent[child]
            path = []
            while vertex != -1:
                path.append((vertex, child))
                child, vertex = vertex, parent[vertex]
            for vertex, child in reversed(path):
                off_path = (branch(v, vertex) for v in tree[vertex] if v not in (child, parent[vertex]))
                moved_tail = intern_bag((*off_path, moved_tail))
            if moved_tail != original:
                yield (original, moved_tail), root, endpoint, parent[endpoint]
    branch.cache_clear()


def complete(graph, root, endpoint, parent):
    fragment = graph.copy()
    fragment.remove_edge(endpoint, parent)
    vertices = sorted(nx.node_connected_component(fragment, endpoint))
    labels = {vertex: i for i, vertex in enumerate(vertices, len(graph))}
    result = graph.copy()
    result.add_edges_from((labels[u], labels[v]) for u, v in fragment.subgraph(vertices).edges())
    result.add_edge(root, labels[endpoint])
    return result, (labels[endpoint], endpoint)


def scan(graphs, prune_automorphisms=False):
    seen = set()
    counts = Counter()
    for graph in graphs:
        tree = adjacency(graph)
        # Codes use local vertex labels, while this key removes label duplicates.
        code = rooted_code(tree, (1,) * len(tree))
        if code in seen:
            continue
        seen.add(code)
        counts["trees"] += 1
        signatures = {}
        for key, *mark in tree_completions(tree, prune_automorphisms):
            counts["completions"] += 1
            earlier = signatures.setdefault(key, [])
            if earlier:
                current, marked = complete(graph, *mark)
                for prior in earlier:
                    other, other_marked = complete(graph, *prior)
                    counts["equal_differences"] += 1
                    witness = validate_candidate(other_marked, marked, other, current)
                    if witness is not None:
                        return {**counts, "witness": witness}
            earlier.append(mark)
    return {**counts, "witness": None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-order", type=int, default=8)
    parser.add_argument("--max-order", type=int, default=16)
    parser.add_argument("--random-count", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20261208)
    parser.add_argument("--prune-automorphisms", action="store_true",
                        help="Keep just one endpoint per orbit under the fixed root")
    args = parser.parse_args()
    if not 2 <= args.min_order <= args.max_order or args.random_count < 0:
        parser.error("Expected a valid order range and nonnegative random count")
    for n in range(args.min_order, args.max_order + 1):
        graphs = nx.nonisomorphic_trees(n) if n <= 12 else component_trees(n, args.random_count, args.seed)
        result = scan(graphs, args.prune_automorphisms)
        print(json.dumps({"branch_order": n, **result}), flush=True)
        if result["witness"]:
            break
