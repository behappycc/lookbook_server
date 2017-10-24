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
    def post(self, request, filename, format=None):
        try:
            file_obj = request.data['image']
            file_obj_copy = copy.deepcopy(file_obj)

            image_chunk = file_obj.read()
            url = imgurRequests(image_chunk)

            # vgg model
            img = Image.open(file_obj_copy)
            process = preprocess(img)
            result_predict = vgg19(process)
            raw_city_rank = rank(result_predict)
            city_rank = [{ 'name': city_name, 'prob': prob } for city_name, prob in raw_city_rank]

            # TODO: rank should be replaced with vgg model prediction
            # rank should be transform to this structure
            # city_rank_to_db = 'Rio De Janeiro,44.8;Prague,24.1;Helsinki,8.4;Casablanca,4.7;Berlin,3.0;others,15.0'


            city_rank_to_db = '{},{};{},{};{},{};{},{};{},{};{},{};'.format(
                city_rank['city'][0],city_rank['prob'][0],
                city_rank['city'][1],city_rank['prob'][1],
                city_rank['city'][2],city_rank['prob'][2],
                city_rank['city'][3],city_rank['prob'][3],
                city_rank['city'][4],city_rank['prob'][4],
                city_rank['city'][5],city_rank['prob'][5],
                city_rank['city'][6],city_rank['prob'][6])


            user = User.objects.create(
                age=request.data['age'],
                gender=request.data['gender'],
                country=request.data['country'],
                city=request.data['city'],
                imgUrl=url,
                rank=city_rank_to_db
            )

            response = {
                'user': user.id,
            }

            print(url)

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


