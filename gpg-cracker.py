import string
import threading
import subprocess as sub
import os
import time
import argparse

base = []
found = False

def arguments():
    parser = argparse.ArgumentParser(description='Process some integers.') 
    parser.add_argument("-f", "--file", required = True,
                    help='file to crack')
    parser.add_argument("--max", required = True,
                    help='maximum of dictionary')
    parser.add_argument("-t","--thread", required = True,
                    help='number of threads')
    parser.add_argument('--charset', required=True,
                    help='charset of the passwords')

    args = parser.parse_args()
    return args

def create_base(lower, digits):
    global base
    if (lower == True and digits == True):
        base = list(string.ascii_lowercase + string.digits)
    elif (lower == True and digits == False):
        base = list(string.ascii_lowercase)
    elif (lower == False and digits == True):
        base = list(string.digits)
    else:
        base = list(string.ascii_lowercase)

    return base


def base_change(number, base):
   (d,m) = divmod(number,len(base))
   if d > 0:
      return base_change(d-1,base) + base[m]
   return base[m]

def decrypt(start, end, dfile):
    for num in range(start, end + 1):
        global found
        if found == True:
            time.sleep(2)
            exit()
        else:
            password = base_change(num, base)
            print(password)
            start = time.time()
            test = sub.run('echo {} | gpg --batch --yes --passphrase-fd 0 ./{}'.format(password, dfile), shell=True)
            end = time.time()
            print(end - start)
            if test.returncode is 0:
                print(str(threading.current_thread().name) + ' ha encontrado la contraseña!!')
                os.system('echo {} > results/pass.txt'.format(password))
                print('Cerrando hilos...')
                os.system('mv {} results/'.format(dfile[:-4]))
                time.sleep(2)
                found = True
            

if __name__ == '__main__':
    lower = digits = False

    args = arguments()
    dfile = args.file

    if args.charset == 'lower':
        lower = True
    elif args.charset == 'digits':
        digits = True
    elif args.charset == 'lower_digits':
        lower = True
        digits = True

    create_base(lower, digits)

    len_charset = int(args.max)
    print(len_charset)
    combinations = pow(len(base), len_charset)
    comb_per_thread = int(combinations) / 8

    start = 0
    end = int(comb_per_thread)

    threads = []
    os.system('mkdir -p results')
    for i in range(int(args.thread)):
        t = threading.Thread(name='Thread %s' %i, target=decrypt, args=(start, end, dfile), daemon=True)
        start += int(comb_per_thread) 
        end += int(comb_per_thread)

        threads.append(t)

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
