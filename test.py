import csv
import time
from PrefixSpan import make_sequence ,find_frequent_item

start = time.time()
data= []
filename1 = 'C50S10T2.5N10000.ascii'
filename2 = 'abc.txt'
with open(filename2) as f:
    for line in f:
        line = line.replace('\n','')
        line = line.split(' ')
        while '' in line: line.remove('')
        data.append(line)

        
f = open('out.txt','w')
f.write('')
find_frequent_item(make_sequence(data),1,'')




end = time.time()
elapsed = end - start
print( "Time taken: ", elapsed, "seconds.")
