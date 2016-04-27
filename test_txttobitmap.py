import unittest
from unittest.mock import patch

from PIL.Image import Image

from txttobitmap import add_pixel, convert

TEST_DATA = bytes([0, 127, 255])


class TxtToBitmapTestCase(unittest.TestCase):
    def test_add_pixel(self):
        with patch.object(Image, 'putpixel', return_value=None) as mock_method:
            img = Image()
            add_pixel(img, 5, 3, 0xffffff)
            mock_method.assert_called_with((2, 1), 0xffffff)

    def test_convert_grayscale(self):
        img = convert(TEST_DATA, 'grayscale')
        self.assertEqual(img.size, (2, 2))
        self.assertEqual(img.mode, 'L')
        self.assertEqual(list(img.getdata()), [0, 127, 255, 0])

    def test_convert_palette(self):
        img = convert(TEST_DATA, 'palette')
        self.assertEqual(img.size, (3, 3))
        self.assertEqual(img.mode, 'RGB')
        self.assertEqual(
            list(img.getdata()),
            [(0, 0, 0), (0, 0, 0), (192, 192, 192), (255, 255, 255),
             (255, 255, 255), (255, 255, 255), (0, 0, 0), (0, 0, 0),
             (0, 0, 0)])

    def test_convert_invalid_args(self):
        self.assertRaises(ValueError, convert, TEST_DATA, 'foobar')
