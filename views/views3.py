from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image, ImageFile
from django.core.files import File
import wave
import sys
import time

from django.core.files.storage import FileSystemStorage

def t1audio(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file4']
        fs = FileSystemStorage()
        nameoffile = fs.save(uploaded_file.name, uploaded_file)
        z1 = request.POST.get('textname')
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

        song = wave.open(string1, mode='rb')
        # Read frames and convert to byte array

        frame_bytes = bytearray(list(song.readframes(song.getnframes())))

        # The "secret" text message
        string =z1
        # Append dummy data to fill out rest of the bytes. Receiver shall detect and remove these characters.iski kya zaroorat h
        string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'
        # Convert text to bit array
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))

        # Replace LSB of each byte of the audio data by one bit from the text bit array
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        # Get the modified bytes
        frame_modified = bytes(frame_bytes)

        # Write bytes to a new wave audio file
        output_file = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\vidushi.wav"
        #f=FileSystemStorage()
        #fs.save(output_file,song)
        #context1['url']=fs.url(output_file)
        with wave.open(output_file, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)
        song.close()




        print(output_file + " Successfully Generated. \n")



    return render(request,"t1audio.html")

def deaudiotext(request):
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
        # Asks user for the file name
        input_file = string1
        song = wave.open(input_file, mode='rb')
        # Convert audio to byte array
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))

        # Extract the LSB of each byte
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        # Convert byte array back to string
        string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
        # Cut off at the filler characters
        decoded = string.split("###")[0]

        # Print the extracted text
        print("Sucessfully decoded: " + decoded)
        song.close()
        return HttpResponse(decoded)
