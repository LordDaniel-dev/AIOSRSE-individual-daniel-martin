#!/bin/bash

echo "Running Grobid paper analysis pipeline..."

echo "1. Generating word cloud"
python src/generate_wordcloud.py

echo "2. Counting figures"
python src/count_figures.py

echo "3. Extracting links"
python src/extract_links.py

echo "Pipeline finished."
echo "Results available in /app/results"
