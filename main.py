from gen_alg import *
import matplotlib.pyplot as plt
import time
import pandas

problem = Problem()
csv = ''
compare_result = ''
batch_number = 4
probability = 0.3
algorithm = GeneticAlgorithm(batch_number, probability, problem)
x = []
y = []
start = time.time()
for i in range(10):
    if i == 0:
        algorithm.iterate()
        x.append(i)
        y.append(algorithm.get_best_solution().cost)
    for j in range(20):
        algorithm.iterate()
    x.append(i * 20 + 20)
    y.append(algorithm.get_best_solution().cost)
    output = 'Iteration: ' + str((i * 20 + 20)) + ',' + 'solution cost: ' + str(algorithm.get_best_solution().cost) + '\n'
    compare_result = str(batch_number) + ',' + str(probability) + ',' + str(algorithm.get_best_solution().cost) + '\n'
    line = str((i * 20 + 20)) + ',' + str(algorithm.get_best_solution().cost) + '\n'
    csv += line
    print(output)
end = time.time()
print(f'Time taken: {end-start} sec or {(end-start)/60} min')
plt.plot(x, y)
plt.xlabel(f'Batch_number: {batch_number}, probability: {probability}')
plt.show()

with open('result.csv', 'w') as file:
    file.write(csv)

with open('compare.csv', 'a+') as file:
    file.write(compare_result)


# a = [0, 2, 4, 6, 7, 8, 9]
# print(a[-1]) batch_number probability, result