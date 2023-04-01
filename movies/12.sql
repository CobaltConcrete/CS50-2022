SELECT title
FROM movies, stars, people
WHERE people.name = 'Johnny Depp'
AND stars.person_id = people.id
AND stars.movie_id = movies.id

AND stars.movie_id IN
(
    SELECT movie_id
    FROM stars, people
    WHERE people.name = 'Helena Bonham Carter'
    AND stars.person_id = people.id
)