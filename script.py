#!/usr/bin/env python3


import requests
import time
import os

USERNAME=''
PASSWORD=''

LOGIN_URL='https://www.eprimo.de/service/account/auth/login'
INVOICES_LIST_URL='https://www.eprimo.de/service/contract/inbox'
PDF_BASE_URL='https://www.eprimo.de'
SESSION = requests.Session()


def get_csrf():
	res = SESSION.get(LOGIN_URL)
	return res.text.split('logincsrf" value="')[1].split('"')[0];


def do_login(username='',password=''):
	# start url
	csrf_token = get_csrf()
	# do login request
	login_data = {'logincsrf': csrf_token, 'login': 'Login', 'email': username, 'password': password}
	login_req = SESSION.post(LOGIN_URL, data=login_data)
	
	#print("Title is %s", title)

def de_date_to_iso(de_date):
	components = de_date.split('.')
	return components[2] + '-' + components[1] + '-' + components[0]

def get_invoice_list():
	res = SESSION.get(INVOICES_LIST_URL)

	page = res.text

	invoice_area = page.split('<div id="inbox-area">')[1].split('</form>')[0];
	invoice_table = invoice_area.split('<table class="dataTable')[1]
	invoice_tbody = invoice_table.split('<tbody>')[1].split('</tbody>')[0];
	
	invoice_trs = invoice_tbody.split('<tr');
	print("got " + str(len(invoice_trs)) + " rows")
	for i in range(1, len(invoice_trs) - 1):
		tds = invoice_trs[i].split('<td')
		de_date = (tds[2].split('</td>')[0].split('>')[1]).strip()
		date = de_date_to_iso(de_date)
		print(date)
		subject = tds[3].split('</td>')[0].split('>')[2].split('<')[0]
		pdf_link = tds[4].split('<td>')[0].split('>')[1].split('href="')[1].split('"')[0]
		print(subject)
		print(pdf_link)
		filename = date + ' ' + subject + '.pdf'
		if (os.path.isfile(filename)) == False:
			res = SESSION.get(PDF_BASE_URL + pdf_link)
			open(filename, 'wb').write(res.content)



def init():
	global USERNAME
	global PASSWORD
	config = open('./login.txt', 'r')
	USERNAME = config.readline().strip()
	PASSWORD = config.readline().strip()

init()
print('user: ' + USERNAME)
print('password: ' + PASSWORD)
do_login(USERNAME, PASSWORD)
get_invoice_list()
