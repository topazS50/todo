import pandas as pd
import itertools


count_ = itertools.count()
MODE_EXIT = count_.next()
MODE_LIST = count_.next()
MODE_SELECT = count_.next()
MODE_ADD = count_.next()
MODE_DEL = count_.next()
MODE_TOP = count_.next()

BARS = '---------'
MAX_PRINT = 10

try:
    df = pd.read_csv('todo.csv', sep='\t', index_col=0)
    df.to_csv('todo.csv~', sep='\t')
except:
    df = pd.DataFrame(columns=['task'])
mode = MODE_LIST
while mode != MODE_EXIT:
    if mode == MODE_LIST:
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
        input_ = raw_input('(a)add, (l)list, (d)delete, (t)top, (e)exit :')
        if input_ == 'a':
            mode = MODE_ADD
        elif input_ == 'l':
            mode = MODE_LIST
        elif input_ == 'e':
            mode = MODE_EXIT
        elif input_ == 'd':
            mode = MODE_DEL
        elif input_ == 't':
            mode = MODE_TOP
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
        df.to_csv('todo.csv', sep='\t')
        mode = MODE_LIST
df.to_csv('todo.csv', sep='\t')
