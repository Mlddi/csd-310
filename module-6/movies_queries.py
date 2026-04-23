import mysql.connector

from dotenv import dotenv_values

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

try:
    # Connect to the database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

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
        print("Movie Name: {}\n".format(movie[0]))

    # --- Query 4: Film names and Directors grouped by Director ---
    print("-- DISPLAYING MOVIES GROUPED BY DIRECTOR --")
    cursor.execute("SELECT film_director, film_name FROM film ORDER BY film_director")
    films = cursor.fetchall()
    for film in films:
        print("Director: {}\nMovie Name: {}\n".format(film[0], film[1]))

except mysql.connector.Error as err:
    print("Error: {}".format(err))

finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()