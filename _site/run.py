from services.downloader import Downloader
from services.writer import Writer
from services.reader import Reader
from services.dater import Dater
from decidim.query import Query
from decidim.result import Result

instances = Reader.read_csv('instances.csv')

query_string = Query.create_query()

platforms = []
for instance in instances:
    print('Getting data from {}'.format(instance['url']))
    result_json = Downloader.get_graphql(instance['url'], query_string)

    if not result_json:
        continue

    platforms.append(Result(result_json, instance).convert_to_JSON())

total = Result.calculate_totals(platforms)
Writer.write_json(total, '_data/total.json')

platforms.append(total)
Writer.write_csv(platforms, 'platforms.csv')

platforms.pop()

for platform in platforms:
    print('Updating history for {}'.format(platform['platform_url']))
    Writer.write_historical(platform, str(Dater.yesterday()))

    print('Getting logo_url and colour from {}'.format(
        platform['platform_url']))
    platform = Result.add_logo_and_colour(platform)

Writer.write_csv(platforms, '_data/platforms.csv')
