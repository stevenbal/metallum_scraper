from MetallumScraper import MetallumScraper
from MySQLConnector import MySQLConnector
import sys

if len(sys.argv) > 1:
    countries = sys.argv[1:]
else:
    print('Please specify the countries to be scraped')
    exit()

scraper = MetallumScraper()
scraped_results = scraper.scrape_for_all(countries)
scraper.close()

with open('database_credentials.txt', 'r') as f:
    host, user, passwd, database = f.readline().split()

connector = MySQLConnector(host, user, passwd, database)
colnames = ['band_name', 'country', 'url', 'album', 'year', 'rating', 'num_reviews', 'album_type']
connector.write_to_database('albums', colnames, scraped_results)
connector.close()