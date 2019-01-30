from watson_developer_cloud import VisualRecognitionV3, WatsonApiException
import os
import json
from nameko.rpc import rpc

class DetectObject(object):
	name = "detect"
	@rpc
	def compute(self,image_url,api_key):
		service = VisualRecognitionV3(
		    '2018-03-19',
		    url='https://gateway.watsonplatform.net/visual-recognition/api',
		    iam_apikey=api_key)
		try:
		    with open(image_url, 'rb') as images_file:
		        car_results = service.classify(
		            images_file=images_file,
		            threshold='0.1',
		            classifier_ids=['default']).get_result()
		        print(json.dumps(car_results, indent=2))
		except WatsonApiException as ex:
		    print(ex)



		classifiers = service.list_classifiers().get_result()
		return classifiers