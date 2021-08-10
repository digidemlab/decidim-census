import csv

from services.downloader import Downloader
from services.writer import Writer
from services.reader import Reader
from services.dater import Dater
from decidim.query import Query
from decidim.result import Result

instances = Reader.read_csv('instances.csv')

query_string = Query.create_query()

organizations = []
for instance in instances:
    print('Getting data from {}'.format(instance['url']))
    result_json = Downloader.get_graphql(instance['url'], query_string)

    if not result_json:
        continue

    organizations.append(Result(result_json, instance).convert_to_JSON())

TOTAL = Result.calculate_totals(organizations)

organizations.append(TOTAL)

Writer.write_csv(organizations, 'organizations.csv')

for organization in organizations:
    print('Updating history for {}'.format(organization['url']))
    Writer.write_historical(organization, str(Dater.yesterday()))

    print('Getting logo_url and colour from {}'.format(organization['url']))
    organization = Result.add_logo_and_colour(organization)

Writer.write_csv(organizations, '_data/organizations.csv')
