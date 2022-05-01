# the-manhattan-project
Team Good-2-Great Final project for Python, Data, and Databases at UT Austin Spring 2022.



### Procedure

The first step in retrieving the data from cocktailDB was to query the endpoints based on the first letter of the cocktail of interest. Thus, we looped through the alphabet from A to Z and through numbers from 0 to 9, querying data for each cocktail in the database starting with each letter and number. Then, we compiled these 36 pieces of output into one data frame and wrote this to a csv, while including the headers for each column.


After cleaning the csv and removing the headers from them, we used GCP Buckets to upload the csv files into our own SQL cloud database. 






## Reproducability Instructions

__NOTE__: [[Need to think about and verify what the system requirements are. We are going to have requirements for access to cloud buckets to upload the CSVs I think, along with GCP for normal stuff. Perhaps other for an app if we try to run one]]

1) Set-up Instructions:
	* Run `pip install -r requirements.txt`
	* Run `cd the-manhattan-project`

2) Instructions to create the database:
    * Make a database instance in GCP.
    * Create a database in GCP SQL and name it `drinks`.
    * In DBeaver, navigate to `drinks` > `databases` > `drinks`. Right-click the database `drinks`, then select `SQL Editor` > `New SQL Script`. 
    * Copy the commands from [create_tables.sql](https://github.com/ElliottMetzler/the-manhattan-project/blob/get_data/setup/create_tables.sql) into the SQL Script and execute it to create the database table.
    * Create a bucket in GCP Cloud Storage
    * Upload the [clean_data_no_header.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/get_data/data/clean_data_no_header.csv) to the newly created bucket.
    * Import the CSV from the bucket into the created table. To do so, you can go to [GCP's SQL](https://console.cloud.google.com/sql/instances/python-pedro/overview?project=deft-diode-342909) and use the import option, when prompt to choose a source, choose the CSV file from the bucket, with file format "CSV". For the "Destination", select the `drinks` database and the `all_cocktails` table.

3) Instructions to produce figures:

4) Instructions to produce quantitative analysis: