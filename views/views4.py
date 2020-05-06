from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image, ImageFile
from django.core.files import File
import sys
import time
import os
from django.core.files.storage import FileSystemStorage




import getopt, os, sys, math, struct, wave
import sys
from timeit import default_timer as timer





def tfaudiocode(request):
    if request.method == 'POST':
        uploaded_file1 = request.FILES['file1']  #textfile
        uploaded_file2 = request.FILES['file2']  #audiofile
        fs = FileSystemStorage()
        nameoffile1 = fs.save(uploaded_file1.name, uploaded_file1)
        nameoffile2 = fs.save(uploaded_file2.name, uploaded_file2)


        print("name1",uploaded_file1.name)
        print("name2",uploaded_file2.name)



        num_lsb = 2

        def prepare(sound_path):
            global sound, params, n_frames, n_samples, fmt, mask, smallest_byte
            sound = wave.open(sound_path, "r")
            print(sound)

            params = sound.getparams()
            #   print("params",params)
            num_channels = sound.getnchannels()
            # print("num_channels",num_channels)
            sample_width = sound.getsampwidth()
            # print("sample_width",sample_width)
            n_frames = sound.getnframes()
            #  print("n_frames",n_frames)
            n_samples = n_frames * num_channels
            # print("n_samples",n_samples)
            #
            #    print("hello")

            if (sample_width == 1):  # samples are unsigned 8-bit integers
                fmt = "{}B".format(n_samples)
                #  print("fmt",fmt)
                # Used to set the least significant num_lsb bits of an integer to zero
                mask = (1 << 8) - (1 << num_lsb)
                #  print("mask",mask)
                # The least possible value for a sample in the sound file is actually
                # zero, but we don't skip any samples for 8 bit depth wav files.
                smallest_byte = -(1 << 8)
            # print("smallest_byte",smallest_byte)
            elif (sample_width == 2):  # samples are signed 16-bit integers
                fmt = "{}h".format(n_samples)
                # print("fmt",fmt)
                # Used to set the least significant num_lsb bits of an integer to zero
                mask = (1 << 15) - (1 << num_lsb)
                # print(1<<15)
                # print(1<<num_lsb)
                # print("mask",mask)

                # The least possible value for a sample in the sound file
                smallest_byte = -(1 << 15)
            # print("smallest_byte",smallest_byte)

            else:
                # Python's wave module doesn't support higher sample widths
                raise ValueError("File has an unsupported bit-depth")

        def hide_data(sound_path, file_path, output_path):
            global sound, params, n_frames, n_samples, fmt, mask, smallest_byte
            # sound_path =input("SOUND FILE(with extension):")
            # file_path =input("SOURCE MESSAGE FILE (with extension):")
            # output_path =input(" OUTPUT SOUND FILE (with extension):")
            prepare(sound_path)
            # We can hide up to num_lsb bits in each sample of the sound file
            max_bytes_to_hide = (n_samples * num_lsb) // 8
            print("maxbytestohide", max_bytes_to_hide)
            filesize = os.stat(file_path).st_size
            print("filesize", filesize)

            if (filesize > max_bytes_to_hide):
                required_LSBs = math.ceil(filesize * 8 / n_samples)
                print(required_LSBs)
                raise ValueError("Input file too large to hide, "
                                 "requires {} LSBs, using {}"
                                 .format(required_LSBs, num_lsb))

            print("Using {} B out of {} B".format(filesize, max_bytes_to_hide))

            # Put all the samples from the sound file into a list
            # print(sound.readframes(n_frames))
            raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
            print("raw_data", raw_data[0:10])
            sound.close()

            input_data = memoryview(open(file_path, "rb").read())
            print("lenofinputdata", len(input_data))

            # The number of bits we've processed from the input file
            data_index = 0
            sound_index = 0

            # values will hold the altered sound data
            values = []
            buffer = 0
            buffer_length = 0
            done = False

            while (not done):
                while (buffer_length < num_lsb and data_index // 8 < len(input_data)):
                    # If we don't have enough data in the buffer, add the
                    # rest of the next byte from the file to it.
                    # print("data_index",data_index)
                    # print("data_index//8",data_index // 8)
                    # print("input_data",input_data[data_index // 8])
                    # print("buffer_length1",buffer_length)
                    buffer += (input_data[data_index // 8] >> (data_index % 8)
                               ) << buffer_length
                    # print("buffer1",buffer)
                    bits_added = 8 - (data_index % 8)
                    buffer_length += bits_added
                    # print("buffer_length2",buffer_length)
                    data_index += bits_added

                # Retrieve the next num_lsb bits from the buffer for use later
                current_data = buffer % (1 << num_lsb)
                # print("current_data",current_data)
                buffer >>= num_lsb
                # print("buffer2",buffer)
                buffer_length -= num_lsb
                # print("buffer_length3",buffer_length)

                while (sound_index < len(raw_data) and
                       raw_data[sound_index] == smallest_byte):
                    print("sound_index1", sound_index)
                    print("raw_data", raw_data[sound_index])
                    # If the next sample from the sound file is the smallest possible
                    # value, we skip it. Changing the LSB of such a value could cause
                    # an overflow and drastically change the sample in the output.
                    values.append(struct.pack(fmt[-1], raw_data[sound_index]))
                    # print("values1",values)
                    sound_index += 1

                if (sound_index < len(raw_data)):
                    # print("sound_index2",sound_index)
                    # print("currentsample1",raw_data[sound_index])
                    current_sample = raw_data[sound_index]
                    sound_index += 1

                    sign = 1
                    if (current_sample < 0):
                        # We alter the LSBs of the absolute value of the sample to
                        # avoid problems with two's complement. This also avoids
                        # changing a sample to the smallest possible value, which we
                        # would skip when attempting to recover data.
                        # print("currentsample2",current_sample)
                        current_sample = -current_sample
                        sign = -1

                    # Bitwise AND with mask turns the num_lsb least significant bits
                    # of current_sample to zero. Bitwise OR with current_data replaces
                    # these least significant bits with the next num_lsb bits of data.
                    altered_sample = sign * ((current_sample & mask) | current_data)
                    # print("alteredsample",altered_sample)

                    values.append(struct.pack(fmt[-1], altered_sample))
                    # print("values2",values)

                if (data_index // 8 >= len(input_data) and buffer_length <= 0):
                    done = True

            while (sound_index < len(raw_data)):
                # At this point, there's no more data to hide. So we append the rest of
                # the samples from the original sound file.
                values.append(struct.pack(fmt[-1], raw_data[sound_index]))
                sound_index += 1

            sound_steg = wave.open(output_path, "w")
            sound_steg.setparams(params)
            sound_steg.writeframes(b"".join(values))
            sound_steg.close()
            print("Data hidden over {} audio file".format(output_path))

        def recover_data(sound_path, output_path, num_lsb, bytes_to_recover):
            # Recover data from the file at sound_path to the file at output_path
            global sound, n_frames, n_samples, fmt, smallest_byte
            prepare(sound_path)

            # Put all the samples from the sound file into a list
            raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
            # Used to extract the least significant num_lsb bits of an integer
            mask = (1 << num_lsb) - 1
            output_file = open(output_path, "wb+")

            data = bytearray()
            sound_index = 0
            buffer = 0
            buffer_length = 0
            sound.close()

            while (bytes_to_recover > 0):

                next_sample = raw_data[sound_index]
                if (next_sample != smallest_byte):
                    # Since we skipped samples with the minimum possible value when
                    # hiding data, we do the same here.
                    buffer += (abs(next_sample) & mask) << buffer_length
                    buffer_length += num_lsb
                sound_index += 1

                while (buffer_length >= 8 and bytes_to_recover > 0):
                    # If we have more than a byte in the buffer, add it to data
                    # and decrement the number of bytes left to recover.
                    current_data = buffer % (1 << 8)
                    buffer >>= 8
                    buffer_length -= 8
                    data += struct.pack('1B', current_data)
                    bytes_to_recover -= 1

            output_file.write(bytes(data))
            output_file.close()
            print("Data recovered to {} text file".format(output_path))

        # sound_path = input("Enter input audio file name (with.wav extension)")
        # file_path = input("Enter text file")
        # output_path = input("Enter output audio file name (with .wav extension)")

        sound_path = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        sound_path = sound_path+"\\"
        sound_path = sound_path+uploaded_file2.name
        file_path = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"
        file_path = file_path+"\\"
        file_path = file_path+uploaded_file1.name
        output_path = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\newaudio111.wav"
        output_file = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\newaudiotest111.txt"

        filesize = os.stat(file_path).st_size
        # start1 = timer()
        print("filesize:",filesize)
        prepare(sound_path)
        hide_data(sound_path, file_path, output_path)
        # end1 = timer()
        # print("Encoding time=",end1-start1)
        # #output_file = input("Enter output text file name")
        # start2 = timer()
        recover_data(output_path, output_file, 2, filesize)
        # end2 = timer()
        # print("Decoding time=",end2-start2)

    return render(request, "t2audio.html")






def deaudiotextfile(request):
    if request.method == 'POST':

        def prepare(sound_path):
            global sound, params, n_frames, n_samples, fmt, mask, smallest_byte
            sound = wave.open(sound_path, "r")
            print(sound)

            params = sound.getparams()
            #   print("params",params)
            num_channels = sound.getnchannels()
            # print("num_channels",num_channels)
            sample_width = sound.getsampwidth()
            # print("sample_width",sample_width)
            n_frames = sound.getnframes()
            #  print("n_frames",n_frames)
            n_samples = n_frames * num_channels
            # print("n_samples",n_samples)
            #
            #    print("hello")

            if (sample_width == 1):  # samples are unsigned 8-bit integers
                fmt = "{}B".format(n_samples)
                #  print("fmt",fmt)
                # Used to set the least significant num_lsb bits of an integer to zero
                mask = (1 << 8) - (1 << num_lsb)
                #  print("mask",mask)
                # The least possible value for a sample in the sound file is actually
                # zero, but we don't skip any samples for 8 bit depth wav files.
                smallest_byte = -(1 << 8)
            # print("smallest_byte",smallest_byte)
            elif (sample_width == 2):  # samples are signed 16-bit integers
                fmt = "{}h".format(n_samples)
                # print("fmt",fmt)
                # Used to set the least significant num_lsb bits of an integer to zero
                mask = (1 << 15) - (1 << num_lsb)
                # print(1<<15)
                # print(1<<num_lsb)
                # print("mask",mask)

                # The least possible value for a sample in the sound file
                smallest_byte = -(1 << 15)
            # print("smallest_byte",smallest_byte)

            else:
                # Python's wave module doesn't support higher sample widths
                raise ValueError("File has an unsupported bit-depth")

        def recover_data(sound_path, output_path, num_lsb, bytes_to_recover):
            # Recover data from the file at sound_path to the file at output_path
            global sound, n_frames, n_samples, fmt, smallest_byte
            prepare(sound_path)

            # Put all the samples from the sound file into a list
            raw_data = list(struct.unpack(fmt, sound.readframes(n_frames)))
            # Used to extract the least significant num_lsb bits of an integer
            mask = (1 << num_lsb) - 1
            output_file = open(output_path, "wb+")

            data = bytearray()
            sound_index = 0
            buffer = 0
            buffer_length = 0
            sound.close()

            while (bytes_to_recover > 0):

                next_sample = raw_data[sound_index]
                if (next_sample != smallest_byte):
                    # Since we skipped samples with the minimum possible value when
                    # hiding data, we do the same here.
                    buffer += (abs(next_sample) & mask) << buffer_length
                    buffer_length += num_lsb
                sound_index += 1

                while (buffer_length >= 8 and bytes_to_recover > 0):
                    # If we have more than a byte in the buffer, add it to data
                    # and decrement the number of bytes left to recover.
                    current_data = buffer % (1 << 8)
                    buffer >>= 8
                    buffer_length -= 8
                    data += struct.pack('1B', current_data)
                    bytes_to_recover -= 1

            output_file.write(bytes(data))
            output_file.close()
            print("Data recovered to {} text file".format(output_path))

        uploaded_file2 = request.FILES['file5']  # containerfile
        fs = FileSystemStorage()

        nameoffile2 = fs.save(uploaded_file2.name, uploaded_file2)

        print("name2", uploaded_file2.name)

        string2 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static"  # path of sstego_message
        string2 = string2 + "\\"
        string2 = string2 + uploaded_file2.name
        print(string2)
        num_lsb = 2
        sound_path = string2
        output_path=r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\secretmessage.txt"
        filesize = 30

        recover_data(sound_path, output_path, num_lsb, filesize)






    return render(request,'deaudiotextfile.html')