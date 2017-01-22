from VLIWC import VLIWC
from glob import iglob as glob 
from os.path import basename
from collections import defaultdict
from joblib import delayed, Parallel

def processFile(script, vliwc, zero_dict, headers):
	with open("../data/LIWC_by_movie/LIWC_"+basename(script).replace(".txt", ".tsv"), 'w') as outpt:
		
		# Write headers
		outpt.write("SPEAKER\tNUM.WORDS\tWPS\t" + "\t".join(headers)+"\n")

		with open(script) as inpt:
			for line_num, line in enumerate(inpt):
				try:
					speaker, utt = line.strip().split("=>")
					speaker = speaker.replace("\n", " ").strip()
					utt = utt.strip()

					if len(utt) > 0:
						measures = vliwc.processText(utt.strip())
					else:
						measures = zero_dict


				except Exception as e:
					print("File: {}\tLine: {} cannot be parsed".format(script, line_num))
					measures = zero_dict

				outpt.write("{}\t{}\t{}\t{}\n".format(speaker, measures['num_words'], measures['wps'], "\t".join([str(measures[h]) if h in measures else "0.0" for h in headers])))

	print("Done with {}".format(script))

if __name__ == '__main__':
	zero_dict = defaultdict(int)
	vliwc = VLIWC(dict_file = "./LIWC2007_English131104.dic")
	headers = sorted(list(vliwc.catDict.values()))
	Parallel(n_jobs = 4, verbose = 1)(delayed(processFile)(script, vliwc, zero_dict, headers) for script in glob("../data/utterances_with_charnames/*.txt"))
	
