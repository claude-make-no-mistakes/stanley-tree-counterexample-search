# Stanley's tree conjecture counterexample search

Stanley's tree conjecture asks whether two non-isomorphic finite trees can have the same chromatic symmetric function. The searches in this repository have produced no counterexample. They compare exact counts of edge subsets classified by the multiset of resulting component orders (the $U$-polynomial), which determines the chromatic symmetric function of a tree because the sign of each power-sum term depends only on the number of components.

## Papers and proofs

- **Single-edge reconstruction and root exchanges:** A finite tree with a marked edge is determined up to edge-preserving isomorphism by its deletion forest and its contraction with the merged vertex marked. This rules out the root-exchange construction for all component orders (and yields the corollary that for non-isomorphic rooted trees $U,V$ of equal order, at most one rooted type $A$ satisfies $U+A\cong V+A$). The four-vertex path and star show that the mark on the contracted vertex is necessary. [Paper (PDF)](edge-reconstruction.pdf) · [LaTeX source](edge-reconstruction.tex) · [Companion note](ROOT-EXCHANGE.md)

- **Multi-edge contractions, common-hub joins, and subtree relocation:**
  - The double contraction and the unordered pair of rooted weight-two mixed components determine a tree and its two specified edges. [Two-edge theorem](TWO-EDGE.md)
  - For three specified edges forming a connected subtree, the positive-contraction layers determine the tree and its three specified edges. [Three-edge theorem](THREE-EDGE-CONNECTED.md)
  - Joining equal copies of a tree at a common attachment vertex with isomorphic marked contractions cannot produce an order-minimal Stanley counterexample, even with polynomial cancellation. [Common attachment](COMMON-HUB.md)
  - Relocating a fixed rooted graft across a single edge cannot produce an order-minimal counterexample; across two edges, both the middle piece and graft must have order at least $6$ and the endpoint pieces must share both connected-subtree profiles and detached-order multisets, giving a computer-assisted lower bound of $40$ vertices. [Subtree relocation](SUBTREE-RELOCATION.md)
  - Full paper: [Paper (PDF)](contraction-reconstruction.pdf) · [LaTeX source](contraction-reconstruction.tex)

## Computational coverage

