from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


class Downloader(object):
    @staticmethod
    def get_graphql(url, query):
        transport = AIOHTTPTransport(url=url + '/api')
        client = Client(transport=transport)

        try:
            return client.execute(gql('{' + query + '}'))
        except Exception as err:
            exception_type = type(err).__name__
            print('Could not fetch data due to a {}'.format(exception_type))
