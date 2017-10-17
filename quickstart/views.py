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
            missing_fields = []
            for field, regex in fields.items():
                try:
                    data = request.data[field]
                    reg = re.match(regex, data)
                    if (reg is None):
                        missing_fields.append(field)
                except Exception, e:
                    print e
                    missing_fields.append(field)
            
            if missing_fields != []:
                print 'missing_fields:'
                print missing_fields
                message = ', '.join(missing_fields)
                return Response({'message': 'Missing fields: ' + message}, status=400)

            age = request.data['age'].encode("utf-8")
            gender = request.data['gender'].encode("utf-8")
            country = request.data['country'].encode("utf-8")
            city = request.data['city'].encode("utf-8")

            file_obj = request.data['image']
            file_obj_copy = copy.deepcopy(file_obj)

            # Imgur upload
            # image_chunk = file_obj.read()
            # url = imgurRequests(image_chunk)

            # vgg model
            # img = Image.open(file_obj_copy)
            # process = preprocess(img)
            # result_predict = vgg19(process)
            # raw_city_rank = rank(result_predict)
            # city_rank = [{ 'name': city_name, 'prob': prob } for city_name, prob in raw_city_rank]

            # response = OrderedDict([
            #     ['age', age],
            #     ['gender', gender],
            #     ['country', country],
            #     ['city', city],
            #     ['imgUrl', url],
            # 	['rank', city_rank],
            # ])

            url = 'http://test/url'

            city_rank = [{'name': 'taiwan', 'prob': 50}, {'name': 'china', 'prob': 50}]
            city_rank_to_db = 'taiwan,50;china,50;'

            response = OrderedDict([
                ['age', age],
                ['gender', gender],
                ['country', country],
                ['city', city],
                ['imgUrl', url],
                ['rank', city_rank],
            ])

            User.objects.create(
                age=age,
                gender=gender,
                country=country,
                city=city,
                imgUrl=url,
                rank=city_rank_to_db
            )

            print(response)

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

        print(content)

        return Response(content)

