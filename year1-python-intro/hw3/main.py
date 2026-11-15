from franchise import Franchise
from movie import Movie

if __name__ == "__main__":
    print("%" * 50)
    print("Creating Harry Potter Franchise")
    print("%" * 50)

    # Create a franchise - starts empty with no movies
    hp = Franchise("Harry Potter", "Fantasy", 2000, 0, 0, "Warner Bros")
    print(f"Total Views (Start): {hp.update_total_views()}")  # expected: 0
    print(f"Average Rating (Start): {hp.update_average_rating():.2f}")  # expected: 0
    print(f"Franchise Score (Start): {hp.score()}")  # expected: 0

    print("\n--- Adding Movies ---")
    # add_item inserts each movie in sorted order by release year automatically
    hp.add_item(
        Movie(
            "Deathly Hallows One", "Fantasy", 2010, 7.7, 2100, "Warner Bros", 146, 15.0
        )
    )
    hp.add_item(
        Movie(
            "Chamber Of Secrets", "Fantasy", 2002, 7.5, 2000, "Warner Bros", 161, 15.0
        )
    )
    hp.add_item(
        Movie("Philosopher Stone", "Fantasy", 2001, 8.1, 2500, "Warner Bros", 152, 12.0)
    )
    hp.add_item(
        Movie(
            "Prisoner Of Azkaban", "Fantasy", 2004, 7.9, 1800, "Warner Bros", 142, 14.0
        )
    )
    hp.add_item(
        Movie("Goblet Of Fire", "Fantasy", 2005, 7.7, 1900, "Warner Bros", 157, 16.0)
    )
    hp.add_item(
        Movie("Order Of Phoenix", "Fantasy", 2007, 7.5, 1700, "Warner Bros", 138, 13.0)
    )
    hp.add_item(
        Movie("Half Blood Prince", "Fantasy", 2009, 7.6, 1600, "Warner Bros", 153, 14.0)
    )
    hp.add_item(
        Movie(
            "Deathly Hallows Two", "Fantasy", 2011, 8.1, 2500, "Warner Bros", 130, 18.0
        )
    )

    print(f"Added {len(hp)} movies\n")

    print("--- Initial Franchise (sorted by year) ---")
    print(hp)

    print("\n--- Score Checks ---")
    # update_total_views sums all movie views and updates the franchise views attribute
    print(f"Total Views: {hp.update_total_views()}")
    # update_average_rating averages all movie ratings and updates the franchise rating attribute
    print(f"Average Rating: {hp.update_average_rating():.2f}")
    # score is rating * views (uses updated values)
    print(f"Franchise Score: {hp.score():.2f}")

    print("\n--- Sort by Profit ---")
    max_profit, max_name, min_profit, min_name = hp.sort_by_profit()
    print(
        f"Max Profit: {max_profit} ({max_name}), Min Profit: {min_profit} ({min_name})"
    )
    print(hp)

    print("\n--- Using deepcopy() method ---")
    # deepcopy creates a completely independent copy of the franchise and all its movies
    # modifying the copy should NOT affect the original
    hp_sorted = hp.deepcopy()
    print(f"Original size: {len(hp)}, Copy size: {len(hp_sorted)}\n")
    print("Copied franchise (sorted by release year):")
    print(hp_sorted)
    print("\nModifying copy doesn't affect original:")
    hp_sorted.remove_item("Philosopher Stone")
    print(f"Original size: {len(hp)}, Copy size: {len(hp_sorted)}")

    print("\n--- Finding Movies ---")
    # find returns the Movie object if found, None otherwise
    found = hp.find("Goblet Of Fire")
    print(f"Found:\n{found}")

    print("\n--- Removing Movie ---")
    # remove_item returns the removed Movie object, or None if not found
    removed = hp.remove_item("Chamber Of Secrets")
    print(f"Removed:\n{removed}")
    print(f"Franchise size: {len(hp)}")

    print("\n--- Trying to Remove Non-Existent Movie ---")
    result = hp.remove_item("Not A Movie")
    print(f"Result: {result}")

    print("\n--- Comparison Example ---")
    # comparison operators use the score() method (rating * views)
    movie1 = Movie(
        "Test Movie One", "Fantasy", 2020, 8.0, 1000, "Warner Bros", 120, 10.0
    )
    movie2 = Movie(
        "Test Movie Two", "Fantasy", 2021, 7.0, 2000, "Warner Bros", 100, 12.0
    )
    print(f"Movie1 ({movie1.name}): Score = {movie1.score()}")
    print(f"Movie2 ({movie2.name}): Score = {movie2.score()}")
    print(f"Movie1 > Movie2: {movie1 > movie2}")
    print(f"Movie1 < Movie2: {movie1 < movie2}")
