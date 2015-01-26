#!/usr/bin/env python3

import sys
import logging
import math

from multiprocessing import Pool
from operator import mul

from PIL import Image, ImageDraw


log = logging.getLogger(__name__)


def xy_coord(index, dimensions):
    width, height = dimensions

    y, x = divmod(index, width)

    if y < height:
        return x, y
    else:
        raise IndexError('Index results in a height greater than height')


def transform(left, right, bottom, top, scale_factor):
    center_x = scale_factor * (right - left) / 2
    center_y = scale_factor * (bottom - top) / 2

    return lambda x, y: (x * scale_factor - center_x,
                         y * scale_factor - center_y)


def draw(function, dimensions):
    image = Image.new('RGB', dimensions)
    context = ImageDraw.Draw(image)

    with Pool(4) as p:
        pixels = p.map(
            function,
            map(lambda index: xy_coord(index, dimensions),
                range(mul(*dimensions))
            )
        )

    for index, colour in enumerate(pixels):
        xy = xy_coord(index, dimensions)

        context.point(xy, fill=colour)

    context.ellipse(
            [(dimensions[0] / 2 - 30, dimensions[1] / 2 - 30),
             (dimensions[0] / 2 + 30, dimensions[1] / 2 + 30)],
            outline=255)

    return image


def mandelbrot(coord, iterations=20):
    def get_colour(c):
        z = 0

        for count in range(iterations):
            z = pow(z, 2) + c
            if abs(z) > 2:
#                log.debug('(%f, %f): outside', c.real, c.imag)
                sc = count + 1 - math.log(math.log(abs(z))) / math.log(2)
                colour = int(sc / iterations * 255)
                return colour, colour, colour

#        log.debug('(%f, %f): inside', c.real, c.imag)
        return 0, 0, 0

    return get_colour(
        # TODO: Figure how to handle transformation in a good way.
        complex(*transform(0, 2560 - 1650, 1440 - 2000, 0, 0.00016)(*coord))
#        complex(*transform(0, 1024, 768, 0, 0.005)(*coord))
    )


def main(args):
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    dimensions = 2560, 1440
#    dimensions = 1024, 758
    image = draw(mandelbrot, dimensions)

    image.save('mandelbrot-2560x1440-AA1x.png')


if __name__ == '__main__':
    main(sys.argv)
