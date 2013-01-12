import Image
from StringIO import StringIO
from math import sqrt
from roygbiv import *

def GetImageColour(image):
    roy = Roygbiv(image)
    return roy.get_average_rgb()

def ColourDistance(x, y):
    assert len(x) == len(y)
    rmean = (x[0]+y[0])/2
    r=x[0]-y[0]
    g=x[1]-y[1]
    b=x[2]-y[2]
    return sqrt((((512+rmean)*r*r)>>8) + 4*g*g + (((767-rmean)*b*b)>>8))

def MapSubImages(mainImage, subImageColours):
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
            for k in xrange(1, len(subImageColours)):
                newDist = ColourDistance(currColour, subImageColours[k])
                # Possibly modify to probabilisity select based on colour dist
                if newDist < bestDist:
                    bestDist = newDist
                    subImageIndex = k
                    
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

def resizeImage(image, factor):

    # get the original image size
    width, height = image.size

    # resize image to the factor of the original one
    if factor != 0:
        width /= factor
        height /= factor
    else:
        width = 1
        height = 1

    # use nearest filter to resize the image
    resizedImage = image.resize((width, height), Image.NEAREST)
    return resizedImage

def process_image(reference, components):
    # Reference = reference image
    # Components = component images that will make up the reference
    images = []
    rImage = resizeImage(StringIO(reference), 10)
    newImageColors = [None for i in range(len(images))]
    for i in range(len(images)):
        newImageColors[i] = GetImageColour(images[i])
    return (rImage, newImageColors)
