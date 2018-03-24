# MonsterCrawler

***Description***<br>
Crawler for job description from job search engine [monster.de](monster.de). The job descriptions then were analyzed using Rapidminer: We built a Document-Term-Matrix for the whole corpus of real job offfers and for fictional job descriptions of our "dreamjobs". Then we used Cosine-Similarity to find the Job offers most similar to our dream-jobs.

***Context***<br>
Master programme [Data Science & Business Analytics](https://www.hdm-stuttgart.de/ds/de/)<br>Lecture [Introduction to Data Science](https://www.hdm-stuttgart.de/ds/de/weiterbildung/modul_03)<br>At [University of Media, Stuttgart (DE)](https://www.hdm-stuttgart.de/)

***Goal / Task***<br>
Come up with a use-case for clustering, classifaction or text analysis and implement a Proof-of-Concept using a self-service-analytics tool like Rapidminer.

***Authors***<br>
Sanna and me ([dynobo](https://github.com/dynobo))

***Timeline***<br>
Mar. 2017 - Apr. 2017

***Repo***<br>
Web-Crawler implemented with Scrapy in Python; Rapidminer workflows for data cleaning, preparation and similiarity search.

----

## Web-Scraper
### Install
Install dependencies:

* scrapy

### Configure
In `/spiders/jobs_spider.py`, in the class `linkSpider`, adjust the variable `url` in order to get the result for desired region and keywords.

### Run
First extract links to job offers from search results:

```
scrapy crawl links -a search=datascience -o datascience.json
scrapy crawl links -a search=itinstuttgart -o itinstuttgart.json
```

Second extract job descriptions:

```
scrapy crawl jobs  -a search=datascience -o datascience.xml
scrapy crawl jobs  -a search=itinstuttgart -o itinstuttgart.xml
```

Third combine the xmls :

```
xml_grep --pretty_print indented --wrap items --descr '' --cond "item" *.xml > jobs.xml
```
