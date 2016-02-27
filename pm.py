#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv,smtplib
from email.mime.text import MIMEText
from email.header import Header
from sys import argv
import logging
 

#LogMode=logging.DEBUG
#LogMode=logging.INFO
#LogMode=logging.WARN

try:
   argv[2]
except IndexError:
   LogMode=logging.INFO
else:
   if argv[2] == "-d":
      LogMode=logging.DEBUG


logging.basicConfig(filename="log.txt",filemode='a',
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%d.%m.%Y %H:%M:%S', level=LogMode)
 
logging.debug("running in debug mode")

logging.info("Mailing script started")

try:
    argv[1]
except IndexError:
    Datei = 'mail.txt'
else:
    Datei = argv[1]

print "Lese aus Datei: %s " % Datei

fo = open(Datei, "r+")
str = fo.read();
fo.close()




with open('liste-lug.csv') as csvfile:
   reader = csv.DictReader(csvfile)
   for row in reader:
       m_name = row['name']
       m_email = row['email']

       logging.debug(" %s - %s " % (m_name, m_email))
 
       SUBJECT = "[lug-bremerhaven] heute Python Treffen" 

       try:
          TXT = str % m_name
       except TypeError:
          TXT = str 

       # Send the mail

       FROM = 'info@lug-bremerhaven.de'
       TO = m_email

       mime = MIMEText(TXT, 'plain', 'utf-8')
       mime ['FROM'] = 'info@lug-bremerhaven.de' 
       mime ['To'] = m_email
       mime ['Subject'] = Header(SUBJECT, 'utf-8')


       server = smtplib.SMTP('localhost')
       server.sendmail(FROM, TO, mime.as_string())
       server.quit()


exit()

