import pandas as pd
import threading
import time
from apachelog import parser


class save_df():
    def __init__(self):
        my_df = None

    def save_df(self, my_df):
        self.my_df = my_df

    def return_df(self):
        return  self.my_df

def read_line(example_class, line):
    my_df = example_class.return_df()
    col_names = r'%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" \"%{X}i\"'

    logline_parser = parser(col_names)

    pars_line = logline_parser.parse(line)
    end_time = time.time()

    try:
        newline = {'%h': pars_line.get('%h'), '%l': pars_line.get('%l'), '%u': pars_line.get('%u'), '%t': pars_line.get('%t'),
                   '%r': pars_line.get('%r'), '%>s': pars_line.get('%>s'), '%b': pars_line.get('%b'), '%{Referr}i': pars_line.get('%{Referer}i'),
                   '%{Useragent}i': pars_line.get('%{User-Agent}i')}
        my_df = my_df.append(newline, ignore_index=True)
        example_class.save_df(my_df)
    except:
        pass

if __name__ == '__main__':
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

    my_df.to_csv('parse_accessLog.csv', header=True, sep=';')
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


