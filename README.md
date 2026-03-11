# AIOSRSE-individual-daniel-martin
Repository for the development of individual assessments of AIOSRSE.

1. Dataset selection criteria

- Source: arXiv
- Years: 2023-2026
- Keyword: "finances"
- Total papers: 10

2. Grobid extraction and parsing

I downloaded the latest full image of Grobid using docker using the following command:
docker pull grobid/grobid:0.8.2-full

To run the container a used the following command:
docker run --rm --init --ulimit core=0 -p 8070:8070 grobid/grobid:0.8.2-full
*The reason I didnt specify GPU with the option --gpus is because my laptop lacks CUDA-compatible options.*

I used the processFulltextDocument service endpoint from the TEI section. Only header consolidation was enabled to improve metadata quality. The other options were disabled since they are not required for abstract extraction, figure counting or URI extraction.

3. Python scripts

The XML files generated with GROBID were processed using three Python scripts located in the src/ directory. These scripts extract the information required for the analysis of the selected papers.

  3.1. Word Cloud Generation

  generate_wordcloud.py extracts the text contained in the <abstract> sections of all the TEI XML files. The abstract texts are combined and cleaned using standard English stopwords. A word cloud is then
  generated to visualize the most frequent terms appearing in the abstracts of the dataset.	
  The resulting image is saved as: results/wordcloud.png
  This visualization highlights the dominant topics and keywords present in the selected research papers.
	
  3.2. Figure Counting

  count_figures.py counts the number of figures in each article. Figures are identified by locating <figure> elements with identifiers following the pattern xml:id="fig_X" in the TEI XML structure.
	Since figures can also be referenced elsewhere in the document (e.g., <ref target="#fig_0">), only the actual <figure> elements are counted to avoid duplicates.
	The script generates a bar chart showing the number of figures per article, with the numeric value displayed above each bar.
	The output is saved as:	results/figures_per_article.png
	
  3.3. Link Extraction

  extract_links.py extracts hyperlinks appearing in each paper. Three patterns were identified in the TEI XML:
	Explicit URL references: <ref type="url" target="https://example.com">
	URLs appearing as plain text inside paragraph elements (often corresponding to footnotes): <p>https://example.com</p>
	Bibliographic links included in reference lists: <ptr target="http://dx.doi.org/..."/>
	All detected links are exported to a CSV file where each row contains the article name and the extracted link.
	The output file is: results/links_per_article.csv
	The CSV uses ; as a delimiter to ensure correct visualization in spreadsheet software.
	
  3.4. Running the scripts
	
  From the src/ directory the scripts can be executed with: python(3) generate_wordcloud.py; python(3) count_figures.py; python(3) extract_links.py.
	Each script processes all XML files located in:	data/grobid_xmls/ and stores the resulting outputs in the results/ directory.
	
  ## Note on AI Usage
  Portions of this step, including documentation and code, were created or refined with the assistance of AI tools. All outputs were reviewed and validated by the author.
