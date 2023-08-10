from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
import requests, tweepy

from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer
import requests
import os

# Create your views here.
# to make any api restfull:
# to get user: we will send GET request to this endpoint /advocates
# to add user: we will send GET request to this endpoint /advocates
# to get single user: we will send GET request to this endpoint /advocates/:id
# to update user: we will send PUT request to this endpoint /advocates/:id
# to delete the user: we will send DELETE request to /advocates/:id
# we need to go more into it to make it restfull api but this is the overall idea
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
@api_view(['GET'])
def endpoints(request):
    print('TWITTER_API_KEY:', TWITTER_API_KEY)
    data = ['/advocates', 'advocates/:username']
    return Response(data) # safe=false means we can not pass python dicstionaries


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def advocates_list(request):
    #Handles GET requests:
    if request.method == 'GET':
        #advocates/?query=Max
        query = request.GET.get('query')

        if query == None:
            query = ''
        advocates = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query)) # icontains is for some values to match although all the values are not there majority is there
        # if we are passing advocates directly into Response(advocates) then it will give error
        # of not JSON serializable object type
        # so to avoid this we need to convert this data into serilized data
        # when we get this kind of data we need to serialize it, it is also called pickling and it modifies the
        # data into Json response
        serializer = AdvocateSerializer(advocates, many = True) # many=True means we are serializing more than 1 objects.
        return Response(serializer.data)
    # api vs rest api:
    # api is not same as restful apis
    # rest api is the way we built the api, how we define the structure of the api.
    # for example I want to built the api for adding advocate in the resful way:
    #Handles POST requests
    if request.method == 'POST':
        advocate = Advocate.objects.create(
            username=request.data['username'],
            bio=request.data['bio']
            )
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

def get_data(url):
    headers = {'Authorization': "Bearer " + str(TWITTER_BEARER_TOKEN)}
    # url = "https://api.twitter.com/2/users/by/username/:username/"
    payload = {}
    # headers = {}
    response = requests.request("GET", url, headers=headers, data=payload).json()
    return response

class AdvocateDetail(APIView):
    def get_object(self, username):
        try:
            return Advocate.objects.get(username=username)
        except Advocate.DoesNotExist:
            raise JsonResponse("Advocate Doesn't Exist")

    def get(self, request, username):
        fields = '?user.fields=profile_img_url,description,public_metrics'
        url = 'https://api.twitter.com/2/users/by/username/' + str(username) + fields
        data = get_data(url=url)
        data['profile_image_url'] = data['profile_image_url'].replace('normal', "400x400")
        print('DATA FROM TWITTER:', data)
        advocate = self.get_object(username)
        advocate.name = data['name']
        advocate.profile_pic = data['profile_image_url']
        advocate.bio = data['description']
        advocate.twitter = 'hhtps://twitter.com/' + username
        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    def put(self, request, username):
        advocate = self.get_object(username)
        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    def delete(self, request, username):
        advocate = self.get_object(username)
        advocate.delete()
        return Response('The user was deleted')


# @api_view(['GET','PUT','DELETE'])
# def advocates_details(request, username):
#     advocate = Advocate.objects.get(username=username)
#     if request.method == 'GET':
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         advocate.username = request.data['username']
#         advocate.bio = request.data['bio']
#         advocate.save()
#         serializer = AdvocateSerializer(advocate, many=False)
#         return Response(serializer.data)
#
#     if request.method == 'DELETE':
#         advocate.delete()
#         return Response('The user was deleted')


@api_view(['POST', 'GET'])
def companies_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)

