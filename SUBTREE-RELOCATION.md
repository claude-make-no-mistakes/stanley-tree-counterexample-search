# Restrictions on relocating a fixed rooted subtree

Consider a tree obtained by attaching a fixed nonempty rooted tree $C$ by an edge to a vertex $u$ of a tree $H$. Compare moving that edge from $u$ to $v$, keeping the root in $C$. The $U$-polynomial of an ordinary tree counts its edge subsets by component orders. Equality of these polynomials is equivalent to equality of chromatic symmetric functions. Use the same definition for vertex-weighted trees, with the total weight replacing the order in every component. For a rooted tree $T$, $R_T(z)$ is the version that uses $z^i$ for its root component of weight $i$. Write $L(z^i)=x_i$ for the linear operation giving that component its usual variable. [Weighted deletion and contraction](https://arxiv.org/abs/1910.11859)

## An adjacent slide cannot give a smallest counterexample

Suppose $uv$ is an edge of $H$ and let $A,B$ be the two sides of that edge, rooted at $u,v$. Write $W(P,C)=L(R_P(z)R_C(z))$. The polynomial $W(P,C)$ counts the weighted contraction of the edge joining the two roots. The difference of the original and relocated tree polynomials is

$$
 U(B)W(A,C)-U(A)W(B,C).
$$

Indeed, terms cutting the graft edge agree, as do the terms retaining both of the two edges in question. The terms cutting $uv$ and retaining the graft give precisely the displayed difference.

Each weighted tree polynomial of total weight $w$ has the form $x_w+f(x_1,\ldots,x_{w-1})$. It is prime in $\mathbb Z[x_1,x_2,\ldots]$, since quotienting by this monic linear polynomial just eliminates $x_w$. It is homogeneous of degree $w$ with $\deg(x_i)=i$. If the displayed difference vanishes, the prime $U(B)$ must equal either $U(A)$ or $W(B,C)$ up to a unit. The latter weights differ by the positive order of $C$, and the coefficient of each leading variable is one. Hence $U(A)=U(B)$ and $W(A,C)=W(B,C)$.

In an order-minimal Stanley counterexample, the smaller trees $A,B$ with equal $U$ must be isomorphic. Joining $C$ to each of their marked roots gives two more smaller trees with equal $U$, since their deletion products agree and their weighted contractions agree. They too are isomorphic. Apply Krasikov's branch interchange theorem on the common unrooted type of $A,B$. The two grafts compared there are a dummy root with $C$ attached by an edge and a single rooted vertex, with the two attachment positions switched. Since the attached trees are isomorphic, the two positions in the common unrooted tree lie in the same orbit. Thus the original sides are isomorphic at their marked roots. Swapping the sides now takes the full original tree to its relocated counterpart. This contradicts minimality. [Krasikov's theorem, restated as Theorem 2.2 by Asciak et al.](https://ajc.maths.uq.edu.au/pdf/60/ajc_v60_p169.pdf)

## A distant slide must have symmetric piece orders

Let $m=|H|$, $c=|C|$ and let $S$ be the set of orders on the $u$ side of successive path-edge cuts from $u$ to $v$. The orders strictly increase. Only these cuts change the two-component terms of $U$. Put $f(s)=x_s x_{m+c-s}$. The difference at that layer is $\sum_{s\in S}(f(m-s)-f(s))$.

Let $g(s)=1_{s\in S}-1_{m-s\in S}$ for integer $s$. The equality of this layer is equivalent to $g(s)+g(m+c-s)=0$ on distinct complementary indices, and to $g(s)=0$ at the midpoint. Extend $g$ by zero outside its support. Since $g(m-s)=-g(s)$, these identities give $g(s)=g(s-c)$ for all integers $s$. A finitely supported function cannot have nonzero period $c$. Thus $S$ is symmetric under $s\mapsto m-s$, and consecutive differences of the side orders show that the orders of the rooted off-path pieces form a palindrome.

One can also telescope the adjacent-slide formula along the path. For $s_0=\min S$, the largest variable index of any summand is $m+c-s_0$. It occurs in the contracted weighted factors at the two extreme cuts, since $\max S=m-s_0$. Each is linear in that variable with coefficient one. The coefficient in their difference is the difference of the ordinary $U$-polynomials of the two endpoint pieces of $H$ after removing all path edges. Thus equality of the full polynomials forces these two endpoint pieces to have equal $U$. In an order-minimal collision they must be isomorphic as unrooted trees.

## A distance-two slide requires a middle piece and graft of order at least six

For a rooted tree $D$, let $P_D(z)$ count connected vertex subsets containing the root by order. The recurrence is $P_D(z)=z\prod_E(1+P_E(z))$, where $E$ ranges over its rooted branches. In any slide with equal $U$, the attachment vertices $u,v$ of $H$ must have equal rooted profiles. The terms cutting the graft edge agree in the two trees. Among the remaining terms with exactly one nonsingleton component, that component contains the graft edge. The two generating functions for its orders are therefore $P_{H,u}P_C$ and $P_{H,v}P_C$. Cancel $P_C$.

Suppose the path has two edges, and let $A,J,B$ be the three rooted off-path pieces in order. The equality of the two profiles on $H$ gives $(P_A-P_B)(1+P_J)=0$, so $P_A=P_B$. Write $a=|A|=|B|$, $b=|J|$, $c=|C|$. In a smallest collision $A$ and $B$ have the same ordinary $U$-polynomial $F$ and the same unrooted type. If the roots are equivalent, reversal is already an isomorphism of the full trees. Since every degree class in every tree of order at most four is a single vertex orbit, equality of the root degrees forces $a\geq5$ in a non-isomorphic pair.

Put $p=R_A$, $q=R_B$, $r=R_J$ and $s=R_C$. Separating the terms retaining the graft by which of the two path edges they retain gives the difference

$$
 F L\bigl[s(U(J)+r)(p-q)\bigr]+L(rq)L(sp)-L(rp)L(sq).
$$

If $J$ and $C$ have the same rooted type, the last two terms cancel. The factor $s(U(J)+r)$ is the rooted polynomial for the tree obtained by joining $C$ and $J$ at their roots, rooted on the $C$ side. The displayed identity then gives identical weighted contractions on joining that tree to $A$ or $B$. The deletion products already agree, so the two joins have equal ordinary $U$. They are smaller than the original pair and hence are isomorphic. Krasikov's theorem as in the adjacent case identifies the attachment roots in $A,B$, which gives a contradiction.

Otherwise take the identity modulo the prime $F$. This eliminates $x_a$. Each remaining factor still has a leading variable of index $a+b$ or $a+c$ with coefficient one, so each is prime in the quotient polynomial ring. Matching factors after reduction gives one of two cases. The straight matching pairs contractions having the same graft, and is forced when $b\ne c$ by their distinct weighted degrees. The crossed matching can occur only when $b=c$.

In the straight case, suppose one graft has order $h\leq5$ and rooted polynomial $w$. Then $L(wp)-L(wq)=FK$ for a homogeneous polynomial $K$ of weighted degree $h$. Set every $x_i$ to the same indeterminate $t$. On a weighted tree with $e$ edges this gives $t(1+t)^e$, by counting retained edges. Consequently $K$ specializes to zero. In particular its $x_1^h$ coefficient is zero. Since $P_A=P_B$, the difference $L(wp)-L(wq)$ has no monomial $x_j x_1^{a+h-j}$ with $j\geq2$. Its coefficient in $FK$ is exactly the coefficient of $x_j x_1^{h-j}$ in $K$ for $2\leq j\leq h$, because the all-singleton term of $F$ has coefficient one and the all-singleton term of $K$ is absent. These coefficients of $K$ are thus zero. For $h\leq5$, after removing these monomials and $x_1^h$, the remaining partitions of $h$ have distinct lengths. The zero specialization then gives $K=0$. The two smaller joins with the graft $w$ have equal ordinary $U$, and minimality and Krasikov again identify the attachment roots.

In the crossed case of common order $h=b=c\leq5$, one matched pair gives $L(rp)-L(sp)=FK$, with $K$ homogeneous of weight $h$. Its all-$t$ specialization again vanishes. In particular it has zero coefficients at $x_1^h$ and $x_h$, which are alone in their respective lengths. The coefficients of $x_j x_1^{a+h-j}$ on the left count the rooted-profile difference $P_A(P_J-P_C)$ by order. For $j\geq h$ the corresponding coefficients on the right vanish. Thus $P_A(P_J-P_C)$ has degree at most $h-1$. If $P_J-P_C$ were nonzero, it would have degree at least two, since both profiles start with $z$. With $\deg P_A=a\geq5$, this is impossible. The recurrence for $P$ distinguishes all rooted trees of each order through five, as checked in [the profile replay](check_rooted_profiles.py). Hence $J$ and $C$ have the same rooted type, a case already excluded.

## Detached orders give a second endpoint test

For the two endpoint pieces of order $a$, let $d_t$ be the difference of the numbers of internal edges whose deletion detaches $t$ vertices from the endpoint root. Extend $d_t$ by zero outside $1,\ldots,a-1$. The equal ordinary endpoint polynomials imply $d_t+d_{a-t}=0$ from their two-component terms. Put $Q_k=\sum_t d_t x_t x_{a+k-t}$, where the sum uses only $1\leq t<a$. In particular $Q_0=0$.

In the three-component terms of the slide difference, an edge cut in the graft attachment or two cuts off the path give equal contributions. Cutting both path edges also gives equal contributions since both endpoint orders are $a$. Pairing the two choices of path cut cancels the contributions from a cut inside $J$ or $C$. A cut in $A$ detaching order $t$ contributes

$$
 x_t(x_{a+c-t}x_{a+b}-x_{a-t}x_{a+b+c})
 +x_t(x_{a+b+c-t}x_a-x_{a+b-t}x_{a+c}).
$$

A cut with that detached order in $B$ contributes the opposite. Hence equality requires $x_{a+b}Q_c+x_aQ_{b+c}-x_{a+c}Q_b=0$. If $b=c$, this gives $Q_{2b}=0$. If $b\ne c$, every surviving monomial of $Q_c$ must contain $x_a$ or $x_{a+c}$, since $x_{a+b}$ is distinct from both. The indices in $Q_c$ are less than $a+c$, and its first index $t$ is less than $a$. Thus $Q_c$ is a multiple of $x_a x_c$. At all $x_i=1$ its value is $\sum_t d_t=0$, so $Q_c=0$.

For positive $k$, the equality $Q_k=0$ implies $d_t+d_{a+k-t}=0$, including an integral midpoint by comparing coefficients. Along with $d_t=-d_{a-t}$ this makes $d$ periodic with period $k$. Its finite support gives $d=0$. Thus the endpoint pieces have identical detached-order multisets.

The profile replay finds that no tree of order at most thirteen has distinct root orbits with both the same $P$ and the same detached-order multiset. It finds one repeated pair at order fourteen. Together with $b,c\geq6$, this gives a computer-assisted bound of $2\cdot14+6+6=40$ on a smallest Stanley collision obtained by a distance-two slide. [Replay log](rooted-profiles.jsonl)
