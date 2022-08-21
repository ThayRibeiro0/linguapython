SELECT AVG(rating)
FROM ratings ORDER BY Ranting DESC
WHERE movie_id = (SELECT id FROM movies WHERE movies.year = 2012 ORDER BY movies.year ASC);