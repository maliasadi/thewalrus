# Copyright 2019 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Hermite Multidimensional Python interface
"""
from itertools import product
from typing import Tuple, Generator
from functools import lru_cache
from numba import jit
from numba.cpython.unsafe.tuple import tuple_setitem
import numpy as np

from .libwalrus import hermite_multidimensional as hm
from .libwalrus import hermite_multidimensional_real as hmr

from .libwalrus import renorm_hermite_multidimensional as rhm
from .libwalrus import renorm_hermite_multidimensional_real as rhmr

from ._hafnian import input_validation


# pylint: disable=too-many-arguments
def hermite_multidimensional(
    R, cutoff, y=None, renorm=False, make_tensor=True, modified=False, rtol=1e-05, atol=1e-08
):
    r"""Returns the multidimensional Hermite polynomials :math:`H_k^{(R)}(y)`.

    Here :math:`R` is an :math:`n \times n` square matrix, and
    :math:`y` is an :math:`n` dimensional vector. The polynomials are
    parametrized by the multi-index :math:`k=(k_0,k_1,\ldots,k_{n-1})`,
    and are calculated for all values :math:`0 \leq k_j < \text{cutoff}`,
    thus a tensor of dimensions :math:`\text{cutoff}^n` is returned.

    This tensor can either be flattened into a vector or returned as an actual
    tensor with :math:`n` indices.

    .. note::

        Note that if :math:`R = (1)` then :math:`H_k^{(R)}(y)`
        are precisely the well known **probabilists' Hermite polynomials** :math:`He_k(y)`,
        and if :math:`R = (2)` then :math:`H_k^{(R)}(y)` are precisely the well known
        **physicists' Hermite polynomials** :math:`H_k(y)`.

    Args:
        R (array): square matrix parametrizing the Hermite polynomial family
        cutoff (int): maximum size of the subindices in the Hermite polynomial
        y (array): vector argument of the Hermite polynomial
        renorm (bool): If ``True``, normalizes the returned multidimensional Hermite
            polynomials such that :math:`H_k^{(R)}(y)/\prod_i k_i!`
        make_tensor (bool): If ``False``, returns a flattened one dimensional array
            containing the values of the polynomial
        modified (bool): whether to return the modified multidimensional Hermite polynomials or the standard ones
        rtol (float): the relative tolerance parameter used in ``np.allclose``
        atol (float): the absolute tolerance parameter used in ``np.allclose``
    Returns:
        (array): the multidimensional Hermite polynomials
    """

    input_validation(R, atol=atol, rtol=rtol)
    n, _ = R.shape

    if (modified is False) and (y is not None):
        m = y.shape[0]
        if m == n:
            ym = R @ y
            return hermite_multidimensional(
                R, cutoff, y=ym, renorm=renorm, make_tensor=make_tensor, modified=True
            )

    if y is None:
        y = np.zeros([n], dtype=complex)

    m = y.shape[0]
    if m != n:
        raise ValueError("The matrix R and vector y have incompatible dimensions")

    Rt = np.real_if_close(R)
    yt = np.real_if_close(y)

    if Rt.dtype == np.float and yt.dtype == np.float:
        if renorm:
            values = np.array(rhmr(Rt, yt, cutoff))
        else:
            values = np.array(hmr(Rt, yt, cutoff))
    else:
        if renorm:
            values = np.array(rhm(np.complex128(R), np.complex128(y), cutoff))
        else:
            values = np.array(hm(np.complex128(R), np.complex128(y), cutoff))

    if make_tensor:
        shape = cutoff * np.ones([n], dtype=int)
        values = np.reshape(values, shape)

    return values


# pylint: disable=too-many-arguments
def hafnian_batched(A, cutoff, mu=None, rtol=1e-05, atol=1e-08, renorm=False, make_tensor=True):
    r"""Calculates the hafnian of :func:`reduction(A, k) <hafnian.reduction>`
    for all possible values of vector ``k`` below the specified cutoff.

    Here,

    * :math:`A` is am :math:`n\times n` square matrix
    * :math:`k` is a vector of (non-negative) integers with the same dimensions as :math:`A`,
      i.e., :math:`k = (k_0,k_1,\ldots,k_{n-1})`, and where :math:`0 \leq k_j < \texttt{cutoff}`.

    The function :func:`~.hafnian_repeated` can be used to calculate the reduced hafnian
    for a *specific* value of :math:`k`; see the documentation for more information.

    .. note::

        If ``mu`` is not ``None``, this function instead returns
        ``hafnian(np.fill_diagonal(reduction(A, k), reduction(mu, k)), loop=True)``.
        This calculation can only be performed if the matrix :math:`A` is invertible.

    Args:
        A (array): a square, symmetric :math:`N\times N` array.
        cutoff (int): maximum size of the subindices in the Hermite polynomial
        mu (array): a vector of length :math:`N` representing the vector of means/displacement
        renorm (bool): If ``True``, the returned hafnians are *normalized*, that is,
            :math:`haf(reduction(A, k))/\ \sqrt{prod_i k_i!}`
            (or :math:`lhaf(fill\_diagonal(reduction(A, k),reduction(mu, k)))` if
            ``mu`` is not None)
        make_tensor: If ``False``, returns a flattened one dimensional array instead
            of a tensor with the values of the hafnians.
        rtol (float): the relative tolerance parameter used in ``np.allclose``.
        atol (float): the absolute tolerance parameter used in ``np.allclose``.
    Returns:
        (array): the values of the hafnians for each value of :math:`k` up to the cutoff
    """
    input_validation(A, atol=atol, rtol=rtol)
    n, _ = A.shape

    if mu is None:
        mu = np.zeros([n], dtype=complex)

    return hermite_multidimensional(
        -A, cutoff, y=mu, renorm=renorm, make_tensor=make_tensor, modified=True
    )


# Note the minus signs in the arguments. Those are intentional and are due to the fact that Dodonov et al. in PRA 50, 813 (1994) use (p,q) ordering instead of (q,p) ordering
@lru_cache()
def partition(photons, cutoff):
    r"""Returns a list of all the ways of putting n photons into modes that have a given cutoff dimension.
    This function is useful to fill the amplitude array by multiplets of constant photon number.

    Args:
        photons (int): number of photons in the multiplet
        cutoff (tuple[int]): the cutoff of each mode
    """
    return [comb for comb in product(*(range(min(photons, i - 1) + 1) for i in cutoff)) if sum(comb) == photons]


@jit(nopython=True)
def dec(tup: Tuple[int], i: int) -> Tuple[int, ...]:  # pragma: no cover
    r"""returns a copy of the given tuple of integers where the ith element has been decreased by 1

    Args:
        tup (Tuple[int]): the given tuple
        i (int): the position of the element to be decreased

    Returns:
        Tuple[int,...]: the new tuple with the decrease on i-th element by 1
    """
    copy = tup[:]
    return tuple_setitem(copy, i, tup[i] - 1)


@jit(nopython=True)
def remove(
    pattern: Tuple[int, ...]
) -> Generator[Tuple[int, Tuple[int, ...]], None, None]:  # pragma: no cover
    r"""returns a generator for all the possible ways to decrease elements of the given tuple by 1

    Args:
        pattern (Tuple[int, ...]): the pattern given to be decreased

    Returns:
        Generator[Tuple[int, Tuple[int, ...]], None, None]: the generator
    """
    for p, n in enumerate(pattern):
        if n > 0:
            yield p, dec(pattern, p)


SQRT = np.sqrt(np.arange(1000))  # saving the time to recompute square roots


def hermite_multidimensional_numba(R, cutoff, y, C=1, dtype=np.complex128):
    # pylint: disable=too-many-arguments
    r"""Returns the renormalized multidimensional Hermite polynomials :math:`C*H_k^{(R)}(y)`.

    Here :math:`R` is an :math:`n \times n` square matrix, and
    :math:`y` is an :math:`n` dimensional vector. The polynomials are
    parametrized by the multi-index :math:`k=(k_0,k_1,\ldots,k_{n-1})`,
    and are calculated for all values :math:`0 \leq k_j < \text{cutoff}`,

    Args:
        R (array[complex]): square matrix parametrizing the Hermite polynomial
        cutoff (int or list[int]): maximum sizes of the subindices in the Hermite polynomial
        y (vector[complex]): vector argument of the Hermite polynomial
        C (complex): first value of the Hermite polynomials, the default value is 1
        dtype (data type): Specifies the data type used for the calculation

    Returns:
        array[data type]: the multidimensional Hermite polynomials
    """
    n, _ = R.shape
    if y.shape[0] != n:
        raise ValueError(f"The matrix R and vector y have incompatible dimensions ({R.shape} vs {y.shape})")
    num_indices = len(y)
    if isinstance(cutoff, int):
        cutoff = tuple([cutoff] * num_indices)
    cutoff = tuple(cutoff)
    array = np.zeros(cutoff, dtype=dtype)
    array[(0,) * num_indices] = C
    for photons in range(1, sum(cutoff) - num_indices + 1):
        for idx in partition(photons, cutoff):
            array = fill_hermite_multidimensional_numba_loop(array, idx, R, y)
    return array


@jit(nopython=True)
def fill_hermite_multidimensional_numba_loop(array, idx, R, y):  # pragma: no cover
    r"""Calculates the renormalized Hermite multidimensional polynomial for a given index.

    Args:
        array (array[data type]): the multidimensional Hermite polynomials
        idx (tuple): index of the gradients to be filled
        R (array[complex]): square matrix parametrizing the Hermite polynomial
        y (vector[complex]): vector argument of the Hermite polynomial

    Returns:
        array[data type]: the hermit multidimensional polynomial for a given index
    """
    i = 0
    for i, val in enumerate(idx):
        if val > 0:
            break
    ki = dec(idx, i)
    u = y[i] * array[ki]
    for l, kl in remove(ki):
        u -= SQRT[ki[l]] * R[i, l] * array[kl]
    array[idx] = u / SQRT[idx[i]]
    return array


def grad_hermite_multidimensional_numba(array, R, cutoff, y, C=1, dtype=np.complex128):
    # pylint: disable=too-many-arguments
    r"""Calculates the gradients of the renormalized multidimensional Hermite polynomials :math:`C*H_k^{(R)}(y)` with respect to its parameters :math:`C`, :math:`y` and :math:`R`.

    Args:
        array (array): the multidimensional Hermite polynomials
        R (array[complex]): square matrix parametrizing the Hermite polynomial
        cutoff (int or list[int]): maximum sizes of the subindices in the Hermite polynomial
        y (vector[complex]): vector argument of the Hermite polynomial
        C (complex): first value of the Hermite polynomials
        dtype (data type): Specifies the data type used for the calculation

    Returns:
        array[data type], array[data type], array[data type]: the gradients of the multidimensional Hermite polynomials with respect to C, R and y
    """
    n, _ = R.shape
    if y.shape[0] != n:
        raise ValueError(f"The matrix R and vector y have incompatible dimensions ({R.shape} vs {y.shape})")
    num_indices = len(y)
    if isinstance(cutoff, int):
        cutoff = tuple([cutoff] * num_indices)
    cutoff = tuple(cutoff)
    dG_dC = array / C
    dG_dR = np.zeros_like(array, dtype=dtype)
    dG_dy = np.zeros_like(array, dtype=dtype)
    for photons in range(1, sum(cutoff) - num_indices + 1):
        for idx in partition(photons, cutoff):
            dG_dR, dG_dy = fill_grad_hermite_multidimensional_numba_loop(dG_dR, dG_dy, array, idx, R, y)
    return dG_dC, dG_dR, dG_dy


@jit(nopython=True)
def fill_grad_hermite_multidimensional_numba_loop(
    dG_dR, dG_dy, array, idx, R, y
):  # pragma: no cover
    # pylint: disable=too-many-arguments
    r"""Calculates the gradients of the renormalized multidimensional Hermite polynomials for a given index.

    Args:
        dG_dR (array[data type]): array representing the gradients with respect to R
        dG_dy (array[data type]): array representing the gradients with respect to y
        array (array[data type]): the multidimensional Hermite polynomials
        idx (tuple): index of the gradients to be filled
        R (array[complex]): square matrix parametrizing the Hermite polynomial
        y (vector[complex]): vector argument of the Hermite polynomial

    Returns:
        array[data type], array[data type]: the gradients of the multidimensional Hermite polynomials with respect to R and y for a given index
    """
    i = 0
    for i, val in enumerate(idx):
        if val > 0:
            break
    ki = dec(idx, i)
    dy = y[i] * dG_dy[ki] + array[ki]
    dR = y[i] * dG_dR[ki]
    for l, kl in remove(ki):
        dy -= SQRT[ki[l]] * dG_dy[kl] * R[i, l]
        dR -= SQRT[ki[l]] * (R[i, l] * dG_dR[kl] + array[kl])
    dG_dR[idx] = dR / SQRT[idx[i]]
    dG_dy[idx] = dy / SQRT[idx[i]]
    return dG_dR, dG_dy
