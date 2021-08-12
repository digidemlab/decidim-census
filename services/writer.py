import csv
import json

from services.reader import Reader


class Writer(object):
    @staticmethod
    def write_csv(list, filename):
        keys = list[0].keys()

        with open(filename, 'w', newline='') as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(list)

    def write_json(dict, filename):
        with open(filename, 'w') as file:
            json_string = json.dumps(dict, ensure_ascii=False,
                                     indent=4).encode('utf-8')
            file.write(json_string.decode())

    def write_historical(platform, date):
        filename = '_data/historical/{} - {}.csv'.format(
            platform['id'], platform['platform_url'].replace('https://', ''))

        data = Reader.read_csv(filename)

        org_with_date = {'date': date}
        org_with_date.update(platform)

        org_with_date.pop('id')
        org_with_date.pop('platform_url')
        org_with_date.pop('source_url')
        org_with_date.pop('app_name')
        org_with_date.pop('platform_name')
        org_with_date.pop('version')

        if [day for day in data if day['date'] == date] == []:
            data.append(org_with_date)

        Writer.write_csv(data, filename)
