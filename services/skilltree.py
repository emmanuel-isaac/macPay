from macPay.settings.base import SKILLTREE_API_URL, X_AUTH_TOKEN

import requests
import json



class SkillTree():
	def __init__(self):
		self.url = SKILLTREE_API_URL
		self.headers = {'X-AUTH-TOKEN': X_AUTH_TOKEN }

	def get_data(self, params, **kwargs):
		url = self.url
		headers = self.headers

		response = requests.get(url, params=params, headers=headers)
		return response.json()

