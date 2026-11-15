import numpy as np

# ייבוא המחלקות מהקבצים שלך
from gradient_descent_1d import GradientDescent1D
from gradient_descent_nd import GradientDescentND
from stochastic_gradient_descent import StochasticGradientDescent
from linear_regression import LinearRegression


def print_result(test_name, passed, expected, actual):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"--- {test_name} ---")
    print(f"Status: {status}")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")
    print("-" * 40)


def test_1d_example():
    # מודל הדוגמה ממסמך המטלה (עמוד 6)
    class ScaleModel:
        def loss(self, parameters, x_data, y_data):
            p = float(parameters)
            return float(np.mean((p * x_data - y_data) ** 2))

        def gradients(self, parameters, x_data, y_data):
            p = float(parameters)
            return float(2 * np.mean((p * x_data - y_data) * x_data))

    x_data = np.array([1, 2, 3], dtype=float)
    y_data = np.array([3, 6, 9], dtype=float)
    optimizer = GradientDescentND(
        model, x_data, y_data, learning_rate=0.01, tolerance=1e-8
    )
    param, loss = optimizer.minimize(0)

    # הבדיקה
    param_passed = np.isclose(param, 3.0, atol=1e-2)
    loss_passed = loss < 0.01
    print_result(
        "Test 1: 1D Gradient Descent (PDF Example)",
        param_passed and loss_passed,
        "Param ~ 3.0, Loss ~ 0.0",
        f"Param={param:.4f}, Loss={loss:.4f}",
    )


def test_nd_example():
    # דוגמת ה-ND ממסמך המטלה (עמוד 8)
    x_data = np.array([-2, -1, 0, 1, 2, 3], dtype=float)
    y_data = np.array([-3.1, -0.8, 1.1, 2.9, 5.2, 6.9], dtype=float)
    model = LinearRegression()
    optimizer = GradientDescentND(model, x_data, y_data, learning_rate=0.01)

    params, loss = optimizer.minimize(np.array([0, 0], dtype=float))

    expected_params = np.array([1.9942857, 1.0361905])
    params_passed = np.allclose(params, expected_params, atol=1e-5)
    loss_passed = loss < 0.02
    print_result(
        "Test 2: ND Batch Gradient Descent (PDF Example)",
        params_passed and loss_passed,
        f"Params ~ {expected_params}, Loss < 0.02",
        f"Params={params}, Loss={loss:.4f}",
    )


def test_sgd_example():
    # דוגמת ה-SGD ממסמך המטלה (עמוד 14)
    x_data = np.array([-2, -1, 0, 1, 2, 3], dtype=float)
    y_data = np.array([-3.1, -0.8, 1.1, 2.9, 5.2, 6.9], dtype=float)
    model = LinearRegression()

    params, loss = model.fit(
        x_data, y_data, learning_rate=0.01, max_iterations=1000, tolerance=1e-8
    )

    expected_params = np.array([1.98968112, 1.03501585])
    params_passed = np.allclose(params, expected_params, atol=1e-5)
    loss_passed = loss < 0.02
    print_result(
        "Test 3: Stochastic Gradient Descent (PDF Example)",
        params_passed and loss_passed,
        f"Params ~ {expected_params}, Loss < 0.02",
        f"Params={params}, Loss={loss:.4f}",
    )


def test_zero_learning_rate():
    x_data = np.array([1, 2, 3], dtype=float)
    y_data = np.array([2, 4, 6], dtype=float)
    model = LinearRegression()

    # אתחול עם פרמטרים שגויים בכוונה
    start_params = np.array([10.0, 10.0])
    model.parameters = start_params
    optimizer = StochasticGradientDescent(model, x_data, y_data, learning_rate=0.0)

    params, _ = optimizer.minimize(start_params)
    passed = np.allclose(params, start_params)
    print_result(
        "Test 4: Edge Case - Zero Learning Rate", passed, f"{start_params}", f"{params}"
    )


def test_zero_iterations():
    x_data = np.array([1, 2, 3], dtype=float)
    y_data = np.array([2, 4, 6], dtype=float)
    model = LinearRegression()

    start_params = np.array([5.0, 5.0])
    optimizer = GradientDescentND(
        model, x_data, y_data, learning_rate=0.1, max_iterations=0
    )

    params, _ = optimizer.minimize(start_params)
    passed = np.allclose(params, start_params)
    print_result(
        "Test 5: Edge Case - Zero Iterations", passed, f"{start_params}", f"{params}"
    )


def test_perfect_fit():
    # נתונים עם התאמה מושלמת לקו y = 2x + 0
    x_data = np.array([1, 2, 3, 4], dtype=float)
    y_data = np.array([2, 4, 6, 8], dtype=float)
    model = LinearRegression()

    params, loss = model.fit(x_data, y_data, learning_rate=0.05)

    expected_params = np.array([2.0, 0.0])
    params_passed = np.allclose(params, expected_params, atol=1e-5)
    loss_passed = np.isclose(loss, 0.0, atol=1e-10)
    print_result(
        "Test 6: Edge Case - Perfect Fit Data",
        params_passed and loss_passed,
        f"Params=[2.0, 0.0], Loss=0.0",
        f"Params={params}, Loss={loss:.10f}",
    )


def test_single_data_point():
    # נקודת נתונים בודדת
    x_data = [1]  # רשימת int, בודק גם את ההמרה
    y_data = [5]
    model = LinearRegression()

    # קו שעובר בנקודה (1,5) יכול להיות y = 5x + 0 (או אינסוף אפשרויות אחרות, אבל ה-loss ירד)
    params, loss = model.fit(x_data, y_data, learning_rate=0.1)

    # הבדיקה העיקרית היא שהקוד לא קורס מחלוקה באפס או שגיאת Slicing
    passed = loss < 1.0  # ה-loss אמור לרדת משמעותית
    print_result(
        "Test 7: Edge Case - Single Data Point (List of ints)",
        passed,
        "Run without errors, Loss < 1.0",
        f"Loss={loss:.4f}",
    )


if __name__ == "__main__":
    print("Starting Homework 4 Tests...\n")
    test_1d_example()
    test_nd_example()
    test_sgd_example()
    test_zero_learning_rate()
    test_zero_iterations()
    test_perfect_fit()
    test_single_data_point()
    print("All tests completed.")
