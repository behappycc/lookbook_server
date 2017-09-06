import json
import requests
from base64 import b64encode

url = "https://api.imgur.com/3/image"
headers = {
	'authorization': "Client-ID 480a349edc32891",
}

def imgurRequests(image_chunk):
	try:
		response = requests.request("POST", url, headers=headers, data={'image': b64encode(image_chunk)})
		json_response = json.loads(response.text)
		result = json_response['data']['link']
	except Exception, e:
		result = ''
	return result