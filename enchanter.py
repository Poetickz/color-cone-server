from joblib import load
from numpy import shape
from numpy import hstack
from numpy import vstack


from multiprocessing import Pool

from ColorCone import ColorCone


class Enchanter(object):

    def __init__(self, level, sensitive):
        self.colors = {}
        self.level = level
        self.sensitive = sensitive

    def dictionary(self, image_obj):
        """
            procesamiento de imagen
        """

        model = load('model-x7.pkl')

        algorithm = ColorCone(model, self.level, self.sensitive)
        subimage = image_obj
        h, w, bpp = shape(subimage)
        for pixelY in range(h):
            for pixelX in range(w):
                blue = subimage[pixelY][pixelX][0]
                green = subimage[pixelY][pixelX][1]
                red = subimage[pixelY][pixelX][2]
                rgbTuple = (red, green, blue)
                if rgbTuple in self.colors.keys():
                    red, green, blue = self.colors[rgbTuple]
                else:

                    red, green, blue = algorithm.modify_rgb(rgbTuple)
                    self.colors[rgbTuple] = (red, green, blue)
                subimage[pixelY][pixelX][0] = blue
                subimage[pixelY][pixelX][1] = green
                subimage[pixelY][pixelX][2] = red

        return subimage

    def pasteImg(self, arrDeImagen):
        """
            combina las 4 partes de la imagen
        """
        topSubimages = hstack((arrDeImagen[0], arrDeImagen[1]))
        bottomSubimages = hstack((arrDeImagen[2], arrDeImagen[3]))
        completeImage = vstack((topSubimages, bottomSubimages))

        return completeImage

    def multiprocess(self, subimgArr):
        """
            funcion que se encarga del multiprocesamiento
        """
        with Pool(4) as p:
            subimgArr = p.map(self.dictionary, subimgArr)
        return subimgArr

    def cutImg(self, originalImage):
        """
            Parte la imagen en 4 subimagenes
        """
        h, w, bpp = shape(originalImage)
        subimageTopLeft = originalImage[: h//2, :w//2]
        subimageTopRigth = originalImage[: h//2, w//2:w]
        subimageBottomLeft = originalImage[h//2: h, :w//2]
        subimageBottomRigth = originalImage[h//2: h, w//2:w]

        return [subimageTopLeft, subimageTopRigth, subimageBottomLeft, subimageBottomRigth]

    def processImage(self, img_obj):
        arrImg = self.cutImg(img_obj)
        arrImg = self.multiprocess(arrImg)
        enchance_image = self.pasteImg(arrImg)

        return enchance_image
