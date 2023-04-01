SELECT AVG(energy)
FROM songs, artists
WHERE artists.name = "Drake"
AND songs.artist_id = artists.id