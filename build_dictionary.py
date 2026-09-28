"""
Run this ONCE to set up your local dictionary.

It reads ECDICT's big text file (ecdict.csv, ~770,000 words) and converts
it into a fast local database file (ecdict.db). Reading the raw text file
takes several seconds every time, but once it's converted to a database,
looking up a single word is instant.

Usage (from a terminal, inside this folder):
    python3 build_dictionary.py
"""

import os
import sys

# The folder this script itself is sitting in (this is also where
# ecdict.csv and stardict.py live). stardict.py knows how to read/write
# dictionary data, so we borrow it instead of writing our own CSV-parsing
# code.
ecdict_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ecdict_folder)

from stardict import DictCsv, StarDict

csv_file_path = os.path.join(ecdict_folder, "ecdict.csv")
database_file_path = os.path.join(ecdict_folder, "ecdict.db")

if os.path.exists(database_file_path):
    print(f"{database_file_path} already exists.")
    print("Delete that file first if you want to rebuild it from scratch.")
    sys.exit(0)

print("Reading ecdict.csv ... this takes about 10-20 seconds, please wait.")
all_words = DictCsv(csv_file_path)
print(f"Loaded {len(all_words)} words from the text file.")

print("Converting to a local database ... this can take a couple of minutes.")
dictionary_database = StarDict(database_file_path)

words_done = 0
for row_number, word in all_words:
    word_info = all_words.query(word)
    dictionary_database.register(word, word_info, commit=False)
    words_done += 1
    if words_done % 100000 == 0:
        print(f"  ...{words_done} words converted so far")

dictionary_database.commit()
print(f"Done! Created {database_file_path}")
print("You can now use lookup.py to search words instantly.")
