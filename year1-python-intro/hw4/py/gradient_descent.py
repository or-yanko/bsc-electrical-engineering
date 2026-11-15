from abc import ABC, abstractmethod
import numpy as np


class GradientDescent(ABC):
    """
    An abstract base class for gradient descent optimizers.

    This class defines the required interface for all gradient descent
    optimizers and handles the initialization and storage of shared
    attributes such as the model, training data, and hyperparameters.
    """

    def __init__(self, model, x_data, y_data, learning_rate, max_iterations, tolerance):
        """
        Initializes the GradientDescent optimizer with the model, data, and hyperparameters.

        Args:
            model (object): The model to optimize.
            x_data (array-like): Training input data.
            y_data (array-like): Training target data.
            learning_rate (float): Step size for the optimizer.
            max_iterations (int): Maximum allowed iterations.
            tolerance (float): Threshold for early stopping.
        """
        self.model = model
        self.x_data = np.array(x_data, dtype=float)
        self.y_data = np.array(y_data, dtype=float)
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.history = []

    @abstractmethod
    def function_value(self, parameters):
        """
        Evaluates the model's loss function for the given parameters.

        Args:
            parameters (float or np.ndarray): The current model parameters.

        Returns:
            float: The computed loss value.
        """
        pass

    @abstractmethod
    def gradient(self, parameters):
        """
        Computes the gradient of the loss function with respect to the given parameters.

        Args:
            parameters (float or np.ndarray): The current model parameters.

        Returns:
            float or np.ndarray: The computed gradient.
        """
        pass

    @abstractmethod
    def step(self, parameters):
        """
        Performs a single parameter update step using the computed gradient.

        Args:
            parameters (float or np.ndarray): The current model parameters.

        Returns:
            float or np.ndarray: The updated parameters.
        """
        pass

    @abstractmethod
    def minimize(self, start_parameters):
        """
        Executes the optimization loop to minimize the loss function.

        Args:
            start_parameters (float or array-like): The initial parameters to start optimization.

        Returns:
            tuple: A tuple containing the final optimized parameters and the final loss value.
        """
        pass

    def get_history(self):
        """
        Retrieves the history of parameter updates.

        Returns:
            list: The list of parameters recorded during the `minimize` process.
        """
        return self.history
