




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import GroupResult
from .tasks import scrape_coin
from .serializers import ScrapSerializer, ScrapStatusSerializer
from celery import group
from .models import *



class StartScrapingView(APIView):
    def post(self, request, *args, **kwargs):
        print('---------dataaaa,',request.data)


        serializer = ScrapSerializer(data=request.data)
        if serializer.is_valid():
            coins=[]
            coins = serializer.validated_data['coins']
            print('-------coins',coins)
            # job = group(scrape_coin.s(coin) for coin in coins).apply_async()
            job_obj1=Job.objects.create()
            for coin in coins:
                task = scrape_coin(coin,job_obj1)
            return Response({'job_id': task['id']}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScrapingStatusView(APIView):
    def get(self, request, job_id, *args, **kwargs):
        # group_result = GroupResult.restore(job_id)
        scrap_list=[]
        scrap=Scrapping_Details.objects.filter(job_obj=job_id,price__isnull=False)
        
        scr=scrap.values('id','coin','price','price_change','market_cap','market_cap_rank',
        'volume',
        'volume_rank',
        'volume_change',
        'circulating_supply',
        'total_supply',
        'diluted_market_cap',
        'contracts',
        'official_links',
        'socials')

        scrap_list.append(scr[0])

        for i in scrap_list:

            cont=Contracts.objects.filter(scraping_details_id=i['id'])
            i['contracts']=cont.values('name','address')

            offi=Official_Links.objects.filter(scraping_details_id=i['id'])
            i['official_links']=offi.values('name','link')

            offi=Socials.objects.filter(scraping_details_id=i['id'])
            i['socials']=offi.values('name','link')
            
        scrap2=Scrapping_Details.objects.filter(job_obj=job_id,price__isnull=True)
        for j in scrap2:
            scrap_list.append({'coin':j.coin,'output':'-'})
             
             
        
        if not scrap:
            return Response({'status': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # results = []
        # for result in group_result.results:
        #     if result.state == 'PENDING':
        #         results.append({'state': 'PENDING', 'result': None})
        #     elif result.state == 'FAILURE':
        #         results.append({'state': 'FAILURE', 'result': str(result.info)})
        #     else:
        #         results.append({'state': 'SUCCESS', 'result': result.result})
        
        return Response({'job_id': job_id, 'tasks': scrap_list}, status=status.HTTP_200_OK)

        