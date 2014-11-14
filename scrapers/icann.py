import scrapekit
import dataset
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin
import lxml 
from datetime import datetime
import time

config = {
  'threads': 1,
  'cache_policy': 'force',
  'data_path': 'data'
}


#name = 'gnso-policyimpl-wg'
#name = 'gnso-policyimpl-dt'
#name ="gnso-ccwg-dt"
#name="gnso-irtpc"
name="gnso-irtpd"
base_url = 'http://forum.icann.org/lists/'+name+"/"
scraper = scrapekit.Scraper('get_emails_'+name, config=config)


@scraper.task
def scrape_index(page_no, url):
	db = dataset.connect('sqlite:///./../database/icann.sqlite')
	db_emails_table = db[name]
	print url
	print str(page_no)

	resp = scraper.get(url)
	if resp.status_code == 200:
		content = resp.html()
		soup = BeautifulSoup(lxml.html.tostring(content))

		msg_lisy_lis = soup.findAll('li')
		for msg_li in msg_lisy_lis:
			msg_a = msg_li.find('a')
			if msg_a.has_key('name'):
				msg_url =  base_url+msg_a['href']
				if db_emails_table.find_one(url=msg_url) is not None:
					print "Exists"
					continue

				email_content = scraper.get(msg_url).html()
				soup2 = BeautifulSoup(lxml.html.tostring(email_content))
				msg_header_lis = soup2.findAll('li')
				email_subject = str(msg_header_lis[1].getText()).replace("Subject:","")
				
				email_from = (str(msg_header_lis[2].getText()).replace("From:","")) .split('&lt;')
				if(len(email_from) > 1):
					email_from_id = str(email_from[1]).replace("&gt;","")
					email_from_name = str(email_from[0]).strip()
				else:
					email_from_id =email_from[0]
					email_from_name =email_from[0]

				email_date = str(msg_header_lis[3].getText()).replace("Date:","").strip()

				email_body = soup2.find('table').getText()

				print email_date
				print email_from_id
				print email_from_name				
				print email_subject
				#print email_body
				msg_details = {"sender":email_from_name, "email":email_from_id ,"subject":email_subject ,"pubdate":email_date ,"url":msg_url ,"body":email_body }
				db_emails_table.insert(msg_details)

		db.commit() 
		#for the next page
		page_no = page_no+1
		next_link = base_url+"mail"+str(page_no)+".html"
		scrape_index.queue(page_no, next_link)

scrape_index.run(1, base_url)
