import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def fit_ellipse_direct_least_squares(x, y):
    """
    Direct least squares fitting of ellipses (Fitzgibbon, Pilu, Fisher 1999).
    Returns conic parameters (a,b,c,d,e,f) of:
        a x^2 + b x y + c y^2 + d x + e y + f = 0
    """
    x = x[:, None]
    y = y[:, None]

    # Design matrix
    D = np.hstack([x * x, x * y, y * y, x, y, np.ones_like(x)])

    # Scatter matrix
    S = D.T @ D

    # Constraint matrix (enforces 4ac - b^2 = 1 for ellipse)
    C = np.zeros((6, 6))
    C[0, 2] = C[2, 0] = 2
    C[1, 1] = -1

    # Solve generalized eigenvalue problem: S a = λ C a
    # We solve inv(S)C a = (1/λ) a
    try:
        eigvals, eigvecs = np.linalg.eig(np.linalg.inv(S) @ C)
    except np.linalg.LinAlgError:
        raise ValueError("Singular matrix encountered in ellipse fit. Check your points distribution.")

    # Find the eigenvector that represents an ellipse: 4ac - b^2 > 0
    cond = []
    for i in range(eigvecs.shape[1]):
        a, b, c, d, e, f = eigvecs[:, i]
        cond.append(4 * a * c - b * b)

    cond = np.array(cond)
    idx = np.where(cond > 0)[0]
    if len(idx) == 0:
        raise ValueError("No valid ellipse found. Your points may not form an ellipse-like shape.")

    # Choose the ellipse solution (usually the first valid one)
    p = np.real(eigvecs[:, idx[0]])
    return p / np.linalg.norm(p)


def ellipse_parameters(a, b, c, d, e, f):
    """
    Convert conic parameters to center, axes, rotation angle.
    """
    # Denominator
    den = b * b - 4 * a * c
    if abs(den) < 1e-12:
        raise ValueError("Degenerate conic (denominator too small).")

    # Center (x0, y0)
    x0 = (2 * c * d - b * e) / den
    y0 = (2 * a * e - b * d) / den

    # Evaluate f at the center
    F0 = f + a * x0 * x0 + b * x0 * y0 + c * y0 * y0 + d * x0 + e * y0

    # Rotation
    theta = 0.5 * np.arctan2(b, a - c)

    # Compute axes lengths
    # Using the eigenvalues of the quadratic form
    term = np.sqrt((a - c) ** 2 + b * b)
    lam1 = a + c + term
    lam2 = a + c - term

    # Ensure correct sign (we want -F0/lam > 0)
    # If F0 is positive, flip signs of all coefficients
    if F0 > 0:
        a, b, c, d, e, f = -a, -b, -c, -d, -e, -f
        den = b * b - 4 * a * c
        x0 = (2 * c * d - b * e) / den
        y0 = (2 * a * e - b * d) / den
        F0 = f + a * x0 * x0 + b * x0 * y0 + c * y0 * y0 + d * x0 + e * y0
        term = np.sqrt((a - c) ** 2 + b * b)
        lam1 = a + c + term
        lam2 = a + c - term
        theta = 0.5 * np.arctan2(b, a - c)

    # semi-axes
    if lam1 == 0 or lam2 == 0:
        raise ValueError("Degenerate ellipse (zero eigenvalue).")

    axis1 = np.sqrt(-2 * F0 / lam1)
    axis2 = np.sqrt(-2 * F0 / lam2)

    # Major/minor ordering
    major = max(axis1, axis2)
    minor = min(axis1, axis2)

    return x0, y0, major, minor, theta


def ellipse_points(x0, y0, a_axis, b_axis, theta, n=400):
    t = np.linspace(0, 2 * np.pi, n)
    ct, st = np.cos(t), np.sin(t)
    x = x0 + a_axis * ct * np.cos(theta) - b_axis * st * np.sin(theta)
    y = y0 + a_axis * ct * np.sin(theta) + b_axis * st * np.cos(theta)
    return x, y


def main():
    path = r"C:\Users\ozhan\Desktop\deneme.xlsx"
    sheet = "Sheet2"

    df = pd.read_excel(path, sheet_name=sheet)

    # Your columns:
    angle = df["ang"].to_numpy(dtype=float)
    p_values = df["p-val"].to_numpy(dtype=float)

    # Convert polar to cartesian (same as your code)
    x = p_values * 50 * np.cos(np.radians(angle))
    y = p_values * 50 * np.sin(np.radians(angle))

    # Fit ellipse
    a, b, c, d, e, f = fit_ellipse_direct_least_squares(x, y)

    # Report parameters
    print("\nConic form:")
    print(f"  {a:.6g} x^2 + {b:.6g} xy + {c:.6g} y^2 + {d:.6g} x + {e:.6g} y + {f:.6g} = 0")

    x0, y0, major, minor, theta = ellipse_parameters(a, b, c, d, e, f)
    print("\nEllipse parameters:")
    print(f"  center = ({x0:.6g}, {y0:.6g})")
    print(f"  semi-major axis = {major:.6g}")
    print(f"  semi-minor axis = {minor:.6g}")
    print(f"  rotation (deg)  = {np.degrees(theta):.6g}")

    # Plot
    xe, ye = ellipse_points(x0, y0, major, minor, theta)

    plt.figure()
    plt.scatter(x, y, s=15, label="data points")
    plt.plot(xe, ye, label="fitted ellipse")
    plt.axis("equal")
    plt.title("Best-fit ellipse")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
