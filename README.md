# Data engineering exercises

**Python** is mandatory for running these exercises.

Each exercise has a "requirements.txt" file that should be installed in order to execute the scripts.

```pip
pip install -r requirements.txt
```

Jupyter notebook is recommended for better data visualization.

To install **venv** to jupyter you must run the following command on **virtualenv**

```python
python -m ipykernel install --user --name=myenv
```

Some exercises have **docker-compose** files to create isolated and secure local environments.

To run those you need to have installed **docker** and **docker-compose** in your host machine.

Then you need to execute the following line inside the folder containing the .yml file.

```docker-compose
docker-compose up
```

This will instanciate one or more containers with binded volumes. Remember, these containers are only intended to be used in development.

To deploy them in production you need to take care of any credentials.

---

## Exercise 1

Shows how to create requests to websites and use it with pandas and jupyter notebooks.

The example shows how to access lotery data using beautiful soup and how to create some statistics with it.

---

## Exercise 2

Shows how to create basic web scrapping applications.

The example shows how to access real state data and podcast data from two different websites using beautiful soup.

---

## Exercise 3

Shows how to create docker containers using docker-compose and how to use postgres as a relational database.

It also instantiates a pg4admin for managing the database and shows a python script to interact with postgres.

Finally it shows how to instantiate a metabase for business intelligence applications.

Metabase provides a friendly user interface to interact with data, create views and dashboards.

---

## Exercise 4

This exercise is for practicing object oriented programming and data ingestion.

It takes trading data from an API of cryptocurrencies and stores it locally into json files.

---

## Challenge 1

This challenge uses a kaggle database available [here](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017?select=shootouts.csv) which contains international football results as match scores and player goals.

The challenge was to import this .csv file into a postgres database and to develop insights from it using any data visualization technique available, like metabase for BI or pandas and seaborn using pure Python.

It was also an oportunity to train some SQL query scripting.

To import the .csv, pgadmin4 was used. A manual import is done after manually creating a table for each .csv.

You can refer on how to import .csvs [here](https://hevodata.com/learn/pgadmin-import-csv/) and [here](https://learnsql.com/blog/how-to-import-csv-to-postgresql/)

To use metabase you need to create new queries. The .sql files in this exercise are good examples to create meaningful information for a dashboard.

You can achieve a similar result from the image.
![Image](Challenge 1\metabase-dashboard.png)

In the jupyter notebook there's an example of importing data from postgres directly into pandas to generate graphs using seaborn.

---

### Exercise 5

This exercise focus on unitary tests.

Mocks and patches are used.

Tests requires particular modules. Those can be installed with the requirements.txt inside the tests folder.

To run tests you should execute the following line after installing the requirements.

```python
python -m pytest
```

All tests are expected to pass in current version.

If you want to see the coverage of the testing codes, you can type:

```python
python -m pytest --cov=mercado_bitcoin tests/
```

The ideal production coverage is above 80%.

Extra:

Now this code is implemented to run on AWS. The overview of the cloud formation is presented on the image below.

![image](https://user-images.githubusercontent.com/14501830/226216295-6e6be35d-b873-4e48-9438-a0af99709287.png)

Please note that to run on AWS you need to configure a .env containing your credentials configured in IAM. An example .env is provided.
The profile needs to have full access to lambda, dynamodb and s3.
Note that lambda only supports up to python 3.9. This project uses python 3.11 so it will not work directly on lambda at the moment.
To use it on zappa serverless to automatically create a lambda service you need to give lambda_function.py as the entrypoint for lambda execution, but again you need up to python 3.9.
But at the moment you can only run this code locally to ingest data and send it to test S3 and DynamoDB writing.

---

### Exercise 6

This exercise is just focused on creating a jenkins instance to schedule a currency quoting.

---

### Exercise 7

This exercise aims to practice web crawlers using selenium.

The first script main.py gets address info from correios do brasil website using CEP code.

To use it you need to insert cep as an argument and run it like:

```python
python main.py <cep>
```

The next script searches for nicholas cage portuguese wikipedia page and gets a table containing the list of all his movies. Then it stores this information into a .csv file.

---

### Exercise 8

This exercise focus on creating an access to AWS s3.

You need to create an account on aws and an API key for your account.

This API id key and password should be provided on a .env file on Exercise 8 folder for aws.py to run correctly.

There's a .env example file on the repo as reference. You should edit it and rename as .env inside Exercise 8 folder.

This script simply creates a test bucket. To avoid unecessary billings, you should delete the test bucket rightly after script execution on AWS console.

---

### Challenge 2

This exercise populates an AWS RDS Postgres with fake customer data to be replicated by a DMS to a bucket. The whole process of creating AWS instances is not documented here and it's an extensive and error prone process.

---

### Exercise 9

This exercise populates a topic (SNS) to feed a queue (SQS) that is consumed by a Kinesis Firehose to store fake messages on a data-lake-raw.

