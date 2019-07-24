import csv
import math
import itertools
from collections import Counter

#Item-based collaborative filtering using cosine similarity

num_jokes=100
num_users=24983

userLines=None
with open('C:/Users/Pratyush/Desktop/7th sem/rs/jester.csv', 'r') as f:
    reader=csv.reader(f)
    userLines=list(reader)

jokesscore={}
userscore={}
usermean={}
for i in xrange(0,num_users):
    userscore[i]=map(float, userLines[i])
    sums=0
    notnull=0
    for j in xrange(1,1+num_jokes):
        if userscore[i][j]!=99:
            sums+=userscore[i][j]
            notnull+=1
    usermean[i]=sums/notnull
    if(i%1000 == 0):
        print [i,j]
vectorMagnitudes = {}
for j in xrange(1,1+num_jokes):
    jokesscore[j]=[]
    for i in xrange(0,num_users):
        if userscore[i][j] != 99:
            jokesscore[j].append(float(userLines[i][j])-usermean[i])
        else:
            jokesscore[j].append(usermean[i])
    temp=[x **2 if x!=99 else 0 for x in jokesscore[j]]
    vectorMagnitudes[j]=math.sqrt(sum(temp))
    if(j%10 == 0):
        print j

with open('C:/Users/Pratyush/Desktop/7th sem/rs/joke_similarities.csv', 'wb') as f:
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
        if(i%10 == 0):
            print i
            