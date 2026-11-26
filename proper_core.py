"""Use parts of size at least two to filter possible collisions of proper trees."""

import argparse
from collections import Counter
from functools import lru_cache
from itertools import product
import json

import networkx as nx

from search import expand, forest_signature, rooted_code


def cut_shapes(adjacency):
    n = len(adjacency)
    edges = [(u, v) for u, neighbors in enumerate(adjacency) for v in neighbors if u < v]
    shapes = [[] for _ in range(n)]
    for cuts in range(1 << len(edges)):
        parent = list(range(n))

        def root(u):
            while u != parent[u]:
                u = parent[u]
            return u

        for i, (u, v) in enumerate(edges):
            if not cuts >> i & 1:
                parent[root(u)] = root(v)
        groups = {}
        for u in range(n):
            r = root(u)
            groups[r] = groups.get(r, 0) | (1 << u)
        shapes[cuts.bit_count()].append(tuple(sorted(groups.values())))
    return shapes


@lru_cache(maxsize=6000)
def sum_on_masks(weights):
    totals = [0] * (1 << len(weights))
    for mask in range(1, len(totals)):
        low = mask & -mask
        totals[mask] = totals[mask ^ low] + weights[low.bit_length() - 1]
    return totals


def cut_signature(totals, shapes):
    counts = Counter(tuple(sorted(totals[block] for block in shape)) for shape in shapes)
    return tuple(sorted(counts.items()))


def validate():
    # Swapping the two entries of the inner ribbon composition gives this weighted path pair.
    pairs = [(2, 3, 2, 5, 3), (3, 2, 3, 5, 2)]
    path = nx.path_graph(5)
    adjacency = tuple(tuple(path[v]) for v in range(5))
    shapes = cut_shapes(adjacency)
    signatures = [tuple(cut_signature(sum_on_masks(w), level) for level in shapes) for w in pairs]
    assert signatures[0] == signatures[1]
    assert rooted_code(adjacency, pairs[0]) != rooted_code(adjacency, pairs[1])
    assert forest_signature(adjacency, pairs[0]) != forest_signature(adjacency, pairs[1])


def weight_orders(weights):
    counts = Counter(weights)

    def visit(remaining):
        if not remaining:
            yield ()
        for w in counts:
            if counts[w]:
                counts[w] -= 1
                for tail in visit(remaining - 1):
                    yield (w, *tail)
                counts[w] += 1

    yield from visit(len(weights))


def scan(order, min_total, max_weight, multiset=None):
    assignments = (weight_orders(multiset) if multiset is not None
                   else product(range(2, max_weight + 1), repeat=order))
    candidates = [weights for weights in assignments if sum(weights) >= min_total]
    buckets = {}
    counts = Counter()
    for core in nx.nonisomorphic_trees(order):
        adjacency = tuple(tuple(core[v]) for v in range(len(core)))
        degrees = tuple(map(len, adjacency))
        shapes = cut_shapes(adjacency)
        unique = set()
        for weights in candidates:
            code = rooted_code(adjacency, weights)
            if code in unique:
                continue
            unique.add(code)
            counts["proper_trees"] += 1
            totals = sum_on_masks(weights)
            key = (totals[-1], tuple(sorted(deg + w - 1 for deg, w in zip(degrees, weights, strict=True))),
                   cut_signature(totals, shapes[1]), cut_signature(totals, shapes[2]))
            bag = buckets.setdefault(key, [])
            if not bag:
                bag.append([adjacency, weights, shapes, None])
                continue
            counts["three_filters_survived"] += 1
            signature = tuple(cut_signature(totals, level) for level in shapes[3:])
            for record in bag:
                alt_adjacency, alt_weights, alt_shapes, other = record
                if other is None:
                    alt_totals = sum_on_masks(alt_weights)
                    other = tuple(cut_signature(alt_totals, level) for level in alt_shapes[3:])
                    record[-1] = other
                if signature != other:
                    continue
                counts["weighted_core_collisions"] += 1
                low = 7
                if forest_signature(adjacency, weights, low) != forest_signature(alt_adjacency, alt_weights, low):
                    continue
                counts["full_comparisons"] += 1
                if forest_signature(adjacency, weights) != forest_signature(alt_adjacency, alt_weights):
                    continue
                a, b = expand(adjacency, weights), expand(alt_adjacency, alt_weights)
                assert not nx.is_isomorphic(a, b)
                return {"witness": [nx.to_graph6_bytes(g, header=False).decode().strip() for g in (a, b)],
                        "core_order": order, "counts": dict(counts)}
            bag.append([adjacency, weights, shapes, signature])
    return {"core_order": order, "minimum_full_order": min_total, "max_weight": max_weight,
            "weight_multiset": multiset, "counts": dict(counts), "witness": None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core", type=int, required=True)
    parser.add_argument("--min-order", type=int, default=30)
    parser.add_argument("--max-weight", type=int, default=4)
    parser.add_argument("--weights", help="Use only permutations of these comma-separated weights")
    args = parser.parse_args()
    if not 3 <= args.core <= 11 or not 2 <= args.max_weight <= 5:
        parser.error("Expected 3–11 core vertices and weights at most 2–5")
    weights = tuple(map(int, args.weights.split(','))) if args.weights else None
    if weights is not None and (len(weights) != args.core or min(weights) < 2 or max(weights) > args.max_weight):
        parser.error("Supply one weight from 2 to --max-weight for each core vertex")
    validate()
    print(json.dumps(scan(args.core, args.min_order, args.max_weight, weights)), flush=True)
