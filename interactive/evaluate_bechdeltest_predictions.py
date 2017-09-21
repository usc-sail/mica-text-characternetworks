#!/users/anil/anaconda3/bin/python

import os
from sklearn.metrics import accuracy_score, f1_score

prediction_file = '../Results/predicted_both.txt'

predicted_passed = os.listdir('../Results/degree_central_graphs/bechdeltest_passed')
predicted_failed = os.listdir('../Results/degree_central_graphs/bechdeltest_failed')

predicted_passed = [x for x in predicted_passed if not x.startswith('Icon')]
predicted_failed = [x for x in predicted_failed if not x.startswith('Icon')]

with open('../Data/userpredicted_movies/userpredicted_passedmovies.txt') as inPtr:
    actual_passed = [x.strip().lower() for x in inPtr.readlines()]

with open('../Data/userpredicted_movies/userpredicted_failedmovies.txt') as inPtr:
    actual_failed = [x.strip().lower() for x in inPtr.readlines()]

#Write results to file
with open('../Results/predicted_passed.txt', 'w') as outPtr:
    outPtr.write('\n'.join(predicted_passed))

with open('../Results/predicted_failed.txt', 'w') as outPtr:
    outPtr.write('\n'.join(predicted_failed))

prediction_vec=[]
actual_vec=[]
with open('../Results/predicted_both.txt', 'w') as outPtr:
    common_movies = list(set(predicted_passed+predicted_failed).intersection(actual_passed+actual_failed))

    outPtr.write("movie\tprediction\tactual\n")
    for movie in common_movies:
        prediction=int(movie in predicted_passed)
        actual=int(movie in actual_passed)
        prediction_vec.append(prediction)
        actual_vec.append(actual)

        outPtr.write("%s\t%d\t%d\n" % (movie, prediction, actual))

print("Accuracy: %f" % (accuracy_score(prediction_vec, actual_vec)))
print("F1-score: %f" % (f1_score(prediction_vec, actual_vec)))
