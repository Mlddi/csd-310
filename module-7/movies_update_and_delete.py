#MaddisonMontijo|Assignment 8.2| 4/28

import mysql.connector

from dotenv import dotenv_values

# BRO, I spent an entire hour getting my interpretatar trying to work again crying >;
# And I swear, I changed my interpeator to Anaconda3 a gazillion times
# I just made a new project again at some point that worked?!


# load .env file
secrets = dotenv_values(".env")

# database config
db_config = {
    "user": secrets["USER"],

    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

def show_films(cursor, title):
    # Print the label/title provided in the argument
    print(f"\n-- {title} --\n")

    # Using a multi-line string (triple quotes) for the SQL query
    query = (
        "SELECT film_name AS Name, film_director AS Director, " 
        "genre_name AS Genre, studio_name AS Studio "  
        "FROM film " 
        "INNER JOIN genre ON film.genre_id = genre.genre_id "  
        "INNER JOIN studio ON film.studio_id = studio.studio_id"
    )
    cursor.execute(query)
    results = cursor.fetchall()

    # Iterate over the data set and display results
    for row in results:
        print(f"Film Name: {row[0]} \nDirector: {row[1]} \nGenre: {row[2]} \nStudio: {row[3]}\n")


try:
    # Connect to the database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    show_films(cursor, "DISPLAYING FILMS")

    # --- Query 1: All fields from Studio ---
    print("-- DISPLAYING STUDIO RECORDS --")
    cursor.execute("SELECT * FROM studio")
    studios = cursor.fetchall()
    for studio in studios:
        print("Studio ID: {}\nStudio Name: {}\n".format(studio[0], studio[1]))

    # --- Query 2: All fields from Genre ---
    print("-- DISPLAYING GENRE RECORDS --")
    cursor.execute("SELECT * FROM genre")
    genres = cursor.fetchall()
    for genre in genres:
        print("Genre ID: {}\nGenre Name: {}\n".format(genre[0], genre[1]))

    # --- Query 3: Movies with run time < 2 hours (120 minutes) ---
    print("-- DISPLAYING MOVIES WITH RUN TIME LESS THAN 2 HOURS --")
    # Assuming runtime is stored in minutes
    cursor.execute("SELECT film_name FROM film WHERE film_runtime < 120")
    movies = cursor.fetchall()
    for movie in movies:
        print("Film Name: {}\n".format(movie[0]))

    # --- Query 4: Film names and Directors grouped by Director ---
    print("-- DISPLAYING MOVIES GROUPED BY DIRECTOR --")
    cursor.execute("SELECT film_director, film_name FROM film ORDER BY film_director")
    films = cursor.fetchall()
    for film in films:
        print("Director: {}\nFilm Name: {}\n".format(film[0], film[1]))

    # ---  Movies Update and Delete  ---#

    show_films(cursor, "DISPLAYING UPDATED FILMS")

    # ---  INSERT : Change values to your choice ---#

    cursor.execute("INSERT INTO film (film_name, film_director,film_releaseDate,film_runtime, genre_id, studio_id) VALUES ('The Martian', 'Christopher Nolan','2015',144, 2,1)")
    db.commit()
    show_films(cursor, "AFTER INSERT")




    #--- UPDATE : Alien to Horror --- #

    cursor.execute("UPDATE film SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror') WHERE film_name = 'Alien'")
    db.commit()
    show_films(cursor, "AFTER UPDATE")

    #---DELETE : Gladitor---#

    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator'")
    db.commit()
    show_films(cursor, "AFTER DELETE")

    db.close()


except mysql.connector.Error as err:
    print("Error: {}".format(err))

finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()