| Search | Coverage | Log |
| --- | --- | --- |
| Leaf decorations | 1,527,815 decorations of cores on 2–6 internal vertices, producing trees of order 30–32 (count includes equivalent decorations). | [pilot.jsonl](pilot.jsonl) |
| Near-collision perturbations | 5,479 distinct variants within their respective source neighborhoods, on 34, 46, and 58 vertices. | [subtree-moves.jsonl](subtree-moves.jsonl) |
| Balanced joins | 1,211,612 pairs of root positions on components of order 15–19. | [balanced-splits.jsonl](balanced-splits.jsonl) |
| Proper trees | 212,723 distinct trees across three families: weights in `{2,3,4}` with total at least 30 on cores of order 8 and 9, and the multiset `2,2,2,3,3,3,4,4,4,4` on cores of order 10. | [core 8](proper-core8.jsonl) · [core 9](proper-core9.jsonl) · [core 10](proper-core10.jsonl) |
| Equal-size subtree exchanges | 128 tree instances across six neighborhoods on 34, 58, and 70 vertices, including the starting trees. No pair of non-isomorphic trees passed the degree and two-cut filter. | [equal-size-exchanges.jsonl](equal-size-exchanges.jsonl) |
| Two pendant-edge relocations | 7,055 isomorphism classes around the left 34-vertex tree and 20,342 around the right. Of the cross-neighborhood pairs, 2,594 passed the degree and two-cut filter; all differed by the exact forest-partition test through seven components. | [two-leaf-moves34.jsonl](two-leaf-moves34.jsonl) |
| Root exchanges across component orders | 3,725,021 root-pair signatures on sampled components of orders 12–22; no matching signed differences. (Ruled out in general by the single-edge reconstruction theorem.) | [unequal-splits.jsonl](unequal-splits.jsonl) |
| Matching endpoint trees | 10,477,944 root-pair trials on sampled components of orders 12–26, including 1,539,891 fingerprints compared after filtering; no matching signed differences. | [matching-fringes.jsonl](matching-fringes.jsonl) |
| Identical-fringe completions | Archived completion scan covering branch orders 8–16 (closed at all orders by the single-edge reconstruction theorem). | [fringe-orbit-completions.jsonl](fringe-orbit-completions.jsonl) |
| Single-edge reconstruction | Verified all 175,072 marked-edge choices across the 13,187 unlabeled trees of orders 2–15; zero collisions. | [edge-reconstruction.jsonl](edge-reconstruction.jsonl) |
| Multiple-edge reconstruction | Verified all 16,440 edge pairs and 8,519 connected edge triples across the 434 unlabeled trees of orders 3–11; zero collisions. | [multiple-edge-reconstruction.jsonl](multiple-edge-reconstruction.jsonl) |
| Three-copy two-edge expansions | Enumerated 3,302,297 attachment arrangements (2,981,858 distinct expansions) on three copies of each unlabeled tree of orders 2–12; zero non-isomorphic matches. | [two-edge-repeats.jsonl](two-edge-repeats.jsonl) |
| Mixed-term cancellation in three equal copies | At component orders 2–12, 313,000 non-isomorphic pairs shared their marked double contraction and all-deleted forest; 2,917 agreed through three components, and none agreed through five. | [two-edge-cancellations.jsonl](two-edge-cancellations.jsonl) |
| Balanced joins with modular polynomial checks | Checked 11,916,567 balanced joins within pools of 200 components per order from 12 to 18. Of 1,671,767 degree and one-cut repeats, none also matched both prime-field evaluations for its component pair. | [balanced-polynomial-search.jsonl](balanced-polynomial-search.jsonl) |
| Rooted connected-subtree & detached-order profiles | Exhaustive check of all rooted trees of orders 1–14; zero same-tree two-profile repeats through order 13, and one at order 14. | [rooted-profiles.jsonl](rooted-profiles.jsonl) |
| Restricted $U_5$ pruning test | Pruning the published 34-vertex near collision ([arXiv:2002.08186](https://arxiv.org/abs/2002.08186)) down to orders 33–30 yields no smaller restricted $U_5$ collision. | [restricted-shrink.jsonl](restricted-shrink.jsonl) |

## Notes on invariants

- **Weighted core projection (`proper_core.py`):** For a proper tree, discarding all terms whose component-size partition contains a $1$ retains every edge incident to a leaf. Contracting those leaf edges and assigning each surviving core vertex the size of its contracted group gives the weighted core projection used in `proper_core.py`.
- **Equal-size branch exchanges (`near_collisions.py`):** Swapping disjoint branches of equal order preserves the degree multiset and all one-edge split sizes: an edge in a moved branch keeps the same component on the side away from the attachment, and an edge in the retained tree receives the same branch weight as before. Because the paired starting trees have different degree multisets, equal-size exchanges alone cannot produce a collision across the paired neighborhoods.

## Replay

Python 3.10+ with NetworkX 3.3+ and `pdflatex` reproduce the saved logs and PDFs:

```sh
python3 search.py
python3 near_collisions.py 1 2 --subtree
python3 near_collisions.py 2 2 --subtree
python3 near_collisions.py 1 3 --subtree
python3 near_collisions.py 1 2 --exchange
python3 near_collisions.py 1 3 --exchange
python3 near_collisions.py 2 3 --exchange
python3 near_collisions.py 1 2 --leaf-distance 2
python3 restricted_shrink.py
python3 balanced_splits.py
python3 balanced_splits.py --min-order 12 --max-order 22 --random-count 3000 --seed 20261205 --across-orders
python3 balanced_splits.py --min-order 12 --max-order 26 --random-count 4500 --seed 20261207 --matching-fringes
python3 fringe_completions.py --min-order 8 --max-order 22 --random-count 2100 --seed 20261208 --prune-automorphisms
python3 check_edge_reconstruction.py --max-order 15
python3 check_multiple_edges.py --max-order 11
python3 two_edge_repeats.py --max-order 12
python3 two_edge_repeats.py --max-order 12 --search-mixed-cancellation
python3 balanced_polynomial_search.py --min-order 12 --max-order 18 --components 200 --seed 20261212
python3 check_rooted_profiles.py --max-order 14
python3 proper_core.py --core 8 --min-order 30 --max-weight 4
python3 proper_core.py --core 9 --min-order 30 --max-weight 4
python3 proper_core.py --core 10 --min-order 31 --weights 2,2,2,3,3,3,4,4,4,4
pdflatex edge-reconstruction.tex && pdflatex edge-reconstruction.tex
pdflatex contraction-reconstruction.tex && pdflatex contraction-reconstruction.tex
```
