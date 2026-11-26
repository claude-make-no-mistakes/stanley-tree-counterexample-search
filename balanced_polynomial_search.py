"""Search balanced joins with the same deletion forest using rooted U-polynomial evaluations."""

import argparse
from collections import Counter
from functools import cache
import json
from random import Random

import networkx as nx

from balanced_splits import branch_bags, component_trees
from near_collisions import adjacency, join, signature
from search import rooted_code


PRIMES = (1_000_000_007, 1_000_000_009)


def rooted_polynomials(tree, values, prime):
    """Return rooted U-polynomials after evaluating the closed-component variables."""
    @cache
    def polynomial(vertex, parent):
        result = [0, 1]
        for child in tree[vertex]:
            if child == parent:
                continue
            term = polynomial(child, vertex)
            closed = sum(values[i] * coeff for i, coeff in enumerate(term)) % prime
            combined = [0] * (len(result) + len(term) - 1)
            for i, a in enumerate(result):
                combined[i] += a * closed
                for j, b in enumerate(term[1:], 1):
                    combined[i + j] += a * b
            result = [entry % prime for entry in combined]
        return tuple(result)

    return tuple(polynomial(root, -1) for root in range(len(tree)))


def component_data(graph, evaluations):
    tree = adjacency(graph)
    n = len(tree)
    powers = tuple(pow(2 * n + 1, i) for i in range(2 * n + 1))
    degree_counts = sum(powers[n + len(neighbors)] for neighbors in tree)

    @cache
    def sizes(vertex, parent):
        descendants = tuple(size for child in tree[vertex] if child != parent
                            for size in sizes(child, vertex))
        return (1 + sum(sizes(child, vertex)[0] for child in tree[vertex] if child != parent), *descendants)

    polynomials = tuple(rooted_polynomials(tree, values, prime) for values, prime in evaluations)
    roots = []
    for root in branch_bags(tree, {}).values():
        degree = len(tree[root])
        gate = degree_counts + powers[n + degree + 1] - powers[n + degree]
        gate += sum(powers[size] for size in sizes(root, -1)[1:])
        rows = tuple(family[root] for family in polynomials)
        hankel = tuple(tuple(sum(coeff * values[i + j] for i, coeff in enumerate(row)) % prime
                             for j in range(n + 1))
                       for row, (values, prime) in zip(rows, evaluations, strict=True))
        roots.append((root, gate, rows, hankel))
    return roots


def check_candidate(first, second, marks, previous):
    left, right = [join((first, a), (second, b))[0] for a, b in (marks, previous)]
    assert not nx.is_isomorphic(left, right), "Distinct balanced joins at root orbits must differ"
    for cap in (3, 5, None):
        if signature(adjacency(left), cap) != signature(adjacency(right), cap):
            return None
    return [nx.to_graph6_bytes(graph, header=False).decode().strip() for graph in (left, right)]


def scan(graphs, seed):
    n = len(graphs[0])
    rng = Random(seed)
    evaluations = tuple((tuple([0] + [rng.randrange(1, prime) for _ in range(2 * n)]), prime)
                        for prime in PRIMES)
    records = [component_data(graph, evaluations) for graph in graphs]
    counts = Counter(joins=0, first_gate_repeats=0, modular_matches=0)
    for i, left in enumerate(records):
        for j in range(i, len(records)):
            seen = {}
            for a, a_gate, _, a_hankel in left:
                for b, b_gate, b_rows, _ in records[j]:
                    if i == j and a > b:
                        continue
                    counts["joins"] += 1
                    gate = a_gate + b_gate
                    group = seen.setdefault(gate, [])
                    if not group:
                        group.append((a, b, a_hankel, b_rows))
                        continue
                    counts["first_gate_repeats"] += 1
                    if len(group[0]) == 4:
                        old_a, old_b, old_hankel, old_rows = group[0]
                        group[0] = old_a, old_b, projection(old_hankel, old_rows)
                    result = projection(a_hankel, b_rows)
                    for old_a, old_b, old_result in group:
                        if result == old_result:
                            counts["modular_matches"] += 1
                            candidate = check_candidate(graphs[i], graphs[j], (a, b), (old_a, old_b))
                            if candidate is not None:
                                return {**counts, "candidate": candidate}
                    group.append((a, b, result))
    return {**counts, "candidate": None}


def projection(hankel, rows):
    return tuple(sum(left * right for left, right in zip(h, r, strict=True)) % prime
                 for h, r, prime in zip(hankel, rows, PRIMES, strict=True))


def sample_components(order, limit, seed):
    seen = set()
    available = []
    graphs = nx.nonisomorphic_trees(order) if order <= 12 else component_trees(order, limit, seed)
    for graph in graphs:
        graph = nx.convert_node_labels_to_integers(graph)
        key = rooted_code(adjacency(graph), (1,) * order)
        if key not in seen:
            seen.add(key)
            available.append(graph)
    if len(available) > limit:
        return Random(seed).sample(available, limit)
    return available


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-order", type=int, default=10)
    parser.add_argument("--max-order", type=int, default=16)
    parser.add_argument("--components", type=int, default=250)
    parser.add_argument("--seed", type=int, default=20261212)
    args = parser.parse_args()
    if not 2 <= args.min_order <= args.max_order or args.components < 1:
        parser.error("Expected a positive component limit and valid order range")
    for order in range(args.min_order, args.max_order + 1):
        graphs = sample_components(order, args.components, args.seed)
        result = scan(graphs, args.seed + order)
        print(json.dumps({"component_order": order, "components": len(graphs), **result}), flush=True)
        if result["candidate"] is not None:
            break
