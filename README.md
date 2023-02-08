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

## Exercise 4

This exercise is for practicing object oriented programming and data ingestion.

It takes trading data from an API of cryptocurrencies and stores it locally into json files.