from django.shortcuts import render

# Create your views here.

from celery import shared_task
from selenium import webdriver
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
from .models import *






class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def __init__(self, coin,job_id):
        self.coin = coin
        self.url = f"{self.BASE_URL}{coin}/"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.job_id=job_id

    def fetch_page(self):
        self.driver.get(self.url)

    def scrape_data(self):
        try:
            self.fetch_page()
            # officail_links_list={}
            # socials_list={}
            # contracts={}
            price = self.driver.find_element(By.XPATH, '//*[@id="section-coin-overview"]/div[2]/span').text
            price_change = self.driver.find_element(By.XPATH, '//*[@id="section-coin-overview"]/div[2]/div/div/p').text
            market_capital = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[1]/dd').text
            market_capital_rank = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[2]/div/span').text
            volume = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[1]/dd').text
            volume_rank = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[2]/div/span').text
            volume_change = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[3]/div/dd').text
            circulating_supply = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[4]/div/dd').text
            total_supply = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[5]/div/dd').text
            diluted_market_cap = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[7]/div/dd').text
            cont_name = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div/div/a/span[1]').text
            cont_address = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[1]/div[2]/div/div[1]/a')

            # contracts['name']=cont_name
            # contracts['address']=cont_address.get_attribute("href").split('/')[-1]


            





            price1=float(re.sub(r'[^0-9.]', '', price))

            price_change1=float(re.sub(r'[^0-9.]', '', price_change.split('%')[-2]))
            market_capital1=market_capital.split('$')[-1]
            market_capital_rank1=int(re.sub(r'[^0-9.]', '', market_capital_rank))
            volume1=float(re.sub(r'[^0-9.]', '', volume.split('$')[-1]))
            volume_rank1=int(re.sub(r'[^0-9.]', '', volume_rank))
            volume_change1=float(re.sub(r'[^0-9.]', '', volume_change))
            circulating_supply1=circulating_supply.split(' ')[-2]
            total_supply1=total_supply.split(' ')[-2]
            diluted_market_cap1=re.sub(r'[^0-9.]', '', diluted_market_cap)
                
            scrap=Scrapping_Details.objects.create(job_obj=self.job_id,coin=self.coin,price=price1,price_change=price_change1,market_cap=market_capital1,market_cap_rank=market_capital_rank1,
                                                 volume=volume1,volume_rank=volume_rank1,volume_change=volume_change1,
                                                 circulating_supply=circulating_supply1,total_supply=total_supply1,diluted_market_cap=diluted_market_cap1)
                
            Contracts.objects.create(scraping_details=scrap,name=cont_name,address=cont_address.get_attribute("href").split('/')[-1])
                
            officail_links_element = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[2]/div[2]/div')
            links=officail_links_element.find_elements(By.CSS_SELECTOR, 'a')
            for link in links:
                href = link.get_attribute('href')
                text = link.text
                print('---------------ii---',href)
                print('---------------ii',text)
                # officail_links_list['name']=text
                # officail_links_list['url']=href
                Official_Links.objects.create(scraping_details=scrap,name=text,link=href)


            
            socials_element = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[3]/div[2]/div')
            links1=socials_element.find_elements(By.CSS_SELECTOR, 'a')
            for link1 in links1:
                href = link1.get_attribute('href')
                text = link1.text
                # socials_list['name']=text
                # socials_list['url']=href
                Socials.objects.create(scraping_details=scrap,name=text,link=href)

        except:
            scrap=Scrapping_Details.objects.create(job_obj=self.job_id,coin=self.coin)

        data={'id':self.job_id.job_id}
        self.driver.quit()
        return data






