"""
generate_wordcloud.py

This script generates a word cloud using the text
from abstracts extracted by Grobid in TEI XML format.

Workflow:
1. Reads all XML files in data/grobid_xml/
2. Extracts the content of the <abstract> tag
3. Cleans and preprocesses the text
4. Generates a word cloud
5. Saves the image to results/wordcloud.png
"""

import os
from lxml import etree
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

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
        background_color="white"
    ).generate(text)

    plt.figure(figsize=(12,6))
    plt.imshow(wordcloud)
    plt.axis("off")

    plt.savefig(OUTPUT_FILE)

    print("Wordcloud saved in:", OUTPUT_FILE)


def main():

    text = extract_abstracts()

    generate_wordcloud(text)


if __name__ == "__main__":
    main()
