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

            age = request.data['age']
            gender = request.data['gender']
            country = request.data['country']
            city = request.data['city']


            file_obj = request.data['image']
            file_obj_copy = copy.deepcopy(file_obj)

            # Imgur upload
            image_chunk = file_obj.read()
            url = imgurRequests(image_chunk)
            print '~~~~~!!!!!~~~~~~~~~~~~~~~'

            # vgg model
            img = Image.open(file_obj_copy)
            process = preprocess(img)
            # result_predict = vgg19(process)
            raw_city_rank = rank(result_predict)
            city_rank = [{ 'name': city_name, 'prob': prob } for city_name, prob in raw_city_rank]

            response = OrderedDict([
                ['age', age],
                ['gender', gender],
                ['country', country],
                ['city', city],
                ['imgUrl', url],
            	['rank', city_rank],
            ])

            url = "https://api.airtable.com/v0/appLqa1uJ8iUbOdKY/FWM_Data"

            headers = {
                'authorization': "Bearer {}".format(os.environ['APIKEY']),
                'content-type': "application/json",
            }

            r = requests.request("POST", url, data=json.dumps(response), headers=headers)
            print r.text
            print '~~~~~!!!!!~~~~'

            return Response(response, status=200)
        except Exception, e:
            print e
            return Response({'message': 'Error occurs'}, status=500)
            


