import uuid
from django.db import models


# Create your models here.
class Job(models.Model):
	job_id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable = False)


class Scrapping_Details(models.Model):
	job_obj=models.ForeignKey(Job,on_delete=models.CASCADE)
	coin=models.CharField(max_length=100, null=True,blank=True)
	price=models.CharField(max_length=100, null=True,blank=True)
	price_change=models.CharField(max_length=100, null=True,blank=True)
	market_cap=models.CharField(max_length=100, null=True,blank=True)
	market_cap_rank=models.CharField(max_length=100, null=True,blank=True)
	volume=models.CharField(max_length=100, null=True,blank=True)
	volume_rank=models.CharField(max_length=100, null=True,blank=True)
	volume_change=models.CharField(max_length=100, null=True,blank=True)
	circulating_supply=models.CharField(max_length=100, null=True,blank=True)
	total_supply=models.CharField(max_length=100, null=True,blank=True)
	diluted_market_cap=models.CharField(max_length=100, null=True,blank=True)
	

class Contracts(models.Model):
	scraping_details=models.ForeignKey(Scrapping_Details,on_delete=models.CASCADE,null=True,blank=True)
	name=models.CharField(max_length=100, null=True,blank=True)
	address=models.CharField(max_length=100, null=True,blank=True)

class Official_Links(models.Model):
	scraping_details=models.ForeignKey(Scrapping_Details,on_delete=models.CASCADE,null=True,blank=True)
	name=models.CharField(max_length=100, null=True,blank=True)
	link=models.URLField(max_length=200,null=True,blank=True )

class Socials(models.Model):
	scraping_details=models.ForeignKey(Scrapping_Details,on_delete=models.CASCADE,null=True,blank=True)
	name=models.CharField(max_length=100, null=True,blank=True)
	link=models.URLField(max_length=200,null=True,blank=True )