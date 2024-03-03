SELECT name FROM people WHERE id in
(SELECT person_id FROM movies
JOIN directors ON movies.id = directors.movie_id
JOIN ratings ON movies.id = ratings.movie_id
WHERE rating >= 9.0);
