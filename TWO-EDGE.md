# Reconstructing a tree from two-edge contractions

Let $S$ be a tree with two specified edges. Deleting both gives three components. Call the component incident to both removed edges $T$ and the other two components outer. The two-edge expansion of the chromatic symmetric function consists of the all-deleted forest, the two forests given by deleting one edge and contracting the other, and the tree given by contracting both edges. Contracting adds vertex weights, and original vertices have weight one. [Weighted deletion and contraction](https://arxiv.org/abs/1910.11859)

**Theorem.** The double contraction and the unordered pair of rooted weight-two components from the mixed terms determine the tree and its unordered pair of specified edges. Each mixed component is rooted at its unique vertex of weight two. The isolated components of the mixed terms and the all-deleted forest can be discarded.

For a vertex, its branch bag is the multiset of rooted components obtained by removing it, with roots at its former neighbors. The branch bag determines the rooted tree. Add and subtract bags in the free abelian group on rooted tree types, writing $[U]$ for one copy of type $U$.

## A common attachment point

If the attachment points coincide, the double contraction has a single mark of weight three. Let $H$ be its branch bag and let $M_1,M_2$ be the two mixed bags. Writing $C,A_1,A_2$ for the central and outer attachment bags gives $H=C+A_1+A_2$ and $M_i=C+A_i$. Thus $C=M_1+M_2-H$ and $A_i=M_i-C$. These rooted types recover the original joins.

## Two distinct attachment points

Otherwise the double contraction has two marks of weight two. Align two candidate double contractions by a weight-preserving isomorphism and number the marks $1,2$. On removing edges of the path between them, write $W_1,\ldots,W_k$ for the rooted pieces at its interior vertices in order. These pieces are the same in both candidates with the same orientation. Let $H_i$ be the known off-path bag at mark $i$ in the double contraction. It is the sum of the central endpoint off-path bag and the bag of the outer component attached there.

Let $E_1,E_2$ be the rooted off-path pieces at the endpoints of the central component. Write $U_i$ for its inward rooted branch from endpoint $i$. The two inward branches are the chains $W_1,\ldots,W_k,E_2$ and $W_k,\ldots,W_1,E_1$, respectively. A chain joins the roots of consecutive pieces and is rooted at the first root. The mixed bag assigned to endpoint $i$ is $H_i+[U_i]$. Use primes for the second candidate while retaining the same $H_i$ and $W_j$.

If the mixed bags align, $U_i\cong U'_i$ for each $i$. Cancel the common off-path bag at each successive interior root of the two chains. This recovers $E_i\cong E'_i$. Subtracting the branch bags of the endpoint pieces from $H_i$ recovers the outer components with their attachment roots. These rooted isomorphisms reconstruct the original tree and specified edge pair.

If the mixed bags cross, equality of their unordered pair gives $H_1+[U_1]=H_2+[U'_2]$ and $H_2+[U_2]=H_1+[U'_1]$. Adding gives equality of the multisets $\{U_1,U_2\}$ and $\{U'_1,U'_2\}$. The aligned possibility is covered by the preceding argument, which uses only equality of the inward branches. Otherwise $U_1\cong U'_2$ and $U_2\cong U'_1$. Moreover $H_1=H_2$ by either crossed equation.

The isomorphism $U_1\cong U'_2$ compares the chains $W_1,\ldots,W_k,E_2$ and $W_k,\ldots,W_1,E'_1$. While at least two unpaired interior pieces remain, the continuation child in either chain contains the first piece of the other chain and a nonempty terminal piece. It is larger than every off-path child of the other root. Therefore the isomorphism matches the continuation children. Cancelling them in the root bags gives $W_1\cong W_k$, then $W_2\cong W_{k-1}$, and so forth. Cancel a common middle piece if the number of pieces is odd. The mirrored pieces now agree throughout both chains, so cancelling the remaining bags gives $E_2\cong E'_1$. The second inward isomorphism gives $E_1\cong E'_2$. If the marks are adjacent, there are no interior pieces and the endpoint types agree immediately under reversal.

Thus the original central components agree under reversal, including their rooted endpoint pieces. Since $H_1=H_2$, subtracting those endpoint bags pairs the outer components under the same reversal. The resulting isomorphism carries the specified edges as a set.

## Implication for counterexample searches

Two-edge term-by-term isomorphism cannot produce a Stanley counterexample, regardless of component types or sizes. If a pair has isomorphic all-deleted forests and double contractions, equality of chromatic symmetric functions is equivalent to equality of the sum of the two mixed chromatic symmetric functions. Any non-isomorphic pair found in that way must have different rooted contracted components in the mixed data. It requires a polynomial identity between the two sums.

## Search with three identical components

The exact search enumerated 3,302,297 attachment arrangements on three copies of each unlabeled tree of orders 2–12. It found 2,981,858 distinct expansions and no matching expansion on non-isomorphic joined trees. The two joining edges are the only edges that split off a component of one copy's order. An internal cut in an outer copy leaves a smaller component, and an internal cut of the central copy either leaves a smaller component or puts more than a full copy on each side. Thus the source isomorphism test may use the central path and the two rooted outer components, up to reversal of the path. A separate implementation using direct graph deletion and weighted contraction matched the counts for all 2,484 unfiltered attachments at component orders 2–5. [Search log](two-edge-repeats.jsonl)

```sh
python two_edge_repeats.py --max-order 12
```
