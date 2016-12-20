from imdb import IMDb 
from os.path import basename
from glob import iglob as glob 

movie_dir = "../data/character_info/*.txt"
out_dir = "../data/genres/"


ia = IMDb()

for f in glob(movie_dir):
	with open(f) as movie:
		line = next(movie).strip()
		movie_id = line.split(": ")[1]

		try:
			movie_obj = ia.get_movie(movie_id)
		except imdb.IMDbError, e:
			print e 

		if movie_obj:
			genres = movie_obj.get('genres')

			with open(out_dir + basename(f), 'w') as outpt:
				outpt.write(line + "\n")
				outpt.write("Genres: {}\n".format(",".join(genres)))

		print "Done with {}".format(basename(f))