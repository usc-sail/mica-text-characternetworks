from glob  import iglob as glob
from os.path import basename, exists

actors = {}
with open('fixed.txt') as inpt:
	for line in inpt:
		act, gender = line.strip().split("\t")
		actors[act] = gender


for f in glob("./files/*.tsv"):

	outfile = './files/corrected/' + basename(f)

	if exists(outfile):
		print(f + " exists")
		continue


	out = []
	with open(f) as inpt:

		# Read first 2 lines
		out.append(next(inpt).strip())
		out.append(next(inpt).strip())

		# start cast 
		for line in inpt:

			line = line.strip()

			if len(line) == 0:
				out.append(line)

			try:
				cast_id, charname, actname, gender = line.split("\t")

				if gender == "0" and actname in actors:
					out.append("{}\t{}\t{}\t{}".format(cast_id, charname, actname, actors[actname]))
				else:
					out.append(line)

			except:
				out.append(line)

	with open(outfile, 'w') as outpt:
		for line in out:
			outpt.write(line + "\n")

