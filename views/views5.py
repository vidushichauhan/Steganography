from django.http import HttpResponse
from django.shortcuts import render
from django.core.files import File
import wave
import sys
import time
from django.core.files.storage import FileSystemStorage

def stegotext(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file10']
        fs = FileSystemStorage()
        nameoffile = fs.save(uploaded_file.name, uploaded_file)
        text = request.POST.get('textname')
        print(nameoffile)
        print(uploaded_file.name)
        print(uploaded_file)
        #print(z1)
        context1={}

        string1 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        string1 = string1 + "\\"
        string1 = string1 + uploaded_file.name
        # string1 = '"'+string1+'"'
        print(string1)
        res = ''.join(format(i, 'b') for i in bytearray(text, encoding='utf-8'))  # coverting text into binary format
        # print(res)
        # print("The string after binary conversion : " + (res))
        length = len(res)
        print(length)

        file1 = open(string1, "r")
        file2 = open(r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\Steg.txt", "w+")

        count = 0
        while True:  # Coverting the text file to steg file
            # read line
            data = file1.readline()
            if (count < length):
                if (res[count] == '1') :  # if Current bit is one
                    data = data[0].lower() + data[1:]  # First letter of line converted to lowercase
            file2.write(data)
            count = count + 1
            if not data:
                break

    return render(request, 'ttext1.html')

def destegotext(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file15']
        fs = FileSystemStorage()
        nameoffile = fs.save(uploaded_file.name, uploaded_file)
        print(nameoffile)
        print(uploaded_file.name)
        print(uploaded_file)

        string1 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        string1 = string1 + "\\"
        string1 = string1 + uploaded_file.name
        # string1 = '"'+string1+'"'
        print(string1)

        crypto = ''
        file2 = open(string1, "r")
        while True:
            data = file2.readline()
            if not data:
                break
            if (data[0].isupper()):  # getting hidden message from text file by checking first letter in everyline is lower or upper case
                crypto = crypto + '0'
            else:
                crypto = crypto + '1'

        # print("Encrypted Code Bits:")
        # print(crypto)
        lengthcr = len(crypto)
        print(lengthcr)

        first = ''
        for i in range(0, lengthcr, 7):
            num = 0

            num = num + int(crypto[i + 0]) * 64
            if (i + 1 < lengthcr):
                num = num + int(crypto[i + 1]) * 32
            if (i + 2 < lengthcr):
                num = num + int(crypto[i + 2]) * 16
            if (i + 3 < lengthcr):
                num = num + int(crypto[i + 3]) * 8
            if (i + 4 < lengthcr):
                num = num + int(crypto[i + 4]) * 4
            if (i + 5 < lengthcr):
                num = num + int(crypto[i + 5]) * 2
            if (i + 6 < lengthcr):
                num = num + int(crypto[i + 6]) * 1
            if (num > 64):
                charac = chr(num)
                first = first + charac
            if (num == 0):
                break

        print(first)
        return HttpResponse(first)


