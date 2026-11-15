import numpy as np

from gradient_descent import GradientDescent


class StochasticGradientDescent(GradientDescent):
    """
    An optimizer that performs stochastic gradient descent for a parameter vector.

    This class trains a model by computing the gradient and updating the
    parameters using a single training example per update.
    """

    def __init__(
        self,
        model,
        x_data,
        y_data,
        learning_rate=0.05,
        max_iterations=1000,
        tolerance=1e-8,
    ):
        """
        Initializes the Stochastic Gradient Descent optimizer.

        Calls the base class constructor to store the model, training data,
        and hyperparameters.

        Args:
            model (object): The model to optimize. Must implement `loss` and `gradients`.
            x_data (array-like): Full training input data.
            y_data (array-like): Full training target data.
            learning_rate (float, optional): Step size for the optimizer. Defaults to 0.05.
            max_iterations (int, optional): Maximum number of epochs. Defaults to 1000.
            tolerance (float, optional): Threshold for early stopping based on vector norm. Defaults to 1e-8.
        """
        super().__init__(
            model, x_data, y_data, learning_rate, max_iterations, tolerance
        )

    def function_value(self, parameters):
        """
        Evaluates the model loss on the full dataset.

        Converts the input parameters to a NumPy array of floats before
        calling the model's loss function against the entire dataset.

        Args:
            parameters (array-like): The current parameter vector.

        Returns:
            float: The computed loss value.
        """
        float_params = np.array(parameters, dtype=float)
        return self.model.loss(float_params, self.x_data, self.y_data)

    def gradient(self, parameters, sample_index=0):
        """
        Computes a one-sample gradient for the specified sample index.

        Uses array slicing to extract a single training example and its target,
        ensuring they remain one-element NumPy arrays.

        Args:
            parameters (array-like): The current parameter vector.
            sample_index (int, optional): The index of the specific data point to use. Defaults to 0.

        Returns:
            np.ndarray: The computed gradient vector for the specified sample.
        """
        float_params = np.array(parameters, dtype=float)
        x_sample = self.x_data[sample_index : sample_index + 1]
        y_sample = self.y_data[sample_index : sample_index + 1]
        grad = self.model.gradients(float_params, x_sample, y_sample)
        return np.array(grad, dtype=float)

    def step(self, parameters, sample_index=0):
        """
        Performs one SGD parameter update using a single sample.

        Calculates the one-sample gradient for the current parameter vector
        and updates it by taking a scaled step in the opposite direction.

        Args:
            parameters (array-like): The current parameter vector.
            sample_index (int, optional): The index of the specific data point to use. Defaults to 0.

        Returns:
            np.ndarray: The updated parameter vector.
        """
        float_params = np.array(parameters, dtype=float)
        grad = self.gradient(float_params, sample_index)
        return float_params - self.learning_rate * grad

    def minimize(self, start_parameters):
        """
        Repeatedly loops over the dataset to apply SGD updates.

        An iteration (epoch) consists of updating the parameter vector for every
        training sample individually. A copy of the parameter
        vector is appended to the history after every single sample update.
        Early stopping is evaluated at the end of each epoch by comparing the
        parameters at the start and end of the epoch.

        Args:
            start_parameters (array-like): The initial parameter vector.

        Returns:
            tuple: A tuple containing the final parameter vector (np.ndarray)
                   and its evaluated full-dataset loss (float).
        """
        curr_param = np.array(start_parameters, dtype=float)
        self.history = [curr_param.copy()]
        samples_number = len(self.x_data)
        for iteration in range(self.max_iterations):
            start_epoch_param = curr_param.copy()
            for index in range(samples_number):
                curr_param = self.step(curr_param, index)
                self.history.append(curr_param.copy())
            if np.linalg.norm(curr_param - start_epoch_param) < self.tolerance:
                break
        return curr_param, self.function_value(curr_param)

    def get_history(self):
        """
        Retrieves the history of parameter vector updates.

        Returns:
            list: The stored list of parameter vector copies recorded after
                  each individual sample update.
        """
        return self.history
