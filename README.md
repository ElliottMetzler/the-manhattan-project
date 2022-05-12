# the-manhattan-project
Team Good-2-Great Final project for Python, Data, and Databases at UT Austin Spring 2022.

Team Members: 
* [Pedro Rodrigues](https://github.com/PedroNBRodrigues) - Data engineering
* [Kashaf Oneeb](https://github.com/koneeb) - Data engineering, Report
* [Austin Longoria](https://github.com/galongoria) - Quantitative/Qualitative Analysis
* [Arpan Chatterji](https://github.com/achatterji1) - Quantitative/Qualitative Analysis
* [Colin McNally](https://github.com/cmcnally23) - Streamlit Development
* [Elliott Metzler](https://github.com/ElliottMetzler) - Project Management, Git Management, Report Writing

Due: 5/13/2022

## Introduction

Ever find yourself hankering for a drink but too tired to get to the store? We get it, it's been a rough week, it's Friday night, and all you want to do is quickly whip something up based on what you already have in the cabinet. That's where we come in. Our goal with The Manhattan Project is to use data on over 500 cocktails and allow you to search based on what you have handy. The Manhattan Project tool will beam you up with a handy list of delicious drinks containing what you've got on hand and how much effort you've got left in you (how many ingredients to include). Cheers!

The remainder of this report is structured as follows: first, we discuss the data used for our analysis and applet; next, we discuss the analytical approach we took [[more specific once we finalize here]]; finally, we conclude with closing thoughts on limitations of our analyis areas for potential extensions to this project and search engine.

## Database

[The Cocktail Database](https://www.thecocktaildb.com/) is "an open, crowd-sourced database of drinks and cocktails from around the world." The online database contains a total of 635 unique drinks ranging from classics like a [Manhattan](https://www.thecocktaildb.com/drink/11008-Manhattan) or a [Martini](https://www.thecocktaildb.com/drink/11728-Martini) to more peculiar concoctions like the [Brain Fart](https://www.thecocktaildb.com/drink/17120-Brain-Fart). It also contains listings for mixed shots like the [Lemon Shot](https://www.thecocktaildb.com/drink/12752-Lemon-Shot) or [Shot-gun](https://www.thecocktaildb.com/drink/16985-Shot-gun). 

Since the Cocktail Database (hereafter "cocktailDB") has a JSON API and richer extraction capabilities with a $2 fee to [Patreon](https://www.patreon.com/thedatadb) (not to be confused with [Patron](https://www.patrontequila.com/age-gate/age-gate.html?origin=%2F&flc=homepage&fln=Post_Homepage_Patron)), we purchased full access. We extracted the data using python, wrote schema in Postgres, and used Google Cloud Platform Buckets to upload csv files and import them into our own database.

The second important piece of data we use are ingredient prices from the web. We used a list of ingredients from the cocktailDB and leveraged Walmart's API for drink prices. As with the data from the cocktailDB, we uploaded a a table for ingredient prices to our own cloud database.

### Procedure

The first step in retrieving our data was to query the cocktailDB API endpoints for each drink in their database. To effectuate this, we cycled through each letter of the alphabet and digit 0-9, querying the database for cocktails starting with each letter or number. This approach yielded all 635 cocktails and their complete information.

The second step was to retrieve data on ingredient prices. 

1. Used BlueCart API which is a database of products sold by Walmart.
2. Used the ingredient list to query each ingredient and retrieved the description and price. 
3. First, we searched results for "best seller" in order to get an array of products that one would realistically purchase.
4. Then, we searched results for "best match" in order to get an array of products that would most closely represent the ingredient we are searching for.
5. The prices listed on BlueCart are not converted into ounces, which is why we also grabbed the description. In most cases, the description included the total measurement of the product in different units. However, the description also may have included numbers that did not relate to measurements. We noticed that the measurement and units was always at the end of the description, so we iterated through the description in reverse order, breaking once the full number was grabbed. We had a similar process for grabbing the units in which we iterated through the description in reverse order and grabbed the word if it exactly matched a unit measurement name. 
6. We did have to drop things like water and beer because these had descriptions such as "12 oz bottles, 12-count." Given the variablility in measurements and counts, we had to drop these and map them manually in the next cleaning process.
7. Next, we converted the total prices into prices per oz.
8. For the items not included in Walmart or with items that we were unable to convert with the above process, we mapped prices per oz based on the average of the first three prices online for the given ingredients.

To do so, we started with the list of unique ingredients in the cocktailDB, performed a combination of programatic and manual cleaning on the ingredients, then queried the Walmart API for as many ingredients as we could find. Finally, we implemented some additional manual web searching for certain missing ingredients to round out our data.


With our list of cocktails, ingredients, and prices, we used GCP Buckets to upload the necessary csv files into our SQL cloud database.

### Data

#### Description of the Raw cocktailDB Data

The raw data contains an entry (row) for each drink and many descriptive features (columns) about that drink. In addition to a unique ID for each drink and the drink name, it contains many classification fields such as the the drink category (i.e. cocktail, shot, punch/party drink, etc.), whether or not the drink is alcoholic and the type of glass this drink typically requires. Furthermore, it contains fields containing written instructions in multiple languages including english, german, french and italian. Most importantly, each cocktail has a set of columns reporting the ingredients required and a corresponding set of columns reporting the measurements of those ingredients. In the raw data, these ingredient measurements are non-standard in format and unit, including entries such as "2 shots", "2L", or "3 parts." Because these measurements are non-standard, this represented the biggest data cleaning effort to make our data useable for analysis.

#### CocktailDB Cleaning Process

Though we broadly attempted to upload the data to our database in as raw of a format as possible, we took some important cleaning steps. We dropped a few columns that we were certain not to use. More importantly, we cleaned the ingredient measurements and converted these values to standard fluid ounces so that we could estimate drink prices.

* The first step in our cleaning process was dropping columns with all missing values. These columns included the alternate drink name `strDrinkAlternate`, instructions in Spanish `strInstructionsES`, French `strInstructionsFR`, Chinese in simplified script `strInstructionsZH-HANS`, and Chinese in traditional script `strInstructionsZH-HANT`. Similarly, we noticed that none of the drinks had more than 12 ingredients, therefore, we dropped the ingredients and their respective measurement columns for ingredients 13 through 15 i.e. `strIngredient13`, `strIngredient14`, `strIngredient15`, `strMeasure13`, `strMeasure14`, and `strMeasure15`. 
* The next step was to remove rows that had none of the ingredient measurements specified, given that at least one ingredient was specified. We observed 7 such cases. For the remaining rows, we added the string "1 oz" for entries where the ingredient was specified but the respective measurement was not. We observed a total of 90 such cases. This step was necessary since we later convert missing values of measurements to "0" for the ingredients that were not specified.
* We then proceeded to create a total number of ingredients column `total_ingredients` that counted across the ingredient columns, 1 through 12 and returned the number of ingredients required to make the drink in the respective row. This column would be useful in specifying the number of ingredients needed to make a drink for our proposed applet.
* Next, we created 12 new "clean" ingredient measurement columns, `strMeasure1_clean` through `strMeasure12_clean` that hold cleaned strings from the actual ingredient measurement columns i.e. `strMeasure1` through `strMeasure12` with commas, and parentheses removed. We also removed specific words appearings before digits which included "Add", "Around rim put", "About", and "Juice of". This would allow us to convert strings to floats later in the cleaning process. 
* We then replaced new-line characters in the measaurement `strMeasure1` through `strMeasure12`, instructions `strInstructions`, `strInstructionsDE`, and `strInstructionsIT`, and image attribution `strImageAttribution` columns with the space character to improve compilation and readability of the csv file. 
* Finally, we created a unit conversion dictionary with all the units specified in the the "clean" measurement columns as keys and their respective measurement in ounces as values. We also converted fractions in the clean measurement columns to floats. Using regex and our unit conversion dictionary, we returned a csv with all the observations in the clean measurement columns converted to floats representing the ingredient measurements in ounces. This would prepare the measurement columns for the quantitative analysis. Note: our cleaning code returns two files: a csv with no headers to allow the data to fit the SQL table schema, and a csv with only headers as a reference to set up the SQL table schema.

#### Description of the Ingredient Prices Scraping Process

[[Austin to fill here / tell Elliott what to fill]]

#### Description of the Ingredient Prices Cleaning Process

[[Elliott to shift notes down when reviewing and drafting]]

## Analysis

We began our analysis by looking at ingredient prevalence. To do so, we checked the top 10 most used ingredients among the entire dataset. Our results are shown below:

Table***


This table shows that only three types of liquor–rum, gin, and vodka–are in at least 15% of the drinks. This was our first clue that some of the drinks in our dataset may not include liquor at all. Since we were interested in alcoholic cocktails...

Our next step was to determine the types of drinks we were interested in. Given this is a project on cocktails, we decided to focus on alcoholic beverages that include liquor. The 5 types of distilled spirits are: brandy, gin, rum, tequila, vodka, and whiskey. We reduced our dataset to include only drinks that included liquor falling into one of these 5 categories. We then looked at the most used spirits in cocktails that include liquor. The results can be seen below:

Table2***

Next, we looked at the prices of drinks and ingredients. It was clear to us that the most expensive ingredients were the different types of liquor, so our next step was to compare the price per ounce of the different types of spirits, which can be seen in the chart below:

BarChart****


Comparing this chart with the previous table (Table2), we can see that the most expensive spirits are used the least often. Interestingly, the least expensive liquor (grain alcohol) is also used the least often. We acknowledge the fact that there may be sampling bias associated with these proportions. However, it should be noted that rum and vodka were subdivided into "rum" and "vodka" and "flavored rum" and "flavored vodka". Even so, the "rum" and "vodka" categories lie in the top 3 most used spirits. We assume this is either because these spirits mix well with other ingredients or people just like the taste of them.

<!-- To determine this relationship, we ran an OLS regression of the amount of ingredients on the type of liquor, while controlling for the total ounces in a drink. Our dataset at this point included drinks that were tens of ounces or more. Since the impact of total ounces on number of ingredients for large drinks is so significant, we further subdivied our data into cocktails that are less than or equal to 8 ounces. This is a reasonable number for a person who is drinking a given cocktail in one sitting. -->  MIGHT GET RID OF THIS BC WE HAVE AN ABV ANALYSIS NOW



## Conclusion

[[Elliott to fill]]

## Reproducability Instructions

__NOTE__: [[Need to think about and verify what the system requirements are. We are going to have requirements for access to cloud buckets to upload the CSVs I think, along with GCP for normal stuff. Perhaps other for an app if we try to run one]]

1) Set-up Instructions:
    * Clone this repository to your local machine.
	* Run `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`, depending on your system.
	* Run `cd the-manhattan-project`

2) Instructions to scrape and clean data:
    * Run `python3 code/pull_raw_data.py` to scrape data from [The Cocktail DB](https://www.thecocktaildb.com) website and create two csv files: [drinks_data_raw.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/drinks_data_raw.csv) which contains raw data on drink recipes and [ingredients_data_raw.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/ingredients_data_raw.csv) which contains a list of all the ingredients specified in the recipes. The ingredient list will be utilized in pulling prices for the ingredients. 
    * Run `python3 code/clean.py` to create two csv files: [drinks_data_clean_no_header.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/drinks_data_clean_no_header.csv) which contains clean data with no headers to faciliate merging it into the SQL table and [drinks_data_headers.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/drinks_data_headers.csv) to serve as a reference for setting up the SQL table schema.

[[Elliott to add instructions on price scraping]]

3) Instructions to create the database:
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

4) Instructions to set up environment to connect SQLAlchemy engine to database:
    * Open the `demo.env` file and save a copy of this file as `.env`
    * Open the `.env` file and populate the variables with the appropriate credentials. Note that these credentials should be consistent with the credentials used to connect to the database using DBeaver in the prior step. 
    * Save the `.env` file and close.

5) Instructions to run Streamlit:
    * Run `streamlit run code/streamlitty.py`
    * Open a browser and copy the url.
    * View and use the applet!
