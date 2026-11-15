from movie import Movie


class MovieNode:
    """
    A class representing a single node in a linked list, containing a Movie object.
    """

    def __init__(self, movie, next=None):
        """
        Initialize a new MovieNode.

        Args:
            movie (Movie): The movie object to be stored in this node.
            next (MovieNode, optional): A reference to the next node in the linked list. Defaults to None.
        """

        self.movie = movie
        self.next = next
