import logging
import httplib2

class CnbTextFile:
  '''
  Download and parse rates from cnb.cz (Czech National Bank) text file directly.
  http://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt
  '''

  api_url         = 'http://www.cnb.cz'
  latest_endpoint = '/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.txt'

  def get_latest_usd_to_czk_rate(self):
    '''
    Connects to the API server and fetches
    latest USD to CZK exchange rate.
    '''
    data     = self.get_data(self.latest_url())
    czk_rate = data['rate']
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
    Fetches a response from the server
    and returns a parsed JSON result.
    '''
    data = self.parse_response(
      self.fetch_data(url)
    )
    return data

  def fetch_data(self, url):
    '''
    Fetches a response from the server.
    '''
    logging.info('Fetching data from {0}'.format(url))
    h = httplib2.Http('.cache')
    resp, content = h.request(url, 'GET')
    return content

  def parse_response(self, response):
    '''
    Parses the text response and returns a dict.
    '''
    logging.info('Parsing response')
    lines = response.decode('utf-8').split('\n')

    for line in lines:
      items = line.split('|')

      try:
        code = items[3]
        rate = items[4]

        if code != 'USD':
          continue

        rate = float( rate.replace(',', '.') )

        return {
          'code': code,
          'rate': rate,
        }
      except IndexError:
        continue

  def get_url(self, endpoint):
    '''
    Assembles an URL for the server.
    '''
    url = '{api_url}{endpoint}'.format(
      api_url  = self.api_url,
      endpoint = endpoint
    )
    return url
