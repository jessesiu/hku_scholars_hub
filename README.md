# Web scraping from HKU scholar hub

The script will search from [HKU scholars hub website](http://hub.hku.hk/) via the input the journal name and period of time.

## Requirements

1. Python version should be 3+
2. Install BeautifulSoup bs4
3. Install urlopen
4. Install xlrd,xlwt,csv

## Run the script

Run the data_availability.py script

Enter the journal name (e.g. plos one): plos one

Enter the search time (e.g. 2016): 2016


## Result

The result file will save as test.txt in current directory. The file format is

| HKU Scholarhub URL  | Manuscript DOI URL | Data Availability Comment |
| ------------- | ------------- |------------- |

Example

| HKU Scholarhub URL  | Manuscript DOI URL | Data Availability Comment |
| ------------- | ------------- |------------- |
| http://hub.hku.hk/handle/10722/241589 | http://dx.doi.org/10.1371%2Fjournal.pone.0169095 |All relevant data are within the paper and its Supporting Information files.|

