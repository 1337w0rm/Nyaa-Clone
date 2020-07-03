from lxml import html
import requests

def magnet(url):
	#url = "https://nyaa.si/view/1252638"
	response = requests.get(url)
	link = html.fromstring(response.content).xpath('/html/body/div/div[1]/div[3]/a[2]/@href')[0]
	return link