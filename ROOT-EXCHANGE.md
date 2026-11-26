# When a root exchange can change the tree

One way to seek a Stanley collision is to join the same two components at different roots. For a tree $T$, let $B_T(v)$ be the multiset of rooted branches hanging from $v$. Each branch is rooted at a neighbor of $v$. Treat the multiset as a vector indexed by rooted tree isomorphism classes.

Suppose $T$ has possible roots $a,b$, and $T'$ has possible roots $c,d$. Compare joining $a$ to $d$ with joining $b$ to $c$. Deletion of the added edge gives the same forest in both cases. Contraction of that edge gives the same rooted weighted tree whenever

$$
D=B_T(a)-B_T(b)=B_{T'}(c)-B_{T'}(d).
$$

The root of the contraction has weight two. The weighted chromatic deletion–contraction formula then gives equal chromatic symmetric functions of the joined trees. This construction allows unequal component orders. [Weighted deletion and contraction](https://arxiv.org/abs/1910.11859)

If $D=0$, adjoining a root to the common branch bag shows that the two roots in each component lie in the same orbit. The joined trees are isomorphic. For nonzero $D$, the following result excludes every exchange in which either component has different rooted trees at the two ends of its marked path, in the sense defined below.

## The part of the difference that determines the component

Write the path from $a$ to $b$ as $x_0,dots,x_d$. For each path edge $x_i x_{i+1}$, let $L_i$ and $R_i$ be the two sides after deletion, rooted at $x_i$ and $x_{i+1}$ respectively. Put $A=L_0$ and $C=R_{d-1}$. These are the endpoint trees obtained by removing the first edge in the direction of the other endpoint.

For a rooted tree $U$, let $F([U])$ be the sum of its rooted descendant subtrees, one for each vertex and including $U$ itself. Extend $F$ linearly. Making $a$ the root of $T$ assigns one downward branch to each edge. Making $b$ the root reverses exactly the path edges. Therefore

$$
F(D)=\sum_{i=0}^{d-1}[R_i]-\sum_{i=0}^{d-1}[L_i].
$$

The sizes of the $R_i$ strictly decrease from $|T|-|A|$ to $|C|$, and the sizes of the $L_i$ strictly increase from $|A|$ to $|T|-|C|$.

If $|A|<|C|$, the largest supported term of $F(D)$ is $+[R_0]$ and the smallest is $-[L_0]$. They survive because no term of opposite sign has either size. Joining their roots recovers $T$ and the rooted isomorphism class of $a$. If $|A|>|C|$, the signs reverse and the procedure recovers the rooted isomorphism class of $b$.

If $|A|=|C|$ and $A\not\cong C$ as rooted trees, both smallest terms survive. Both largest terms also survive. To see this, compare the rooted descendants of size $|A|$ in $R_0$ and $L_{d-1}$. Descendants off the path contribute equally. Along the path the only descendants of that size are $C$ in $R_0$ and $A$ in $L_{d-1}$. Thus $R_0$ and $L_{d-1}$ have different rooted descendant multisets. The largest positive term and the smallest negative term again recover $T$ and the rooted type of $a$.

These three regimes are visible from the signs at the extreme sizes. In the first two regimes one sign occurs at each extreme. In the equal-size regime both signs occur at both extremes. Once the recovered endpoint gives its full branch bag, adding or subtracting $D$ recovers the other endpoint's branch bag and hence its individual rooted isomorphism type. The procedure determines the component and both rooted types whenever $A\not\cong C$.

## The remaining case

Write the branch bags at $a,b$ as $B_T(a)=[R_0]+B_A(a)$ and $B_T(b)=[L_{d-1}]+B_C(b)$. If $A\cong C$, their off-path bags cancel and the nonzero difference has one positive and one negative unit, counting multiplicity. If $A\not\cong C$, the two path terms do not cancel one another, by the size comparison above. Neither can cancel against the opposite off-path bag, since each path term contains the entire opposite endpoint tree. The off-path bags themselves differ, so there is at least one additional signed unit in $D$. This detects the remaining case directly from the original difference.

Consequently, if two components have the same nonzero $D$ and either has different rooted endpoint trees, the reconstruction applies to both. It gives pairwise rooted isomorphisms at the corresponding attachment vertices. Exchanging the two components then exhibits an isomorphism of the joined trees. Only a difference of the form $[U]-[V]$ can produce a non-isomorphic pair by this method. In that case the two rooted endpoint trees within each component are isomorphic, and the reconstruction above leaves open whether the joins can differ.

An independent mathematical referee checked the alternating signs, the cancellation test at equal sizes, and the isomorphism argument. The resulting search uses `--matching-fringes` to compare only the remaining differences across both equal and unequal component orders.

## Constructing all completions of one positive branch

Fix the positive rooted branch $U$, with root $u$. For each vertex $b\ne u$, take the descendant subtree rooted at $b$ as the candidate endpoint tree $C$. Attach a new copy of $C$ to $u$ to obtain the full component $T$ with its new endpoint $a$. The negative branch $V$ can be obtained from $U$ by moving the original copy of $C$ from its parent to $u$, then making its former parent the root. This is exactly the branch obtained by deleting the original edge to $b$ in $T$. Every nonzero identical-endpoint difference with positive side $U$ arises in this way.

The code compares all negative branches from the same rooted $U$. If two agree, it constructs the joins and checks isomorphism directly. When two endpoints in $U$ are in the same orbit under the fixed root, the corresponding completions give the same rooted data. If two candidate endpoint trees $C$ are themselves rooted-isomorphic, attaching them to the same $U$ gives the same rooted type at $a$. The equality of differences then also gives the same rooted type at $b$, so the resulting joins are isomorphic.

There is a further restriction for unequal component orders. Let $g(s)$ be the sum of the coefficients of $F(D)$ on rooted trees of size $s$. Each path edge supplies sides of complementary sizes in $T$, so $g(s)=-g(|T|-s)$. If $g$ is nonzero, its smallest and largest supported sizes sum to $|T|$. A common difference can therefore span different component orders only if all the size totals $g(s)$ vanish.
