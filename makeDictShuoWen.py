import os.path
import pickle

import util

kImportDatabase = "./database/etym8_trad_index.p"
kWriteFile = "./dict_output/dict_chnsetym.txt"

kPlecoNewLineChar = ""
kPlecoDoubleNew = kPlecoNewLineChar + kPlecoNewLineChar


class DictWriter:
    def __init__(self, file):
        util.exit_if_file_exists(file)

        print("Opening for write: " + file)
        self._output_file = open(file, "w")

    def write_entry(self, simplified, traditional, defn, pinyin=" "):
        str = ""
        str += simplified
        str += "[" + traditional + "]"
        str += "\t" + pinyin
        str += "\t" + defn
        str += "\n"
        print(str, file=self._output_file, end='')


    def append_to_def(self, label, text, num_newlines):
        if text == "" or text == "none": return ""

        return label + ": " + text + kPlecoNewLineChar * num_newlines

    """
    > 說文: 
    > etymologyLabel: 
    > CharCog:
    > CharPhon:
    > simplificationLabel:
    """
    def make_def(self, shuowen, etymology, cog, phon, simplification, pinyin_to_defn):
        defn = ""
        defn += self.append_to_def("說文", shuowen, 2)
        defn += self.append_to_def("Etym", etymology, 2)
        defn += self.append_to_def("Cog", cog, 1)
        defn += self.append_to_def("Phon", phon, 2)
        defn += self.append_to_def("Simplify", simplification, 2)

        for pinyin in pinyin_to_defn.keys():
            defn += self.append_to_def(pinyin, pinyin_to_defn[pinyin], 1)

        defn = defn.rstrip(kPlecoNewLineChar)
        return defn

    def write_char_entry_to_dict(self, char_entry):
        shuowen = char_entry['ShuoWen']
        etymology = char_entry['etymologyLabel']
        if shuowen == "none" and etymology == "none": return

        charPhon = char_entry['charPhon']
        charCog = char_entry['charCog']
        simplificationLabel = char_entry['simplificationLabel']
        pinyin_to_defn = char_entry['pinyin_to_defn']


        simplified = char_entry['SimplifiedChar']
        if simplified == "-": simplified = ""
        traditional = char_entry['TraditionalChar']

        defn = self.make_def(shuowen, etymology, charCog, charPhon, simplificationLabel, pinyin_to_defn)

        # one entry per pronunciation
        for pinyin in pinyin_to_defn.keys():
            self.write_entry(simplified, traditional, defn, pinyin)


def main():
    database = pickle.load(open(kImportDatabase, 'rb'))

    dict_writer = DictWriter(kWriteFile)

    counter = 0
    for key in database:
        counter += 1

        char_entry = database[key]
        dict_writer.write_char_entry_to_dict(char_entry)

    print("Created %d entries" % counter)


if __name__ == "__main__":
    main()
