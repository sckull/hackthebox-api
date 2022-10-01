'''HackTheBox Machines module.'''
from .exceptions import HackTheBoxException
from .api import HackTheBox
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re, base64, requests, sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Utils(HackTheBox):
	'''test'''
	def __init__(self):
		'''Initialize HackTheBox'''
		HackTheBox.__init__(self)

	def get_user(self, user_id: int) -> dict:
		return self.request(endpoint='/api/profile/user/{:d}/'.format(user_id)).json()
	
	def check_url(self, url):
		''' Check status of IMG URL and changes according of the status.'''
		status = lambda url: True if requests.get(url, timeout=5).status_code == 200 else False
		if status(url):			
			# print(bcolors.OKGREEN+">>>>> " + url +" <<<<<<<<<< MAIN"+bcolors.END)
			return url
		else:			
			url = url + '?v=1'
			# print(bcolors.BOLD+">>>>> " + url + " <<<<<<<<<< if not MAIN"+bcolors.END)
			return url	

	def get_img_machine(self, url):
		buffered = BytesIO()
		url = self.check_url(url)
		try:
			req = Image.open(requests.get(url, timeout=5, stream=True).raw)
		except:
		    print(bcolors.WARNING+"error:", sys.exc_info()[0], bcolors.END)
		    print(bcolors.FAIL+bcolors.BOLD+ str(url)+bcolors.END)
		    return False
		    raise
		icon_sizes = [(24, 24),(64,64)]
		new_image = req.resize(icon_sizes[0])
		new_image.save(buffered, format="ICO",quality=100)
		new_image = base64.b64encode(buffered.getvalue())
		base = "![box_img_maker](data:image/png;base64,{0})".format(new_image.decode('utf-8'))
		#print(bcolors.WARNING+str(new_image)+bcolors.END)
		return base

		