SELECT name FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.id in
    (SELECT movie_id FROM stars
    WHERE person_id =
        (SELECT id FROM people
        WHERE birth = 1958
        AND name = 'Kevin Bacon'))
AND name != 'Kevin Bacon';
