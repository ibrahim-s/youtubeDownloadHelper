# -*- coding: utf-8 -*-
# geturl.py

import requests
import os, sys
import time
import threading 
from logHandler import log

currentPath= os.path.abspath(os.path.dirname(__file__))
sys.path.append(currentPath)
from user_agent import generate_user_agent
del sys.path[-1]
userAgent= generate_user_agent()
headers = {'User-Agent': userAgent}

class GetUrl(threading.Thread):
	def __init__(self, youtubeUrl):
	# youtubeUrl, after being processed and added to it 'ss'.
		threading.Thread.__init__(self)
		self.daemon=True
		self.youtubeUrl= youtubeUrl
		self.response= None

	def run(self):
		response = requests.get(self.youtubeUrl, headers=headers)
		time.sleep(5)
		#log.info(f'response: {response}')
		self.response= response
		response.close()
