import os
from random import *

def permutations(word):
    if len(word)<=1:
        return [word]

    #get all permutations of length N-1
    perms=permutations(word[1:])
    char=word[0]
    result=[]
    #iterate over all permutations of length N-1
    for perm in perms:
        #insert the character into every possible location
        for i in range(len(perm)+1):
            result.append(perm[:i] + char + perm[i:])
    return result

name1 = "Meteor"
name2 = "Spinner"
perms1 = permutations(name1)
perms2 = permutations(name2)

numOfGames = int(10 + 10*random())

print "\n" + str(numOfGames) + " Games in 1!\n\n"

print "1. Meteor Survival"
print "2. Spinner"
print "3. Bob, the Builder"
print "4. Dash to Crash"

for i in range(5,numOfGames,2):
    print str(i) + ". " + perms1[int(random()*len(perms1))]
    print str(i+1) + ". " + perms2[int(random()*len(perms2))]

choice = input("Please pick a game: ")

if choice % 2 == 1:
    os.system("python Spinner.py")
else:
    os.system("java bob.jar")
