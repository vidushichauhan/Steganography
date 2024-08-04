DIT University Project

Steganography Website Project

Overview

This project is a web application built using Python and Django, designed to implement the Least Significant Bit (LSB) technique for steganography. Steganography is the practice of hiding secret data within non-secret files or messages to avoid detection. This application allows users to hide text data within image files, providing a secure way to embed sensitive information within seemingly innocuous images.

Features

- User-Friendly Interface:A clean and intuitive web interface for uploading images and inputting secret data.
- LSB Steganography: Utilizes the Least Significant Bit technique to encode and decode hidden messages within image files.
- Data Security: Ensures that the hidden data is not detectable through visual inspection of the image.
- Encoding and Decoding: Provides functionality for both hiding (encoding) data into images and extracting (decoding) hidden data from images.
- File Handling: Supports common image formats such as PNG and JPEG.

Technologies Used

- Backend:Python, Django
- Frontend: HTML, CSS, JavaScript
- Image Processing: Pillow (Python Imaging Library)

How to Use

1. Upload Image: Users can upload an image file in which they want to hide the data.
2. Input Secret Data: Users input the secret text data they wish to embed within the image.
3. Encode Data: The application processes the image and embeds the secret data using the LSB technique.
4. Download Encoded Image: Users can download the modified image file with the hidden data.
5. Decode Data: Users can upload an encoded image to extract and view the hidden data.


 Conclusion

This steganography web application provides a simple and effective way to hide and retrieve secret data within  files, making use of the LSB technique. It demonstrates the practical implementation of steganography in a web environment, combining the power of Python and Django with modern web technologies.


