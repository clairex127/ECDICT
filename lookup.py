"""
Look up an English word or phrase, print its Chinese meaning and an
English definition, and save it as a new row in an Excel file for
later practice.

After showing the meaning, it asks in the terminal whether the word is
one you'd actually use in everyday talking (y) or one you just want to
be able to understand when you see/hear it (n), and saves the entry to
the matching sheet ("use" or "understand").

Usage (from a terminal, inside this folder):
    python3 lookup.py caricature
    python3 lookup.py "in the long run"
"""

import argparse
import os
import sys
from datetime import date

import openpyxl

# --- where things live -------------------------------------------------

# The folder this script itself is sitting in (this is also where
# ecdict.db and stardict.py live). stardict.py knows how to read the
# local dictionary database, so we borrow it instead of writing our own.
ecdict_folder = os.path.dirname(os.path.abspath(__file__)) # folder path
sys.path.insert(0, ecdict_folder)
from stardict import StarDict

dictionary_file_path = os.path.join(ecdict_folder, "ecdict.db")

# The Excel file this tool keeps adding new words to. It lives right next
# to this script.
excel_file_path = os.path.join(ecdict_folder, "clairevocab.xlsx")

column_headers = ["Word", "Phonetic", "Chinese Meaning", "English Definition", "Date Added"]


# --- reading command-line arguments -------------------------------------

parser = argparse.ArgumentParser(description="Look up a word and log it to Excel.")
parser.add_argument("word", nargs="+", help="the word or phrase to look up")
args = parser.parse_args()

# nargs="+" collects every word you typed into a list, e.g. typing
#   python3 lookup.py in the long run
# gives args.word == ["in", "the", "long", "run"], so we join it back
# into one phrase with spaces.
word_to_look_up = " ".join(args.word)


# --- looking up the word -------------------------------------------------

dictionary = StarDict(dictionary_file_path)
word_info = dictionary.query(word_to_look_up)

if word_info is None:
    print(f'"{word_to_look_up}" was not found in the dictionary.')
    sys.exit(1)

phonetic = word_info["phonetic"] or ""
chinese_meaning = word_info["translation"] or ""
english_definition = word_info["definition"] or ""

print(f"{word_info['word']}")
print(f"{phonetic}")
print(f"{chinese_meaning}")
print(f"{english_definition}")


# --- asking which sheet this word belongs in -----------------------------

# input() pauses the script and waits for you to type something and press
# Enter. We keep asking in a loop until you type a y/n answer we recognise,
# so a typo can't silently file the word in the wrong sheet.
while True:
    answer = input("\nIs it for everyday talking use? (y/n): ").strip().lower()
    if answer in ("y", "yes"):
        sheet_name = "use"
        break
    elif answer in ("n", "no"):
        sheet_name = "understand"
        break
    else:
        print("Please type y or n.")


# --- saving it to the Excel file -----------------------------------------

if os.path.exists(excel_file_path):
    workbook = openpyxl.load_workbook(excel_file_path)
else:
    workbook = openpyxl.Workbook()
    # A brand new workbook starts with one empty sheet called "Sheet" -
    # we don't want that leftover, so remove it once our own sheet exists.
    workbook.remove(workbook.active)

if sheet_name in workbook.sheetnames:
    sheet = workbook[sheet_name]
else:
    sheet = workbook.create_sheet(sheet_name)
    sheet.append(column_headers)

sheet.append([word_info["word"], phonetic, chinese_meaning, english_definition, date.today().isoformat()])
workbook.save(excel_file_path)

print(f'\nSaved to "{sheet_name}" sheet in {excel_file_path}')
