import csv
import time
from PrefixSpan import make_sequence ,find_frequent_item

start = time.time()
data= []

with open('abc.txt') as f:
    for line in f:
        line = line.replace('\n','')
        line = line.split(' ')
        while '' in line: line.remove('')
        data.append(line)

        
f = open('sequent_done.txt', 'w')

f.write(str(find_frequent_item(make_sequence(data),2,'')))
f.close()

end = time.time()
elapsed = end - start
print( "Time taken: ", elapsed, "seconds.")
