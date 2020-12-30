import argparse
import png

NB_OF_BITS = 8

def base10ToByte(val):  
    res = bin(val).replace("b", "") 
    zerosToAdd = NB_OF_BITS-len(res) 
    return zerosToAdd*"0"+res


def getPixelList(path):
    r=png.Reader(path)
    pix_list = []
    for row in r.asRGBA8()[2]:
        pix_list.append(list(row))
    return pix_list

def main():

        stringToHide = input("enter string to hide : ")
        asciiBinary = [base10ToByte(ord(c)) for c in stringToHide]
        print('ASCII',asciiBinary)
        file_path = input("Enter png path : ")
        pix_list = getPixelList(file_path)
        print('pixels',len(pix_list))

main()