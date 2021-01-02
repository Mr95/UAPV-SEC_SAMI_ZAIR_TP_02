import argparse
import png

NB_OF_BITS = 8
NB_PX_PER_CHAR = 2
MAX_RGB = 255

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

def isEven(v):
    return int(v)%2 == 0

def hideMessageAlgo(pix_list,asciiBinary):
    cptB = cptC = 0
    i=0
    while i<len(pix_list):
        j=0
        while j<len(pix_list[i]):
            if(cptB >= NB_OF_BITS):
                if(cptC+1 < len(asciiBinary)):
                    cptC += 1
                    cptB = 0
                    if(not(isEven(pix_list[i][j]))): 
                        if(pix_list[i][j] == MAX_RGB):
                            pix_list[i][j] -= 1
                        else:
                            pix_list[i][j] += 1
                else:
                    if(isEven(pix_list[i][j])): 
                        if(pix_list[i][j] == MAX_RGB):
                            pix_list[i][j] -= 1
                        else:
                            pix_list[i][j] += 1
                    return
            else:
                if(isEven(asciiBinary[cptC][cptB])):
                    if(not(isEven(pix_list[i][j]))): 
                        if(pix_list[i][j] == MAX_RGB):
                            pix_list[i][j] -= 1
                        else:
                            pix_list[i][j] += 1
                else:
                    if(isEven(pix_list[i][j])): 
                        if(pix_list[i][j] == MAX_RGB):
                            pix_list[i][j] -= 1
                        else:
                            pix_list[i][j] += 1
                cptB += 1
            j=j+1
        i=i+1

def isImageSupportMessage(pix_list,nbpx,stringToHide):
    return len(stringToHide)*nbpx < len(pix_list)*len(pix_list[0])
        
def saveInPng(pix_list,fname):
    png.from_array(pix_list, 'RGBA').save(fname)
    print("save done")

def readMeassageAlgo(pix_list):
    cptB = cptC = 0
    asciiBinary = [""]
    i=0
    while i<len(pix_list):
        j=0
        while j<len(pix_list[i]):
            if(cptB >= NB_OF_BITS):
                if(isEven(pix_list[i][j])):
                    cptC = cptC + 1
                    asciiBinary.append("") 
                    cptB = 0            
                else:
                    return asciiBinary     
            else:
                if(not(isEven(pix_list[i][j]))): 
                    asciiBinary[cptC] = asciiBinary[cptC] + "1"
                else:
                    asciiBinary[cptC] = asciiBinary[cptC] + "0"
                cptB = cptB + 1
            
            j=j+1
        i=i+1
    return asciiBinary

def decryptBinaryAscii(binary_char_ascii):  
    str = ""
    for char in binary_char_ascii:
        str = str+chr(int(char,2))
    return str

def main():

        stringToHide = input("enter string to hide : ")
        asciiBinary = [base10ToByte(ord(c)) for c in stringToHide]
        print('ASCII',asciiBinary)
        file_path = input("Enter png path : ")
        pix_list = getPixelList(file_path)
        print('pixels',len(pix_list))

        if(isImageSupportMessage(pix_list,NB_PX_PER_CHAR,stringToHide)):
            hideMessageAlgo(pix_list,asciiBinary)
            saveInPng(pix_list,'test.png')
        else:
            print("not enougth space")

        file_path = input("Enter png to decode : ")
        pix_list = getPixelList(file_path)
        print("decrypted string: ",decryptBinaryAscii(readMeassageAlgo(pix_list)))
main()