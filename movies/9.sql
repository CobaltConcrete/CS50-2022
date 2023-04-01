SELECT name
FROM people, movies, stars
WHERE stars.person_id = people.id
AND movies.id = stars.movie_id
AND movies.year = 2004
GROUP BY name, people.id
ORDER BY birth;