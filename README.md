# icann_mail_archive
Scraping the ICANN email archives. 


#Running

- Go to icann.py
- Edit the value of variable name to point the name of the list you want to scrape
- For example to scrape http://forum.icann.org/lists/gnso-irtpd/ make name='gnso-irtpd'
- Install dependencies by pip install -r requirements.txt
- Run scraper by python icann.py
- The data will be in the database icann.sqlite inside the table with the name same as email list name



