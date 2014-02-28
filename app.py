import logging
import config

from api      import Api
from notifier import Notifier

def main():
  logging.basicConfig(
    filename = 'info.log',
    level    = logging.DEBUG,
    format   = '%(asctime)s - %(levelname)s - %(message)s'
  )

  logging.info('Start')

  client     = Api(config.app_id)
  latest_czk = client.get_latest_usd_to_czk_rate()
  # latest_czk = 19.82228 # Debug

  notifier = Notifier(config.email_settings)
  notifier.send(latest_czk)

  logging.info('Finish')

if __name__ == '__main__':
  main()
