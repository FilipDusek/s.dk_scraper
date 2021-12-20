# About
This is a collection of scripts I've used to create a dataset with info about available student apartments in Copenhagen. It wasn't designed to solve this problem generally and you will likely need to customize this if you want to do something similar with this code.

`main.py` has the code for spider that scrapes apartment information from https://s.dk/

`sdk-analysis.ipynb` uses google maps API to annotate the scraped dataset with information about commute distances by public transport/bike to some common locations around Copenhagen. It also annotates with info about distance to closest supermarket. 


# Instructions
1. Install scrapy:
```pip install scrapy```
2. Run the spider:
```scrapy runspider main.py```

