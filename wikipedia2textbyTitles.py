import mwxml
import mwparserfromhell
import bz2
import sys
import argparse
import codecs
import os
import re


# Function to extract plain text from wikitext
def extract_text_from_wikitext(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    return wikicode.strip_code()

# Function to extract categories from wikitext based on language-specific category namespace
def extract_categories_from_wikitext(wikitext, category_namespace):
    wikicode = mwparserfromhell.parse(wikitext)
    categories = []
    for link in wikicode.filter_wikilinks():
        if link.title.lower().startswith(category_namespace.lower() + ":"):
            categories.append(str(link.title))
    return categories

    
parser = argparse.ArgumentParser(description='Script to convert Wikipedia dumps to text files according to a set of categories')
parser.add_argument('-d','--dump', action="store", dest="dump_path", help='The wikipedia dump.',required=True)
parser.add_argument('-l','--language', action="store", dest="language", help='The language code (en, es, fr ...).',required=True)
parser.add_argument('-o','--outdir', action="store", dest="outdir", help='The output directory.',required=True)
parser.add_argument('-t','--titlesfile', action="store", dest="titlesfile", help='A file where the converted article titles will be stored. By default titles-list.txt.',required=False)

args = parser.parse_args()
dump_path = args.dump_path
language = args.language
categoriesfile=args.categories
outdir=args.outdir
titlesfile=args.titlesfile

if not os.path.exists(outdir):
    os.makedirs(outdir)


usertitles=[]
entrada=codecs.open(titlesfile,"r",encoding="utf-8")
for linia in entrada:
    linia=linia.rstrip()
    usertitles.append(linia)
entrada.close()

# Open the dump file
with bz2.open(dump_path, 'rb') as f:
    # Parse the dump file
    dump = mwxml.Dump.from_file(f)
    
    # Iterate over each page in the dump
    for page in dump:
        if not page.redirect:  # Skip redirect pages
            for revision in page:
                # Extract categories from the wikitext
                #categories = extract_categories_from_wikitext(revision.text, category_namespace)
                
                text = extract_text_from_wikitext(revision.text)
                if page.title in usertitles:
                    print(f"Title: {page.title}")
                    sortidatitles.write(page.title+"\n")
                    filename=page.title.replace(" ","_")+".txt"
                    full_path = os.path.join(outdir, filename)
                    try:
                        sortida=codecs.open(full_path,"w",encoding="utf-8")
                        sortida.write(page.title+"\n")
                        linies=text.split("\n")
                        for linia in linies:
                            linia=linia.strip()
                            
                            if not linia.startswith(category_namespaces[language]) and not linia.startswith("|") and not linia.startswith("<") and not linia.startswith("!") and not linia.startswith("{")and len(linia)>0:
                                sortida.write(linia+"\n")
                        sortida.close()
                    except:
                        pass
sortidatitles.close()
