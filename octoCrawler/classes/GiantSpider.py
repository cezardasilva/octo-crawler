
import os
import json
import pymongo
from PIL import Image
from pymongo import MongoClient
from octoCrawler.deathbycaptcha import SocketClient
from octoCrawler.bypass_api import BypassAPI


class GiantSpider():

	def decodeCaptcha(self, cnpj=None, driver=None, base=None, box=None):
		self.client = SocketClient("XXX", "XXX")
		self.box = box;
		captcha_name = self.takeScreenshot(cnpj, driver, base)
		captcha = self.client.decode(captcha_name, 15)
		if captcha:
			os.remove(captcha_name)
			self.catpcha_solved = captcha["text"]
		else:
			self.catpcha_solved = False
		return self.catpcha_solved

	def decodeCaptchaBypass(self, id=None, driver=None, base=None, box=None):
		self.box = box;
		self.client = BypassAPI()
		captcha_name = self.takeScreenshot(id, driver, base)
		captcha = self.client.bc_submit_captcha("XXXXXXXXXXXXXXXXXXXX", captcha_name)
		if captcha:
			os.remove(captcha_name)
			self.catpcha_solved = captcha['value']
		else:
			self.catpcha_solved = False
			self.client.bc_submit_feedback(ret, 0)
		return self.catpcha_solved


	def takeScreenshot(self, cnpj=None, driver=None, base=None):
		captcha_name = 'captcha' + str(cnpj) + '.png'
		screen_name = base + str(cnpj) + '.png'
		driver.get_screenshot_as_file(screen_name)
		im = Image.open(screen_name)
		croped = im.crop(self.box)
		croped.save(captcha_name)

		os.remove(screen_name)
		return captcha_name

	def saveItem(self, Item=None, name=None):
		self.client = MongoClient('localhost:27017')
		db = self.client.robot
		collection = db[name]
		inserted_id = collection.insert(dict(Item))
		return inserted_id

	def updateFile(self, cnpj=None):
		self.client = MongoClient()
		db = self.client.robot
		Fila = db["Fila"]
		Fila.update({'cnpj': cnpj}, {'$set':{'status': 'Processado'}})

	def extractNumber(self, string):
		num = ""
		tokens = string.split()
		for token in tokens:
		    for char in token:
		        if char.isdigit():
		            num = num + char
		return num