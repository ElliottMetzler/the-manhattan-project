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
    * 1) Make a database instance in Google Cloud Platform ("GCP"). Go to GCP SQL and create a PostgreSQL 13 database instance, you can use the ["Create an instance"](https://console.cloud.google.com/sql/choose-instance-engine?project=deft-diode-342909) to do so. Make sure you whitelist the IPs in block 0.0.0.0/0 and select a password for it.
    * 2) Create a database in GCP SQL and name it `drinks`. You can do that by going to the "Databases" tab in the newly created instance.
    * 3) Connect to your database with DBeaver. Your host is the `Public IP Address` found in GCP SQL on the "Overview" tab. The port will be the default Postgres port: `5432` and the username is the default Postgres username: `postgres`, you don't have to change it. The password is the same password you created for the instance. The database you need to select is `drinks`.
    * 4) In DBeaver, navigate to `drinks` > `databases` > `drinks`. Right-click the database `drinks`, then select `SQL Editor` > `New SQL Script`. 
    * 5) Copy the commands from [create_tables.sql](https://github.com/ElliottMetzler/the-manhattan-project/blob/get_data/setup/create_tables.sql) into the SQL Script and execute it to create the database tables.
    * 6) Create a bucket in GCP Cloud Storage. You can do that by accessing ["Cloud Storage"](https://console.cloud.google.com/storage/browser?_ga=2.133749006.1075698642.1652116044-1317346431.1646212364&_gac=1.195626590.1651155734.CjwKCAjw9qiTBhBbEiwAp-GE0Yk6cV8xAcydrJuB-bCw6AUvFJOwOvxnNvhWUdilN62kp9mxZnKz_hoCepoQAvD_BwE&project=deft-diode-342909&prefix=) in the GCP platform.
    * 7) Upload the `clean_data_no_header.csv` and the `ingredient_prices_clean.csv` to the newly created bucket. 
    * 8) Import the `clean_data_no_header.csv` from the bucket into the created table. To do so, you can go to GCP's SQL and use the import option, when prompt to choose a source, choose the CSV file from the bucket, with file format "CSV". For the "Destination", select the `drinks` database and the `all_cocktails` table. 
    * 9) After that import the `ingredient_prices_clean.csv` from the bucket into the created table. You should repeat the following step, but select the `ingredient_prices` table instead of the `all_cocktails`.
    * 10) Before you can run query commands, you must give it the right credentials to connect to your database. Copy the file demo.env to .env and modify it by providing the credentials you created in step (3). An easy way to do this is to run cp demo.env .env and then modify the file.

3) Instructions to produce figures:

4) Instructions to produce quantitative analysis: