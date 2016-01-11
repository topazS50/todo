import pandas as pd
import itertools


count_ = itertools.count()
MODE_EXIT = count_.next()
MODE_LIST = count_.next()
MODE_SELECT = count_.next()
MODE_ADD = count_.next()
MODE_DEL = count_.next()

try:
    df = pd.read_csv('todo.csv', sep='\t', index_col=0)
except:
    df = pd.DataFrame()
mode = MODE_LIST
while mode != MODE_EXIT:
    if mode == MODE_LIST:
        print df
        mode = MODE_SELECT
    elif mode == MODE_SELECT:
        input_ = raw_input('add, list, exit')
        if input_ == 'a':
            mode = MODE_ADD
        elif input_ == 'l':
            mode = MODE_LIST
        elif input_ == 'e':
            mode = MODE_EXIT
    elif mode == MODE_ADD:
        input_ = raw_input('task: ')
        df.append([input_], ignore_index=True)
        if input_ == '':
            mode = MODE_LIST

df.to_csv('todo.csv', sep=True)
