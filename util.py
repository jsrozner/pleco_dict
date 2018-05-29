import os
import pprint
import unicodedata

pp = pprint.PrettyPrinter(indent=2)


def exit_if_file_exists(filename):
    if os.path.isfile(filename):
        exit(print("File exists already. Exit!"))


def sanitize_text(text):
    text_clean = ''.join(c for c in text if c.encode('utf-8') != b'\x00')
    no_new_line = str.replace(text_clean, "\n", " ")
    #if text_clean != no_new_line: print("found newline in %s" % text)
    return no_new_line


tone_table = {0x304: ord('1'),
              0x301: ord('2'),
              0x30c: ord('3'),
              0x300: ord('4')}


def _to_tone_number(s):
    return unicodedata.normalize('NFD', s).translate(tone_table)


def _move_tone_to_end(s):
    outputstr = ""
    number = ""
    for c in s:
        if str.isdigit(c):
            number = c
        else:
            outputstr += c
    return str.strip(outputstr) + number


def pinyin_to_numbered(s):
    return _move_tone_to_end(_to_tone_number(s))
