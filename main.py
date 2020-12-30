import argparse
import png

NB_OF_BITS = 8

def base10ToByte(val):  
    res = bin(val).replace("b", "") 
    zerosToAdd = NB_OF_BITS-len(res) 
    return zerosToAdd*"0"+res



def main():

        stringToHide = input("enter string to hide : ")
        asciiBinary = [base10ToByte(ord(c)) for c in stringToHide]
        print('ASCII',asciiBinary)

main()