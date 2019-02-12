# metallum_scraper

A Python scraper that scrapes albums with a rating above a specified threshold from Metal-Archives
and writes them and their metadata to a MySQL database.

## Dependencies
Written in Python version 3.6.2, dependencies are listed in 'environment.yml'.
Using an environment manager such as conda, the correct packages can be easily installed
by using the following bash command:
```console
user@user:~$ conda env create -f environment.yml
```
The environment can be activated using:
```console
user@user:~$ source activate metallum_scraper
```

The environment can be deactivated using:
```console
user@user:~$ source deactivate
```

## Setting up Selenium webdriver
The required Firefox webdriver for Selenium can be acquired [here](https://www.seleniumhq.org/download/)

## Setting up the MySQL database
Using the following bash command, a MySQL database with the name 'metallum' will
be created, with a table called 'albums'

Make sure that MySQL is already installed on your machine
```console
user@user:~$ mysql -u <user> -p < dump.sql 
```

## Setting up database information
In order to make the script run correctly, a file called 'database_credentials.txt'
must be created, which should adhere to the following structure:
```
<hostname> <user> <password> <database>
```
Where the credentials are to be filled in (hostname will most likely be localhost
and the database name is metallum by default)

## Usage
The script can be used as follows:
```console
user@user:~$ python scrape_metallum.py <Country1> <Country2> ...
```
Where Country1, Country2, ... denote the countries you want the albums to be
scraped for