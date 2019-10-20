import gnupg
import os
import sys
import threading
import signal
import time
import argparse

def createDictionary(min, max, lower, upper, number):
    letter = 'qwertyuiopasdfghjklzxcvbnm'
    numbers = '1234567890'
    dictt = ''

    if (upper==False and number==False and lower==False): dictt = letter
    if (upper==False and number == False and lower == True): dictt = letter
    if (upper==False and number == True and lower == False): dictt = numbers
    if (upper==False and number ==True and lower == True): dictt = numbers + letter
    if (upper==True and number == False and lower == False): dictt = letter.upper()
    if (upper==True and number == False and lower == True): dictt = letter.upper() +letter
    elif (upper==True and number == True and lower == False): dictt = letter.upper() + numbers
    elif (upper==True and number==True and lower==True): dictt = letter + letter.upper() + numbers

    print('Generating dictionary with: '+dictt)
    os.system('crunch '+min+' '+max+' '+dictt+' -o dict.txt')

if __name__ == '__main__':
    lower = upper = number = False
    #Arguments 
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
    
    args = vars(parser.parse_args())
    if args['upper']:
        upper = True
    if args['lower']:
        lower = True
    if args['number']:
        number = True
   
    createDictionary(args['min'],args['max'],lower, upper, number)