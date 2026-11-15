import numpy as np
from stochastic_gradient_descent import StochasticGradientDescent


class LinearRegression:
    """
    A linear regression model trained using stochastic gradient descent.

    This class represents a line equation of the form y = mx + b. It provides
    methods to predict outputs, compute mean squared error (MSE), and compute
    the analytic gradients for the slope (m) and intercept (b).
    """

    def __init__(self, initial_parameters=None):
        """
        Initializes the linear regression model.

        Sets the starting parameters (slope and intercept). If no initial
        parameters are provided, it defaults to [0, 0].

        Args:
            initial_parameters (array-like, optional): The starting values for
                [slope, intercept]. Defaults to None.
        """
        if initial_parameters is None:
            self.parameters = np.array([0, 0], dtype=float)
        else:
            self.parameters = np.array(initial_parameters, dtype=float)
        self.history = []

    def predict(self, x, parameters=None):
        """
        Computes predictions for the given inputs based on the line equation.

        Args:
            x (array-like): The input data.
            parameters (array-like, optional): The parameters [m, b] to use.
                If None, uses self.parameters. Defaults to None.

        Returns:
            np.ndarray: The predicted values.
        """
        if parameters is None:
            parameters = self.parameters
        float_params = np.array(parameters, dtype=float)
        m, b = float_params[0], float_params[1]
        x_float_np_arr = np.array(x, dtype=float)
        return m * x_float_np_arr + b

    def loss(self, parameters, x_data, y_data):
        """
        Computes the Mean Squared Error (MSE) loss.

        Args:
            parameters (array-like): The parameter vector [m, b].
            x_data (array-like): The training input data.
            y_data (array-like): The training target data.

        Returns:
            float: The computed mean squared error.
        """
        x_data_floats, y_data_floats = np.array(x_data, dtype=float), np.array(
            y_data, dtype=float
        )
        predictions = self.predict(x_data_floats, parameters)
        error = predictions - y_data_floats
        return float(np.mean(error**2))

    def gradients(self, parameters, x_data, y_data):
        """
        Computes the analytic gradients of the MSE loss with respect to m and b.

        Args:
            parameters (array-like): The parameter vector [m, b].
            x_data (array-like): The training input data.
            y_data (array-like): The training target data.

        Returns:
            np.ndarray: An array containing the partial derivatives [dm, db].
        """
        float_params = np.array(parameters, dtype=float)
        x_data_floats = np.array(x_data, dtype=float)
        y_data_floats = np.array(y_data, dtype=float)
        prediction = self.predict(x_data_floats, float_params)
        errors = prediction - y_data_floats
        n = len(x_data_floats)
        dL_to_dm = (2 / n) * np.sum(errors * x_data_floats)
        dL_to_db = (2 / n) * np.sum(errors)
        return np.array([dL_to_dm, dL_to_db], dtype=float)

    def fit(
        self,
        x_data,
        y_data,
        learning_rate=0.05,
        max_iterations=1000,
        tolerance=1e-8,
    ):
        """
        Trains the linear regression model using Stochastic Gradient Descent.

        Args:
            x_data (array-like): The full training input data.
            y_data (array-like): The full training target data.
            learning_rate (float, optional): Step size for SGD. Defaults to 0.05.
            max_iterations (int, optional): Maximum epochs for SGD. Defaults to 1000.
            tolerance (float, optional): Early stopping threshold. Defaults to 1e-8.

        Returns:
            tuple: The final parameter vector and the final evaluated loss.
        """
        optimizer = StochasticGradientDescent(
            self, x_data, y_data, learning_rate, max_iterations, tolerance
        )
        final_params, curr_loss = optimizer.minimize(self.parameters)
        self.parameters = final_params
        self.history = optimizer.get_history()
        return final_params, curr_loss

    def get_history(self):
        """
        Retrieves the training history.

        Returns:
            list: The history of parameters recorded by the optimizer during fit.
        """
        return self.history
