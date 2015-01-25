#!/usr/bin/env python3

import logging

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

    for linear_coord in range(mul(*dimensions)):
        xy = xy_coord(linear_coord, dimensions)

        context.point(xy, fill=function(xy))

    return image


def mandelbrot(coord, iterations=50):
    def get_colour(c):
        z = 0

        for count in range(iterations):
            z = pow(z, 2) + c
            if abs(z) > 2:
                log.debug('(%f, %f): outside', c.real, c.imag)
                return count, count, count

        log.debug('(%f, %f): inside', c.real, c.imag)
        return 0, 0, 0

    return get_colour(
        # TODO: Figure how to handle transformation in a good way.
        complex(*transform(0, 1024, 768, 0, 0.005)(*coord))
    )


def main(args):
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    dimensions = 1024, 768
    image = draw(mandelbrot, dimensions)

    image.save('test.png')


if __name__ == '__main__':
    main(sys.argv)
