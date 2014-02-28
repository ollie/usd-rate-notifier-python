import logging

from smtplib         import SMTP
from email.mime.text import MIMEText
from datetime        import date

class Notifier:
  '''
  Send an e-mail with ease. :-)
  '''

  def __init__(self, settings):
    '''
    Some e-mail settings:

    settings = {
      'host':     'smtp.gmail.com',
      'port':     587,
      'username': 'your.username@example.org',
      'password': 'your password',
      'from':     'your.email@example.org',
      'to':       'your.email@example.org',
    }
    '''
    self.settings = settings

  def send(self, usd_to_czk_rate):
    '''
    Take the exchange rate, compose a message
    and send that.
    '''
    message = self.compose_message(usd_to_czk_rate)
    self.send_message(message)

  def compose_message(self, usd_to_czk_rate):
    '''
    Creates a simple e-mail message with exchange
    rate in the subject.
    '''
    subject = 'USD rate ({0})'.format( date.today().strftime('%b %-d, %Y') )
    text    = '1 USD costs {0:.3f} CZK.'.format( usd_to_czk_rate )

    message            = MIMEText(text)
    message['Subject'] = subject
    message['From']    = self.settings['from']
    message['To']      = self.settings['to']
    return message

  def send_message(self, message):
    '''
    Sends the actual message.
    '''
    logging.info('Sending message')
    with SMTP() as smtp:
      smtp.connect(self.settings['host'], self.settings['port'])
      smtp.ehlo()
      smtp.starttls()
      smtp.login(self.settings['username'], self.settings['password'])
      smtp.send_message(message)
