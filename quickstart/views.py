import re
import os
import cgi
import json
import copy
from collections import OrderedDict
from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
from quickstart.preprocess import preprocess
from PIL import Image
from quickstart.model_vgg19 import vgg19
from quickstart.rank import rank
import numpy as np
from quickstart.imgur import imgurRequests
import cStringIO
import requests
from models import User

from rest_framework import generics

# regelar expression
# r'^.+@.+\..+$'
fields = {
    'age': r'\d+', 
    'gender': r'(male|female)', 
    'country': r'.',
    'city': r'.+'
}


class FileUploadView(views.APIView):
    def post(self, request, format=None):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            age = body['age']
            gender = body['gender']
            country = body['country']
            city = body['city']

            file_obj = body['imgUrl'].encode('utf-8q')
            print(file_obj)

            # Imgur upload
            image_chunk = file_obj.read()
            print(image_chunk)

            # TODO: url and rank should be replaced with the Imgur url and vgg model prediction
            url = 'https://i.imgur.com/Sc59JV1.jpg'

            # rank should be transform to this structure
            city_rank_to_db = 'Rio De Janeiro,44.8;Prague,24.1;Helsinki,8.4;Casablanca,4.7;Berlin,3.0;others,15.0'

            user = User.objects.create(
                age=age,
                gender=gender,
                country=country,
                city=city,
                imgUrl=url,
                rank=city_rank_to_db
            )

            response = {
                'user': user.id,
            }

            return Response(response, status=200)
        except Exception, e:
            print e
            return Response({'message': 'Error occurs'}, status=500)


class GetUserView(generics.RetrieveAPIView):
    """
    Get User info by id
    """
    def get(self, request, id, format=None):
        user = User.objects.get(id=id)
        city_rank = user.rank.split(';')

        obj = []
        for city in city_rank:
            if city:
                obj.append({'name': city.split(',')[0], 'prob': city.split(',')[1]})

        content = {
            'id': str(user.id),
            'age': user.age,
            'gender': user.gender,
            'country': user.country,
            'city': user.city,
            'imgUrl': user.imgUrl,
            'rank': obj,
        }

        return Response(content, status=200)

