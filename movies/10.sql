SELECT name
FROM directors, ratings, people
WHERE ratings.rating >= 9.0
AND directors.movie_id = ratings.movie_id
AND people.id = directors.person_id
GROUP BY name, people.id