import logging
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException
import time

class MetallumScraper:
    """
    Class that creates a Selenium scraper that is able to collect the names
    and data of albums, with a review rating above a threshold, from Metal-Archives
    for specific countries
    """
    base_url = 'https://www.metal-archives.com/browse/country'
    logging.basicConfig(filename='process_times.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

    def __init__(self, min_rating=85):
        """
        Description:    initializer for the scraper, stores the minimum rating
                        threshold, instantiates a Selenium webdriver with a
                        Firefox profile and navigates to the Metal-Archives
                        website
        """
        self.min_rating = min_rating
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        self.browser = webdriver.Firefox(firefox_profile)
        self.browser.get(MetallumScraper.base_url)
    
    def get_country_links(self, countries):
        """
        Description:    function that acquires the urls to the pages that list
                        all the bands for a single country, for the specified list
                        of countries
        
        Input:
        -countries:     list, the names of the countries for which the albums
                        will be scraped
        
        Output:
        -country_links: list, contains the names of the countries and their
                        respective urls
        """
        results = self.browser.find_elements_by_xpath("//div[@class='countryCol']/a")
        country_links = [(link.text, link.get_attribute('href')) for link in results if link.text in countries]
        return country_links

    def get_band_links(self, country, country_link):
        """
        Description:    retrieves the urls for all the bands from a single country

        Input:
        -country:       str, the name of the country
        -country_link:  str, the url of the page with all the bands for that country

        Output:
        -band_links:    list, contains the band names and the urls to their
                        band pages
        """
        band_links = []
        self.browser.get(country_link)
        while True:
            time.sleep(2)
            band_urls = self.browser.find_elements_by_xpath("//table[@id='bandListCountry']/tbody/tr/td/a")
            band_links += [(link.text, link.get_attribute('href')) for link in band_urls]
            try:
                next_page = self.browser.find_element_by_xpath("//div[@id='bandListCountry_paginate']/a[@class='next paginate_button']")
                next_page.click()
            except NoSuchElementException as e:
                break
        return band_links

    def scrape_bands_for_country(self, country, band_links):
        """
        Description:    function that scrapes the albums for all the bands from
                        a single country and logs the time it took to scrape,
                        as well as the average number of requests per second
                        issued by the scraper

        Input:
        -country:       str, the name of the country
        -band_links:    list, contains the band names and the urls to their
                        band pages

        Output:
        -results:       list, contains the scraped albums and extra information
                        about them (year of release, rating, etc.)
        """
        results = []
        t1 = time.time()
        for band_name, band_link in band_links:
            while True:
                self.browser.get(band_link)
                time.sleep(0.4)
                discog_elements = self.browser.find_elements_by_xpath("//table[@class='display discog']/tbody/tr")
                if discog_elements:
                    break
                else:
                    time.sleep(5)

            for row in discog_elements:
                table_entry = row.text.split()
                rating_string = table_entry[-1]
                if '%' in rating_string:
                    num_reviews = table_entry[-2]
                    year = table_entry[-3]
                    album_type = table_entry[-4]
                    album = ' '.join(table_entry[:-4])
                    rating = int(rating_string.replace('(', '').replace(')', '').replace('%', ''))
                    if rating >= self.min_rating:
                        url = row.find_elements_by_tag_name('a')[0].get_attribute('href')
                        results.append((band_name, country, url, album, year, rating, num_reviews, album_type))
        t2 = time.time()
        total_time = round(t2 - t1)
        logging.info(f'{len(band_links)} requests over {total_time} s = {len(band_links)/float(total_time)} per second')
        return results

    def scrape_for_all(self, countries):
        """
        Description:    scrapes the results for all of the specified countries
                        and logs the total processing time for each country

        Input:
        -countries      list, the names of the countries for which the albums
                        will be scraped

        Output:
        -results:       list, contains the scraped albums and extra information
                        for all specified countries
        """
        results = []
        country_links = self.get_country_links(countries)
        for country, country_link in country_links:
            start_time = time.time()
            band_links = self.get_band_links(country, country_link)
            results += self.scrape_bands_for_country(country, band_links)
            end_time = time.time()
            total_time = round(end_time - start_time, 2)
            logging.info(f'Processing time for {country} is {total_time} s')
        return results

    def close(self):
        """
        Description:    closes the webdriver
        """
        self.browser.quit()