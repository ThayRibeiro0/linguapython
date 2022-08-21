SELECT movies.title
FROM people
JOIN movies ON stars.movie_id = movies.id
JOIN ratings on movies.id = ratings.movie_id
JOIN stars ON people.id = stars.person_id
WHERE people.name = "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5;