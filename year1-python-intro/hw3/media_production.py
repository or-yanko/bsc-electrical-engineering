class MediaProduction:
    """
    Base class representing general media content.
    Handles the core attributes and validation for any media production.
    """

    def __init__(self, name, genre, release_year, rating, views, production_company):
        """
        Initializes the MediaProduction object with strict input validation.
        Raises a ValueError if any input is invalid according to the assignment rules.
        """
        # Validate name: must be a proper title-cased string with single spaces and no special chars.
        if not self.is_validated_str_input(name):
            raise ValueError
        self.name = name

        # Validate genre using the same string format rules as name.
        if not self.is_validated_str_input(genre):
            raise ValueError
        self.genre = genre

        # Validate release_year: must be a positive integer.
        # Note: type(release_year) is bool is checked because bool is a subclass of int in Python.
        if (
            type(release_year) is bool
            or not isinstance(release_year, int)
            or release_year <= 0
        ):
            raise ValueError
        self.release_year = release_year

        # Validate rating: must be a number (int or float) between 0.0 and 10.0 inclusive.
        if (
            type(rating) is bool
            or not isinstance(rating, (int, float))
            or not 0.0 <= rating <= 10.0
        ):
            raise ValueError
        self.rating = rating  # Kept as is without float() conversion to match specific test print formats.

        # Validate views: must be a non-negative integer (>= 0).
        if type(views) is bool or not isinstance(views, int) or views < 0:
            raise ValueError
        self.views = views

        # Validate production_company using the same string format rules as name.
        if not self.is_validated_str_input(production_company):
            raise ValueError
        self.production_company = production_company

    @staticmethod
    def is_validated_str_input(s):
        """
        Helper method to validate string inputs (name, genre, production_company).
        Rules: String, not empty, single spaces only, alphabetical characters only (no numbers/symbols), and Title Case.
        """
        if type(s) is not str or not s:
            return False
        # Check for single spaces between words
        if s != " ".join(s.split()):
            return False
        # Check if all characters (excluding spaces) are alphabetic
        if not s.replace(" ", "").isalpha():
            return False
        # Check if the string is properly Title Cased (starts with upper-case, rest lower)
        if not s.istitle():
            return False
        return True

    def score(self):
        """Returns the product of rating and views as the score."""
        return self.views * self.rating

    def set_rating(self, rating):
        """
        Updates the rating if the input is a valid number between 0.0 and 10.0.
        Returns True if the update is successful and the value actually changed, otherwise False.
        """
        if type(rating) is bool or not isinstance(rating, (int, float)):
            return False
        if not 0.0 <= rating <= 10.0:
            return False
        if self.rating == rating:
            return False
        self.rating = rating
        return True

    def set_views(self, views):
        """
        Updates the views if the input is a positive integer.
        Returns True if the update is successful and the value actually changed, otherwise False.
        """
        if type(views) is bool or not isinstance(views, int):
            return False
        if views <= 0:
            return False
        if self.views == views:
            return False
        self.views = views
        return True

    def __str__(self):
        """String representation of the media production, formatted with 10 '=' separators."""
        return f'{10*"="}\n{self.name}, {self.genre}, {self.release_year}, Rating: {self.rating}, Views: {self.views}, Score: {self.score()}\n{10*"="}'

    def __repr__(self):
        """Formal string representation, mirrors __str__."""
        return f'{10*"="}\n{self.name}, {self.genre}, {self.release_year}, Rating: {self.rating}, Views: {self.views}, Score: {self.score()}\n{10*"="}'

    # Operator overloading based on score(). If scores are equal, falls back to rating.
    def __eq__(self, other):
        if not isinstance(other, MediaProduction):
            raise ValueError
        if self.score() == other.score():
            return self.rating == other.rating
        return False

    def __ne__(self, other):
        if not isinstance(other, MediaProduction):
            raise ValueError
        if self.score() == other.score():
            return self.rating != other.rating
        return True

    def __lt__(self, other):
        if not isinstance(other, MediaProduction):
            raise ValueError
        if self.score() == other.score():
            return self.rating < other.rating
        return self.score() < other.score()

    def __gt__(self, other):
        if not isinstance(other, MediaProduction):
            raise ValueError
        if self.score() == other.score():
            return self.rating > other.rating
        return self.score() > other.score()

    def __le__(self, other):
        if not isinstance(other, MediaProduction):
            raise ValueError
        if self.score() == other.score():
            return self.rating <= other.rating
        return self.score() <= other.score()

    def __ge__(self, other):
        if not isinstance(other, MediaProduction):
            raise ValueError
        if self.score() == other.score():
            return self.rating >= other.rating
        return self.score() >= other.score()
