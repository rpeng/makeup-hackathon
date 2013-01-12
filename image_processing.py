from PIL import Image
from StringIO import StringIO
from math import sqrt
from roygbiv import *
from random import random, seed, randint
from time import time

#Image dimension in terms of subimages (along smallest dimension)
minDimSize = 70

def GetImageColour(image):
    roy = Roygbiv(image)
    return roy.get_average_rgb()

def ColourDistance(x, y):
    return ColourDistance1(x, y)

def ColourDistance0(x, y):
    # Euclidian Distance
    assert len(x) == len(y)
    return sqrt(sum(((i-j)**2 for (i, j) in zip(x, y))))

def ColourDistance1(x, y):
    # Ranges from 0 to 765
    assert len(x) >= 3 and len(y) >= 3
    rmean = (x[0]+y[0])/2
    r=x[0]-y[0]
    g=x[1]-y[1]
    b=x[2]-y[2]
    return sqrt((((512+rmean)*r*r)>>8) + 4*g*g + (((767-rmean)*b*b)>>8))

def DecideToReplace(bestDist, newDist):
    # return newDist < bestDist
    delta = (bestDist - newDist)
    mark = (1.0 + delta / (1.0 + abs(delta))) / 2.0
    return random() < mark
    

def MapComponents(mainImage, subImageColours):
    assert len(subImageColours) > 0
    
    pix = mainImage.load()
    width, height = mainImage.size
    mappingArray = []

    for i in xrange(width):
        mappingArray.append([])
        for j in xrange(height):
            currColour = pix[i, j]
            subImageIndex = 0
            bestDist = ColourDistance(currColour, subImageColours[0])

            split = randint(0, len(subImageColours) - 1)
            k = split

            while True:
                #print k, split
                newDist = ColourDistance(currColour, subImageColours[k])
                if DecideToReplace(bestDist, newDist):
                    bestDist = newDist
                    subImageIndex = k
                k += 1
                if (k == len(subImageColours)):
                    k = 0
                if (k == split):
                    break
                

            #mid = randint(0, len(subImageColours))
            #for k in range(mid, len(subImageColours)) + range(mid):
            #    newDist = ColourDistance(currColour, subImageColours[k])
            #    if DecideToReplace(bestDist, newDist):
            #        bestDist = newDist
            #        subImageIndex = k
                    
            mappingArray[i].append(subImageIndex)

    return mappingArray

def construct_image(subimage_array, mapping_array):
    final_im=Image.new('RGB', (len(mapping_array)*25,
    len(mapping_array[0])*25))
            
    for i in range(len(mapping_array)):
        for j in range(len(mapping_array[i])):
            im=subimage_array[mapping_array[i][j]]
            final_im.paste(im,(i*25,j*25))

    return final_im

def scaleImage(image, factor):

    # get the original image size
    width, height = image.size

    # resize image to the factor of the original one
    if factor != 0:
        width /= factor
        height /= factor
    else:
        width = 1
        height = 1

    return resizeImage(image, (width, height))

def resizeImage(image, size):
    # use bilinear filter to resize the image
    resizedImage = image.resize(size, Image.BILINEAR)
    return resizedImage

def open_image_stream(imgStream):
    return Image.open(StringIO(imgStream))

def process_reference(reference):
    refImage = open_image_stream(reference)
    width, height = refImage.size
    minDim = min(width, height)
    # Want minimum dimension to be approximately minDimSize px
    scale = (minDim + minDimSize - 1)/minDimSize # ceil of minDim/minDimSize

    if (scale > 1):
        return scaleImage(refImage, scale)
    return refImage

def process_components(components):
    componentImages = []
    componentColours = []
    for component in components:
        img = resizeImage(open_image_stream(component), (25, 25))
        componentImages.append(img)
        componentColours.append(GetImageColour(img))

    return componentImages, componentColours

def process_image(reference, components):
    # Binary stream of reference image
    # Binary stream of component images
    # Returns jpg formatted output image stream
    
    # Reference = reference image
    # Components = component images that will make up the reference

    seed(time())

    refImage = process_reference(reference) 
    componentImages, componentColours = process_components(components)
    componentPositions = MapComponents(refImage, componentColours)
    mosaicImage = construct_image(componentImages, componentPositions)

    buff = StringIO()
    mosaicImage.save(buff, format="JPEG")
    mosaicStream = buff.getvalue()
    buff.close()
    return mosaicStream
