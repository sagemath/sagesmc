r"""
Kyoto Path Model for Affine Highest Weight Crystals
"""

#*****************************************************************************
#       Copyright (C) 2013 Travis Scrimshaw <tscrim at ucdavis.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#****************************************************************************

from sage.structure.parent import Parent
from sage.structure.unique_representation import UniqueRepresentation
from sage.categories.infinite_enumerated_sets import InfiniteEnumeratedSets
from sage.categories.highest_weight_crystals import HighestWeightCrystals
from sage.combinat.crystals.tensor_product import TensorProductOfCrystals, \
    TensorProductOfRegularCrystalsElement
from sage.combinat.root_system.root_system import RootSystem

class KyotoPathModel(TensorProductOfCrystals):
    r"""
    The Kyoto path model for an affine highest weight crystal.

    .. NOTE::

        Here we are using anti-Kashiwara notation and might differ from
        some of the literature.

    Consider a Kac--Moody algebra `\mathfrak{g}` of affine Cartan type `X`,
    and we want to model the `U_q(\mathfrak{g})`-crystal `B(\lambda)`.
    First we consider the set of fundamental weights `\{\Lambda_i\}_{i \in I}`
    of `\mathfrak{g}` and let `\{\overline{\Lambda}_i\}_{i \in I_0}` be the
    corresponding fundamental weights of the corresponding classical Lie
    algebra `\mathfrak{g}_0`. To model `B(\lambda)`, we start with a sequence
    of perfect `U_q^{\prime}(\mathfrak{g})`-crystals `(B^{(i)})_i` of level
    `l` such that

    .. MATH::

        \lambda \in \overline{P}_l^+ = \left\{ \mu \in \overline{P}^+ \mid
        \langle c, \mu \rangle = l \right\}

    where `c` is the canonical central element of `U_q(\mathfrak{g})`
    and `\overline{P}^+` is the nonnegative weight lattice spanned by
    `\{ \overline{\Lambda}_i \mid i \in I \}`.

    Next we consider the crystal isomorphism `\Phi_0 : B(\lambda_0) \to B^{(0)}
    \otimes B(\lambda_1)` defined by `u_{\lambda_0} \mapsto b^{(0)}_{\lambda_0}
    \otimes u_{\lambda_1}` where `b^{(0)}_{\lambda_0}` is the unique element in
    `B^{(0)}` such that `\varphi\left( b^{(0)}_{\lambda_0} \right) = \lambda_0`
    and `\lambda_1 = \varepsilon\left( b^{(0)}_{\lambda_0} \right)` and
    `u_{\mu}` is the highest weight element in `B(\mu)`. Iterating this, we
    obtain the following isomorphism:

    .. MATH::

        \Phi_n : B(\lambda) \to B^{(0)} \otimes B^{(1)} \otimes \cdots
        \otimes B^{(N)} \otimes B(\lambda_{N+1}).

    We note by Lemma 10.6.2 in [HK02]_ that for any `b \in B(\lambda)` there
    exists a finite `N` such that

    .. MATH::

        \Phi_N(b) = \left( \bigotimes_{k=0}^{N-1} b^{(k)} \right)
        \otimes u_{\lambda_N}.

    Therefore we can model elements `b \in B(\lambda)` as a
    `U_q^{\prime}(\mathfrak{g})`-crystal by considering an infinite list of
    elements `b^{(k)} \in B^{(k)}` and defining the crystal structure by:

    .. MATH::

        \begin{aligned}
        \overline{\mathrm{wt}}(b) & = \lambda_N + \sum_{k=0}^{N-1}
        \overline{\mathrm{wt}}\left( b^{(k)} \right)
        \\ e_i(b) & = e_i\left( b^{\prime} \otimes b^{(N)} \right) \otimes
        u_{\lambda_N},
        \\ f_i(b) & = f_i\left( b^{\prime} \otimes b^{(N)} \right) \otimes
        u_{\lambda_N},
        \\ \varepsilon_i(b) & = \max\bigl( \varepsilon_i(b^{\prime}) -
        \varphi_i\left( b^{(N)} \right), 0 \bigr),
        \\ \varphi_i(b) & = \varphi_i(b^{\prime}) + \max\left(
        \varphi_i\left( b^{(N)} \right) - \varepsilon_i(b^{\prime}), 0 \right),
        \end{aligned}

    where `b^{\prime} = b^{(0)} \otimes \cdots \otimes b^{(N-1)}`. To
    translate this into a finite list, we consider a finite sequence
    `b^{(0)} \otimes \cdots \otimes b^{(N-1)} \otimes b^{(N)}_{\lambda_N}`
    and if

    .. MATH::

        f_i\left( b^{(0)} \otimes \cdots b^{(N-1)} \otimes
        b^{(N)}_{\lambda_N} \right) = b_0 \otimes \cdots \otimes b^{(N-1)}
        \otimes f_i\left( b^{(N)}_{\lambda_N} \right),

    then we take the image as `b^{(0)} \otimes \cdots \otimes f_i\left(
    b^{(N)}_{\lambda_N}\right) \otimes b^{(N+1)}_{\lambda_{N+1}}`. Similarly
    we remove `b^{(N)}_{\lambda_{N}}` if we have `b_0 \otimes \cdots
    \otimes b^{(N-1)} \otimes b^{(N-1)}_{\lambda_{N-1}} \otimes
    b^{(N)}_{\lambda_N}`. Additionally if

    .. MATH::

        e_i\left( b^{(0)} \otimes \cdots \otimes b^{(N-1)} \otimes
        b^{(N)}_{\lambda_N} \right) = b^{(0)} \otimes \cdots \otimes
        b^{(N-1)} \otimes e_i\left( b^{(N)}_{\lambda_N} \right),

    then we consider this to be `0`.

    REFERENCES:

    .. [HK02] *Introduction to Quantum Groups and Crystal Bases.*
       Jin Hong and Seok-Jin Kang. 2002. Volume 42.
       Graduate Studies in Mathematics. American Mathematical Society.

    INPUT:

    - ``B`` -- A single or list of `U_q^{\prime}` perfect crystal(s) of
      level `l`
    - ``weight`` -- A weight in `\overline{P}_l^+`

    EXAMPLES::

        sage: B = KirillovReshetikhinCrystal(['A',2,1], 1,1)
        sage: L = RootSystem(['A',2,1]).weight_space()
        sage: C = KyotoPathModel(B, L.fundamental_weight(0))
        sage: mg = C.module_generators[0]; mg
        [[[3]]]
        sage: mg.f_string([0,1,2,2])
        [[[3]], [[3]], [[1]]]

    An example of type `A_5^{(2)}`::

        sage: B = KirillovReshetikhinCrystal(['A',5,2], 1,1)
        sage: L = RootSystem(['A',5,2]).weight_space()
        sage: C = KyotoPathModel(B, L.fundamental_weight(0))
        sage: mg = C.module_generators[0]; mg
        [[[-1]]]
        sage: mg.f_string([0,2,1,3])
        [[[-3]], [[2]], [[-1]]]
        sage: mg.f_string([0,2,3,1])
        [[[-3]], [[2]], [[-1]]]

    An example of type `D_3^{(2)}`::

        sage: B = KirillovReshetikhinCrystal(['D',3,2], 1,1)
        sage: L = RootSystem(['D',3,2]).weight_space()
        sage: C = KyotoPathModel(B, L.fundamental_weight(0))
        sage: mg = C.module_generators[0]; mg
        [[]]
        sage: mg.f_string([0,1,2,0])
        [[[0]], [[1]], []]

    An example using multiple crystals of the same level::

        sage: B1 = KirillovReshetikhinCrystal(['A',2,1], 1,1)
        sage: B2 = KirillovReshetikhinCrystal(['A',2,1], 2,1)
        sage: L = RootSystem(['A',2,1]).weight_space()
        sage: C = KyotoPathModel([B1, B2, B1], L.fundamental_weight(0))
        sage: mg = C.module_generators[0]; mg
        [[[3]]]
        sage: mg.f_string([0,1,2,2])
        [[[3]], [[1], [3]], [[3]]]
        sage: mg.f_string([0,1,2,2,2])
        sage: mg.f_string([0,1,2,2,1,0])
        [[[3]], [[2], [3]], [[1]], [[2]]]
        sage: mg.f_string([0,1,2,2,1,0,0,2])
        [[[3]], [[1], [2]], [[1]], [[3]], [[1], [3]]]
    """
    @staticmethod
    def __classcall_private__(cls, crystals, weight):
        """
        Normalize input to ensure a unique representation.

        EXAMPLES::

            sage: B = KirillovReshetikhinCrystal(['A',2,1], 1,1)
            sage: L = RootSystem(['A',2,1]).weight_space()
            sage: C = KyotoPathModel(B, L.fundamental_weight(0))
            sage: C2 = KyotoPathModel((B,), L.fundamental_weight(0))
            sage: C3 = KyotoPathModel([B], L.fundamental_weight(0))
            sage: C is C2 and C2 is C3
            True
        """
        if isinstance(crystals, list):
            crystals = tuple(crystals)
        elif not isinstance(crystals, tuple):
            crystals = (crystals,)

        if any(not B.is_perfect() for B in crystals):
            raise ValueError("all crystals must be perfect")
        level = crystals[0].level()
        if any(B.level() != level for B in crystals[1:]):
            raise ValueError("all crystals must have the same level")
        ct = crystals[0].cartan_type()
        if sum( ct.dual().c()[i] * weight.scalar(h) for i,h in
                enumerate(RootSystem(ct).weight_space().simple_coroots()) ) != level:
            raise ValueError( "%s is not a level %s weight"%(weight, level) )

        return super(KyotoPathModel, cls).__classcall__(cls, crystals, weight)

    def __init__(self, crystals, weight):
        """
        Initialize ``self``.

        EXAMPLES::

            sage: B = KirillovReshetikhinCrystal(['A',2,1], 1,1)
            sage: L = RootSystem(['A',2,1]).weight_space()
            sage: C = KyotoPathModel(B, L.fundamental_weight(0))
            sage: TestSuite(C).run() # long time
        """
        Parent.__init__(self, category=(HighestWeightCrystals(), InfiniteEnumeratedSets()))

        self._cartan_type = crystals[0].cartan_type()
        self.crystals = crystals # public for TensorProductOfCrystals
        self._weight = weight
        self._epsilon_dicts = [{b.Epsilon():b for b in B} for B in crystals]
        self._phi_dicts = [{b.Phi():b for b in B} for B in crystals]
        self.module_generators = (self.element_class(self, [self._phi_dicts[0][weight]]),)

    def _repr_(self):
        """
        Return a string representation of ``self``.

        EXAMPLES::

            sage: B = KirillovReshetikhinCrystal(['A',2,1], 1,1)
            sage: L = RootSystem(['A',2,1]).weight_space()
            sage: KyotoPathModel(B, L.fundamental_weight(0))
            Kyoto path realization of B(Lambda[0]) using [Kirillov-Reshetikhin crystal of type ['A', 2, 1] with (r,s)=(1,1)]
        """
        return "Kyoto path realization of B(%s) using %s"%(self._weight, list(self.crystals))

    class Element(TensorProductOfRegularCrystalsElement):
        """
        An element in the Kyoto path model.
        """
        # For simplicity (and safety), we use the regular crystals implementation
        def epsilon(self, i):
            r"""
            Return `\varepsilon_i` of ``self``.

            EXAMPLES::

                sage: B = KirillovReshetikhinCrystal(['A',2,1], 1,1)
                sage: L = RootSystem(['A',2,1]).weight_space()
                sage: C = KyotoPathModel(B, L.fundamental_weight(0))
                sage: mg = C.module_generators[0]
                sage: [mg.epsilon(i) for i in C.index_set()]
                [0, 0, 0]
                sage: elt = mg.f(0)
                sage: [elt.epsilon(i) for i in C.index_set()]
                [1, 0, 0]
                sage: elt = mg.f_string([0,1,2])
                sage: [elt.epsilon(i) for i in C.index_set()]
                [0, 0, 1]
                sage: elt = mg.f_string([0,1,2,2])
                sage: [elt.epsilon(i) for i in C.index_set()]
                [0, 0, 2]
            """
            x = self.e(i)
            eps = 0
            while x is not None:
                x = x.e(i)
                eps = eps + 1
            return eps

        def phi(self, i):
            r"""
            Return `\varphi_i` of ``self``.

            EXAMPLES::

                sage: B = KirillovReshetikhinCrystal(['A',2,1], 1,1)
                sage: L = RootSystem(['A',2,1]).weight_space()
                sage: C = KyotoPathModel(B, L.fundamental_weight(0))
                sage: mg = C.module_generators[0]
                sage: [mg.phi(i) for i in C.index_set()]
                [1, 0, 0]
                sage: elt = mg.f(0)
                sage: [elt.phi(i) for i in C.index_set()]
                [0, 1, 1]
                sage: elt = mg.f_string([0,1])
                sage: [elt.phi(i) for i in C.index_set()]
                [0, 0, 2]
            """
            x = self.f(i)
            phi = 0
            while x is not None:
                x = x.f(i)
                phi = phi + 1
            return phi

        def e(self, i):
            """
            Return the action of `e_i` on ``self``.

            EXAMPLES::

                sage: B = KirillovReshetikhinCrystal(['A',2,1], 1,1)
                sage: L = RootSystem(['A',2,1]).weight_space()
                sage: C = KyotoPathModel(B, L.fundamental_weight(0))
                sage: mg = C.module_generators[0]
                sage: all(mg.e(i) is None for i in C.index_set())
                True
                sage: mg.f(0).e(0) == mg
                True
            """
            position = self.positions_of_unmatched_plus(i)
            if position == []:
                return None
            k = position[0]
            if k == len(self)-1:
                return None
            crystal = self[k].e(i)
            if k == len(self)-2 and crystal.Epsilon() == self._list[-1].Phi():
                l = self._list[:-1]
                l[-1] = crystal
                return self.__class__(self.parent(), l)
            return self.set_index(k, crystal)

        def f(self, i):
            """
            Return the action of `f_i` on ``self``.

            EXAMPLES::

                sage: B = KirillovReshetikhinCrystal(['A',2,1], 1,1)
                sage: L = RootSystem(['A',2,1]).weight_space()
                sage: C = KyotoPathModel(B, L.fundamental_weight(0))
                sage: mg = C.module_generators[0]
                sage: mg.f(2)
                sage: mg.f(0)
                [[[1]], [[2]]]
                sage: mg.f_string([0,1,2])
                [[[2]], [[3]], [[1]]]
            """
            position = self.positions_of_unmatched_minus(i)
            if position == []:
                return None
            k = position[len(position)-1]
            if k == len(self)-1:
                l = self._list[:]
                k = len(l) % len(self.parent().crystals)
                l.append(self.parent()._phi_dicts[k][ l[-1].Epsilon() ])
                l[-2] = l[-2].f(i)
                return self.__class__(self.parent(), l)
            return self.set_index(k, self[k].f(i))

