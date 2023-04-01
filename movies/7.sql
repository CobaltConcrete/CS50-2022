SELECT title, rating
FROM movies, ratings
WHERE ratings.movie_id = movies.id
AND movies.year = 2010
AND ratings.votes > 0
ORDER BY ratings.rating DESC, movies.title;