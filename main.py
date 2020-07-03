import datetime
from telegram.ext import Updater
import logging
from config import Config
import xml.etree.ElementTree as ET
import wget, os, re, time
import magnet as m

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

global title
title = list()

regex="(?<=\[)(HorribleSubs?)|(Hanasaku?)|(DmonHiro?)(?=\])"


def start(context):
	wget.download('https://nyaa.si/?page=rss',  'nyaa.xml')
	tree = ET.parse('nyaa.xml')
	os.remove('nyaa.xml')
	i = 0
	for link,tit in zip(tree.findall('.//guid'),tree.findall('.//title')):
		enc = re.search(regex, tit.text)
		if enc:
			if tit.text in title:
				i += 1
				continue
			else:
				title.append(tit.text)
				mag = m.magnet(link.text)
				text = "/mirror " + mag
				i += 1
				print(tit.text)
				if i > 100:
					break
				context.bot.sendMessage(Config.CHANNEL_ID, text)
				time.sleep(900)
		else:
			continue

def main():
    updater = Updater(Config.BOT_TOKEN, use_context=True)
    logging.info("Bot started")
    j = updater.job_queue
    j.run_repeating(start, 60, 0)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()