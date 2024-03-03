SELECT name FROM people WHERE id in
(SELECT person_id FROM movies
JOIN stars ON movies.id = stars.movie_id
WHERE year = 2004)
ORDER BY birth;
