# Docker env for postgres

You need to have docker installed and configured to run this exercise.

First you have to build the image from the docker file using

```dockerfile
docker build -t web_apache
```

This creates an image to expose a html file using web_apache.

Then you have to create containers for postrgres and pgadmin using docker compose:

```docker-compose
docker-compose up
```

"charts.csv" is used to populate the database it is a collection of all "The Hot 100" charts released since its inception in 1958 as stated in [kaggle](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs) from where this data was collected.

"create-table-billboard" has the SQL for table creation and some example queries.

