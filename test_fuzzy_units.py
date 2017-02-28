
from hypothesis import given, strategies as st, assume
from math import isclose
from unittest import TestCase

from fuzzy import functions as fun

class Test_Functions(TestCase):
    @given(st.floats(allow_nan=False, allow_infinity=False))
    def test_noop(self, x):
        f = fun.noop()
        assert f(x) == x

    @given(st.floats(allow_nan=False, allow_infinity=False))
    def test_inv(self, x):
        assume(0 <= x <= 1)
        f = fun.inv(fun.noop())
        assert isclose(f(f(x)), x, abs_tol=1e-16)

    @given(st.floats(allow_nan=False, allow_infinity=False), 
           st.floats(allow_nan=False, allow_infinity=False))
    def test_constant(self, c, r):
        f = fun.constant(c)
        assert f(r) == c


    @given(st.floats(min_value=0, max_value=1),
           st.floats(min_value=0, max_value=1),
           st.floats(allow_nan=False))
    def test_alpha(self, lower, upper, x):
        assume(lower < upper)
        f = fun.alpha(lower, upper, fun.noop())
        if x <= lower:
            assert f(x) == lower
        elif x >= upper:
            assert f(x) == upper
        else:
            assert f(x) == x

    @given(st.floats(), 
           st.floats(min_value=0, max_value=1),
           st.floats(min_value=0, max_value=1),
           st.floats(),

          )
    def test_singleton(self, p, non_p_m, p_m, x):
        assume(0 <= non_p_m <= 1)
        assume(0 <= p_m <= 1)
        f = fun.singleton(p, non_p_m, p_m)
        assert f(x) == (p_m if x == p else non_p_m)
    
    
    @given(st.floats(allow_nan=False),
          st.floats(allow_nan=False),
          st.floats(allow_nan=False))
    def test_linear(self, m, b, x):
        f = fun.linear(m, b)
        assert 0 <= f(x) <= 1