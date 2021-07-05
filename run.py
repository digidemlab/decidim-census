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
        'users_count': result.get_stat('users_count'),
        'processes_count': result.get_stat('processes_count'),
        'assemblies_count': result.get_stat('assemblies_count'),
        'comments_count': result.get_stat('comments_count'),
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
        'debates': result.get_metric('debates')
    }
    organizations.append(organization)

TOTAL = {
    'url':
    '',
    'app_name':
    'TOTAL',
    'name':
    'TOTAL',
    'version':
    '',
    'users_count':
    sum(o['users_count'] for o in organizations),
    'processes_count':
    sum(o['processes_count'] for o in organizations),
    'assemblies_count':
    sum(o['assemblies_count'] for o in organizations),
    'comments_count':
    sum(o['comments_count'] for o in organizations),
    'users':
    sum(o['users'] for o in organizations),
    'participatory_processes':
    sum(o['participatory_processes'] for o in organizations),
    'assemblies':
    sum(o['assemblies'] for o in organizations),
    'comments':
    sum(o['comments'] for o in organizations),
    'meetings':
    sum(o['meetings'] for o in organizations),
    'proposals':
    sum(o['proposals'] for o in organizations),
    'accepted_proposals':
    sum(o['accepted_proposals'] for o in organizations),
    'votes':
    sum(o['votes'] for o in organizations),
    'endorsements':
    sum(o['endorsements'] for o in organizations),
    'survey_answers':
    sum(o['survey_answers'] for o in organizations),
    'results':
    sum(o['results'] for o in organizations),
    'debates':
    sum(o['debates'] for o in organizations)
}

organizations.append(TOTAL)

Writer.write_csv(organizations, 'organizations.csv')
