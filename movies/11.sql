SELECT title
FROM movies, stars, ratings, people
WHERE people.name = 'Chadwick Boseman'
AND stars.person_id = people.id
AND stars.movie_id = movies.id
AND ratings.movie_id = movies.id
ORDER by rating DESC
LIMIT 5;