"""
generate_wordcloud.py

Generates a word cloud from <abstract> sections in TEI XML files
produced by Grobid.

Processing steps:
1) Parse all XML files in ../data/grobid_xmls/
2) Extract textual content from <abstract> (TEI namespace)
3) Merge all abstracts into a single corpus
4) Remove English stopwords (NLTK)
5) Generate a word cloud with linear frequency scaling
6) Export:
   - results/wordcloud.png  (word cloud image)
   - results/word_frequencies.txt  (token frequencies)
"""

import os
from lxml import etree
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import csv

nltk.download('stopwords')

XML_DIR = "../data/grobid_xmls"
OUTPUT_FILE = "../results/wordcloud.png"

STOPWORDS = set(stopwords.words("english"))

def extract_abstracts():

    abstracts = []

    for file in os.listdir(XML_DIR):
        if file.endswith(".xml"):
            path = os.path.join(XML_DIR, file)

            tree = etree.parse(path)

            ns = {"tei": "http://www.tei-c.org/ns/1.0"}

            abstract = tree.xpath("//tei:abstract//text()", namespaces=ns)

            text = " ".join(abstract)

            abstracts.append(text)

    return " ".join(abstracts)


def generate_wordcloud(text):

    wordcloud = WordCloud(
        width=1200,
        height=600,
        stopwords=STOPWORDS,
        background_color="white",
	relative_scaling=1.0
    ).generate(text)

    freqs = wordcloud.process_text(text)

    sorted_freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)

    plt.figure(figsize=(12,6))
    plt.imshow(wordcloud)
    plt.axis("off")

    plt.savefig(OUTPUT_FILE)


    print("\nWordcloud saved in:", OUTPUT_FILE)

    with open("../results/word_frequencies.csv", "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["word", "frequency"])
        for word, count in sorted_freqs:
            writer.writerow([word, count])

    print("Word frequencies saved in ../results/word_frequencies.csv")

def main():

    text = extract_abstracts()

    generate_wordcloud(text)


if __name__ == "__main__":
    main()
