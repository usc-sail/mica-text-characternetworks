import wikipedia
import re 

from nltk.tokenize import sent_tokenize

# Look for something like "is an English actor", "is an Indian actress", "is an actor"
exp_male = re.compile(r'is an?.*?actor')
exp_female = re.compile(r'is an?.*?actress')


with open('errors.txt') as e:
	for line in e:
		_,act = line.strip().split("\t")

		try:
			summ = wikipedia.summary(act)


			sentence = sent_tokenize(summ)

			t_male = exp_male.search(sentence[0])
			t_female = exp_female.search(sentence[0])

			if t_male is not None and t_female is None:
				print("{}\t2".format(act))
			elif t_male is None and t_female is not None:
				print("{}\t1".format(act))
			else:
				print("{}\t0".format(act))

			
		except:
			print("{}\t0".format(act))
			continue


		
