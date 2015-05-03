from macPay.settings.base import SKILLTREE_API_URL

import requests
import json



class SkillTree():
	def __init__(self):
		self.url = SKILLTREE_API_URL

	def get_data(self, params, **kwargs):
		url = self.url

		response = requests.get(url, params=params)
		return response.json()

