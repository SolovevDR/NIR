import pandas as pd
import threading
import time

class save_df():
    def __init__(self):
        my_df = None

    def save_df(self, my_df):
        self.my_df = my_df

    def return_df(self):
        return  self.my_df

def read_line(example_class, line):
    separators = ['"', ' ', '[', ']']
    curretnSep = ''

    resultList = []
    newString = ''

    my_df = example_class.return_df()

    for s in line:
        if s in separators:
            if curretnSep == '':
                curretnSep = s
                if newString != '': resultList.append(newString)
                newString = ''
            elif curretnSep == s or curretnSep == '[' and s == ']':
                curretnSep = ''
                if newString != '': resultList.append(newString)
                newString = ''
            elif curretnSep == ' ':
                curretnSep = s
            elif (curretnSep == '"' or curretnSep == '[') and s == ' ':
                newString += s
        else:
            newString += s
    print(resultList)
    if len(resultList) != 0:
        newline = {'%h': resultList[0], '%l': resultList[1], '%u': resultList[2], '%t': resultList[3],
                   '%r': resultList[4], '%>s': resultList[5], '%b': resultList[6], '%{Referr}i': resultList[7],
                   '%{Useragent}i': resultList[8]}
        my_df = my_df.append(newline, ignore_index=True)
        example_class.save_df(my_df)

start_time = time.time()
col_names = ['%h', '%l', '%u', '%t', '%r', '%>s', '%b', '%{Referr}i', '%{Useragent}i']
my_df = pd.DataFrame(columns=col_names)
exaple_class = save_df()
exaple_class.save_df(my_df)

threads = []
k = 0

with open("1.txt") as infile:
    for line in infile:

        if k < 400:
            t = threading.Thread(target=read_line, args=(exaple_class, line,))
            t.start()
            threads.append(t)
        else:
            for thread in threads:
                thread.join()
                threads = []


my_df = exaple_class.return_df()

my_df.to_csv('file1.csv', header=True, sep=';')
end_time = time.time()
print('end time: ', end_time - start_time)

# with open("accessLog.txt") as infile:
#     for line in infile:
#         print(line)

# with open('accessLog.txt') as infile:
#     print(infile.read())

# col_names = ['%h', '%l', '%u', '%t', '%r', '%>s', '%b', '%{Referr}i', '%{Useragent}i']
# my_df  = pd.DataFrame(columns = col_names)
# print(my_df.head())


