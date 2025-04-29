welcome to my first web scraping project
in this project I tried to extract 5 important features of each home appliance category
given in excel file: code.xlsx
I was told by my employer to do these tasks:
start by choosing a sub-dataset including first 2 models of each category-brand
then search on the search engines like: google, yahoo, bing for each category-brand-model of sub-dataset
and extract their related links that belong to one of the below sites:
digikala.com, sallambabaa.com, torob.com, atramart.com, entekhabcenter.com
then open the extracted links to scrape for feature extraction of that specified category-brand-model
in the next stage you should clean your data(extracted features) and
do clustering on each category to find the most similar models in each category
then save and show the result of clustering stage and specify similar models in each category

I did it in 3 significant phases:

1. link extraction (getLinks.py)
2. feature extraction (getFeatures.py)
3. data cleaning and clustering (dataCleaningAndML)

to get started on this project:

1. install all libraries(some unnecessaries are existed) by run this code in terminal:
	pip install -r requirements.txt

2. if selenium doesn't install using pip, you should download its .whl file:
	selenium-4.29.0-py3-none-any.whl
   and locate it in project main folder and run this code in terminal:
	pip install selenium-4.29.0-py3-none-any.whl

3. download chromedriver 133.0.6943.126 (version is important due to its dependency)
   and locate it in project main folder

4. the whole data(category-brand-model) should be in file: code.xlsx
	its ready! run main.py to call main() method

--> Results will be saved as some images and *.csv files
