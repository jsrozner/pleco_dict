import pickle

import util

from parse_shuowen_2 import ShuowenAttributes as SA

kImportDatabase = "./database/shuowenout4.p"
kWriteFile = "./dict_output/dict_shuowen.txt"

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
        sanitized_label = util.sanitize_text(label)
        sanitized_text = util.sanitize_text(text)
        line_end = kPlecoNewLineChar * num_newlines

        if label != "":
            return sanitized_label + ": " + sanitized_text + line_end

        return sanitized_text + line_end

    """
    > 說文: 
    > Explanation entries
    > Related chars
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

    def write_char_entry_to_dict(self, char_entry, key=""):
        # no simplified provided
        traditional = key

        shuowen = char_entry[SA.kDefn.name]
        explanations = char_entry[SA.kExplanations.name]

        if shuowen == "none" and explanations == "none": return

        pinyin = char_entry[SA.kPinyin.name]
        related_chars = char_entry.get(SA.kRelatedChars.name)

        # Build defn
        defn = ""
        defn += self.append_to_def("說文", shuowen, 2)

        # Top level explain:
        top_level_explain = explanations.get('宋代 徐鉉 徐鍇 注釋')
        if top_level_explain is not None:
            defn += self.append_to_def("宋代 徐鉉 徐鍇 注釋", "", 2)
            for e in top_level_explain:
                defn += self.append_to_def("注釋", e, 2)

        # Shuowen explain
        shuowen_explain = explanations.get('清代 段玉裁《說文解字注》')
        if shuowen_explain is not None:
            defn += self.append_to_def("清代 段玉裁《說文解字注》", "", 2)
            for k,v in shuowen_explain.items():
                defn += self.append_to_def(k, "", 1)
                defn += self.append_to_def("", v, 2)

        if related_chars is not None:
            print("related chars not none")
            for rc in related_chars:
                defn += self.append_to_def("", rc, 1)

        self.write_entry("", traditional, defn, pinyin)


def main():
    database = pickle.load(open(kImportDatabase, 'rb'))

    dict_writer = DictWriter(kWriteFile)

    counter = 0
    for key in database:
        counter += 1

        # todo: this ignores 30 duplicates
        char_entry = database[key][0]
        dict_writer.write_char_entry_to_dict(char_entry, key)

    print("Created %d entries" % counter)


if __name__ == "__main__":
    main()
