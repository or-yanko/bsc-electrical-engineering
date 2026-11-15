from media_production import MediaProduction
from movie import Movie
from movie_node import MovieNode


class Franchise(MediaProduction):
    """
    Represents a franchise containing multiple movies managed as a Linked List.
    Inherits from MediaProduction.
    """

    def __init__(self, name, genre, release_year, rating, views, production_company):
        """
        Initializes the Franchise. Uses the parent constructor for core properties.
        Sets up an empty linked list to store MovieNode objects.
        """
        super().__init__(name, genre, release_year, rating, views, production_company)
        self.head = None  # Pointer to the first MovieNode in the linked list
        self.size = 0  # Number of movies in the franchise

    def add_item(self, movie):
        """
        Adds a movie to the linked list if:
        1. It is a valid Movie instance.
        2. Its name is unique within the franchise.
        The list is maintained in ascending order based on release_year.
        """
        if not isinstance(movie, Movie):
            return False

        # Step 1: Check for duplicate movie names in the existing linked list
        pointer = self.head
        while pointer is not None:
            if pointer.movie.name == movie.name:
                return False
            pointer = pointer.next

        # Step 2: Create a new node and insert it in the correct sorted position (by release_year)
        new_node = MovieNode(movie)

        # Case A: List is empty, or the new movie is older than the current head
        if self.head is None or self.head.movie.release_year > movie.release_year:
            new_node.next = self.head
            self.head = new_node
            self.size += 1
            return True

        # Case B: Traverse to find the correct insertion point
        pointer = self.head
        while (
            pointer.next is not None
            and pointer.next.movie.release_year <= movie.release_year
        ):
            pointer = pointer.next

        # Insert the new node between pointer and pointer.next
        new_node.next = pointer.next
        pointer.next = new_node
        self.size += 1
        return True

    def remove_item(self, name):
        """
        Removes a movie from the linked list by its name.
        Returns the removed Movie object, or None if not found.
        """
        if self.head is None:
            return None

        # Case A: The movie to remove is at the head of the list
        if self.head.movie.name == name:
            tmp = self.head.movie
            self.head = self.head.next
            self.size -= 1
            return tmp

        # Case B: The movie is somewhere else in the list (requires two pointers)
        pointer_l, pointer_r = self.head, self.head.next
        while pointer_r is not None:
            if pointer_r.movie.name == name:
                pointer_l.next = pointer_r.next  # Bypass the node to be removed
                self.size -= 1
                return pointer_r.movie
            pointer_l, pointer_r = pointer_l.next, pointer_r.next
        return None

    def find(self, name):
        """Returns the Movie object with the specified name, or None if not found."""
        pointer = self.head
        while pointer is not None:
            if pointer.movie.name == name:
                return pointer.movie
            pointer = pointer.next
        return None

    def update_total_views(self):
        """
        Traverses the linked list, sums all movie views, and updates the Franchise views attribute.
        """
        pointer, total_views = self.head, 0
        while pointer is not None:
            total_views += pointer.movie.views
            pointer = pointer.next
        self.views = total_views
        return total_views

    def update_average_rating(self):
        """
        Traverses the linked list, calculates the average rating of all movies,
        and updates the Franchise rating attribute.
        """
        if self.size == 0:
            self.rating = 0.0
            return 0.0

        pointer, total_rating = self.head, 0
        while pointer is not None:
            total_rating += pointer.movie.rating
            pointer = pointer.next

        avg = float(total_rating / self.size)
        self.rating = avg
        return avg

    def __len__(self):
        """Returns the number of movies in the franchise."""
        return self.size

    def __str__(self):
        """
        String representation specific to Franchise.
        Uses 10 '*' separators and formats rating to 1 decimal place using `:.1f` as instructed.
        """
        string = f"**********\n{self.name} (Rating: {self.rating:.1f}, Views: {self.views}, Score: {self.score()}): \n"
        current = self.head
        while current is not None:
            string += f"{current.movie}\n"
            current = current.next
        string += "**********"
        return string

    def __repr__(self):
        """Formal representation, mirrors __str__."""
        return self.__str__()

    def sort_by_release_year(self):
        """
        Sorts the linked list by release_year in ascending order.
        This is an In-Place Bubble Sort on a linked list (modifies `next` pointers, not values).
        """
        if self.head is None or self.head.next is None:
            return

        swapped = True
        while swapped:
            swapped, prev, curr = False, None, self.head
            while curr is not None and curr.next is not None:
                # Compare adjacent nodes by release year
                if curr.movie.release_year > curr.next.movie.release_year:
                    nxt = curr.next

                    # Pointer manipulation to swap nodes
                    curr.next = nxt.next
                    nxt.next = curr

                    if prev is None:
                        self.head = nxt  # Update head if swap occurred at the beginning
                    else:
                        prev.next = nxt

                    prev = nxt
                    swapped = True
                else:
                    prev = curr
                    curr = curr.next

    def sort_by_profit(self):
        """
        Sorts the linked list by profitability (ticket_price * views) in descending order.
        This is an In-Place Bubble Sort.
        Returns a tuple: (max_profit, max_profit_movie_name, min_profit, min_profit_movie_name).
        """
        if self.head is None:
            return (0, "", 0, "")

        swapped = True
        while swapped:
            swapped, prev, curr = False, None, self.head
            while curr is not None and curr.next is not None:
                # Calculate profit for current and next movie
                curr_profit = curr.movie.ticket_price * curr.movie.views
                nxt_profit = curr.next.movie.ticket_price * curr.next.movie.views

                # Sort in descending order: swap if current profit is less than next profit
                if curr_profit < nxt_profit:
                    nxt = curr.next

                    # Pointer manipulation to swap nodes
                    curr.next = nxt.next
                    nxt.next = curr

                    if prev is None:
                        self.head = nxt
                    else:
                        prev.next = nxt
                    prev = nxt
                    swapped = True
                else:
                    prev = curr
                    curr = curr.next

        # Traverse to the end to find the minimum profit node (last node after descending sort)
        pointer = self.head
        while pointer.next is not None:
            pointer = pointer.next

        # Head contains the max profit, pointer (last node) contains the min profit
        max_prof = self.head.movie.ticket_price * self.head.movie.views
        min_prof = pointer.movie.ticket_price * pointer.movie.views

        return (max_prof, self.head.movie.name, min_prof, pointer.movie.name)

    def deepcopy(self):
        """
        Creates and returns a deep copy of the Franchise.
        A new Franchise object is created, and new Movie objects are instantiated
        and added to ensure no references to the original objects are shared.
        """
        copy_franchise = Franchise(
            self.name,
            self.genre,
            self.release_year,
            self.rating,
            self.views,
            self.production_company,
        )

        current = self.head
        while current is not None:
            # Create a brand new Movie object copying the attributes of the current movie
            copy_movie = Movie(
                current.movie.name,
                current.movie.genre,
                current.movie.release_year,
                current.movie.rating,
                current.movie.views,
                current.movie.production_company,
                current.movie.duration,
                current.movie.ticket_price,
            )
            # add_item inherently maintains the sorted order (by release year)
            copy_franchise.add_item(copy_movie)
            current = current.next

        return copy_franchise
