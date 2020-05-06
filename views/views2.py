#                                                        for textfile image steganography
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image, ImageFile
from django.core.files import File
import sys
import time
import os
from django.core.files.storage import FileSystemStorage

# file = open("vidhi.txt",'r')
# text = file.read()
# print(text)

# string = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
# print(string)
# string = string + "\\"
# string = string + "vidhi.txt"
# print(string)
#
# file = open(string,'r')
# text = file.read()
# print(text)


def tfimagecode(request):
    context={}
    imageExtension = "png"
    bitsPerChar = 8
    bitsForSize = 32
    bitsPerPixel = 3
    fileSize = 0
    imageSize = 0
    if request.method == 'POST':

        # filename = "test.txt"
        # filename =  r"C:\Users\Vidushi Chauhan\Desktop\stego\test1.txt"
        imageExtension = "png"
        bitsPerChar = 8
        bitsForSize = 32
        bitsPerPixel = 3

        def canEncode(filename, imageName):
            fileSize = 0
            imageSize = 0
            extensionSize = len("".join(filename[filename.find("."):]))
            #    print("extension size ",extensionSize)
            sizeInfo = int(bitsForSize / bitsPerChar)
            #    print("size info ",sizeInfo)

            try:
                fileSize = os.path.getsize(filename)
            #       print("file size ",fileSize)
            except os.error:
                print("Could not find file %s." % filename)
                return False

            try:
                imageSize = os.path.getsize(imageName)
            #        print("image size ",imageSize)
            except os.error:
                print("Could not find file %s." % imageName)
                return False

            totalSize = extensionSize + sizeInfo + fileSize
            #    print("total size ",totalSize)
            return totalSize <= imageSize

        def getFileData(filename):
            inFile = None

            try:
                inFile = open(filename, "rb")
            except IOError:
                print("Could not open file %s." % filename)

            bytes = [l for line in inFile for l in line]
            # print("bytes ",bytes)
            binaries = [bin(b)[2:].rjust(bitsPerChar, '0') for b in bytes]
            # print("binaries ",binaries)
            binaries = "".join(binaries)
            # print("binaries again ", binaries)

            extension = filename[filename.find('.') + 1:]
            # print("extension " , extension)
            extension = [bin(ord(b))[2:].rjust(bitsPerChar, '0') for b in extension]
            # print("extension again " , extension)
            extension = "".join(extension) + '0' * bitsPerChar
            # print("extension again 2 ", extension)

            size = int(len(binaries) / bitsPerChar)
            # print("size " , size)
            size = [bin(size)[2:].rjust(bitsForSize, '0')]
            # print("size  aagain ",size)
            size = "".join(size) + '0' * bitsPerChar
            # print("size again 2 ",size)

            bitStuffing = (len(extension) + len(size) + len(binaries)) % bitsPerPixel
            # print("bit stuffing " ,bitStuffing)

            data = "".join([extension, size, binaries, '0' * bitStuffing])
            # print("data " , data)
            data = [data[i * bitsPerPixel: i * bitsPerPixel + bitsPerPixel] for i in
                    range(0, int(len(data) / bitsPerPixel))]
            # print("data " , data)

            return data

        def createNewPixels(imageFilename, data):
            img = Image.open(imageFilename)
            imgSize = img.size

            pixels = list(img.getdata())
            # print("pixels " , pixels)

            binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar, '0') for p in pixel) for pixel in pixels]

            for i in range(len(data)):
                for j in range(len(data[i])):
                    binaryPixels[i][j] = list(binaryPixels[i][j])
                    binaryPixels[i][j][-1] = data[i][j]
                    binaryPixels[i][j] = "".join(binaryPixels[i][j])

            newPixels = [tuple(int(p, 2) for p in pixel) for pixel in binaryPixels]
            #    print("new pixels ",newPixels)
            return newPixels, imgSize

        def encodeLSB(filename, imageFilename, newFilename):
            if canEncode(filename, imageFilename):
                data = getFileData(filename)
                newPixels, imgg = createNewPixels(imageFilename, data)

                # stegoImageFilename = ".".join([newFilename, imageExtension])
                stegoImageFilename = ".".join([newFilename])

                newImg = Image.new("RGB", imgg)
                newImg.putdata(newPixels)
                newImg.save(stegoImageFilename)

                return newImg
        uploaded_file1 = request.FILES['files1']
        uploaded_file2 = request.FILES['files2']
        fs = FileSystemStorage()
        nameoffile1 = fs.save(uploaded_file1.name, uploaded_file1)
        nameoffile2 = fs.save(uploaded_file2.name, uploaded_file2)
        context['url'] = fs.url(nameoffile2)
        string1 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        string1 = string1 + "\\"
        string1 = string1 + uploaded_file1.name
        string2 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        string2 = string2 + "\\"
        string2 = string2 + uploaded_file2.name

        filename=string1
        imaeFilename=string2
        newFilename=r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\helloyaar.png"

        encodeLSB(filename, imaeFilename, newFilename)


        return render(request,"tfimage1.html",context)

