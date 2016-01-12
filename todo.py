#! /usr/bin/python
import os
import pandas as pd
import itertools


count_ = itertools.count()
MODE_EXIT = count_.next()
MODE_LIST = count_.next()
MODE_SELECT = count_.next()
MODE_ADD = count_.next()
MODE_DEL = count_.next()
MODE_TOP = count_.next()
MODE_BOTTOM = count_.next()
MODE_DOWN = count_.next()
MODE_DONE = count_.next()

BARS = '---------'
MAX_PRINT = 10

ROOTDIR = '/home/ogawak/developper/setup_linux/todo'
CSV = os.path.join(ROOTDIR, 'todo.csv')
CSV_BKP = os.path.join(ROOTDIR, 'todo.csv~')
CSV_DONE = os.path.join(ROOTDIR, 'done.csv')

try:
    df = pd.read_csv(CSV, sep='\t', index_col=0)
    df.to_csv(CSV_BKP, sep='\t')
except:
    df = pd.DataFrame(columns=['task', 'status'])
mode = MODE_LIST
while mode != MODE_EXIT:
    if mode == MODE_LIST:
        os.system('clear')
        print BARS
        counter_ = 0
        for id_, row in df.iterrows():
            print id_, row[0]
            if counter_ == MAX_PRINT:
                input_ = raw_input(BARS + ' (s)skip: ')
                if input_ == 's':
                    break
                counter_ = 0
            else:
                print BARS
            counter_ += 1
        mode = MODE_SELECT
    elif mode == MODE_SELECT:
        input_ = raw_input('(a)add, (l)list, (d)delete, (t)top, (dw)down, (done), (e)exit :')
        if input_ == 'a':
            mode = MODE_ADD
        elif input_ == 'l':
            mode = MODE_LIST
        elif input_ in ['e','']:
            mode = MODE_EXIT
        elif input_ == 'd':
            mode = MODE_DEL
        elif input_ == 't':
            mode = MODE_TOP
        elif input_ == 'b':
            mode = MODE_BOTTOM
        elif input_ == 'dw':
            mode = MODE_DOWN
        elif input_ == 'done':
            mode = MODE_DONE
    elif mode == MODE_ADD:
        input_ = raw_input('task: ')
        if input_ == '':
            mode = MODE_LIST
        else:
            df = df.append(pd.DataFrame([input_], columns=['task']), ignore_index=True)
            df.to_csv('todo.csv', sep='\t')
    elif mode == MODE_DEL:
        id_delete = int(raw_input('id to delete: '))
        print str(df.loc[id_delete])
        input_ = raw_input('delete this?[y/N]: ')
        if input_ == 'y':
            df = df.drop([id_delete])
        mode = MODE_LIST
    elif mode == MODE_TOP:
        i = int(raw_input('id to bring top: '))
        reorder_ = [i] + range(i) + range(i+1, len(df))
        df = df.reindex(reorder_).reset_index(drop=True)
        df.to_csv(CSV, sep='\t')
        mode = MODE_LIST
    elif mode == MODE_BOTTOM:
        i = int(raw_input('id to bring bottom: '))
        reorder_ = range(i) + range(i+1, len(df)) + [i]
        df = df.reindex(reorder_).reset_index(drop=True)
        df.to_csv(CSV, sep='\t')
        mode = MODE_LIST
    elif mode == MODE_DOWN:
        input_ = raw_input('id to bring down: ').split(',')
        if len(input_) == 2:
            i, j= [int(x) for x in input_]
        else:
            i = int(input_[0])
            j = 1
        reorder_ = range(len(df))
        reorder_[i], reorder_[i+j] = reorder_[i+j], reorder_[i]
        df = df.reindex(reorder_).reset_index(drop=True)
        df.to_csv(CSV, sep='\t')
        mode = MODE_LIST
    elif mode == MODE_DONE:
        id_ = int(raw_input('id done: '))
        with open(CSV_DONE, 'a') as fa:
            df.loc[id_:id_].to_csv(fa, header=False)
        df = df.drop([id_])
        df = df.reset_index(drop=True)
        mode = MODE_LIST

df.to_csv(CSV, sep='\t')
