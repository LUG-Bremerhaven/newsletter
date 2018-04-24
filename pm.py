#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import csv,smtplib
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from email.header import Header
from sys import argv
import logging, netrc, csv, sys
 

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

#some standards:
FROM = 'info@lug-bremerhaven.de'
SUBJECT = "[lug-bremerhaven] Veranstaltungsinfo"

# Define which host in the .netrc file to use
HOST = 'lug-mailserver'


# Read from the .netrc file in your home directory
try:
  secrets = netrc.netrc()
  login, account, password = secrets.authenticators( HOST )
except IOError as err:
  print("Error opening .netrc file")
  logging.error("Error opening .netrc file")
  logging.debug(err)
  exit()
except netrc.NetrcParseError as err:
  print("Error while parsing .netrc file")
  logging.error("Error while parsing .netrc file")
  logging.debug(err)
  exit()

logging.debug('User: %s' % login)
logging.debug('Server: %s' % account)
logging.debug('Password: %s' % password)


SMTPserver = account
#USERNAME = login
#PASSWORD = password 

# define the content of the mail. get it from mail.txt or, if defined, use the commandline given file
# eg: /opt/mailer/pm.py /opt/mailer/usertreffen.txt

try:
    argv[1]
except IndexError:
    Datei = 'mail.txt'
else:
    Datei = argv[1]

print "Lese aus Datei: %s " % Datei

try:
    fo = open(Datei, "r+")
except IOError:
    print("Die Datei '%s' kann nicht geoeffnet werden!" % Datei)
    exit(1)
CONTENT = fo.read();
fo.close()




with open('liste-lug.csv') as csvfile:
   reader = csv.DictReader(csvfile)
   for row in reader:
       m_name = row['name']
       m_email = row['email']

       logging.debug(" %s - %s " % (m_name, m_email))
 
       try:
          TXT = CONTENT % m_name
       except TypeError:
          TXT = CONTENT 

       # Send the mail

       TO = m_email

       mime = MIMEText(TXT, 'plain', 'utf-8')
       mime ['FROM'] = 'info@lug-bremerhaven.de' 
       mime ['To'] = m_email
       mime ['Subject'] = Header(SUBJECT, 'utf-8')


       #server = smtplib.SMTP(SMTPserver)
       try:
              conn = SMTP(SMTPserver)
              conn.set_debuglevel(False)
              conn.login(login, password)
              try:
                 conn.sendmail(FROM, TO, mime.as_string())
              finally:
                 conn.quit()

       except Exception, exc:
              sys.exit( "mail failed; %s" % str(exc) ) # give a error message
              #sys.exit( "mail failed; " ) # give a error message

       #server.sendmail(FROM, TO, mime.as_string())
       #server.quit()


exit()

