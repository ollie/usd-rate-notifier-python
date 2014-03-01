import logging
import httplib2
import json

class Api:
  '''
  Open Exchange Rates API.
  You will need an App ID for access.
  '''

  api_url         = 'http://openexchangerates.org'
  latest_endpoint = '/api/latest.json'

  def __init__(self, app_id):
    '''
    Don't forget to pass the app_id.
    '''
    self.app_id = app_id

  def get_latest_usd_to_czk_rate(self):
    '''
    Connects to the API server and fetches
    latest USD to CZK exchange rate.
    '''
    data = self.get_data(self.latest_url())
    czk_rate = data['rates']['CZK']
    return czk_rate

  def latest_url(self):
    '''
    Assembles an URL for the list
    of the latest exchange rates.
    '''
    url = self.get_url(self.latest_endpoint)
    return url

  def get_data(self, url):
    '''
    Fetches a response from the API server
    and returns a parsed JSON result.
    '''
    data = self.parse_response(
      self.fetch_data(url)
    )
    return data

  def fetch_data(self, url):
    '''
    Fetches a response from the API server.
    '''
    logging.info('Fetching data from {0}'.format(url))
    h = httplib2.Http('.cache')
    resp, content = h.request(url, 'GET')
    return content

  def parse_response(self, response):
    '''
    Parses the JSON response and returns a dict.
    '''
    logging.info('Parsing response')
    data = json.loads(response.decode('utf-8'))
    return data

  def get_url(self, endpoint):
    '''
    Assembles an URL for the API server.
    '''
    url = '{api_url}{endpoint}?app_id={app_id}'.format(
      api_url  = self.api_url,
      endpoint = endpoint,
      app_id   = self.app_id
    )
    return url
