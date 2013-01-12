from image_processing import process_image
from webmakeup import get_image_from_url
import glob
import os

#RefImagePath = "testing/image.jpeg"
RefImagePath = "testing/ericProf.jpg"
CpntImageDir = "testing/ericPhotos"
FileFormats = ["jpg", "jpeg", "gif", "bmp", "png"]
MosaicFilename = "eric"

def LoadRefImage():
    return open(RefImagePath, "rb").read()

def LoadCpntImages():
    cpntImageStreams = []
    
    filenames = []
    for fmt in FileFormats:
        filenames.extend(glob.glob(CpntImageDir+'/*.'+fmt))
   
    for file in filenames:
        cpntImageStreams.append(open(file, "rb").read())

    return cpntImageStreams

def Test():
    refImageStream = LoadRefImage()
    cpntImageStreams = LoadCpntImages()
    mosaic = process_image(refImageStream, cpntImageStreams)
    outFile = open(MosaicFilename+".jpg", "wb")
    outFile.write(mosaic)
    outFile.close()

def FacebookTest():
    refImageStream = get_image_from_url(r'http://blogs-images.forbes.com/jonbruner/files/2011/07/facebook_logo.jpg')
    cpntImageStreams = LoadCpntImages()
    mosaic = process_image(refImageStream, cpntImageStreams)
    outFile = open("facebook.jpg", "wb")
    outFile.write(mosaic)
    outFile.close()

def HackTest():
    refImageStream = get_image_from_url(r'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-snc6/211085_364348883660343_553562280_n.jpg')
    cpntImageStreams = LoadCpntImages()
    mosaic = process_image(refImageStream, cpntImageStreams)
    outFile = open("hack.jpg", "wb")
    outFile.write(mosaic)
    outFile.close()

