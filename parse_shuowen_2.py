import pickle
import os

from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from enum import Enum

import util

dir = "/Users/jsrozner/Desktop/test/www.shuowen.org/view/"
kOutputDatabaseName = "./database/shuowenout4.p"
debug = False

writeOutput = True

dictionary = {}


class ShuowenAttributes(Enum):
    kClassifiers = "classifiers"
    kPinyin = "pinyin"
    kPhonetic = "phonetic_desc"
    kDefn = "shuowen"
    kImages = "images"
    kRelatedChars = "related_chars"
    kExplanations = "explanations"

# IDs in output dict:
# each entry is a list
#   (there are about 30 entries with duplicates
#   duplicates are either diff pinyin or diff entry
#
# pinyin
# ? classifiers (two char groupings) - list(2 elements)
# ? phonetic description
# shuowen defn - str
# image files - list
# related chars - potentially older variants (can have multiple entries)
# definitions - 1 - 2 explanation entries: {'宋代 徐鉉 徐鍇 注釋', '清代 段玉裁《說文解字注》'}


def write_to_entry(char_entry, key, value):
    if type(value) == type(""):
        value = value.strip()
        if str.find(value, "\n") != -1:
            print("error, newline found")
            print(str.find(value, "\n"))
            print(value)

    char_entry[key.name] = value


def main():
    # Don't do work for nothing
    if os.path.isfile(kOutputDatabaseName):  exit(print("File exists already. Exit!"))


    counter = 0
    top_counter = 0
    duplicate_count = 0
    for root, dirs, files in os.walk(dir):
        # No recurse; this is hacky
        if top_counter == 1: break
        top_counter += 1

        # Iterate all html pages
        for filename in files:
            counter += 1
            if debug and counter == 10: break
            if counter % 200 == 0:print(counter)

            with open(dir + filename) as f:
                try:
                    data=f.read()
                    soup = bs(data, 'html.parser')
                except:
                    print("Exception in read file " + dir + filename)
                    continue

            curr_char = soup.find_all("li", class_="active")[1].text

            # Current char and setup
            curr_char_entry = {}

            # Classifiers
            classifiers_raw = soup.find(class_="span6").text
            write_to_entry(curr_char_entry, ShuowenAttributes.kClassifiers,
                           list(map(str.strip, str.split(classifiers_raw, "|"))))

            # Phonetics
            phonetics_raw = soup.find(class_="span6 text-right").text
            phonetics_parsed = list(map(str.strip, str.split(phonetics_raw, "|")))
            phonetics_pinyin = util.pinyin_to_numbered(phonetics_parsed[0])
            phonetics_desc = phonetics_parsed[1]
            write_to_entry(curr_char_entry, ShuowenAttributes.kPinyin, phonetics_pinyin)
            write_to_entry(curr_char_entry, ShuowenAttributes.kPhonetic, phonetics_desc)

            # Extra character info
            # This is always identical and can be removed
            curr_char_bkup = str.strip(soup.find(class_="media-object pull-left").text)
            if curr_char != curr_char_bkup: print("curr char and backup diff")

            # Shuowen def
            shuowen = str.strip(soup.find(class_="media-body").text)
            write_to_entry(curr_char_entry, ShuowenAttributes.kDefn, shuowen)

            # img files
            img_html = soup.find_all(class_="img")
            write_to_entry(curr_char_entry, ShuowenAttributes.kImages,
                           list(map(lambda x: x.find("img").get("src"), img_html)))

            # Potential additional char info
            # todo: interspersed new lines
            if len(img_html) > 1:
                extra_chars = list(map(lambda x: str.strip(x.text).replace("\n", ": "), img_html[1:]))
                if debug:
                    print("extra chars " + curr_char)
                    util.pp.pprint(extra_chars)

                write_to_entry(curr_char_entry, ShuowenAttributes.kRelatedChars.name, extra_chars)

            # Definitions
            #todo: some new lines
            definitions = soup.find_all(class_="row-fluid secondary")
            definitions_parsed = OrderedDict()
            for de in definitions:
                title = de.find("h3").text
                explns = list(map(lambda x: str.strip(x.text), de.find_all("blockquote")))
                explns = list(filter(None, explns))
                section_hdrs = list(map(lambda x: x.text, de.find_all("dt")))
                section_hdrs = list(filter(None, section_hdrs))

                for i in range(0, len(explns)):
                    if str.find(explns[i], "\n") != -1:
                        print("error: newline in dict explanations")
                        print(filename)
                        print(curr_char)

                if section_hdrs:
                    for i in range(0, len(section_hdrs)):
                        if str.find(section_hdrs[i], "\n") != -1:
                            print("error: newline in dict explanations")
                            print(filename)
                            print(curr_char)

                    if len(explns) != len(section_hdrs): "print nonmatching explns and section headers"
                    definitions_parsed[title] = OrderedDict(zip(section_hdrs, explns))
                else:
                    #Note: This can be longer than a single line
                    definitions_parsed[title] = explns

            curr_char_entry[ShuowenAttributes.kExplanations.name] = definitions_parsed

            if dictionary.get(curr_char) is None:
                dictionary[curr_char] = [curr_char_entry]
            else:
                duplicate_count +=1
                dictionary[curr_char].append(curr_char_entry)

            if debug: util.pp.pprint(dictionary[curr_char])


    print("duplicates: %d" % duplicate_count)

    # Write final DB
    if not debug and writeOutput:
        pickle.dump(dictionary, open(kOutputDatabaseName,"wb"))
        print("parsed %d chars" % counter)


if __name__ == "__main__":
    main()
