import os
import pickle

from bs4 import BeautifulSoup as bs

import util

dir = "/Users/jsrozner/Desktop/test/chineseetymology.org/"
kOutputDatabaseName = "./database/etym8_trad_index.p"
debug = False

writeOutput = True


#todo: there are 667 duplicates
#todo only 4821 entries generated

# Web IDs
ids = {
    'testChar',
    'EnglishExplanation',
    'SimplifiedUCS2Hex',
    'SimplifiedGB0Hex',
    'SimplifiedChar',
    'simplificationLabel',
    'TraditionalUCS2Hex',
    'TraditionalB5Hex',
    'TraditionalChar',
    'charPhon',
    'charCog',
    'ShuoWen',
    'PictureImages',
    'etymologyLabel',
    'SealImages',
    'LstImages',
    'BronzeImages',
    'OracleImages'
}

# Supplemental IDs:
#   images -> [all image files, in order] (list)
#   pinyin_to_defn -> [pinyin => defn] (dict)

def main():
    # Don't do work for nothing
    util.exit_if_file_exists(kOutputDatabaseName)

    dictionary = {}

    counter = 0
    not_analyzed_count = 0
    top_counter = 0
    excepted_file_count = 0
    duplicate_count = 0
    for root, dirs, files in os.walk(dir):
        # No recurse; this is hacky
        if top_counter == 1: break
        top_counter += 1

        # Iterate all html pages
        for filename in files:
            counter += 1
            if debug: print(counter)
            if counter % 200 == 0: print(counter)

            duplicate = False

            with open(dir + filename) as f:
                try:
                    data=f.read()
                    soup = bs(data, 'html.parser')
                except:
                    print("Exception in read file " + dir + filename)
                    excepted_file_count += 1
                    continue

            # Get current char
            test_char = soup.find(id="testChar").text
            if str.find(test_char, "Not analyzed yet") != -1:
                not_analyzed_count += 1
                continue
            curr_char = test_char

            trad_char = soup.find(id="TraditionalChar")
            if trad_char and trad_char.text != "?":
                curr_char = trad_char.text
            # No need to check simplified; at this point it would be same as test_char

            # Initialize current dict
            if dictionary.get(curr_char) is not None:
                print("Error this entry exists already")
                duplicate_count += 1
                duplicate = True
                old_entry = dictionary.get(curr_char)

            dictionary[curr_char] = {}
            dictionary[curr_char]["images"] = []
            # dictionary[curr_char]["pinyin_to_defn"] is handled below

            # Read in all ids
            for id in ids:
                id_text = soup.find(id=id).text
                id_text_clean = util.sanitize_text(id_text)
                dictionary[curr_char][id] = id_text_clean

            # Handle all image names
            for tag in soup.find_all("img"):
                src = tag.get('src')
                if(src.split("/",1)[0]) != 'CharacterImages': continue
                dictionary[curr_char]["images"].append(src)


            ####### Generate pinyin -> defn mapping #######

            # Get the section with english explanation
            id_html = soup.find(id="EnglishExplanation")

            # Get all pronunciations
            pronunciation_htmls = id_html.find_all('a')
            pronunciations = list(map(lambda x: x.text, pronunciation_htmls))

            # Remove pronunciation from html
            for p in pronunciation_htmls:
                p.decompose()

            # Get defns
            defns = id_html.text.split(" English Senses For (英文): ")
            defns = list(filter(None, defns))
            defns = list(map(util.sanitize_text, defns))

            pinyin_to_defn = dict(zip(pronunciations, defns))
            dictionary[curr_char]["pinyin_to_defn"] = pinyin_to_defn

            if duplicate:
                util.pp.pprint(old_entry)
                util.pp.pprint(dictionary[curr_char])

            if debug:
                #Optional debug
                util.pp.pprint(dictionary[curr_char])
                input("press enter")

    # Write final DB
    if not debug and writeOutput:
        pickle.dump(dictionary, open(kOutputDatabaseName,"wb"))
        print("parsed %d chars" % counter)
        print("not analyzed yet %d" % not_analyzed_count)
        print("duplicates %d" % duplicate_count)


if __name__ == "__main__":
    main()
