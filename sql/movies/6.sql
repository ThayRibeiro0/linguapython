SELECT AVG(rating)
FROM ratings
WHERE movie.id = (SELECT id FROM movies WHERE movies.year = 2012);