class Result(object):
    def __init__(self, json):
        self.json = json

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
