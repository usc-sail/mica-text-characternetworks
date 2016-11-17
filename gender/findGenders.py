####################################################################################################################################
#
# This looks up IMDB ids in TMDB and retrieves the cast gender info
# Author: VRMP
# Date: 11/16/16
#
####################################################################################################################################
import tmdbsimple as tmdb
from os.path import exists 

tmdb.API_KEY = 'fad36d118bb1596735ee7e46c92ac997'

with open('./imdbs_tofix.txt') as imdbs:

	for imdb_id in imdbs:

		imdb_id = imdb_id.strip()
		movie_results = tmdb.Find(id=imdb_id).info(external_source='imdb_id').get('movie_results', None)

		if movie_results and len(movie_results) > 0:

			movie = movie_results[0]
			movie_obj = tmdb.Movies(id = movie['id'])

			info = movie_obj.info()
			# genres = info['genres']
			title = info['original_title']
			imdb_id = info['imdb_id']
			# revenue = info['revenue']

			outfile = './files/{}_chargenders.tsv'.format(title.replace(' ', '_'))
	
			with open(outfile, 'w') as outpt:
				
				outpt.write("Title: {}\nIMDB: {}\n\n".format(title, imdb_id))

				cast = movie_obj.credits().get('cast', None)

				if cast:
					for c in cast:

						actorid = c['id']
						charname = c['character']
						actorname = c['name']

						actor = tmdb.People(id = actorid)
						gender = actor.info()['gender']

						outpt.write("{}\t{}\t{}\t{}\n".format(actorid, charname, actorname, gender))

			print("Done with {}".format(title))