import argparse
import png

NB_OF_BITS = 8
NB_PX_PER_CHAR = 2
MAX_RGB = 255

# return the binary value in 8 bits of ascii
def base10ToByte(val):  
    res = bin(val).replace("b", "") 
    zerosToAdd = NB_OF_BITS-len(res) 
    return zerosToAdd*"0"+res

# this method is for getting pixels of the image
def getPixelList(path):
    r=png.Reader(path)
    pix_list = []
    for row in r.asRGBA8()[2]:
        pix_list.append(list(row))
    return pix_list
    
# check if is even number 
def isEven(v):
    return int(v)%2 == 0

# this method is for hiding the message into the png image
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

# test if the image support the length of message 
def isImageSupportMessage(pix_list,nbpx,stringToHide):
    return len(stringToHide)*nbpx < len(pix_list)*len(pix_list[0])

# saving the png image
def saveInPng(pix_list,fname):
    png.from_array(pix_list, 'RGBA').save(fname)
    print("save done")

# this method is for reading message
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

# this method is for decrypting message
def decryptBinaryAscii(binary_char_ascii):  
    str = ""
    for char in binary_char_ascii:
        str = str+chr(int(char,2))
    return str

parser = argparse.ArgumentParser()
parser.add_argument("-f",help="filename")
parser.add_argument("-w",help="write",action="store_true")
parser.add_argument("-t",help="text")
args = parser.parse_args()

def main():

    file_path = stringToHide = None
    if(args.f):
        file_path = args.f
    else:
        file_path = input("Enter png path : ")

    if not(args.w):
        pix_list = getPixelList(file_path)
        print("decrypted string: ",decryptBinaryAscii(readMeassageAlgo(pix_list)))
    else:
    
       if(args.t):
            stringToHide = args.t
       else:    
            stringToHide = input("enter string to hide : ")

       asciiBinary = [base10ToByte(ord(c)) for c in stringToHide]
       pix_list = getPixelList(file_path)
       
       if(isImageSupportMessage(pix_list,NB_PX_PER_CHAR,stringToHide)):
            hideMessageAlgo(pix_list,asciiBinary)
            saveInPng(pix_list,'result.png')
       else:
            print("not enougth space")

main()