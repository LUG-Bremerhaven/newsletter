#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import csv,smtplib
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from email.header import Header
from sys import argv
import os
import logging
import netrc
import csv
import sys
import argparse
 

#LogMode=logging.DEBUG
#LogMode=logging.INFO
#LogMode=logging.WARN

# this function parses the cmdline arguments
def parse_cmdline():
    usage = '%s [OPTIONS] FILE\n' % (sys.argv[0])
    parser = argparse.ArgumentParser(usage)
    parser.add_argument(
        '--log-file', type=str,
        dest='logfile', metavar='FILE', default="log.txt",
        help='Filename of the logfile')
    parser.add_argument(
        '--log-level', type=str,
        dest='loglevel', metavar='level', default="INFO",
        help='Available loglevel: INFO, DEBUG')
    parser.add_argument(
        '--subject', type=str,
        dest='subject', metavar='mailheader', default="[lug-bremerhaven] Veranstaltungsinfo",
        help='Subject of the mail')
    parser.add_argument(
        '--from', type=str,
        dest='fromOrigin', metavar='mailheader', default="info@lug-bremerhaven.de",
        help='originator/from')
    parser.add_argument(
        '--list', type=str,
        dest='list', metavar='csvfile', default="liste-lug.csv",
        help='List of all member email addresses as csv')
    parser.add_argument('FILE', default='mail.txt')
    args = parser.parse_args()
    return args

arguments = parse_cmdline()

logging.basicConfig(filename=arguments.logfile,filemode='a',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d.%m.%Y %H:%M:%S', level=arguments.loglevel)
logging.info("Mailing script started")
 
logging.debug("running in debug mode")

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

logging.debug("Lese aus Datei: %s " % arguments.FILE)

try:
    fo = open(arguments.FILE, "r+")
except IOError:
    print("Die Datei '%s' kann nicht geoeffnet werden!" % arguments.FILE)
    logging.info("Couldn't open '%s'" % arguments.FILE)
    exit(1)
CONTENT = fo.read();
fo.close()


if not os.path.isfile(arguments.list):
  print("Die Datei '%s' kann nicht gefunden werden!" % arguments.list)
  logging.info("Couldn't find '%s'" % arguments.list)
  exit(1)
with open(arguments.list) as csvfile:
   logging.debug("The mail subject & originator:'%s' & '%s'" %(arguments.subject, arguments.fromOrigin))
   reader = csv.DictReader(csvfile)
   mailcounter = 0 # count the mails to send 
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
       mime ['FROM'] = arguments.fromOrigin
       mime ['To'] = m_email
       mime ['Subject'] = Header(arguments.subject, 'utf-8')


       #server = smtplib.SMTP(SMTPserver)
       try:
              conn = SMTP(SMTPserver)
              conn.set_debuglevel(False)
              conn.login(login, password)
              try:
                 conn.sendmail(arguments.fromOrigin, TO, mime.as_string())
                 mailcounter += 1
              finally:
                 conn.quit()

       except Exception, exc:
              sys.exit( "mail failed; %s" % str(exc) ) # give a error message
              #sys.exit( "mail failed; " ) # give a error message

       #server.sendmail(FROM, TO, mime.as_string())
       #server.quit()

logging.info("Send '%i' mails" % mailcounter)
exit()

