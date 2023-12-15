from scipy.optimize import minimize
import numpy as np

c1 = np.array((0.262617004746481000, 0.260884896827677000, 0.256617389979587000))
c2 = np.array((0.000931334226877499, 0.001704349026635550, 0.003630941188077970))
c3 = np.array((1.54, 0.30, 0.37))


def equations(z: np.ndarray) -> np.ndarray:
    # sigma_SU, sigma_MU, sigma_R = z

    inner1 = -z.sum()
    inner2 = np.exp(45*inner1)
    inner3 = c1 * z * inner2/(inner1 + c2)
    f = c3 - inner3/(inner3.sum() + 0.719582172729324 * inner2)
    return f


def lstsq_cost(z: np.ndarray) -> float:
    f = equations(z)
    return f.dot(f)
    pass

def regression_tests() -> None:
    expected = (1.48037098, 0.29461646, 0.33099203)
    actual = equations(np.array((8.13e-5, 2.02e-5, 3.84e-4)))
    assert np.allclose(expected, actual)

    expected = (0.93253452, 0.21240985, 0.06805596)
    actual = equations(np.array((-0.49717498, -0.00991807,  0.50892057)))
    assert np.allclose(expected, actual)


def optimize() -> None:
    result = minimize(
        fun=lstsq_cost, method='powell',
        x0=(0, 0, 0), tol=1e-9,
    )
    assert result.success, result.message
    np.set_printoptions(precision=2)
    print('Function at roots:', equations(result.x))
    np.set_printoptions(precision=20)
    print('Roots:', result.x)


if __name__ == '__main__':
    #regression_tests()
    optimize()
    pass