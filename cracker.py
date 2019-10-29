import gnupg
import os
import sys
import threading
import signal
import time
import argparse
import string

found = False

def arguments():
    parser = argparse.ArgumentParser(description='Process some integers.') 
    parser.add_argument("-f", "--file",required = True,
                    help='file to crack')
    parser.add_argument("--min",required = True,
                    help='minimum of dictionary')
    parser.add_argument("--max",required = True,
                    help='maximum of dictionary')
    parser.add_argument("-t","--thread",required = True,
                    help='number of threads')
    parser.add_argument('-l','--lower',action='store_true',help='add minus to')
    parser.add_argument("-u", "--upper",action='store_true',
                    help='add mayus to')
    parser.add_argument("-n", "--number",action='store_true',
                    help='add number to dictionary')

    args = parser.parse_args()
    return args

def createDictionary(min, max, lower, upper, number):
    letter = 'qwertyuiopasdfghjklzxcvbnm'
    numbers = '1234567890'
    dictt = ''

    if (upper==False and number==False and lower==False): dictt = letter
    if (upper==False and number == False and lower == True): dictt = letter
    if (upper==False and number == True and lower == False): dictt = numbers
    if (upper==False and number ==True and lower == True): dictt = numbers + letter
    if (upper==True and number == False and lower == False): dictt = letter.upper()
    if (upper==True and number == False and lower == True): dictt = letter.upper() + letter
    elif (upper==True and number == True and lower == False): dictt = letter.upper() + numbers
    elif (upper==True and number==True and lower==True): dictt = letter + letter.upper() + numbers

    print('Generating dictionary with: '+dictt)
    os.system('crunch '+min+' '+max+' '+dictt+' -o dict.txt')

def decrypt(gpg, file_encrypted, password):
    start = time.time()
    with open(file_encrypted, 'rb') as f:
        status = gpg.decrypt_file(f, passphrase=password, always_trust=True, output='gpg_mensaje_descifrado')
    end = time.time()
    print(end - start)
    if status.ok:
        return True


def search(inicio, final, dicc, pass_por_hilo, file_encrypted, gpg):
    for ps in dicc[int(inicio):int(final) + int(pass_por_hilo)]:
        global found
        if found:
            time.sleep(2)
            exit()
        else:
            status = decrypt(gpg, file_encrypted, ps)
            if status == True:
                print(str(threading.current_thread().name) + ' ha encontrado la contraseña')
                os.system('echo ' + ps + ' > results/pass.txt')
                print('Cerrando hilos...')
                os.system('mv gpg_mensaje_descifrado results/')
                time.sleep(2)
                found = True


if __name__ == '__main__':
    lower = upper = number = False
    #Arguments
    args = arguments()
    gpg = gnupg.GPG()
    archivo = args.file

    if args.upper:
        upper = True
    if args.lower:
        lower = True
    if args.number:
        number = True
   
    createDictionary(args.min, args.max, lower, upper, number)
    os.system('mkdir -p results')
    f = open('dict.txt', 'r')
    dicc = f.read().splitlines()
    n_pass = len(dicc)
    
    pass_por_hilo = n_pass / int(args.thread)
    inicio = 0
    final = pass_por_hilo

    threads = []
    print('Hola')

    for i in range(int(args.thread)):
        t = threading.Thread(name='Thread %s' %i, target=search, args=(inicio, final, dicc, pass_por_hilo, args.file, gpg), daemon=True)
        inicio += pass_por_hilo
        final += pass_por_hilo
        threads.append(t)

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
