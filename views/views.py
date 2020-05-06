from django.http import HttpResponse
from django.shortcuts import render
from django.core.files import File
import wave
import sys
import time
from django.core.files.storage import FileSystemStorage


def index(request):
    return render(request, 'index.html')


def res1(request):
    imagestego = request.GET.get('imagestego','default1')
    print(imagestego)
    if imagestego != 'default1':
        return render(request, 'res1.html')

    audiostego = request.GET.get('audiostego', 'default2')
    print(audiostego)
    if audiostego != 'default2':
        return render(request, 'res2.html')

    videostego = request.GET.get('videostego', 'default4')
    print(videostego)
    if videostego != 'default4':
        return render(request, 'res4.html')

    textstego = request.GET.get('textstego', 'default3')
    print(textstego)
    if textstego != 'default3':
        return render(request, 'res3.html')




def tfimage(request):
    texts1 = request.GET.get('texts1', 'default5')
    print(texts1)
    if texts1 == 'on':
        return render(request, 'timage.html')

    textfile1 = request.GET.get('textfile1', 'default6')
    print(textfile1)
    if textfile1 == 'on':
        return render(request, 'tfimage.html')
    texts12 = request.GET.get('texts12', 'default13')
    print(texts12)
    if texts12 == 'on':
        return render(request, 'deimagetex.html')

    textfile12 = request.GET.get('textfile2', 'default14')
    print(textfile12)
    if textfile12 == 'on':
        return render(request, 'deimagetextfile.html')


def taudio(request):
    texts = request.GET.get('texts', 'default7')
    print(texts)
    if texts == 'on':
        return render(request, 'taudio.html')

    textfile = request.GET.get('textf', 'default8')
    print(textfile)
    if textfile == 'on':
        return render(request, 'tfaudio.html')

    texts1 = request.GET.get('texts1', 'default13')
    print(texts1)
    if texts1 == 'on':
        return render(request, 'deaudiotext.html')

    textfile1 = request.GET.get('textfile2', 'default14')
    print(textfile1)
    if textfile1 == 'on':
        return render(request, 'deaudiotextfile.html')


def ttext(request):
    texts = request.GET.get('texts', 'default9')
    print(texts)
    if texts == 'on':
        return render(request, 'ttext.html')

    textfile = request.GET.get('textfile', 'default10')
    print(textfile)
    if textfile == 'on':
        return render(request, 'tftext.html') #isme error aa skti h agr aai toh page name dekh lena

    texts1 = request.GET.get('texts1', 'default13')
    print(texts1)
    if texts1 == 'on':
        return render(request, 'detexttex.html')

    textfile1 = request.GET.get('textfile2', 'default14')
    print(textfile1)
    if textfile1 == 'on':
        return render(request, 'detexttexfile.html')


def tvideo(request):
    texts = request.GET.get('texts', 'default11')
    print(texts)
    if texts == 'on':
        return render(request, 'tvideo.html')

    textfile = request.GET.get('textfile', 'default12')
    print(textfile)
    if textfile == 'on':
        return render(request, 'tfvideo.html')

    texts1 = request.GET.get('texts1', 'default13')
    print(texts1)
    if texts1 == 'on':
        return render(request, 'devideotext.html')

    textfile1 = request.GET.get('textfile2', 'default14')
    print(textfile1)
    if textfile1 == 'on':
        return render(request, 'devideotextfile.html')



#def upload1(request):
 #   context = {}
  #  if request.method == 'POST':
   #     uploaded_file = request.FILES['file2']
    #    fs = FileSystemStorage()
     #   name = fs.save(uploaded_file.name,uploaded_file)
      #  context['url'] = fs.url(name)
   # return render(request, 'image1.html', context)
