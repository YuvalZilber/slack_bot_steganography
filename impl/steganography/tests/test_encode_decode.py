import os
import shutil
import unittest

from impl.steganography.tests.utils import decrypt, encrypt

input_files = ('s_small_black', 's_big_black', 's_small_white', 's_big_white')
s = 'abcdefgh'
texts = [s[:i] for i in range(1, 9)]
bpps = list(range(1, 9))

cd = os.path.dirname(__file__)
output_dir = f"{cd}/outputs"
sanity_output_dir = f"{cd}/outputs/sanity"


def read(file_alias):
    with open(f"{cd}/resources/{file_alias}.txt") as file:
        return file.read().replace("\\t", "\t")


class EncodeDecodeSanity(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.mkdir(output_dir)
        os.mkdir(sanity_output_dir)

    def test_sanity(self):
        for input_file in input_files:
            for text in texts:
                for bpp in bpps:
                    print("-" * 100)
                    print(f"Test! {input_file}_{text}_{bpp}.png")
                    result_path = f"{sanity_output_dir}/{input_file}_{text}_{bpp}.png"
                    encrypt(f"{cd}/resources/{input_file}.png", text, bpp, result_path)

                    new_text = decrypt(result_path)
                    self.assertEqual(text, new_text, f"{input_file}, {text}, {bpp}")

    def test_big_text_small_image(self):
        # global output_dir
        # output_dir = f"{output_dir}"
        colors = ("black", "white")
        for color in colors:
            text = read("10000")
            for bpp in range(1, 7):
                self.myAssertRaises(bpp, text)
            for bpp in range(7, 9):
                result_path = f"{output_dir}/s_small_{color}_10000.txt_{bpp}.png"
                encrypt(f"{cd}/resources/s_small_{color}.png", text, bpp, result_path)

    def myAssertRaises(self, bpp, text):
        print("-" * 100)
        result_path = f"{output_dir}/s_small_black_10000.txt_{bpp}.png"
        self.assertRaises(Exception, encrypt, f"{cd}/resources/s_small_black.png", text, bpp, result_path)

    def test_exact_limit(self):
        # global output_dir
        # output_dir = f"{output_dir}"
        text = read("10000")[:1575]
        try:
            result_path = f"{output_dir}/ex_small_black_{len(text)}.txt_1.png"
            encrypt(f"{cd}/resources/s_small_black.png", text, 1, result_path)
        except:
            pass
        else:

            new_text = decrypt(result_path)
            self.fail(f"should raise at 1575\ninfo:text==new_text -> {text == new_text}")
        text = text[:-1]
        result_path = f"{output_dir}/ex_small_black_{len(text)}.txt_1.png"
        encrypt(f"{cd}/resources/s_small_black.png", text, 1, result_path)
        new_text = decrypt(result_path)
        self.assertEqual(text, new_text)
        # self.myAssertRaises(1, text)

    def input_file(self):
        raise NotImplementedError()

    def text(self):
        raise NotImplementedError()

    def bpp(self):
        raise NotImplementedError()
