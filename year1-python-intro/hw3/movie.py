from media_production import MediaProduction


class Movie(MediaProduction):
    """
    Represents a single movie.
    Inherits shared properties from the MediaProduction base class.
    """

    def __init__(
        self,
        name,
        genre,
        release_year,
        rating,
        views,
        production_company,
        duration,
        ticket_price,
    ):
        """
        Initializes a Movie object.
        Calls the parent MediaProduction constructor first, then validates and initializes
        movie-specific attributes: duration and ticket_price.
        """
        # Call base class constructor to handle general attributes and validation
        super().__init__(name, genre, release_year, rating, views, production_company)

        # Validate duration: must be a strictly positive integer
        if type(duration) is bool or not isinstance(duration, int) or duration <= 0:
            raise ValueError
        self.duration = duration

        # Validate ticket_price: must be a strictly positive number (int or float)
        if (
            type(ticket_price) is bool
            or not isinstance(ticket_price, (int, float))
            or ticket_price <= 0
        ):
            raise ValueError
        self.ticket_price = (
            ticket_price  # Kept without float conversion per requirements
        )

    def set_duration(self, duration):
        """
        Updates the movie duration if the input is a strictly positive integer.
        Returns True on successful update, False otherwise.
        """
        if type(duration) is bool or not isinstance(duration, int):
            return False
        if duration <= 0:
            return False
        if self.duration == duration:
            return False
        self.duration = duration
        return True

    def set_ticket_price(self, price):
        """
        Updates the movie ticket price if the input is a strictly positive number.
        Returns True on successful update, False otherwise.
        """
        if type(price) is bool or not isinstance(price, (int, float)):
            return False
        if price <= 0:
            return False
        if self.ticket_price == price:
            return False
        self.ticket_price = price
        return True

    def __str__(self):
        """
        Extends the parent string representation by appending duration and ticket_price.
        The 10 '=' characters remain at the very end.
        """
        # Remove the closing '=\n' from the base class string to append new data
        base = super().__str__().strip("=\n")
        return f"==========\n{base}, Duration: {self.duration}, Ticket Price: {self.ticket_price}\n{'='*10}"

    def __repr__(self):
        """Formal string representation, mirrors __str__."""
        base = super().__repr__().strip("=\n")
        return f"==========\n{base}, Duration: {self.duration}, Ticket Price: {self.ticket_price}\n{'='*10}"
