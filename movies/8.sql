SELECT people.name
FROM movies, stars, people
WHERE movies.title = 'Toy Story'
AND stars.movie_id = movies.id
AND people.id = stars.person_id;