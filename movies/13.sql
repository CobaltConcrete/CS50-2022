SELECT name
FROM stars, people
WHERE stars.person_id = people.id
AND name != 'Kevin Bacon'

AND stars.movie_id IN

(
    SELECT movie_id
    FROM stars, people
    WHERE people.name = 'Kevin Bacon'
    AND birth = 1958
    AND stars.person_id = people.id
)

GROUP BY name, people.id