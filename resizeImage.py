from PIL import Image
import os

def resizeImage(image, factor):

  origImage = Image.open(image)

  # get the original image size
  width, height = origImage.size

  # resize image to the factor of the original one
  if factor != 0:
      width /= factor
      height /= factor
  else:
      width = 1
      height = 1

  # use nearest filter to resize the image
  resizedImage = origImage.resize((width, height), Image.NEAREST)
  return resizedImage

def process_image(reference, path):
    images = []
    for root, dirs, files in os.walk(os.path.abspath(path)):
        for fname in files:
            if fname[-5:] == ".jpeg":
                images.append(os.path.join(root, fname))
                print os.path.join(root, fname)

    rImage = resizeImage(reference, 10)
    newImageColors = [None for i in range(len(images))]
    for i in range(len(images)):
        newImageColors[i] = GetImageColour(images[i])
    return (rImage, newImageColors)
