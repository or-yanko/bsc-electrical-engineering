from gradient_descent import GradientDescent


class GradientDescent1D(GradientDescent):
    """
    An optimizer that performs batch gradient descent for a model with a single scalar parameter.

    This class updates the single parameter using the full dataset for every update step.
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
        Initializes the 1D Gradient Descent optimizer.

        This method calls the base class constructor to store the model, data,
        and hyperparameters. It relies on the base class to handle data conversions
        and history initialization.

        Args:
            model (object): The model to optimize. Must implement `loss` and `gradients`.
            x_data (array-like): Training input data.
            y_data (array-like): Training target data.
            learning_rate (float, optional): Step size for the optimizer. Defaults to 0.1.
            max_iterations (int, optional): Maximum allowed iterations. Defaults to 1000.
            tolerance (float, optional): Threshold for early stopping. Defaults to 1e-6.
        """
        super().__init__(
            model, x_data, y_data, learning_rate, max_iterations, tolerance
        )

    def function_value(self, parameters):
        """
        Evaluates the model loss on the full dataset for a single scalar parameter.

        This method acts as a wrapper around the model's loss function, ensuring
        the input parameter is properly cast to a float and evaluated against
        the complete stored training dataset.

        Args:
            parameters (float or int): The current scalar model parameter to evaluate.

        Returns:
            float: The computed loss value for the given parameter.
        """
        float_params = float(parameters)
        return self.model.loss(float_params, self.x_data, self.y_data)

    def gradient(self, parameters):
        """
        Computes the derivative of the loss using the full dataset.

        This method acts as a wrapper around the model's gradient function. It
        ensures the input parameter is cast to a float, computes the gradient
        using the entire stored training dataset, and casts the resulting
        derivative to a float before returning it.

        Args:
            parameters (float or int): The current scalar model parameter.

        Returns:
            float: The computed derivative of the loss function.
        """
        float_params = float(parameters)
        return float(self.model.gradients(float_params, self.x_data, self.y_data))

    def step(self, parameters):
        """
        Performs a single scalar parameter update step.

        This method calculates the gradient for the current parameter and
        updates it by taking a step in the direction opposite to the gradient,
        scaled by the learning rate.

        Args:
            parameters (float or int): The current scalar model parameter.

        Returns:
            float: The updated parameter value after one gradient descent step.
        """
        float_params = float(parameters)
        grad = self.gradient(float_params)
        return float_params - (self.learning_rate * grad)

    def minimize(self, start_parameters):
        """
        Repeatedly applies parameter updates until convergence or the iteration limit is reached.

        This method executes the main optimization loop. It updates the parameter using
        the `step` method, records each new value in the `history`, and checks for early
        stopping if the absolute change in the parameter is smaller than the specified tolerance.

        Args:
            start_parameters (float or int): The initial parameter value to start the optimization.

        Returns:
            tuple: A tuple containing the final optimized parameter (float) and
                   its evaluated loss (float).
        """
        current_param = float(start_parameters)
        self.history = [current_param]
        # repeat the process
        for iteration in range(self.max_iterations):
            next_param = self.step(current_param)
            self.history.append(next_param)
            # early stopping conditions
            if abs(next_param - current_param) < self.tolerance:
                current_param = next_param
                break
            current_param = next_param
        return current_param, self.function_value(current_param)

    def get_history(self):
        """
        Retrieves the history of parameter updates.

        Returns:
            list: The stored list of parameter values visited during training.
        """
        return self.history
