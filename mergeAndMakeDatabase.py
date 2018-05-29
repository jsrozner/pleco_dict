import pickle

import util


kImportDatabaseEtym = "./database/etym5_testchar.p"
kImportDatabaseShuo = "./database/shuowen3multipinyin.p"

kFinalDatabase = "./database/merged3.p"

""" Etym core components
> 說文: 
> etymologyLabel: 
> CharCog:
> CharPhon:
> simplificationLabel:
"""

""" Shuowen core components
See other file
"""


def main():
    util.exit_if_file_exists(kFinalDatabase)

    database_orig = pickle.load(open(kImportDatabaseEtym, 'rb'))
    database_shuo = pickle.load(open(kImportDatabaseShuo, 'rb'))

    total_count = 0
    new_char_count = 0

    for k in database_shuo.keys():
        total_count +=1
        existing_entry = database_orig.get(k)
        if not existing_entry:
            new_char_count += 1
            database_orig[k] = {}

        database_orig[k]["_shuowen_source"] = database_shuo[k]

    print(new_char_count)
    print(database_orig.__len__())

    pickle.dump(database_orig, open(kFinalDatabase, "wb"))


if __name__ == "__main__":
    main()
