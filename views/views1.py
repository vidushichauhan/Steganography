#                                                    for text image steganography
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image, ImageFile
from django.core.files import File
import wave
import sys
import time
from django.core.files.storage import FileSystemStorage

def upload1(request):
    context = {}
    context1 = {}
    bitsPerChar = 8
    bitsPerPixel = 3
    maxBitStuffing = 2
    extension = "png"
    if request.method == 'POST':

        def canEncode(message, image):
            width, height = image.size
            imageCapacity = width * height * bitsPerPixel
            messageCapacity = (len(message) * bitsPerChar) - (bitsPerChar + maxBitStuffing)
            return imageCapacity >= messageCapacity

        def createBinaryTriplePairs(message):
            binaries = list(
                "".join([bin(ord(i))[2:].rjust(bitsPerChar, '0') for i in message]) + "".join(['0'] * bitsPerChar))
            binaries = binaries + ['0'] * (len(binaries) % bitsPerPixel)
            binaries = [binaries[i * bitsPerPixel:i * bitsPerPixel + bitsPerPixel] for i in
                        range(0, int(len(binaries) / bitsPerPixel))]
            return binaries

        def embedBitsToPixels(binaryTriplePairs, pixels):
            binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar, '0') for p in pixel) for pixel in pixels]
            for i in range(len(binaryTriplePairs)):
                for j in range(len(binaryTriplePairs[i])):
                    binaryPixels[i][j] = list(binaryPixels[i][j])
                    binaryPixels[i][j][-1] = binaryTriplePairs[i][j]
                    binaryPixels[i][j] = "".join(binaryPixels[i][j])

            newPixels = [tuple(int(p, 2) for p in pixel) for pixel in binaryPixels]
            return newPixels

        def encodeLSB(message, imageFilename, newImageFilename):
            img = Image.open(imageFilename)
            size = img.size

            if not canEncode(message, img):
                return None

            binaryTriplePairs = createBinaryTriplePairs(message)

            pixels = list(img.getdata())
            newPixels = embedBitsToPixels(binaryTriplePairs, pixels)

            newImg = Image.new("RGB", size)
            newImg.putdata(newPixels)

            finalFilename = ".".join([newImageFilename, extension])
            newImg.save(finalFilename)

            return newImg

        uploaded_file = request.FILES['file2']
        fs = FileSystemStorage()
        nameoffile = fs.save(uploaded_file.name, uploaded_file)
        string = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        # print(string)
        string = string + "\\"
        string = string + uploaded_file.name

        context['url'] = fs.url(nameoffile)

        z1 = request.POST.get('textname')
        bitsPerChar = 8
        bitsPerPixel = 3
        maxBitStuffing = 2
        extension = "png"
        newImageFilename=r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\ImageTextEncoded"


        encodeLSB(z1, string, newImageFilename)

    return render(request, 'image1.html', context)

def deimagetext(request):
    if request.method == 'POST':
        def getLSBsFromPixels(binaryPixels):
            bitsPerChar = 8
            totalZeros = 0
            binList = []
            for binaryPixel in binaryPixels:
                for p in binaryPixel:
                    if p[-1] == '0':
                        totalZeros = totalZeros + 1
                    else:
                        totalZeros = 0
                    binList.append(p[-1])
                    if totalZeros == bitsPerChar:
                        return binList

        def decodeLSB(imageFilename):
            bitsPerChar = 8
            img = Image.open(imageFilename)
            pixels = list(img.getdata())
            binaryPixels = [list(bin(p)[2:].rjust(bitsPerChar, '0') for p in pixel) for pixel in pixels]
            binList = getLSBsFromPixels(binaryPixels)
            message = "".join([chr(int("".join(binList[i:i + bitsPerChar]), 2)) for i in range(0, len(binList) - bitsPerChar, bitsPerChar)])
            return message

        uploaded_file1 = request.FILES['file2']
        fs = FileSystemStorage()
        nameoffile = fs.save(uploaded_file1.name, uploaded_file1)
        string1 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        string1 = string1 + "\\"
        string1 = string1 + uploaded_file1.name
        # string1 = '"'+string1+'"'
        print(string1)
        imageFilename = string1

        message = decodeLSB(imageFilename)
        return HttpResponse(message)