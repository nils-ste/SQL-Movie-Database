import random
import movie_storage_sql as storage
import statistics
import requests

def user_interface():
    """displays the menu and asks for a input and returns it"""
    print(
        "\n\n********** My Movies Database ********** \n\n"
        "Menu:\n"
        "0. Exit\n"
        "1. List movies\n"
        "2. Add movie\n"
        "3. Delete movie\n"
        "4. Update movie\n"
        "5. Stats\n"
        "6. Random movie\n"
        "7. Search movie\n"
        "8. Movies sorted by rating"
    )
    choice = input("Enter choice (0-8): ")
    if choice.isdigit() and 0 <= int(choice) <= 8:
        return choice
    else:
        return


def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


def command_add_movie():
    """adds a movie with its respective rating and release year to the database"""
    movies = storage.list_movies()
    valid_title = False

    while not valid_title:
        #according to task only required validation no empty
        title = input("enter movie name: ")
        if title:
            valid_title = True

    is_new_title_valid = True

    for existing_title in movies:
        if existing_title.lower() == title.lower():
            print("This movie is already present in the database. Please choose another one.")
            is_new_title_valid = False

    if is_new_title_valid:
        url = f"https://www.omdbapi.com/?i=tt3896198&apikey=841017c3&t={title}"
        response = requests.get(url)
        if response.status_code != 200:
            print("Something went wrong")
            return
        data = response.json()
        year = data["Year"]
        rating = data["imdbRating"]
        poster = data["Poster"]



        storage.add_movie(title, year, rating, poster)


def command_delete_movie():
    """deletes a movie from the database"""
    valid_title = False

    while not valid_title:
        # according to task only required validation no empty
        title = input("which movie do you want to delete? ")
        if title:
            valid_title = True
    storage.delete_movie(title)


def command_update_movie():
    """updates a movie rating in the database"""
    movies = storage.list_movies()
    movie_name = input("which movies rating do you want to edit? ")
    movie_found = False

    for movie in movies:
        if movie.get("title") == movie_name:
            movie_found = True

    if movie_found:
        is_rating_valid = False
        while not is_rating_valid:
            rating = input("enter movie rating (1-10): ")
            try:
                rating = float(rating)
                if 0 <= rating <= 10:
                    is_rating_valid = True
                else:
                    raise ValueError
            except ValueError:
                print("Invalid rating. Please try again.")
        storage.update_movie(movie_name, rating)

    else:
        print("Movie not found in database.")


def command_stats():
    """prints average rating, median rating, best and worst movie"""
    movies = storage.list_movies()

    ratings = []
    for info in movies.values():
        ratings.append(float(info["rating"]))

    average = round(sum(ratings) / len(movies), 2)
    median = statistics.median(ratings)

    best_rating = 0
    best_movie_name = []
    for movie, info in movies.items():
        if float(info["rating"]) > best_rating:
            best_rating = float(info["rating"])
            best_movie_name = movie
    for movie, info in movies.items():
        if float(info["rating"]) == best_rating and movie not in best_movie_name:
            best_movie_name.append(movie)

    worst_rating = 10
    worst_movie_name = []
    for movie, info in movies.items():
        if float(info["rating"]) < worst_rating:
            worst_rating = float(info["rating"])
            worst_movie_name = movie
    for movie, info in movies.items():
        if float(info["rating"]) == worst_rating and movie not in worst_movie_name:
            worst_movie_name.append(movie)

    print(
        f"\nAverage rating: {average}\n"
        f"Median rating: {median}\n"
        f"Best movie: {best_movie_name}, {best_rating}\n"
        f"Worst movie: {worst_movie_name}, {worst_rating}"
    )


def command_random_movie():
    """prints a random movie from the list"""
    movies = storage.list_movies()

    # pick a random title from the keys
    random_title = random.choice(list(movies.keys()))
    movie = movies[random_title]

    print(
        f"Random movie: {random_title}, Released: {movie['year']}, "
        f"IMDB Rating: {movie['rating']}"
    )


def command_search_movie():
    """prints a search movie from the database"""
    movies = storage.list_movies()
    valid_query = False

    while not valid_query:
        # according to task only required validation no empty
        query = input("Enter movie name to look up: ")
        if query:
            valid_query = True
        else:
            print("Wrong input. Please try again.")


    for movie, info in movies.items():
        if query.lower() in movie.lower():
            print(
                f"Title: {movie['title']}, Released: {movie['year']},"
                f"IMDB Rating {movie['rating']}"
            )
            break

    else:
        print(f"\n{query} not found in database.")


def command_rating_list():
    """prints list sorted by rating"""
    print("\nMovies sorted by IMDB Rating\n")
    movies = storage.list_movies()
    sorted_movies = sorted(
        movies.items(),
        key=lambda item: item[1]["rating"],
        reverse=True
    )

    for title, info in sorted_movies:
        print(
            f"Title: {title}, Released: {info['year']}, "
            f"IMDB Rating {info['rating']}"
        )


def main():
    """Runs the interactive menu loop."""
    # Using if-elif-else ensures only valid menu options are processed,
    # preventing errors from invalid inputs and handling them gracefully.
    while True:
        user_decision = user_interface()
        # if, elif, else forma
        if user_decision == "0":
            print("Bye!")
            break
        elif user_decision == "1":
            command_list_movies()
            input("Press enter to continue...")
        elif user_decision == "2":
            command_add_movie()
            input("Press enter to continue...")
        elif user_decision == "3":
            command_delete_movie()
            input("Press enter to continue...")
        elif user_decision == "4":
            command_update_movie()
            input("Press enter to continue...")
        elif user_decision == "5":
            command_stats()
            input("Press enter to continue...")
        elif user_decision == "6":
            command_random_movie()
            input("Press enter to continue...")
        elif user_decision == "7":
            command_search_movie()
            input("Press enter to continue...")
        elif user_decision == "8":
            command_rating_list()
            input("Press enter to continue...")
        else:
            print("\nPlease enter numbers between 0 and 8")
            input("Press enter to continue...")


if __name__ == "__main__":
    main()
