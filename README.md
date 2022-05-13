# the-manhattan-project
Team Good-2-Great Final project for Python, Data, and Databases at UT Austin Spring 2022.

Team: 
* [Pedro Rodrigues](https://github.com/PedroNBRodrigues) - Data Engineering, Report
* [Kashaf Oneeb](https://github.com/koneeb) - Data Engineering, Report
* [Austin Longoria](https://github.com/galongoria) - Data Engineering, Analysis
* [Arpan Chatterji](https://github.com/achatterji1) - Analysis
* [Colin McNally](https://github.com/cmcnally23) - Streamlit Front End Dev
* [Elliott Metzler](https://github.com/ElliottMetzler) - Project Management, Git Management, Report, Streamlit Back End Dev

Due: 5/13/2022

## Introduction

Ever find yourself hankering for a drink but too tired to get to the store? We get it, it's been a rough week, it's Friday night, and all you want to do is quickly whip something up based on what you already have in your cabinet. That's where we come in. Our goal with The Manhattan Project is to use data on over 500 cocktails and allow you to search based on what you have handy. The Manhattan Project tool will beam you up with a handy list of delicious drinks containing what you've got on hand and how much effort you've got left in you (how many ingredients to include). Cheers!

The remainder of this report is structured as follows: first, we discuss the data used for our analysis and applet; next, we discuss our analytical approach and results; finally, we conclude with closing thoughts on limitations of our analysis areas for potential extensions to this project and search engine.

## Database

[The Cocktail Database](https://www.thecocktaildb.com/) is "an open, crowd-sourced database of drinks and cocktails from around the world." The online database contains a total of 635 unique drinks ranging from classics like a [Manhattan](https://www.thecocktaildb.com/drink/11008-Manhattan) or a [Martini](https://www.thecocktaildb.com/drink/11728-Martini) to more peculiar concoctions like the [Brain Fart](https://www.thecocktaildb.com/drink/17120-Brain-Fart). It also contains listings for mixed shots like the [Lemon Shot](https://www.thecocktaildb.com/drink/12752-Lemon-Shot) or [Shot-gun](https://www.thecocktaildb.com/drink/16985-Shot-gun). 

Since the Cocktail Database (hereafter "cocktailDB") has a JSON API and richer extraction capabilities with a $2 fee to [Patreon](https://www.patreon.com/thedatadb) (not to be confused with [Patron](https://www.patrontequila.com/age-gate/age-gate.html?origin=%2F&flc=homepage&fln=Post_Homepage_Patron)), we purchased full access. We extracted and cleaned the data using Python, wrote schema in Postgres, and used Google Cloud Platform Buckets to upload csv files and import them into our own database.

The second important piece of data we used are ingredient prices from the web. We compiled a list of ingredients from the cocktailDB and leveraged [BlueCart API](https://www.bluecartapi.com) for drink prices. As with the data from the cocktailDB, we uploaded a table of ingredient prices to our database.

### Cocktail Data

The first step in retrieving our data was to query the cocktailDB API endpoints for each drink in their database. To do this, we looped over each letter of the alphabet and digits 0-9, querying the database for cocktails starting with each letter or number. This approach yielded all 635 cocktails and their complete information.

#### Description of the Cocktail Data

The raw data contains an entry (row) for each drink and many descriptive features (columns) about that drink. In addition to a unique ID for each drink and the drink name, it contains a handful of classification fields such as the the drink glass type (e.g. highball, shot glass, punch bowl, etc.) and whether or not the drink is alcoholic. Additionally, it contains fields containing written instructions in multiple languages including English, German, French and Italian. Most importantly for our purposes, each cocktail has a batch of columns reporting the ingredients required to make that cocktail and a corresponding set of columns reporting the measurements of those ingredients. In the raw data, these ingredient measurements are non-standard in format and unit, including entries such as "2 shots", "2L", or "3 parts." Since these measurements are non-standard, this represented the biggest data cleaning effort to prepare our data for analysis.

#### Cocktail Data Cleaning Process

Though we broadly attempted to upload the data to our database in as raw of a format as possible, we took some important cleaning steps. We dropped a few columns that we were certain not to use. Most importantly, we cleaned the ingredient measurements and converted these values to ounces so that we could estimate drink prices.

* The first step in our cleaning process was dropping columns with all missing values. These columns included the alternate drink name `strDrinkAlternate`, instructions in Spanish `strInstructionsES`, French `strInstructionsFR`, Chinese in simplified script `strInstructionsZH-HANS`, and Chinese in traditional script `strInstructionsZH-HANT`. Similarly, we noticed that none of the drinks had more than 12 ingredients, therefore, we dropped the ingredients and their respective measurement columns for ingredients 13 through 15 i.e. `strIngredient13`, `strIngredient14`, `strIngredient15`, `strMeasure13`, `strMeasure14`, and `strMeasure15`. 
* The next step was to remove rows that had none of the ingredient measurements specified, given that at least one ingredient was specified. We observed 7 such cases. For the remaining rows, we added the string "1 oz" for entries where the ingredient was specified but the respective measurement was not. We observed a total of 90 such cases. This step was necessary since we later convert missing values of measurements to "0" for the ingredients that were not specified.
* We then proceeded to create a total number of ingredients column `total_ingredients` that counted across the ingredient columns, 1 through 12 and returned the number of ingredients required to make the drink in the respective row. This column would be useful in specifying the number of ingredients needed to make a drink for our proposed applet.
* Next, we created 12 new "clean" ingredient measurement columns, `strMeasure1_clean` through `strMeasure12_clean` that hold cleaned strings from the actual ingredient measurement columns i.e. `strMeasure1` through `strMeasure12` with commas, and parentheses removed. We also removed specific words appearing before digits which included "Add", "Around rim put", "About", and "Juice of". This would allow us to convert strings to floats later in the cleaning process. 
* We then replaced new-line characters in the measurements `strMeasure1` through `strMeasure12`, instructions `strInstructions`, `strInstructionsDE`, and `strInstructionsIT`, and image attribution `strImageAttribution` columns with the space character to improve compilation and readability of the csv file. 
* Finally, we created a unit conversion dictionary with all the units specified in the "clean" measurement columns as keys and their respective measurement in ounces as values. We also converted fractions in the clean measurement columns to floats. Using regex and our unit conversion dictionary, we returned a csv with all the observations in the clean measurement columns converted to floats representing the ingredient measurements in ounces. This would prepare the measurement columns for the quantitative analysis. Note: our cleaning code returns two files: a csv with no headers to allow the data to fit the SQL table schema, and a csv with only headers as a reference to set up the SQL table schema.

### Ingredient Prices Data

To retrieve data on ingredient prices, we combined a list of ingredients from the cocktail database to search a Walmart price database called BlueCart API. Using this, we performed a combination of programatic and manual cleaning on the ingredient prices, then imported the resulting data into our database. One key nuance to our approach to searching the BlueCart API was using two searches to achieve most representative results. We queried both for "best seller" and "best match" for each ingredient.  we  then combined these two searches in an effort to get the closest, most accurate, representation of the price of that ingredient.

#### Description of the Ingredient Prices Data

The raw ingredient prices data returned from the BlueCart API included information on the ingredient name (based on our search parameters) and the price of the ingredient. However, this ingredient price was also not in standardized unit format, so as with the Cocktail Data we had to perform a cleaning process to convert units into a consistent format for use. Thus, in addition to the name of the product and the price, we retrieved the description to obtain the size of the portion so we could perform analysis to convert units.

#### Ingredient Prices Data Cleaning Process

To clean the Ingredient Prices Data, we utilized the descriptions for the products. We found that the measurement and units were consistently appearing at the end of the product description, so we iterated through descriptions in reverse order to extract the unit and portion size. As stated before we took results on Walmart's website for both "best seller" and "best match", each of which yielded slightly different results. In the cases where we received price data for both queries, we averaged the values for both. However, in most cases there was a price for only one type of result. This is because "best seller" most times gave unrelated products. Similarly, best match did not always give the correct item. For certain ingredients, we were unable to systematically perform conversions, so we implemented a manual verification and review step separately to fill in necessary missing entries and convert in certain cases. For our final step, we converted prices to a per ounce basis.

## Streamlit Applet

The primary goal of this project was to use our database to produce a handy Streamlit applet to allow users to query for drinks using various search parameters. We allow users to query based on the following parameters:
* Ingredient Count: the maximum number of ingredients they have available or would be willing to include in their cocktail.
* Main Liquors: Some main liquors like Vodka, Whiskey, or Tequila to allow users to easily find recipes with common ingredients.
* Other Ingredients: Using a unique list of ingredients appearing in the database, we allow users to get specific if they have something they'd like to focus on or use up.

## Analysis

The secondary goal of this project was to use our database to analyze the cocktail data.

We began our analysis by looking to understand the prevalence of various ingredients. Prior to any ingredient recoding, we found over 400 ingredients in the raw data. However, through careful review to account for things like typos and unecessary specificity, we recoded the ingredients list to ultimately include around 70 unique ingredient categories. We summarize the prevalence of various ingredient categories in Table 1.

### Table 1: Top 10 Most Prevalent Ingredient Categories

![](/tables/usage.png)

As shown in the table, fruit juice is the most common ingredient in our cocktail data, appearing in approximately 40 percent of all cocktails. Various types of liqueurs, fruits, and sugars also appear very frequently, with over 30 percent prevalence. The most common liquors are rum, gin, and vodka. Something that suprised us when reviewing this analysis was to find that the milk category, which includes items like milk or cream, was slightly more prevalent than soda. Perhaps there are more variations of the [White Russian](https://www.thekitchn.com/the-celluloid-p-16-8755) than we previously thought.

To further drill down the focus of our analysis on liquor rather than the other ingredients, we also performed exploratory analysis on a subset of the data in which each drink contained an identified key liquor. Once we filtered the data and focused on drinks containing alcohol, we were able to better understand within the alcohol category what was most common. We summarized this analysis in Table 2.

### Table 2: Liquor Prevalence Summary

![](/tables/liquor.png)

As we would have expected, we still see rum, vodka, and gin as the most common types of liquor. We note that despite separating the rum and vodka categories into plain and flavored, we still found these as two of the top three. This analysis was consistent with our previous understanding that these three liquors tend to mix well in cocktails and thus are very common. We similarly expected liquors like bourbon, scotch, and cognac to appear at the bottom of this list since they are much more commonly consumed neat or on the rocks rather than sullied in a cocktail.

In addition to understanding the prevalence of ingredients and liquors, we wanted to understand the pricing component of drinks in our database. Generally speaking, the liquor is the most expensive ingredient in a given cocktail, so we first present our estimates of cost of liquor in dollars per ounce. 

### Figure 1: Liquor Price ($/ounce)

![](/figures/prices.png)

By comparing this chart to Table 2, we see that the most expensive spirits are used the least often. Interestingly, the least expensive liquor (grain alcohol) is also used the least often. However, we suspect that this is simply because no one *really* wants to be drinking everclear.

With both of these exploratory observations in mind, we arrive at the core question of our analysis: is less truly more? Does one get more return on investment from a complex, tasty artisan cocktail with several ingredients or from drinking something concentrated and straightforward? 

To help us answer this question, we first calculated the ounces of alcohol per dollar for each drink. For example, if a 12 ounce beer contains 10 percent alcohol by volume and costs 6 dollars, the ounces of alcohol per dollar for that drink would be (12 x 0.10) / 6 = 0.2oz / $. Similarly, a 12 ounce beer containing 5 percent alcohol by volume that costs 3 dollars would also report (12 x 0.05) / 3 = 0.2oz / $.

Additionally, we filtered our data such that the drinks in question contained at least 2.5 ounces and no more than 15 ounces. We performed this filter to ensure we focused on cocktails as opposed to shots or punch bowls.

Our last step prior to running the model was to analyze the relationships between candidate variables. We produced a correlation table and present the results as a heatmap below in Figure 3.

### Figure 3: Correlation Heat Map: OLS Model Features 

![Heat Map](/figures/heat_map.png)

As we can see, most variable correlations fall somewhere between 0.0 and 0.2. In the bottom right corner we can see some stronger relationships. As we would expect, ounces of alcohol and ounces of alcohol per dollar are related (since one is a function of the other). Alcohol content per dollar and number of ingredients are negatively correlated. We see a positive correlation between number of ingredients and cost.

There is no significant relationship between total ounces and either ounce of alcohol or the number of ingredients. Thus, our final list of covariates includes ounces of alcohol, number of ingredients, and dummies for each liquor type. We display the output of our regression model below.

### Table 3: Regression Output

![](/figures/ols.png)

From this output, we can make a few interesting observations. The negative coefficient for the number of ingredients can be interpreted as follows: An additional ingredient leads to an expected decrease of 0.141 ounces of alcohol per dollar. This result makes sense because more often than not, the incremental incredient will not be alcoholic. Furthermore, additional ingredients increase the total cost of the cocktail, driving down the expected ounces of alcohol per dollar. Next, we see a positive coefficient for ounces of alcohol. On average, an increase in one ounce of alcohol leads to an increase in 0.614 ounces of alcohol per dollar. This may be the result of the cost of alcohol, which could offset the increase in ounces of alcohol per dollar in a way that prevents a one-to-one relationship. Last, we see mostly negative coefficients on the liquor dummy variables, though some are not statistically significant. We note that the dummy variable dropped from the regression is is grain alcohol.

## Conclusion

Through The Manhattan Project, we were able to provide the world a great service, though perhaps slightly less explosive than the last time around. Our Streamlit app provides the user with a handy interface to search for some fun, interesting, and unique cocktails based solely on what they've got handy and how much effort they are willing to expend. Furthermore, our quantitative analysis shows the benefits of just a little more research when evaluating your cocktail choices.

Though we are proud of our progress, our project of course carries some important caveats. On the data side of things, we certainly are limited in some key areas. To convert units in our cocktail data from non-standard to standard, we had to make some judgement calls. When pricing our ingredients, we also had to make some judgement calls as far as producing reasonable estimates. Of course, prices are subject to variability in stores around the country, and also are subject to differences in liquor quality going into the cocktail. For instance, a Kamchatka martini and a Grey Goose martini are two very different drinks carrying two very different prices, however, for our purposes, we simply are taking best selling alcohol estimates for vodka and using these in our pricing formula. Furthermore, we are limited by The Cocktail Database being an open source database where anyone with a key can edit or add new cocktails, which may lead to contamination of the data through random creations or data entry errors.

A limitation, or perhaps better described as an area for extension, is in our ability to categorize or rank drinks in our search algorithm. We do not have any sort of popularity metric for our drinks, so the output based on the parameters is random so long as enough cocktails fit the search criteria. A nice extension in the future may be to find data on drink popularity and implement this into our search algorithm. Another good extension requiring more robust input data would be to allow for more granular search and price estimates based on a more thorough ingredient price search. We could indeed price out Grey Goose Martinis as opposed to Kirkland brand vodka Martinis with additional data and time to implement adjustments.

In the future, we look forward to expanding our cocktail search engine capabilities.

## Reproducability Instructions

1) Set-up Instructions:
    * Clone this repository to your local machine following the standard procedure of copying the SSH clone path and running `git clone <CLONE_PATH>`.
    * Run `cd the-manhattan-project`
    * Run `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`, depending on your system.

2) Instructions to source and clean the data:
    * Run `python3 code/pull_raw_data.py` to scrape data from [The Cocktail DB](https://www.thecocktaildb.com) website and create two csv files: [drinks_data_raw.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/drinks_data_raw.csv) which contains raw data on drink recipes and [ingredients_data_raw.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/ingredients_data_raw.csv) which contains a list of all the ingredients specified in the recipes. The ingredient list will be utilized in pulling prices for the ingredients. Note that you will need to acquire an API key and insert it into the file. Specifically, replace the string "INSERT_API_KEY" with your API key. To acquire an API key, you can go to [The Cocktail DB Patreon](https://www.patreon.com/thedatadb). The $2 level supporter is more than enough for a key that gives access to all the drinks in the database and the ingredient list API search. After acquiring it, it should take up to an hour to receive it, keep in mind that the creators work under the GMT working hours, so it may take longer.
    * Run `python3 code/clean.py` to create two csv files: [drinks_data_clean_no_header.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/drinks_data_clean_no_header.csv) which contains clean data with no headers to faciliate merging it into the SQL table and [drinks_data_headers.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/drinks_data_headers.csv) to serve as a reference for setting up the SQL table schema.
    * Run `python3 code/prices_pull.py` to scrape data from the BlueCart API. Note that you will need to acquire an API key and insert it into the file in the parameters section. Specifically, replace the string "INSERT_API_KEY" with your API key. To get a BlueCart API key, head to [their website](https://www.bluecartapi.com/) and follow the instructions. This pulling file will create two .txt files in the data folder: [items_best_match.txt](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/items_best_match.txt) and [items_best_seller.txt](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/items_best_seller.txt) containing the raw json data.
    * Run `python3 code/prices_clean.py`. This file will produce the [ingredients_prices_raw.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/ingredient_prices_raw.csv) file containing the cleaned, but incomplete data pull.
    * Run `python3 code/input_missing_prices.py`. This file will produce the [ingredient_prices_clean.csv](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/data/ingredient_prices_clean.csv) file with the complete ingredient prices data.

3) Instructions to create the database:
    * Make a database instance in [Google Cloud Platform ("GCP")](https://cloud.google.com/). Go to GCP SQL and create a PostgreSQL 13 database instance, you can use the ["Create an instance"](https://console.cloud.google.com/sql/choose-instance-engine?project=deft-diode-342909) to do so. Make sure you whitelist the IPs in block `0.0.0.0/0` and select a password for it.
    * Create a database in GCP SQL and name it `drinks`. You can do that by going to the "Databases" tab in the newly created instance.
    * Connect to your database with DBeaver. Your host is the `Public IP Address` found in GCP SQL on the "Overview" tab. The port will be the default Postgres port: `5432` and the username is the default Postgres username: `postgres`, you don't have to change it. The password is the same password you created for the instance. The database you need to select is `drinks`.
    * In DBeaver, navigate to `drinks` > `databases` > `drinks`. Right-click the database `drinks`, then select `SQL Editor` > `New SQL Script`. 
    * Copy the commands from [create_tables.sql](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/setup/create_tables.sql) into the SQL Script and execute it to create the database tables.
    * Create a bucket in GCP Cloud Storage. You can do that by accessing ["Cloud Storage"](https://console.cloud.google.com/storage/browser?_ga=2.133749006.1075698642.1652116044-1317346431.1646212364&_gac=1.195626590.1651155734.CjwKCAjw9qiTBhBbEiwAp-GE0Yk6cV8xAcydrJuB-bCw6AUvFJOwOvxnNvhWUdilN62kp9mxZnKz_hoCepoQAvD_BwE&project=deft-diode-342909&prefix=) on the GCP platform.
    * Upload the `drinks_data_clean_no_header.csv` and the `ingredient_prices_clean.csv` to the newly created bucket. 
    * Import the `drinks_data_clean_no_header.csv` from the bucket into the created table. To do so, you can go to GCP's SQL and use the "import" option, when prompted to choose a source, choose the CSV file from the bucket, with file format "CSV". For the "Destination", select the `drinks` database and the `all_cocktails` table. 
    * Next, import the `ingredient_prices_clean.csv` from the bucket into the created table. You should repeat the following step, but select the `ingredient_prices` table instead of the `all_cocktails` table.
    * Before you can run query commands, you must give it the right credentials to connect to your database. Copy the file demo.env to .env and modify it by providing the credentials you created above. An easy way to do this is to run `cp demo.env .env` and then modify the .env file.

    Note: The file [database.py](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/code/database.py) addresses database configuration using SQLAlchemy and creates an engine to initialize a DBAPI connection.

4) Instructions to run the Streamlit app:
    * Run `streamlit run code/streamlitty.py`. This file utilizes the module [streamlit_query_functions.py](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/code/streamlit_query_functions.py). This will produce two lines of output in your terminal window: a network url and a external url. 
    * Open your browser of choice and copy the network url from the terminal to your browser search bar. Click enter or refresh.
    * View and use the applet!
    
5) Instructions to run Quantitative Analysis:
    * Run `python3 code/tables.py`. This will utilize the file [quant_preprocess.py](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/code/quant_preprocess.py) which queries the database for ingredient names, ingredient measurements, and ingredient prices. The `quant_preprocess.py` file, in turn, utilizes the file [ingredient_map.py](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/code/ingredient_map.py) which uses a unique list of the ingredients in our data and creates a mapping dictionary to simplify them. Running `tables.py` should create three figures in the [figures](https://github.com/ElliottMetzler/the-manhattan-project/tree/main/figures) directory and two tables in the [tables](https://github.com/ElliottMetzler/the-manhattan-project/tree/main/tables) directory. All the outputs will be created in a .png format. Note: You will need to add Google Chrome to your PATH in order to output tables properly-this is a requirement of the dataframe_image package.
        * The `figures` directory will hold the following png's:  
            * [heat_map.png](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/figures/heat_map.png) which is a heat map of correlations between various liquors and calculated attributes of drinks.
            * [ols.png](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/figures/ols.png) which is a regression results table of regressing `oz_alc_per_dollar` on various covariates. 
            * [prices.png](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/figures/prices.png) which is a bar chart summarizing the cost of liquor against the type of liquor. 
        * The `tables` directory will hold the following png's:
            * [liquor.png](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/tables/liquor.png) which displays a list of liquors and the proportion of drinks containing the respective liquor (for liquors with proportion of drinks higher than 0.29%)
            * [usage.png](https://github.com/ElliottMetzler/the-manhattan-project/blob/main/tables/usage.png) which displays a list of the remaining ingredients and the proportion of drinks containing the respective ingredient (for ingredients with proportion of drinks higher than 13%)