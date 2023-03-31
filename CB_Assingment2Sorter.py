import json
import GenomeAligner
from multiprocessing import Process, cpu_count, Queue

if __name__ == "__main__":
    # inputData = {}
    inputData = []
    with open('testData.json', 'r') as f:
        data = json.load(f)
    # print(data)

    newest_individual = data[-1]
    # oldest_individual = data[0]
    # print(newest_individual)

    # Dictionary for checking correct order
    # correct_alignment = {}
    # for ind in data:
    #     string = ""
    #     for c in ind[1]:
    #         string += c
    #     ind[1] = string
    #     correct_alignment.update({ind[1]: ind[0]})

    # Create a sequence aligner object
    genomeLength = len(data[0][1])
    ga = GenomeAligner.GenomeAligner(genomeLength, genomeLength)

    # 
    sortedList = []
    current_closest = newest_individual

    number_tasks = len(data)
    num_processes = cpu_count()
    tasks_to_accomplish = Queue()
    tasks_complete = Queue()
    processes = []

    for i in data:
        tasks_to_accomplish.put(i)

    for w in range(num_processes):
        tasks_to_accomplish.put(None)
        p = Process(target=ga.find_best_match, args=(data, tasks_to_accomplish, tasks_complete))
        processes.append(p)
        p.start()


    for p in processes:
        p.join()

    while not tasks_complete.empty():
        sortedList.append(tasks_complete.get())

    print(sortedList)

    for ind in sortedList:
        newString = ""
        for c in ind[1]:
            newString += c
        ind[1] = newString
        print(ind)
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
