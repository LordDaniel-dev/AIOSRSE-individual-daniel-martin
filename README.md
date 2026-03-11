# AIOSRSE-individual-daniel-martin
Repository for the development of individual assessments of AIOSRSE.

Pipeline: PDF → Grobid → TEI XML → Python scripts → Results

1. Dataset selection criteria

- Source: arXiv
- Years: 2023-2026
- Keyword: "finances"
- Total papers: 10

2. Grobid extraction and parsing

I downloaded the latest full image of Grobid using docker using the following command:
docker pull grobid/grobid:0.8.2-full

To run the container I used the following command:
docker run --rm --init --ulimit core=0 -p 8070:8070 grobid/grobid:0.8.2-full
*The reason I didnt specify GPU with the option --gpus is because my laptop lacks CUDA-compatible options.*

I used the processFulltextDocument service endpoint from the TEI section in http://localhost:8070/ (web). Only header consolidation was enabled to improve metadata quality. The other options were disabled since they are not required for abstract extraction, figure counting or URI extraction.

3. Python scripts

The XML files generated with GROBID were processed using three Python scripts located in the src/ directory. These scripts extract the information required for the analysis of the selected papers.

	3.1. Word Cloud Generation
	
	generate_wordcloud.py extracts the text contained in the <abstract> sections of all the TEI XML files. The abstract texts are combined and cleaned using standard English stopwords. All the identified words are exported to a CSV file where each row contains the word or pattern of words (i.e. food security) and the frequency in the text (number value). A word cloud is then generated to visualize the most frequent terms appearing in the abstracts of the dataset.	
	The resulting image is saved as: results/wordcloud.png
	The resulting CSV is saved as: results/word_frequencies.csv
	This visualization highlights the dominant topics and keywords present in the selected research papers.
	
	Validation of Results
	
	Validation was performed by manually comparing the extracted text from the <abstract> sections in the TEI XML files with the original PDF abstracts. The extracted text was verified to match the abstract content in the original articles.
	
	3.2. Figure Counting

	count_figures.py counts the number of figures in each article. Figures are identified by locating <figure> elements with identifiers following the pattern xml:id="fig_X" in the TEI XML structure.
	Since figures can also be referenced elsewhere in the document (e.g., <ref target="#fig_0">), only the actual <figure> elements are counted to avoid duplicates.
	The script generates a bar chart showing the number of figures per article, with the numeric value displayed above each bar.
	The output is saved as:	results/figures_per_article.png
	
	Validation of Results
	
	To validate the number of figures per article:
	Figures were manually counted in the original PDF documents. The counts were compared with the values obtained from the <figure xml:id="fig_X"> elements in the TEI XML files. This ensured that figure references (such as <ref target="#fig_0">) were not counted as figures.
	
	3.3. Link Extraction

 	extract_links.py extracts hyperlinks appearing in each paper. Three patterns were identified in the TEI XML:
	Explicit URL references: <ref type="url" target="https://example.com">
	URLs appearing as plain text inside paragraph elements (often corresponding to footnotes): <p>https://example.com</p>
	Bibliographic links included in reference lists: <ptr target="http://dx.doi.org/..."/>
	All detected links are exported to a CSV file where each row contains the article name and the extracted link.
	The output file is: results/links_per_article.csv
	The CSV uses ; as a delimiter to ensure correct visualization in spreadsheet software.

	Validation of Results

	Validation of extracted links was performed by manually checking each article and confirming that the detected URLs correspond to:
	Explicit URL references; links appearing in footnotes; DOI references in bibliographies
	
	3.4. Running the scripts
	
	From the src/ directory the scripts can be executed with: python(3) generate_wordcloud.py; python(3) count_figures.py; python(3) extract_links.py.
	Each script processes all XML files located in:	data/grobid_xmls/ and stores the resulting outputs in the results/ directory.
	
	## Note on AI Usage
	Portions of this step, including documentation and code, were created or refined with the assistance of AI tools. All outputs were reviewed and validated by the author.

4. Dockerization

To ensure reproducibility of the experiment, the analysis pipeline can be executed inside a Docker container. This avoids dependency issues and guarantees that the scripts run in a controlled environment.

	4.1 Build the Docker image

	First, clone the repository and build the Docker image:
	git clone <repository_url>
	cd <repository_name>
	docker build -t <image_name> .
	The build process installs all required Python dependencies and prepares the environment needed to run the analysis scripts.

	4.2 Run the experiment
	Once the image is built, the full analysis pipeline can be executed with:
	docker run --rm -v $(pwd)/results:/app/results grobid-paper-analysis
	This command runs the container, executes the full analysis pipeline and stores the generated results in the local results/ directory. The --rm flag removes the container after execution.

	4.3 Pipeline executed inside the container
	The Docker environment executes the analysis pipeline starting from the TEI XML files already generated from the original PDFs. To keep the container lightweight and reduce build time, the transformation step from PDF articles to TEI XML using GROBID is not included in the Docker image. 
	However, this step can be reproduced independently using the official Grobid Docker image a bit differently from above. 
	First, download the official Grobid container: docker pull grobid/grobid:0.8.2-full
	Then start the Grobid service: docker run -t --rm -p 8070:8070 grobid/grobid:0.8.2-full
	Once the service is running, the PDFs can be processed using the Grobid client to generate the TEI XML files: http://localhost:8070/ (web.
