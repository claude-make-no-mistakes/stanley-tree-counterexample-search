# Reconstructing three connected specified edges

**Theorem.** Let $S$ be a tree with three specified edges forming a connected subtree. For each edge, either delete it or contract it, adding weights at the endpoints on contraction. For each positive number of contractions, retain the resulting multiset of weighted forests up to isomorphism. These data determine $S$ and its three specified edges up to isomorphism.

Write a branch bag for the multiset of rooted branches at a vertex. Along the four-vertex specified subtree, use the bag of each vertex after discarding its specified edges. Vertices outside that subtree are unaltered. Thus the fully contracted tree has one vertex of weight four, whose bag $Q$ is the sum of the four original bags. Conversely, a tree producing these data must have its three specified edges connected, since three contractions yielded a vertex of weight four.

The specified subtree is a star or a path. Only a path gives a term with two vertices of weight two after contracting two edges and deleting one. For a star, each of the three two-contraction terms has one root of weight three. Subtract its bag from $Q$ to recover the bag at the specified leaf separated by the deletion. This gives all three leaf bags as a multiset, including multiplicity. Subtract their sum from $Q$ to recover the center. These data reconstruct the star of rooted pieces.

For a path, let $A,B,C,D$ be the four rooted pieces in order, using the same letters for their root bags in sums. The two terms with a weight-three root recover $A,D$ as an unordered pair of rooted types by the same subtraction. At one contraction, the term contracting the middle edge has weight-two root bag $Q-A-D=B+C$ and the unrooted versions of $A,D$ as companions. Remove one occurrence of this known term from the multiset. The remaining terms contract a terminal edge and give respectively

$$
 (A+B; C,D),\qquad(C+D; A,B),
$$

where the entries before the divider are marked root bags and the two companions after it are unrooted trees.

Suppose two paths have the same data. Orient the second path $A',B',C',D'$ so that its two terminal-contraction terms match the first path in the displayed order. This is possible even if the two terms are equal. If $A'=A$ and $D'=D$ as rooted types, equality of the marked bags immediately gives $B'=B,C'=C$. Otherwise $A'=D,D'=A$, with $A,D$ distinct as rooted types.

The two-piece join of $A,B$ across its specified edge and the corresponding join of $A',B'$ have the same marked contraction $A+B=A'+B'$ from the first terminal-contraction term. They have the same unrooted deletion forest from the companions of the second term. The single-edge reconstruction theorem therefore gives equality of the unordered rooted pieces of those joins, since its isomorphism carries the joining edge to its counterpart. Here this implies $B=D$ and $B'=A$. Applying the argument to the other end gives $C=A$ and $C'=D$. The paths are reversals of one another and the full trees are isomorphic, preserving the three specified edges as a set. [Single-edge reconstruction theorem](ROOT-EXCHANGE.md)

Consequently, a search based on term-by-term isomorphism of three-edge expansions can focus on disconnected sets of specified edges. Polynomial cancellation remains a separate possibility even for connected sets. [Weighted deletion and contraction](https://arxiv.org/abs/1910.11859)
