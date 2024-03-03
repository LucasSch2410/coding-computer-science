SELECT title FROM movies
WHERE id in
(SELECT movie_id FROM stars
WHERE person_id IN (
    SELECT id FROM people
    WHERE name = 'Bradley Cooper' OR name = 'Jennifer Lawrence'
)
GROUP BY movie_id
HAVING COUNT(movie_id) = 2);
