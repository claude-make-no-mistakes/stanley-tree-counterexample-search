"""Search local subtree changes around the near collisions of arXiv:2002.08186."""

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json

import networkx as nx

from search import forest_signature, rooted_code


def join(left, right, identify=False):
    g, root_a = left
    h, root_b = right
    joined = nx.disjoint_union(g, h)
    root_a = list(g).index(root_a)
    root_b = len(g) + list(h).index(root_b)
    if identify:
        nx.contracted_nodes(joined, root_a, root_b, self_loops=False, copy=False)
    else:
        joined.add_edge(root_a, root_b)
    return joined, root_a


def near_pair(k, l):
    path = nx.path_graph(3)
    levels = [((path, 1), (path, 0))]
    for _ in range(max(k, l)):
        a, b = levels[-1]
        levels.append((join(a, b), join(b, a)))
    a, b = levels[k]
    c, d = levels[l]
    return join(join(a, c, True), join(b, d, True))[0], join(join(a, d, True), join(b, c, True))[0]


def adjacency(graph):
    return tuple(tuple(graph[u]) for u in range(len(graph)))


def degree_and_cuts(tree):
    n = len(tree)
    def traverse(vertex, parent):
        visited = 1 << vertex
        for child in tree[vertex]:
            if child != parent:
                child_mask = traverse(child, vertex)
                masks.append(child_mask)
                visited |= child_mask
        return visited

    masks = []
    traverse(0, -1)
    sizes = {mask: mask.bit_count() for mask in masks}
    one = Counter(min(s, n-s) for s in sizes.values())
    two = Counter()
    for a, b in combinations(masks, 2):
        s, t = sizes[a], sizes[b]
        if a & b:
            parts = (min(s,t), abs(s-t), n-max(s,t))
        else:
            parts = (s, t, n-s-t)
        two[tuple(sorted(parts))] += 1
    return tuple(sorted(len(neighbors) for neighbors in tree)), tuple(sorted(one.items())), tuple(sorted(two.items()))


def variants(source, subtree=False):
    n = len(source)
    source = nx.convert_node_labels_to_integers(source)
    ones = (1,) * n
    base = adjacency(source)
    seen = {rooted_code(base, ones)}
    yield base
    for u, v in list(source.edges()):
        for detached, old in ((u, v), (v, u)):
            if not subtree and source.degree(detached) != 1:
                continue
            source.remove_edge(detached, old)
            for vertex in sorted(nx.node_connected_component(source, old) - {old}):
                source.add_edge(detached, vertex)
                trial = adjacency(source)
                code = rooted_code(trial, ones)
                if code not in seen:
                    seen.add(code)
                    yield trial
                source.remove_edge(detached, vertex)
            source.add_edge(detached, old)


def equal_size_exchanges(source):
    """Swap disjoint pendant trees with equal order at two distinct attachment vertices."""
    graph = nx.convert_node_labels_to_integers(source)
    base = adjacency(graph)
    weights = (1,) * len(graph)
    seen = {rooted_code(base, weights)}
    yield base

    by_size = defaultdict(list)
    for u, v in graph.edges():
        for root, parent in ((u, v), (v, u)):
            component = set()
            pending = [(root, parent)]
            while pending:
                vertex, previous = pending.pop()
                component.add(vertex)
                pending.extend((child, vertex) for child in graph[vertex] if child != previous)
            by_size[len(component)].append((root, parent, component))

    for branches in by_size.values():
        for (a, pa, left), (b, pb, right) in combinations(branches, 2):
            if pa == pb or not left.isdisjoint(right) or pa in right or pb in left:
                continue
            graph.remove_edges_from(((a, pa), (b, pb)))
            graph.add_edges_from(((a, pb), (b, pa)))
            trial = adjacency(graph)
            graph.remove_edges_from(((a, pb), (b, pa)))
            graph.add_edges_from(((a, pa), (b, pb)))
            code = rooted_code(trial, weights)
            if code not in seen:
                seen.add(code)
                yield trial


def signature(tree, cap=None):
    labels = {v: i for i, v in enumerate(u for u, neighbors in enumerate(tree) if len(neighbors) > 1)}
    core = tuple(tuple(labels[v] for v in tree[u] if v in labels) for u in labels)
    weights = tuple(1 + sum(len(tree[v]) == 1 for v in tree[u]) for u in labels)
    return forest_signature(core, weights, max_components=cap)


def scan(k, l, subtree=False, exchange=False):
    y, z = near_pair(k, l)
    n = len(y)
    # Theorem 12's first differing component count is k+l+4.
    left_base, right_base = (adjacency(nx.convert_node_labels_to_integers(tree)) for tree in (y, z))
    cap = k + l + 4
    ones = (1,) * n
    left, right = (signature(tree, cap) for tree in (left_base, right_base))
    assert min(len(p) for p in left.keys() | right.keys() if left[p] != right[p]) == cap
    groups = defaultdict(list)
    left_variants = equal_size_exchanges(y) if exchange else variants(y, subtree=subtree)
    right_variants = equal_size_exchanges(z) if exchange else variants(z, subtree=subtree)
    for tree in left_variants:
        groups[degree_and_cuts(tree)].append((rooted_code(tree, ones), tree))

    full_checks = 0
    truncated_checks = 0
    right_count = 0
    for tree in right_variants:
        right_count += 1
        code = rooted_code(tree, ones)
        candidates = [other for left_code, other in groups.get(degree_and_cuts(tree), ()) if left_code != code]
        if not candidates:
            continue
        target = signature(tree, cap)
        truncated_checks += len(candidates)
        survivors = [other for other in candidates if signature(other, cap) == target]
        if survivors:
            full = signature(tree)
            for other in survivors:
                full_checks += 1
                if full == signature(other):
                    return {"n": n, "witness_adjacencies": [tree, other]}
    move = "equal-size-exchange" if exchange else ("subtree" if subtree else "pendant")
    return {"n": n, "k": k, "l": l, "left_variants": sum(map(len, groups.values())),
            "right_variants": right_count, "moves": move,
            "truncated_comparisons": truncated_checks, "full_comparisons": full_checks, "witness_adjacencies": None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("k", type=int, choices=range(4))
    parser.add_argument("l", type=int, choices=range(4))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--subtree", action="store_true")
    mode.add_argument("--exchange", action="store_true")
    args = parser.parse_args()
    print(json.dumps(scan(args.k, args.l, subtree=args.subtree, exchange=args.exchange)))
