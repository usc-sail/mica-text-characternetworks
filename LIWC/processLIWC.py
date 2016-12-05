from VLIWC import VLIWC
from glob import iglob as glob 
from os.path import basename

vliwc = VLIWC(dict_file = "./LIWC2007_English131104.dic")
headers = sorted(list(vliwc.catDict.values()))

for script in glob("../data/utterances_with_charnames/*.txt"):
	with open("../data/LIWC_by_movie/LIWC_"+basename(script).replace(".txt", ".tsv"), 'w') as outpt:
		
		# Write headers
		outpt.write("SPEAKER\tNUM.WORDS\tWPS\t" + "\t".join(headers)+"\n")

		with open(script) as inpt:
			for line_num, line in enumerate(inpt):
				try:
					speaker, utt = line.strip().split(" => ")
					speaker = speaker.replace("\n", " ")

					measures = vliwc.processText(utt.strip())

					outpt.write("{}\t{}\t{}\t{}\n".format(speaker, measures['num_words'], measures['wps'], "\t".join([str(measures[h]) if h in measures else "0.0" for h in headers])))

				except Exception as e:
					print("File: {}\tLine: {} cannot be parsed".format(script, line_num))
					print(e)
					outpt.write("{}\t\n".format(speaker))

	print("Done with {}".format(script))

