import csv


class Reader(object):
    def read_csv(filename):
        try:
            with open(filename) as file:
                reader = csv.DictReader(file)
                return list(reader)
        except OSError:
            return []
