"""Compare connected-subtree profiles and detached-order counts of rooted trees."""

import argparse
import json

import networkx as nx


def multiply(left, right):
    coefficients = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            coefficients[i + j] += a * b
    return coefficients


def rooted_data(tree, root, parent=None):
    branches = [rooted_data(tree, child, root)
                for child in tree[root] if child != parent]
    rooted_type = tuple(sorted(branch_type for branch_type, _, _ in branches))
    profile = [0, 1]
    detached = []
    for _, child_profile, child_detached in branches:
        profile = multiply(profile, (1, *child_profile[1:]))
        detached.append(len(child_profile) - 1)
        detached.extend(child_detached)
    return rooted_type, tuple(profile), tuple(sorted(detached))


def census(order):
    profiles = set()
    rooted_types = 0
    same_tree_repeats = 0
    same_tree_two_profile_repeats = 0
    trees = nx.nonisomorphic_trees(order) if order > 1 else (nx.empty_graph(1),)
    for tree in trees:
        data = {}
        for root in tree:
            key, profile, detached = rooted_data(tree, root)
            data[key] = profile, detached
        tree_profiles = {profile for profile, _ in data.values()}
        rooted_types += len(data)
        same_tree_repeats += len(data) - len(tree_profiles)
        same_tree_two_profile_repeats += len(data) - len(set(data.values()))
        profiles.update(tree_profiles)
    return {"order": order, "rooted_types": rooted_types,
            "distinct_profiles": len(profiles), "same_tree_repeats": same_tree_repeats,
            "same_tree_two_profile_repeats": same_tree_two_profile_repeats}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, default=12)
    args = parser.parse_args()
    if args.max_order < 1:
        parser.error("--max-order must be positive")
    for order in range(1, args.max_order + 1):
        print(json.dumps(census(order)), flush=True)


if __name__ == "__main__":
    main()
