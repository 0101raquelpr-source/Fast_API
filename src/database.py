from src.models.movie_model import Movie

# This file acts as a temporary in-memory database.
# It can be easily replaced later with a real database connection.
movies: list[Movie] = [
    Movie(id=1, title="Avatar", overview="En un exuberante planeta llamado Pandora...", year=2009, rating=7.8, category="Acción"),
    Movie(id=2, title="Pulp Fiction", overview="Las vidas de dos sicarios de la mafia...", year=1994, rating=8.9, category="Crimen"),
    Movie(id=3, title="Forrest Gump", overview="Las presidencias de Kennedy y Johnson...", year=1994, rating=8.8, category="Drama"),
    Movie(id=4, title="The Dark Knight", overview="Cuando la amenaza conocida como el Joker...", year=2008, rating=9.0, category="Acción"),
    Movie(id=5, title="Schindler's List", overview="En la Polonia ocupada por los alemanes...", year=1993, rating=8.9, category="Biografía"),
    Movie(id=6, title="The Lord of the Rings: The Return of the King", overview="Gandalf y Aragorn lideran el Mundo de los Hombres...", year=2003, rating=8.9, category="Aventura"),
    Movie(id=7, title="Fight Club", overview="Un oficinista insomne y un fabricante de jabón...", year=1999, rating=8.8, category="Drama"),
]
