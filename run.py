import csv

from services.downloader import Downloader
from services.writer import Writer
from decidim.result import Result

with open('instances.csv') as instances_file:
    reader = csv.DictReader(instances_file)
    instances = list(reader)

queries = ['decidim', 'organization', 'metrics']

query_string = ''

for query in queries:
    with open('queries/{}.graphql'.format(query)) as graphql_file:
        graphql_query = graphql_file.read()

    query_string += graphql_query

organizations = []
for instance in instances:
    print('Getting data from {}'.format(instance['url']))
    result_json = Downloader.get_graphql(instance['url'], query_string)

    if not result_json:
        continue

    result = Result(result_json)

    organization = {
        'url': instance['url'],
        'app_name': result.application_name(),
        'name': result.name(),
        'version': result.version(),
        'users': result.get_metric('users'),
        'participatory_processes':
        result.get_metric('participatory_processes'),
        'assemblies': result.get_metric('assemblies'),
        'comments': result.get_metric('comments'),
        'meetings': result.get_metric('meetings'),
        'proposals': result.get_metric('proposals'),
        'accepted_proposals': result.get_metric('accepted_proposals'),
        'votes': result.get_metric('votes'),
        'endorsements': result.get_metric('endorsements'),
        'survey_answers': result.get_metric('survey_answers'),
        'results': result.get_metric('results'),
        'debates': result.get_metric('debates'),
    }
    organizations.append(organization)

Writer.write_csv(organizations, 'organizations.csv')
