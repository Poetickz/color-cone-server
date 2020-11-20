from colormath.color_objects import sRGBColor, HSLColor
from colormath.color_conversions import convert_color
import numpy as np
from sklearn.preprocessing import PolynomialFeatures


class ColorCone(object):

    def __init__(self, model, level=0.5, color_sensitivity=0.05):
        self.model = model
        self.level = level
        self.color_sensitivity = color_sensitivity

    def modify_rgb(self, rgb_tuple):
        sRGB = self._set_sRGBCOLOR(rgb_tuple)
        hsl = convert_color(sRGB, HSLColor).get_value_tuple()
        if self._not_convinient_color(hsl):
            return rgb_tuple

        modified_color = self._enchance_color(hsl)

        new_color = self._get_new_rgb(modified_color)

        return new_color

    def _enchance_color(self, hsl):
        intensity_change = self._get_intensity(int(hsl[0]))
        new_saturation = self._saturate_it(hsl[1], intensity_change)

        return (hsl[0], new_saturation, hsl[2])

    def _get_intensity(self, hue):

        if(hue > 280):
            hue = hue - 280

        # n = len(self.model.coef_[0])
        # Change 8 to n to different model
        exponents = np.array([*range(0, 8, 1)])
        list_x = np.array([hue]*8)  # Change 8 to n to different model
        intensity = self.model.predict(
            [np.array(np.power(list_x, exponents))])[0][0]

        if intensity < 0:
            intensity = 0

        return intensity

    def _saturate_it(self, saturation, intensity):
        if (intensity < self.color_sensitivity):
            return (saturation*self.level)*(1 + intensity)
        else:
            return (saturation*0.9)*(1 + intensity)

    def _not_convinient_color(self, hsl):
        if ((hsl[0] < 240 and hsl[0] > 205) or (hsl[2] > 0.7 or hsl[2] < 0.1)):
            return True

        return False

    def _set_sRGBCOLOR(self, rgb):
        float_rgb = self._rgb_int_to_float(rgb)
        return sRGBColor(float_rgb[0], float_rgb[1], float_rgb[2])

    def _get_new_rgb(self, hsl):
        new_hsl = HSLColor(hsl[0], hsl[1], hsl[2])
        new_rgb = convert_color(new_hsl, sRGBColor).get_value_tuple()
        new_rgb_int = self._rgb_float_to_int(new_rgb)

        return new_rgb_int

    def _rgb_int_to_float(self, rgb):
        return (float(rgb[0]/255.0), float(rgb[1]/255.0),  float(rgb[2]/255.0))

    def _rgb_float_to_int(self, rgb):
        return (int(rgb[0]*255), int(rgb[1]*255),  int(rgb[2]*255))
