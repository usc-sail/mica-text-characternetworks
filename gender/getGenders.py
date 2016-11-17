####################################################################################################################################
#
# Searches TMBD for the movie title and retrieve cast genders
# Author: VRMP
# Date: 11/16/16
#
####################################################################################################################################
import tmdbsimple as tmdb
from os.path import exists 

tmdb.API_KEY = 'fad36d118bb1596735ee7e46c92ac997'
search = tmdb.Search()

with open('./data/titles.txt') as titles:

	for title in titles:

		title = title.strip()

		if exists('./data/out/{}_chargenders.tsv'.format(title.replace(' ', '_'))):
			print("{} exists".format(title))
			continue

		movie = search.movie(query = title).get('results', None)

		if movie and len(movie) > 0:

			movie = movie[0]

			outfile = './data/out/{}_chargenders.tsv'.format(title.replace(' ', '_'))
	
			with open(outfile, 'w') as outpt:

				movie_obj = tmdb.Movies(id = movie['id'])

				info = movie_obj.info()
				# genres = info['genres']
				original_title = info['original_title']
				imdb_id = info['imdb_id']
				# revenue = info['revenue']

				outpt.write("Title: {}\nIMDB: {}\n\n".format(original_title, imdb_id))

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