def deimagetextfile(request):

    if request.method == 'POST':
        uploaded_file1 = request.FILES['files']
        fs = FileSystemStorage()
        nameoffile = fs.save(uploaded_file1.name, uploaded_file1)
        #img = None
        newFile = None
        string1 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        string1 = string1 + "\\"
        string1 = string1 + uploaded_file1.name
        # string1 = '"'+string1+'"'
        print(string1)
        stegoFilename=string1
        imageExtension = "png"
        bitsPerChar = 8
        bitsForSize = 32
        bitsPerPixel = 3



        ################## Decoding functions #######################################

        def getLSBs(binaryPixels):
            return [p[-1] for pixel in binaryPixels for p in pixel]

        def getExtensionInfo(lsbPixels):
            extension = []
            currentIndex = 0
            for p in range(0, len(lsbPixels), bitsPerChar):
                letter = lsbPixels[p:p + bitsPerChar]
                letter = "".join(letter)
                if letter == "00000000":
                    currentIndex = currentIndex + bitsPerChar
                    break
                extension.append("".join(letter))
                currentIndex = currentIndex + bitsPerChar

            extension = "".join([chr(int(e, 2)) for e in extension])
            #    print("extension ",extension)
            return (extension, currentIndex)

        def getSizeInfo(lsbPixels, index):
            totalZeros = 0
            currentIndex = 0
            size = []
            for p in lsbPixels[index:]:
                if currentIndex == bitsForSize:
                    break
                size.append(p)
                currentIndex = currentIndex + 1
            size = int("".join(size), 2)
            return (size, index + currentIndex)

        def getData(lsbPixels, index, size):
            currentIndex = 0
            data = []
            for p in range(index, len(lsbPixels[index:]), bitsPerChar):
                if currentIndex == size * bitsPerChar:
                    break
                data.append("".join(lsbPixels[p:p + bitsPerChar]))
                currentIndex = currentIndex + bitsPerChar

            return (data[1:], currentIndex)

        def decodeLSB(stegoFilename, finalFilename):

            #img = None
            newFile = None

            try:
                img = Image.open(stegoFilename)
            except:
                print("Could not open file %s." % stegoFilename)
                return None

            pixels = list(img.getdata())
            binaryPixels = [(bin(p)[2:].rjust(bitsPerChar, '0') for p in pixel) for pixel in pixels]
            lsbPixels = getLSBs(binaryPixels)

            extension, currentIndex = getExtensionInfo(lsbPixels)
            size, currentIndex = getSizeInfo(lsbPixels, currentIndex)
            data, currentIndex = getData(lsbPixels, currentIndex, size)

            try:
                newFile = open(finalFilename, "wb")
            except IOError:
                print("Could not open file %s." % finalFilename)

            for d in data:
                newFile.write(bytes([int(d, 2)]))

        newFile = None
        string1 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        string1 = string1 + "\\"
        string1 = string1 + uploaded_file1.name
        # string1 = '"'+string1+'"'
        print(string1)
        s = string1
        imageExtension = "png"
        bitsPerChar = 8
        bitsForSize = 32
        bitsPerPixel = 3
        finalFilename=r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\hello.txt"

        decodeLSB(s, finalFilename)

    return render(request,'deimagetextfile.html')
