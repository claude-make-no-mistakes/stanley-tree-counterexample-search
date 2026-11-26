# Stanley's tree conjecture counterexample search

The conjecture asks whether two non-isomorphic trees can have the same chromatic symmetric function. The searches in this repository have produced no counterexample. They compare exact counts of edge subsets classified by the sizes of the resulting components. For a tree, the sign of each coefficient in the power-sum expansion depends only on the number of components. [Conjecture and recent reductions](https://arxiv.org/abs/2611.18940)

**A tree with a marked edge is determined by the forest after deleting that edge and the tree after contracting it, with the merged vertex marked.** The proof rules out the root-exchange construction for all component orders. The four-vertex path and star show that the mark on the contracted vertex is necessary. [Paper](edge-reconstruction.pdf) · [Proof](ROOT-EXCHANGE.md)

For two-edge expansions, a term-by-term match can change the full tree only if the central component has the same unrooted type as an outer component. [Two-edge reduction](TWO-EDGE.md)

| Search | Coverage |
| --- | --- |
| Leaf decorations | 1,527,815 decorations of cores on two to six internal vertices, producing trees of order 30–32. The count includes equivalent decorations. |
| Near-collision perturbations | 5,479 distinct variants within their respective source neighborhoods, on 34, 46, and 58 vertices. |
| Balanced joins | 1,211,612 pairs of root positions, on components of order 15–19. |
| Proper trees | 212,723 distinct trees across three families. Use weights in `{2,3,4}` with total at least 30 on cores of order eight and nine, and the multiset `2,2,2,3,3,3,4,4,4,4` on cores of order ten. |
| Equal-size subtree exchanges | 128 tree instances across six neighborhoods on 34, 58, and 70 vertices, including the starting trees. No pair of non-isomorphic trees passed the degree and two-cut filter. |
| Two pendant-edge relocations | 7,055 isomorphism classes around the left 34-vertex tree and 20,342 around the right. Of the cross-neighborhood pairs, 2,594 passed the degree and two-cut filter. All differed by the exact forest-partition test through seven components. |
| Root exchanges | Reconstruction rules out the entire construction. [Proof and exact search](ROOT-EXCHANGE.md) |
| Root exchanges across component orders | 3,725,021 root-pair signatures on sampled components of orders 12–22. No matching signed differences. [Run log](unequal-splits.jsonl) |
| Matching endpoint trees | 10,477,944 root-pair trials on sampled components of orders 12–26, including 1,539,891 fingerprints compared after filtering. No matching signed differences. [Run log](matching-fringes.jsonl) |
| Edge reconstruction | Checked all 175,072 edge choices of the 13,187 unlabeled trees of orders 2–15. No two distinct marked-edge types shared both reconstruction data. [Run log](edge-reconstruction.jsonl) |

For a proper tree, discard all terms whose component-size partition contains a (1). The remaining forests contain every edge incident to a leaf. Contract those leaf edges and give the surviving vertex the size of its contracted group. This is the weighted core projection used in `proper_core.py`.

Swapping disjoint branches of equal order preserves the degree multiset and all one-edge split sizes. An edge in a moved branch keeps the same component on the side away from the attachment, and an edge in the retained tree receives the same branch weight as before. An independent check recovered these invariants directly from every generated tree. The source trees in each pair have different degree multisets, so equal-size exchanges alone cannot produce a collision across the paired neighborhoods.

## Replay

Python 3.10 and NetworkX 3.3 reproduce the saved logs.

```sh
python search.py
python near_collisions.py 1 2 --subtree
python near_collisions.py 1 2 --exchange
python near_collisions.py 1 3 --exchange
python near_collisions.py 2 3 --exchange
python near_collisions.py 1 2 --leaf-distance 2
python balanced_splits.py
python balanced_splits.py --min-order 12 --max-order 22 --random-count 3000 --seed 20261205 --across-orders
python balanced_splits.py --min-order 12 --max-order 26 --random-count 4500 --seed 20261207 --matching-fringes
python fringe_completions.py --min-order 8 --max-order 22 --random-count 2100 --seed 20261208 --prune-automorphisms
python check_edge_reconstruction.py --max-order 15
python proper_core.py --core 8 --min-order 30 --max-weight 4
python proper_core.py --core 9 --min-order 30 --max-weight 4
python proper_core.py --core 10 --min-order 31 --weights 2,2,2,3,3,3,4,4,4,4
```

`restricted_shrink.py` tests whether pruning the published 34-vertex near collision preserves equality in the restricted (U_5) polynomial. [Near-collision construction](https://arxiv.org/abs/2002.08186)

The archived completion scan covers fully processed branch orders 8–16. The reconstruction proof closes this search at every order. [Run log](fringe-orbit-completions.jsonl)
