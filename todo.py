import os
import pandas as pd
import itertools
import subprocess
import re
import glob


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


count_ = itertools.count()
MODE_EXIT = count_.next()
MODE_LIST = count_.next()
MODE_SELECT = count_.next()
MODE_ADD = count_.next()
MODE_ADDTOP = count_.next()
MODE_DEL = count_.next()
MODE_TOP = count_.next()
MODE_BOTTOM = count_.next()
MODE_DOWN = count_.next()
MODE_DONE = count_.next()
MODE_PEND = count_.next()
MODE_EDIT = count_.next()
MODE_MOVE = count_.next()

BARS = '---------'
MAX_PRINT = 10
EDITOR = 'nano'

ROOTDIR = os.path.join(os.path.expanduser('~'), '.todo')
CSV = os.path.join(ROOTDIR, 'todo.csv')
CSV_BKP = os.path.join(ROOTDIR, 'todo.csv~')
CSV_DONE = os.path.join(ROOTDIR, 'done.csv')
CSV_PEND = os.path.join(ROOTDIR, 'pend.csv')


def fill_empty_cells(df):
    df[df['time_added'].isnull()]['time_added'] = df['time_updated']

def display_list(df):
    fill_empty_cells(df)
    df = df.sort_values(by='time_updated', ascending=False)
    df = df.reset_index(drop=True)
    os.system('clear')
    print BARS
    counter_ = 0
    for id_, row in df.iterrows():
        if id_ == 0:
            print bcolors.OKGREEN + str(id_) + ' ' + row[0] + ' ' + row[1] + bcolors.ENDC
        else:
            print id_, row[0], row[1]
        if counter_ == MAX_PRINT:
            input_ = raw_input(BARS + ' (s)skip: ')
            if input_ == 's':
                break
            counter_ = 0
        else:
            print BARS
        counter_ += 1


def now_():
    return pd.datetime.now().strftime("%Y%m%d.%H%M.%S.%f")


def add_item(df, input_):
    df = df.append(pd.DataFrame([[input_, now_(), now_()]], columns=['task', 'time_added', 'time_updated']), ignore_index=True)
    return df


mode_read = 0
def main():
    df = pd.DataFrame()
    try:
        if mode_read == 0:
            df = pd.read_csv(CSV, sep='\t', index_col=0)
        elif mode_read == 1:
            listdir_ = glob.glob(os.path.join(ROOTDIR, 'todo') + '/*.csv')
            for file_ in listdir_:
                df_in = pd.read_csv(file_, sep='\t')
                df = df.append(df_in)
            df = df.reset_index(drop=True)
    except:
        df = pd.DataFrame(columns=['task', 'status'])
    mode = MODE_LIST
    while mode != MODE_EXIT:
        if mode == MODE_LIST:
            display_list(df)
            mode = MODE_SELECT
        elif mode == MODE_SELECT:
            input_ = raw_input('(a)add, (at)add top, (l)list, (d)delete, (t)top, (dw)down, (done), (e)exit :')
            if input_ == 'a':
                mode = MODE_ADD
            elif input_ == 'at':
                mode = MODE_ADDTOP
            elif input_ == 'l':
                mode = MODE_LIST
            elif input_ in ['e', '']:
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
            elif input_ == 'pend':
                mode = MODE_PEND
            elif input_ == 'ed':
                mode = MODE_EDIT
        elif mode == MODE_ADD:
            input_ = raw_input('task: ')
            if input_ == '':
                mode = MODE_LIST
            else:
                # under dev
                df = add_item(df, input_)
                df.to_csv('todo.csv', sep='\t')
        elif mode == MODE_ADDTOP:
            input_ = raw_input('task: ')
            if input_ == '':
                mode = MODE_LIST
            else:
                df = add_item(df, input_)
                reorder_ = [len(df) - 1] + range(len(df) - 1)
                df = df.reindex(reorder_).reset_index(drop=True)
                df.to_csv('todo.csv', sep='\t')
        elif mode == MODE_DEL:
            id_delete = int(raw_input('id to delete: '))
            print str(df.loc[id_delete])
            input_ = raw_input('delete this?[y/N]: ')
            if input_ == 'y':
                df = df.drop([id_delete])
                df = df.reset_index(drop=True)
            mode = MODE_LIST
        elif mode == MODE_TOP:
            i = int(raw_input('id to bring top: '))
            reorder_ = [i] + range(i) + range(i+1, len(df))
            df = df.reindex(reorder_).reset_index(drop=True)
            df.loc[0, 'time_updated'] = now_()
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
                i, j = [int(x) for x in input_]
            else:
                i = int(input_[0])
                j = 1
            reorder_ = range(i) + range(i+1, i+j+1) + [i] + range(i+j+1, len(df))
            df = df.reindex(reorder_).reset_index(drop=True)
            df.to_csv(CSV, sep='\t')
            mode = MODE_LIST
        elif mode == MODE_DONE:
            id_ = int(raw_input('id done: '))
            with open(CSV_DONE, 'a') as fa:
                df.loc[id_, 'time_done'] = now_()
                df.loc[id_:id_].to_csv(fa, sep='\t', header=False)
            df = df.drop([id_])
            df = df.reset_index(drop=True)
            mode = MODE_LIST
        elif mode == MODE_PEND:
            id_ = int(raw_input('id done: '))
            with open(CSV_PEND, 'a') as fa:
                df.loc[id_:id_].to_csv(fa, header=False)
            df = df.drop([id_])
            df = df.reset_index(drop=True)
            mode = MODE_LIST
        elif mode == MODE_EDIT:
            id_ = int(raw_input('id edit: '))
            fileedit = re.sub('[ .,:]', '', df.loc[id_]['task'])
            subprocess.check_call(EDITOR + ' ' + os.path.join(ROOTDIR, fileedit), shell=True)
            mode = MODE_LIST

    for i in range(len(df)):
        basename = str(df.iloc[i]['time_added']) + '-' + str(df.iloc[i]['task']).replace('/', '_') + '.csv'
        df[i:i+1].to_csv(os.path.join(ROOTDIR, 'todo', basename), sep='\t', index=False)


if __name__ == '__main__':
    main()
