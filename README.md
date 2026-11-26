# Stanley's tree conjecture counterexample search

The conjecture asks whether two non-isomorphic trees can have the same chromatic symmetric function. The searches in this repository have produced no counterexample. They compare exact counts of edge subsets classified by the sizes of the resulting components. For a tree, the sign of each coefficient in the power-sum expansion depends only on the number of components. [Conjecture and recent reductions](https://arxiv.org/abs/2611.18940)

| Search | Coverage |
| --- | --- |
| Leaf decorations | 1,527,815 decorations of cores on two to six internal vertices, producing trees of order 30–32. The count includes equivalent decorations. |
| Near-collision perturbations | 5,479 distinct variants within their respective source neighborhoods, on 34, 46, and 58 vertices. |
| Balanced joins | 1,211,612 pairs of root positions, on components of order 15–19. |
| Proper trees | All assignments of weights (2,3,4) with total at least 30 on cores of order eight and nine. A separate order-ten scan uses the multiset (2,2,2,3,3,3,4,4,4,4), giving total order 31. |

For a proper tree, discard all terms whose component-size partition contains a (1). The remaining forests contain every edge incident to a leaf. Contract those leaf edges and give the surviving vertex the size of its contracted group. This is the weighted core projection used in `proper_core.py`.

## Replay

Python 3.10 and NetworkX 3.3 reproduce the saved logs.

```sh
python search.py
python near_collisions.py 1 2 --subtree
python balanced_splits.py
python proper_core.py --core 8 --min-order 30 --max-weight 4
python proper_core.py --core 9 --min-order 30 --max-weight 4
python proper_core.py --core 10 --min-order 31 --weights 2,2,2,3,3,3,4,4,4,4
```

`restricted_shrink.py` tests whether pruning the published 34-vertex near collision preserves equality in the restricted (U_5) polynomial. [Near-collision construction](https://arxiv.org/abs/2002.08186)
