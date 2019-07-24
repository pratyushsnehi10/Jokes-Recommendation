import itertools
import csv
from collections import Counter

num_jokes=100
joke_id = []
jscore = 0
jid = 0
j_score = []

while True:
    jid, jscore = raw_input("Enter the joke id and your rating here (Enter 'n' 'n' to stop): ").split()
    if jid=='n':
        break
    else:
        joke_id.append(int(jid))
        j_score.append(float(jscore))

js=[]
with open('C:/Users/Pratyush/Desktop/7th sem/rs/joke_similarities.csv', 'r') as f:
    reader=csv.reader(f)
    joke_simi=[tuple(float(n) for n in line.split(",")) for line in f]
    length=len(joke_simi)

import numpy as np
c = 0
prediction={}
for j in xrange(1, 1+num_jokes):
    simi_sum = 0
    weighted_sum = 0
    for k in range(len(joke_id)):
        if(j==joke_id[k]):
            simi_sum = -1
            weighted_sum = 100
            break
        else:
            simi_sum += abs(joke_simi[c+np.int(joke_id[k]-1)][2])
            weighted_sum += joke_simi[c+np.int(joke_id[k]-1)][2]*j_score[k]
            
    c = c + 100
    predict= weighted_sum/simi_sum
    prediction[j]=float('%.2f'%predict)
from operator import itemgetter
prediction = sorted(prediction.items(), key=itemgetter(1), reverse = True)
print "\nYour jokes recommendation are"
print prediction[0:5]
print "\n"    
