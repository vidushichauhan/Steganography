import argparse
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image, ImageFile
from django.core.files import File
import sys
import time
import os
from django.core.files.storage import FileSystemStorage





def upload3(request):
    if request.method == 'POST':
        uploaded_file1 = request.FILES['file1']  #messagefile
        uploaded_file2 = request.FILES['file2']  #containerfile
        fs = FileSystemStorage()
        nameoffile1 = fs.save(uploaded_file1.name, uploaded_file1)
        nameoffile2 = fs.save(uploaded_file2.name, uploaded_file2)
        print("name1",uploaded_file1.name)
        print("name2",uploaded_file2.name)
        string1 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static" #path of container
        string1 = string1 + "\\"
        string1 = string1 + uploaded_file1.name
        # string1 = '"'+string1+'"'
        print(string1)
        string2 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static" #path of sstego_message
        string2 = string2 + "\\"
        string2 = string2 + uploaded_file2.name
        # string1 = '"'+string1+'"'
        print(string2)


        path_to_container = string2
        path_to_message = string1
        key = ""
        ####################################################################################################################

        def convert_key(key):
            """Convert source key to cryptographic and steganographic keys"""
            if len(key) < 10:
                key = "fjJD2Yf3FNJ1933wy532fdsd30283HhfbFHEjsfgycurcn372t7f284dg2d27egf624"
                print(f"The entered key is less than 10 characters long.\n"
                      f"The default key is set: {key}")

            crypto_key = key[0:len(key) // 2]
            stego_key = key[len(key) // 2:]

            crypto_key_int = sum([ord(c) << (8 * x) for x, c in enumerate(reversed(crypto_key))])
            stego_key_int = sum([ord(c) << (8 * x) for x, c in enumerate(reversed(stego_key))])
            return crypto_key_int, stego_key_int

        # we transform the user key into cryptographic and steganographic keys
        crypto_key, stego_key = convert_key(key)   ##calling convert key

        def get_container(path):
            """Putting the contents of the file with the container in a variable"""
            with open(path, "r") as file:
                container = file.read()
            return container

        # extract container from file
        container = get_container(path_to_container)

        # extract message from file

        ########################## ENCODING #################################
        def get_message(path):
            """Putting the contents of a message file into a variable"""
            message = ""
            with open(path, "r") as file:
                for line in file:
                    for char in line:
                        if ord(char) == 10:
                            message += chr(13) + chr(10)
                        else:
                            message += char
            if not message:
                exit("Hidden message cannot be empty!")
            return message

        message = get_message(path_to_message)
        print(f"Secret message: \n{message}")

        class SpeckCipher(object):
            """Реализация шифра Speck"""

            def encrypt_round(self, x, y, k):
                """Раунд шифра Speck"""
                rs_x = ((x << (self.word_size - self.alpha_shift)) + (x >> self.alpha_shift)) & self.mod_mask
                add_sxy = (rs_x + y) & self.mod_mask
                new_x = k ^ add_sxy
                ls_y = ((y >> (self.word_size - self.beta_shift)) + (y << self.beta_shift)) & self.mod_mask
                new_y = new_x ^ ls_y
                return new_x, new_y

            def __init__(self, key):
                self.key_size = 128
                self.block_size = 128
                self.word_size = self.block_size >> 1
                self.rounds = 32
                self.mod_mask = (2 ** self.word_size) - 1
                self.mod_mask_sub = (2 ** self.word_size)
                self.beta_shift = 3
                self.alpha_shift = 8

                self.key = key & ((2 ** self.key_size) - 1)

                # генерируем список раундовых ключей
                self.key_schedule = [self.key & self.mod_mask]
                l_schedule = [(self.key >> (x * self.word_size)) & self.mod_mask for x in
                              range(1, self.key_size // self.word_size)]

                for x in range(self.rounds - 1):
                    new_l_k = self.encrypt_round(l_schedule[x], self.key_schedule[x], x)
                    l_schedule.append(new_l_k[0])
                    self.key_schedule.append(new_l_k[1])

            def encrypt(self, plaintext):
                """Метод шифрования блока исходного текста"""
                b = (plaintext >> self.word_size) & self.mod_mask
                a = plaintext & self.mod_mask

                b, a = self.encrypt_function(b, a)

                ciphertext = (b << self.word_size) + a
                return ciphertext

            def decrypt(self, ciphertext):
                """Метод расшифровывания блока шифр-текста"""
                b = (ciphertext >> self.word_size) & self.mod_mask
                a = ciphertext & self.mod_mask

                b, a = self.decrypt_function(b, a)

                plaintext = (b << self.word_size) + a
                return plaintext

            def encrypt_function(self, upper_word, lower_word):
                """Раундовая функция шифрования Speck"""
                x = upper_word
                y = lower_word

                for k in self.key_schedule:
                    rs_x = ((x << (self.word_size - self.alpha_shift)) + (x >> self.alpha_shift)) & self.mod_mask
                    add_sxy = (rs_x + y) & self.mod_mask
                    x = k ^ add_sxy
                    ls_y = ((y >> (self.word_size - self.beta_shift)) + (y << self.beta_shift)) & self.mod_mask
                    y = x ^ ls_y
                return x, y

            def decrypt_function(self, upper_word, lower_word):
                """Раундовая функция расшифровывания Speck"""
                x = upper_word
                y = lower_word

                for k in reversed(self.key_schedule):
                    xor_xy = x ^ y
                    y = ((xor_xy << (self.word_size - self.beta_shift)) + (xor_xy >> self.beta_shift)) & self.mod_mask
                    xor_xk = x ^ k
                    msub = ((xor_xk - y) + self.mod_mask_sub) % self.mod_mask_sub
                    x = ((msub >> (self.word_size - self.alpha_shift)) + (msub << self.alpha_shift)) & self.mod_mask
                return x, y




        # message encryption
        def encrypt_message(message, key):
            """Encrypt secret message"""
            encrypted_message = ""
            cipher = SpeckCipher(key)

            blocks_count = len(message) // 16 + 1
            ############################################################################################################
            def prepare_blocks(message):
                """Blocking a secret message"""
                blocks = []
                step = 16

                if len(message) % 16 == 0:
                    blocks_count = len(message) // 16
                    for i in range(blocks_count):
                        block = message[i * 16:step]
                        step += 16
                        blocks.append(block)
                    last_block = chr(128) + "0" * 15
                    blocks.append(last_block)
                else:
                    blocks_count = len(message) // 16 + 1
                    for i in range(blocks_count - 1):
                        block = message[i * 16:step]
                        step += 16
                        blocks.append(block)

                    last_block_count = 16 - (blocks_count * 16 - len(message))
                    last_block = message[(blocks_count - 1) * 16: (blocks_count - 1) * 16 + last_block_count] + \
                                 chr(128) + "0" * (blocks_count * 16 - len(message) - 1)
                    blocks.append(last_block)

                for i in range(len(blocks)):
                    blocks[i] = sum([ord(c) << (8 * x) for x, c in enumerate(reversed(blocks[i]))])
                return blocks

            ############################################################################################################
            blocks = prepare_blocks(message)

            for i in range(blocks_count):
                encrypted_block = cipher.encrypt(blocks[i])
                encrypted_message_bytes = bytearray.fromhex('{:08x}'.format(encrypted_block))
                for byte in encrypted_message_bytes:
                    encrypted_message += chr(byte)
            return encrypted_message

        message = encrypt_message(message, crypto_key)
        print(f"Encrypted message: {message}")

        def text2bin(message):
            """Convert text to binary"""
            return "".join(format(ord(ch), "08b") for ch in message)

        # convert message to double code
        message = text2bin(message)

        def check_container(container, message):
            """Checking Container Capacity"""
            if len(message) > container.count(" "):
                exit("The message will not fit in this container!")

        # checking container for message capacity
        check_container(container, message)

        def lin_rand_arr():
            """
        Pseudo random number generator"""
            global g_random_seed
            a = 52  # factor
            c = 65  # increment
            m = 71  # module
            g_random_seed = (a * g_random_seed + c) % m



        def stego_message(container, message, key):
            """Hiding a message in a container"""
            stego_container = ""
            p_container = 0  # pointer to character in container
            p_message = 0  # pointer to character in message

            global g_random_seed
            g_random_seed = key
            lin_rand_arr()

            stego_type = 1
            exit_flag = False
            while True:
                if exit_flag:
                    break

                count = g_random_seed
                while count > 0:
                    if container[p_container] == " ":
                        if stego_type == 1:
                            stego_container += chr(0x0) if message[p_message] == "1" else chr(0x20)
                        elif stego_type == 2:
                            stego_container += chr(0x0) if message[p_message] == "0" else chr(0x20)
                        p_message += 1
                        count -= 1
                    else:
                        stego_container += container[p_container]
                    p_container += 1

                    try:
                        message[p_message]
                    except IndexError:
                        exit_flag = True
                        stego_container += container[p_container:]
                        break

                stego_type = 1 if stego_type == 2 else 2
                lin_rand_arr()

            with open(r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\stego_container.txt", "w") as file:
                file.write(stego_container)



        # embedding a message in a container
        stego_message(container, message, stego_key)


        ###################################################################################################################




    return render(request, 'tftext1.html')

def detextfile(request):
    if request.method == 'POST':

        uploaded_file2 = request.FILES['file5']  #containerfile
        fs = FileSystemStorage()

        nameoffile2 = fs.save(uploaded_file2.name, uploaded_file2)

        print("name2",uploaded_file2.name)

        string2 = r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static" #path of sstego_message
        string2 = string2 + "\\"
        string2 = string2 + uploaded_file2.name
        print(string2)
        path_of_encoded_file = string2

        def get_container(path):
            """Putting the contents of the file with the container in a variable"""
            with open(path, "r") as file:
                container = file.read()
            return container

        def lin_rand_arr():
            """
        Pseudo random number generator"""
            global g_random_seed
            a = 52  # factor
            c = 65  # increment
            m = 71  # module
            g_random_seed = (a * g_random_seed + c) % m

        def destego_message(container, key):
            """Retrieving a message from a container"""
            message = ""
            last_byte = ""
            p_container = 0  # pointer to character in container
            num_of_spaces = 0

            global g_random_seed
            g_random_seed = key
            lin_rand_arr()

            stego_type = 1
            exit_flag = False
            while True:
                if exit_flag:
                    break

                count = g_random_seed
                while count > 0:
                    if len(last_byte) == 8:
                        if num_of_spaces >= 8 and (last_byte == "11111111" or last_byte == "00000000"):
                            exit_flag = True
                            break
                        message += last_byte
                        last_byte = ""
                    try:
                        if ord(container[p_container]) == 0x0:
                            last_byte += "1" if stego_type == 1 else "0"
                            count -= 1
                            num_of_spaces = 0

                        elif ord(container[p_container]) == 0x20:
                            last_byte += "0" if stego_type == 1 else "1"
                            count -= 1
                            num_of_spaces += 1
                    except IndexError:
                        exit_flag = True
                        break
                    p_container += 1

                stego_type = 1 if stego_type == 2 else 2
                lin_rand_arr()
            return message

        key = ""


        def convert_key(key):
            """Convert source key to cryptographic and steganographic keys"""
            if len(key) < 10:
                key = "fjJD2Yf3FNJ1933wy532fdsd30283HhfbFHEjsfgycurcn372t7f284dg2d27egf624"
                print(f"The entered key is less than 10 characters long.\n"
                      f"The default key is set: {key}")

            crypto_key = key[0:len(key) // 2]
            stego_key = key[len(key) // 2:]

            crypto_key_int = sum([ord(c) << (8 * x) for x, c in enumerate(reversed(crypto_key))])
            stego_key_int = sum([ord(c) << (8 * x) for x, c in enumerate(reversed(stego_key))])
            return crypto_key_int, stego_key_int

        crypto_key, stego_key = convert_key(key)

        container1 = get_container(path_of_encoded_file)
        message = destego_message(container1, stego_key)

        def bin2text(message):
            """Convert binary code to text"""
            res = ""
            step = 8
            for i in range(0, len(message), 8):
                res += chr(int(message[i:step], 2))
                step += 8
            return res

        class SpeckCipher(object):
            """Реализация шифра Speck"""

            def encrypt_round(self, x, y, k):
                """Раунд шифра Speck"""
                rs_x = ((x << (self.word_size - self.alpha_shift)) + (x >> self.alpha_shift)) & self.mod_mask
                add_sxy = (rs_x + y) & self.mod_mask
                new_x = k ^ add_sxy
                ls_y = ((y >> (self.word_size - self.beta_shift)) + (y << self.beta_shift)) & self.mod_mask
                new_y = new_x ^ ls_y
                return new_x, new_y

            def __init__(self, key):
                self.key_size = 128
                self.block_size = 128
                self.word_size = self.block_size >> 1
                self.rounds = 32
                self.mod_mask = (2 ** self.word_size) - 1
                self.mod_mask_sub = (2 ** self.word_size)
                self.beta_shift = 3
                self.alpha_shift = 8

                self.key = key & ((2 ** self.key_size) - 1)

                # генерируем список раундовых ключей
                self.key_schedule = [self.key & self.mod_mask]
                l_schedule = [(self.key >> (x * self.word_size)) & self.mod_mask for x in
                              range(1, self.key_size // self.word_size)]

                for x in range(self.rounds - 1):
                    new_l_k = self.encrypt_round(l_schedule[x], self.key_schedule[x], x)
                    l_schedule.append(new_l_k[0])
                    self.key_schedule.append(new_l_k[1])

            def encrypt(self, plaintext):
                """Метод шифрования блока исходного текста"""
                b = (plaintext >> self.word_size) & self.mod_mask
                a = plaintext & self.mod_mask

                b, a = self.encrypt_function(b, a)

                ciphertext = (b << self.word_size) + a
                return ciphertext

            def decrypt(self, ciphertext):
                """Метод расшифровывания блока шифр-текста"""
                b = (ciphertext >> self.word_size) & self.mod_mask
                a = ciphertext & self.mod_mask

                b, a = self.decrypt_function(b, a)

                plaintext = (b << self.word_size) + a
                return plaintext

            def encrypt_function(self, upper_word, lower_word):
                """Раундовая функция шифрования Speck"""
                x = upper_word
                y = lower_word

                for k in self.key_schedule:
                    rs_x = ((x << (self.word_size - self.alpha_shift)) + (x >> self.alpha_shift)) & self.mod_mask
                    add_sxy = (rs_x + y) & self.mod_mask
                    x = k ^ add_sxy
                    ls_y = ((y >> (self.word_size - self.beta_shift)) + (y << self.beta_shift)) & self.mod_mask
                    y = x ^ ls_y
                return x, y

            def decrypt_function(self, upper_word, lower_word):
                """Раундовая функция расшифровывания Speck"""
                x = upper_word
                y = lower_word

                for k in reversed(self.key_schedule):
                    xor_xy = x ^ y
                    y = ((xor_xy << (self.word_size - self.beta_shift)) + (xor_xy >> self.beta_shift)) & self.mod_mask
                    xor_xk = x ^ k
                    msub = ((xor_xk - y) + self.mod_mask_sub) % self.mod_mask_sub
                    x = ((msub >> (self.word_size - self.alpha_shift)) + (msub << self.alpha_shift)) & self.mod_mask
                return x, y



        def decrypt_message(encrypted_message, key):
            """Decryption of secret message"""
            decrypted_message = ""
            step = 16
            cipher = SpeckCipher(key)

            # print(len(encrypted_message))
            blocks_count = len(encrypted_message) // 16

            for i in range(blocks_count):
                block = encrypted_message[i * 16:step]

                encrypted_block_int = sum([ord(c) << (8 * x) for x, c in enumerate(reversed(block))])
                decrypted_block_int = cipher.decrypt(encrypted_block_int)
                decrypted_block_bytes = bytearray.fromhex('{:032x}'.format(decrypted_block_int))

                if i == blocks_count - 1:
                    for j in range(len(decrypted_block_bytes)):
                        if decrypted_block_bytes[j] == 0x80:
                            k = j
                    for j in range(0, k):
                        decrypted_message += chr(decrypted_block_bytes[j])
                else:
                    for j in range(len(decrypted_block_bytes)):
                        decrypted_message += chr(decrypted_block_bytes[j])
                step += 16

            return decrypted_message




        #
        # convert binary to decimal
        message = bin2text(message)
        # print(f"Encrypted message: {message}, \ nLength: {len (message)}")

        # decryption of secret message
        message = decrypt_message(message, crypto_key)

        def put_message(message):
            """Writing the extracted message to a file"""
            with open(r"C:\Users\Vidushi Chauhan\PycharmProjects\stegoproject\stego\stego\static\secret_message.txt", "w") as file:
                for char in message:
                    if ord(char) != 13:
                        file.write(char)



        # writing the extracted message to a file and displaying it on the screen
        put_message(message)
        print(f"Secret message2: \n{message}")

    return render(request, 'detexttexfile.html')