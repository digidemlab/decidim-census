from decidim.web_parser import WebParser


class Result(object):
    def __init__(self, json, instance):
        self.instance = instance
        self.json = json

    def id(self):
        return self.instance['id']

    def platform_url(self):
        return self.instance['url']

    def source_url(self):
        return self.instance.get('source')

    def decidim(self):
        return self.json['decidim']

    def organization(self):
        return self.json['organization']

    def metrics(self):
        return self.json['metrics']

    def application_name(self):
        return self.decidim()['applicationName']

    def version(self):
        return self.decidim()['version']

    def name(self):
        return self.organization()['name']

    def stats(self):
        return self.organization()['stats']

    def get_stat(self, name):
        return [
            stat['value'] for stat in self.stats() if stat['name'] == name
        ][0]

    def get_metric(self, name):
        return [
            metric['count'] for metric in self.metrics()
            if metric['name'] == name
        ][0]

    def convert_to_JSON(self):
        return {
            'id': self.id(),
            'platform_url': self.platform_url(),
            'source_url': self.source_url(),
            'app_name': self.application_name(),
            'platform_name': self.name(),
            'version': self.version(),
            'users_count': self.get_stat('users_count'),
            'processes_count': self.get_stat('processes_count'),
            'assemblies_count': self.get_stat('assemblies_count'),
            'comments_count': self.get_stat('comments_count'),
            'users': self.get_metric('users'),
            'participatory_processes':
            self.get_metric('participatory_processes'),
            'assemblies': self.get_metric('assemblies'),
            'comments': self.get_metric('comments'),
            'meetings': self.get_metric('meetings'),
            'proposals': self.get_metric('proposals'),
            'accepted_proposals': self.get_metric('accepted_proposals'),
            'votes': self.get_metric('votes'),
            'endorsements': self.get_metric('endorsements'),
            'survey_answers': self.get_metric('survey_answers'),
            'results': self.get_metric('results'),
            'debates': self.get_metric('debates')
        }

    def add_logo_and_colour(platform):
        platform['logo_url'], platform[
            'background-color'] = WebParser.get_logo_url_and_colour(
                platform['platform_url'])

        return platform

    def sum_metric(platforms, name):
        return sum(o[name] for o in platforms)

    def calculate_totals(platforms):
        return {
            'id':
            '',
            'platform_url':
            '',
            'source_url':
            '',
            'app_name':
            'TOTAL',
            'platform_name':
            'TOTAL',
            'version':
            '',
            'users_count':
            Result.sum_metric(platforms, 'users_count'),
            'processes_count':
            Result.sum_metric(platforms, 'processes_count'),
            'assemblies_count':
            Result.sum_metric(platforms, 'assemblies_count'),
            'comments_count':
            Result.sum_metric(platforms, 'comments_count'),
            'users':
            Result.sum_metric(platforms, 'users'),
            'participatory_processes':
            Result.sum_metric(platforms, 'participatory_processes'),
            'assemblies':
            Result.sum_metric(platforms, 'assemblies'),
            'comments':
            Result.sum_metric(platforms, 'comments'),
            'meetings':
            Result.sum_metric(platforms, 'meetings'),
            'proposals':
            Result.sum_metric(platforms, 'proposals'),
            'accepted_proposals':
            Result.sum_metric(platforms, 'accepted_proposals'),
            'votes':
            Result.sum_metric(platforms, 'votes'),
            'endorsements':
            Result.sum_metric(platforms, 'endorsements'),
            'survey_answers':
            Result.sum_metric(platforms, 'survey_answers'),
            'results':
            Result.sum_metric(platforms, 'results'),
            'debates':
            Result.sum_metric(platforms, 'debates')
        }
