import json
import GenomeAligner
import random

with open('testData.json', 'r') as f:
    data = json.load(f)

newest_individual = data[-1]

# random.shuffle(data)



# Create a sequence aligner object
genomeLength = len(data[0][1])
ga = GenomeAligner.GenomeAligner(genomeLength, genomeLength)

# 
sortedList = []
current_closest = newest_individual


while current_closest != None:
    sortedList.append(current_closest)
    print(f"Removing {current_closest}")
    data.remove(current_closest)
    # print(current_closest)
    next_closest = ga.find_best_match(current_closest, data)
    if(next_closest != None):
        current_closest.append(next_closest[0])
    current_closest = next_closest

# print(sortedList)
sortedList = sortedList[::-1]
# 
sortedList.sort(key=lambda x:x[0])

for ind in sortedList:
    print(ind)


    # newString = ""
    # for c in ind[1]:
        # newString += c
    # ind[1] = newString
# while len(data) >= 0:
    # sortedList.append(current_closest)
    # data.remove(current_closest)
    # print(current_closest)
    # current_closest = ga.find_best_match(current_closest, data)

# print(sortedList)

# for i in range(0, len(data)):
#     data[i].append(ga.calc_alignscore(data[i][1], newest_individual[1]))


# for i in range(0, len(data)):
#     print(data[i][0], data[i][3])
# data.sort(key= lambda x:x[3])
# for i in range(0, len(data)):
#     data[i].append(i*3)
#     print(int(data[i][4])-int(data[i][0]), data[i][3])

# def col_average(arr, column):
#     total = 0
#     for i in arr:
#         diff = i[4] - i[0]
#         total += diff if diff > 0 else -1 * diff
#     return total / len(data)

# print(col_average(data, ))
# while len(data) >= 0:
    # sortedList.append(newest_individual)
    # data.remove(newest_individual)
    # match_score = None
    # for i in data:
        # data[i].append(ga.calc_alignscore(data[i][1], newest_individual[1]))
# ga.print_best_alignment()
