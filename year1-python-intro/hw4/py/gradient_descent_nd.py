import numpy as np

from gradient_descent import GradientDescent


class GradientDescentND(GradientDescent):
    """
    An optimizer that performs batch gradient descent for a parameter vector.

    This class updates an array of parameters using the full dataset for every update step.
    """

    def __init__(
        self,
        model,
        x_data,
        y_data,
        learning_rate=0.1,
        max_iterations=1000,
        tolerance=1e-6,
    ):
        """
        Initializes the ND Gradient Descent optimizer.

        Calls the base class constructor to handle the storage of the model,
        training data, and hyperparameters.

        Args:
            model (object): The model to optimize. Must implement `loss` and `gradients`.
            x_data (array-like): Training input data.
            y_data (array-like): Training target data.
            learning_rate (float, optional): Step size for the optimizer. Defaults to 0.1.
            max_iterations (int, optional): Maximum allowed iterations. Defaults to 1000.
            tolerance (float, optional): Threshold for early stopping based on vector norm. Defaults to 1e-6.
        """
        super().__init__(
            model, x_data, y_data, learning_rate, max_iterations, tolerance
        )

    def function_value(self, parameters):
        """
        Evaluates the model loss on the full dataset for a parameter vector.

        Converts the input parameters to a NumPy array of floats before
        calling the model's loss function.

        Args:
            parameters (array-like): The current parameter vector.

        Returns:
            float: The computed loss value.
        """
        float_params = np.array(parameters, dtype=float)
        return self.model.loss(float_params, self.x_data, self.y_data)

    def gradient(self, parameters):
        """
        Computes the gradient vector using the full dataset.

        Converts the parameters to a NumPy array of floats, evaluates the
        gradients using the model, and ensures the returned gradient is
        also a NumPy array of floats.

        Args:
            parameters (array-like): The current parameter vector.

        Returns:
            np.ndarray: The computed gradient vector.
        """
        float_params = np.array(parameters, dtype=float)
        return np.array(
            self.model.gradients(float_params, self.x_data, self.y_data), dtype=float
        )

    def step(self, parameters):
        """
        Performs one vector update step.

        Calculates the gradient for the current parameter vector and updates it
        by taking a scaled step in the opposite direction of the gradient.

        Args:
            parameters (array-like): The current parameter vector.

        Returns:
            np.ndarray: The updated parameter vector.
        """
        float_params = np.array(parameters, dtype=float)
        grad = self.gradient(float_params)
        return float_params - self.learning_rate * grad

    def minimize(self, start_parameters):
        """
        Repeatedly applies vector gradient descent updates.

        Executes the optimization loop, storing a copy of the parameter vector
        in history at each step. The loop stops when the maximum number of iterations
        is reached or if the Euclidean norm of the parameter change is strictly
        less than the tolerance.

        Args:
            start_parameters (array-like): The initial parameter vector.

        Returns:
            tuple: A tuple containing the final parameter vector (np.ndarray)
                   and its evaluated loss (float).
        """
        curr_param = np.array(start_parameters, dtype=float)
        self.history = [curr_param.copy()]
        for iteration in range(self.max_iterations):
            next_param = self.step(curr_param)
            self.history.append(next_param.copy())
            if np.linalg.norm(next_param - curr_param) < self.tolerance:
                curr_param = next_param
                break
            curr_param = next_param
        return curr_param, self.function_value(curr_param)

    def get_history(self):
        """
        Retrieves the history of parameter vector updates.

        Returns:
            list: The stored list of parameter vector copies.
        """
        return self.history
