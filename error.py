import csv
import math

#Item-based collaborative filtering using cosine similarity

num_jokes=100
num_users=24983

userLines=None
with open('C:/Users/Pratyush/Desktop/7th sem/rs/jester.csv', 'r') as f:
    reader=csv.reader(f)
    userLines=list(reader)

train = userLines[:20000]

####### Training Model ###########

jokesscore={}
userscore={}
usermean={}
for i in xrange(0,len(train)):
    userscore[i]=map(float, train[i])
    sums=0
    notnull=0
    for j in xrange(1,1+num_jokes):
        if userscore[i][j]!=99:
            sums+=userscore[i][j]
            notnull+=1
    usermean[i]=sums/notnull

vectorMagnitudes = {}
for j in xrange(1,1+num_jokes):
    jokesscore[j]=[]
    for i in xrange(0,len(train)):
        if userscore[i][j] != 99:
            jokesscore[j].append(float(train[i][j])-usermean[i])
        else:
            jokesscore[j].append(usermean[i])
    temp=[x **2 if x!=99 else 0 for x in jokesscore[j]]
    vectorMagnitudes[j]=math.sqrt(sum(temp))

with open('C:/Users/Pratyush/Desktop/7th sem/rs/joke_similarities_train.csv', 'wb') as f:
    writer=csv.writer(f)
    jokes=list(jokesscore)
    for i, jokeA in enumerate(jokes):
        for jokeB in jokes[0:]:
            if(jokeA == jokeB):
                similarity = 1
                writer.writerow([jokeA, jokeB, '%.4f'%similarity])
            else:
                vectorA=jokesscore[jokeA]
                vectorB=jokesscore[jokeB]
                similarity=sum([a * b  if a!=99 and b!=99 else 0 for a, b in zip(vectorA, vectorB)])
                similarity/=vectorMagnitudes[jokeA] * vectorMagnitudes[jokeB]
                writer.writerow([jokeA, jokeB, '%.4f'%similarity])
                
########### Prediction ###########

test = userLines[20000:]
for j in range(len(test)):
    test[j].pop(0)

a = []
test_rating = []

for i in range(len(test)):
    a.append(list(enumerate(test[i], start = 1)))
    b = []
    for j in range(len(a[i])):
        if(a[i][j][1] != '99'):
            b.append(a[i][j])
        else:
            continue
    test_rating.append(b)

for i in range(len(test_rating)):
    test_rating[i].sort(key=lambda tup: tup[1], reverse = True)

test_id = []
rating_test = []
predict_id = []
rating_pred = []

for i in range(len(test_rating)):
    test_id.append([x[0] for x in test_rating[i][:20]])
    predict_id.append([x[0] for x in test_rating[i][20:]])
    rating_test.append([x[1] for x in test_rating[i][:20]])
    rating_pred.append([x[1] for x in test_rating[i][20:]])
        
with open('C:/Users/Pratyush/Desktop/7th sem/rs/joke_similarities_train.csv', 'r') as f:
    reader=csv.reader(f)
    joke_simi=[tuple(float(n) for n in line.split(",")) for line in f]
    length=len(joke_simi)

import numpy as np
prediction= []
for i in range(len(test_id)):
    simi_sum = 0
    weighted_sum = 0
    m = []        
    for j in range(len(predict_id[i])):
        for k in range(0,20):
            simi_sum += abs(joke_simi[(test_id[i][k]-1)*100 + predict_id[i][j]][2])
            weighted_sum += np.float(joke_simi[(test_id[i][k]-1)*100 + predict_id[i][j]][2]) *  np.float(rating_test[i][k])
        predict = weighted_sum/simi_sum
        m.append([predict_id[i][j],'%0.2f'%predict])
    prediction.append(m)
    if(i%100 == 0):
        print("Iteration numer %d" %i)
        
################# Error Calculation ###############
    
mae = 0    
rmse = 0
count = 0
for i in range(len(test_id)):
    d = 0
    e = 0
    for j in range(len(rating_pred[i])):
        d += abs(np.float(rating_pred[i][j]) - np.float(prediction[i][j][1]))
        e += d*d
    count += len(rating_pred[i])
    rmse += e
    mae += d/len(rating_pred[i])
mae = mae / len(test_id)
nmae = mae / 10.76
rmse = np.sqrt(rmse / (count*len(test_id)))
print("The mean absolute error is: %f"%mae)
print("The root mean square error is: %f"%rmse)
print("The normalized mean absolute error is: %f"%nmae)
