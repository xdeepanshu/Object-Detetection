from watson_developer_cloud import VisualRecognitionV3, WatsonApiException
import os
import json
from nameko.rpc import rpc

api_key = "0tuAZ32qBLrn-RSsorNDwunBdafAyXjuUOIu6qqfyDU-"

class DetectObject(object):
	name = "detect"
	results = None
	@rpc
	def compute(self,image_url,api_key=api_key):
		service = VisualRecognitionV3(
		    '2018-03-19',
		    url='https://gateway.watsonplatform.net/visual-recognition/api',
		    iam_apikey=api_key)
		try:
		    results = service.classify(
		        url=image_url,
		        threshold='0.2',
		        classifier_ids=['default']).get_result()
		    print(json.dumps(results, indent=2))
		except WatsonApiException as ex:
		    print(ex)
		    results = None
		return results