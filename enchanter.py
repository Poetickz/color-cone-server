from joblib import load
from numpy import shape
from numpy import hstack
from numpy import vstack


from multiprocessing import Pool

from ColorCone import ColorCone


colors = {}


def dictionary(image_obj):
    """
        procesamiento de imagen
    """

    model = load('model-x7.pkl')

    algorithm = ColorCone(model, 1.025, 0.5)
    subimage = image_obj
    h, w, bpp = shape(subimage)
    for pixelY in range(h):
        for pixelX in range(w):
            blue = subimage[pixelY][pixelX][0]
            green = subimage[pixelY][pixelX][1]
            red = subimage[pixelY][pixelX][2]
            rgbTuple = (red, green, blue)
            if rgbTuple in colors.keys():
                red, green, blue = colors[rgbTuple]
            else:

                red, green, blue = algorithm.modify_rgb(rgbTuple)
                colors[rgbTuple] = (red, green, blue)
            subimage[pixelY][pixelX][0] = blue
            subimage[pixelY][pixelX][1] = green
            subimage[pixelY][pixelX][2] = red

    return subimage


def pasteImg(arrDeImagen):
    """
        combina las 4 partes de la imagen
    """
    topSubimages = hstack((arrDeImagen[0], arrDeImagen[1]))
    bottomSubimages = hstack((arrDeImagen[2], arrDeImagen[3]))
    completeImage = vstack((topSubimages, bottomSubimages))

    return completeImage


def multiprocess(subimgArr):
    """
        funcion que se encarga del multiprocesamiento
    """
    with Pool(4) as p:
        subimgArr = p.map(dictionary, subimgArr)
    return subimgArr


def cutImg(originalImage):
    """
        Parte la imagen en 4 subimagenes
    """
    h, w, bpp = shape(originalImage)
    subimageTopLeft = originalImage[: h//2, :w//2]
    subimageTopRigth = originalImage[: h//2, w//2:w]
    subimageBottomLeft = originalImage[h//2: h, :w//2]
    subimageBottomRigth = originalImage[h//2: h, w//2:w]

    return [subimageTopLeft, subimageTopRigth, subimageBottomLeft, subimageBottomRigth]


def processImage(img_obj):
    arrImg = cutImg(img_obj)
    arrImg = multiprocess(arrImg)
    enchance_image = pasteImg(arrImg)

    return enchance_image
