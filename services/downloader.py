import time
import urllib.request

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class Downloader(object):
    @staticmethod
    def get(url):
        try:
            return urllib.request.urlopen(url).read()
        except urllib.error.URLError as err:
            print(err)
            print(f'ERROR: The certificate is invalid for {url}.')
            return None
        except urllib.error.HTTPError as err:
            print(f'ERROR {err.code}: Could not download {url}.')
            if (err.code == 403):
                print('Retrying in 1 second')
                time.sleep(1)
                return Downloader.get(url)
            else:
                print('Permanent error: skipping this platform')
                return None

    @staticmethod
    def get_graphql(url, query, retry=0):
        transport = AIOHTTPTransport(url=url + '/api')
        client = Client(transport=transport, execute_timeout=30)

        try:
            return client.execute(gql('{' + query + '}'))
        except Exception as err:
            exception_type = type(err).__name__
            if (exception_type == 'TimeoutError' and retry < 2):
                print('Timeout error. Retrying in 1 second')
                time.sleep(1)
                return Downloader.get_graphql(url, query, retry + 1)
            else:
                print(
                    'Could not fetch data due to a {}'.format(exception_type))
                return None
