from MetallumScraper import MetallumScraper
from MySQLConnector import MySQLConnector

scraper = MetallumScraper()
scraped_results = scraper.scrape_for_all(['Mongolia'])
scraper.close()

with open('database_credentials.txt', 'r') as f:
    host, user, passwd, database = f.readline().split()

connector = MySQLConnector(host, user, passwd, database)
colnames = ['band_name', 'country', 'url', 'album', 'year', 'rating', 'num_reviews', 'album_type']
connector.write_to_database('albums', colnames, scraped_results)
connector.close()