import os
import random

path = './rndimgdb'
retlist = []
for file_name in os.listdir(path):
    retlist.append(file_name)
retval = random.randint(0,len(retlist))
print(retlist[retval])