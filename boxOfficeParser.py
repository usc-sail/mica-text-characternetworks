import requests
from lxml import html 
from urllib.request import urlopen
import re 
import logging 

logging.basicConfig(format='%(asctime)s %(message)s', level = logging.INFO)

names = {}
with open("./data/speakersWithCharacterInfo/names.txt") as inpt:
	for line in inpt:
		id, *movie = line.strip().split(": ", 2)
		q = ": ".join(movie)

		# Heuristics on name
		# If name contains coma, and it is not Body, Rest & Motion or 
		# Synecdoche, New York then place after comma first
		if "," in q:
			before, after = q.rsplit(',', 1)

			if "New York" not in after or \
			   "Rest & Motion" not in after or \
			   "Wanda" not in after or \
			   "Stupid" not in after:
				q = after.strip() + " " + before.strip()
				logging.info("New title: {}".format(q))

		q = "http://www.boxofficemojo.com/search/?q={}".format(q)

		names[id] = q

# Load the ones already found
found = {}
with open("./data/boxoffice.txt") as inpt:
	for line in inpt:
		id,_,_ = line.strip().split("\t")
		found[id] = line

logging.info("Previously found: {}".format(len(found.keys())))

mov_link = re.compile('/movies/\?id=(.*)\.htm')
exp = re.compile("Domestic Total Gross: <b>(.*?)</b>")

boxoffices = set()
with open('./data/boxoffice.txt', 'w') as outpt: 

	# Write the ones already found 
	for id, line in found.items():
		outpt.write("{}".format(line))
		boxoffices.add(id)


	for id, q in names.items():
		logging.info("Requesting: {}".format(id))

		search = requests.get(q).text 
		
		# Get links that points to movies
		for mov in mov_link.findall(search):

			if mov not in boxoffices:
				url = "http://www.boxofficemojo.com/movies/?id={}.htm".format(mov)
				page = requests.get(url).text

				gross = exp.findall(page)

				if len(gross) > 0:
					outpt.write("{}\t{}.htm\t{}\n".format(id, mov, gross[0]))
					outpt.flush()

				boxoffices.add(mov)