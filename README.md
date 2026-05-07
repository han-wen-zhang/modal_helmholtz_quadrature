# modal_helmholtz_quadrature

Generalized Gaussian Quadratures for evaluating the modal Helmholtz Green's function.

This repository contains 18 generalized Gaussian quadrature (GGQ) tables used in

> H. Zhang, *Fast Evaluation of the Azimuthal Fourier Modes of the 3D Helmholtz Green's Function and Their Derivatives*, 2026.

The tables are designed for the near-singular integrand on the steepest-descent contour $\gamma_1$ that arises in the contour-deformation algorithm for evaluating the azimuthal Fourier modes $G_{k,m}(r,z,r',z')$ of the three-dimensional Helmholtz Green's function and their derivatives.

## What the tables integrate

Each table is a quadrature on $[0,1]$ that integrates the five families

$$\int_0^1 \frac{P_n(t)}{\sqrt{t^2 - 2 i b_m}} dt \qquad \int_0^1 \frac{P_n(t)}{\sqrt{t^2 - 2 i b_m} (t^2 - i b_m)} dt \qquad \int_0^1 \frac{P_n(t)}{\sqrt{t^2 - 2 i b_m} (t^2 - i b_m)^2} dt$$

$$\int_0^1 \frac{P_n(t) t^2 \sqrt{t^2 - 2 i b_m}}{t^2 - i b_m} dt \qquad \int_0^1 \frac{P_n(t) t^2 \sqrt{t^2 - 2 i b_m}}{(t^2 - i b_m)^2} dt$$

exactly for all polynomials $P_n$ of degree $n = 0, 1, \ldots, 63$. Here $b_m \ge 0$ is the near-singular parameter (denoted $\beta_-$ in the paper).

## Coverage

The 18 tables cover dyadic ranges of $b_m$:

| table | $b_m$ range         | nodes |
|------:|---------------------|------:|
| 1     | [2^-5,  2^-1]       |    66 |
| 2     | [2^-10, 2^-5]       |    76 |
| 3     | [2^-15, 2^-10]      |    78 |
| 4     | [2^-20, 2^-15]      |    78 |
| 5     | [2^-25, 2^-20]      |    79 |
| 6     | [2^-30, 2^-25]      |    79 |
| 7     | [2^-35, 2^-30]      |    79 |
| 8     | [2^-40, 2^-35]      |    78 |
| 9     | [2^-45, 2^-40]      |    78 |
| 10    | [2^-50, 2^-45]      |    78 |
| 11    | [2^-55, 2^-50]      |   114 |
| 12    | [2^-60, 2^-55]      |   116 |
| 13    | [2^-65, 2^-60]      |    75 |
| 14    | [2^-70, 2^-65]      |   111 |
| 15    | [2^-75, 2^-70]      |   116 |
| 16    | [2^-80, 2^-75]      |   110 |
| 17    | [2^-85, 2^-80]      |   110 |
| 18    | [2^-90, 2^-85]      |   118 |

In the well-separated regime $b_m > 2^{-1}$, the integrand is smooth and a standard Gauss-Legendre rule on $[0,1]$ suffices; that case is not covered here.

## Files

- `modal_helmholtz_quadrature.f` — Fortran 77 source. Contains 18 subroutines `load_quad1` through `load_quad18`. Each is called as
  ```fortran
        call load_quadk(xlist, wlist, nn)
  ```
  where `xlist` and `wlist` are `real*8` arrays of length at least 118 supplied by the caller, and `nn` returns the actual node count.

- `quadrature_tables/quadNN.txt` (for `NN = 01,...,18`) — plain-text per-table files. Each contains a header followed by lines `x_i  w_i`.

## Usage notes

The tables are defined on $[0,1]$. To integrate over $[0, \tau]$ for any $\tau > 0$, rescale: replace $x_i \mapsto \tau x_i$ and $w_i \mapsto \tau w_i$.

## Construction

The tables were constructed using the nonlinear optimization procedure of

> J. Bremer, Z. Gimbutas, and V. Rokhlin, *A nonlinear optimization procedure for generalized Gaussian quadratures*, SIAM J. Sci. Comput. **32** (2010), 1761-1788.

## Citation

If you use these tables, please cite

> H. Zhang, *Fast Evaluation of the Azimuthal Fourier Modes of the 3D Helmholtz Green's Function and Their Derivatives*, 2026.
