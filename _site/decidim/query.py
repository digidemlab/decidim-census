class Query(object):
    def create_query():
        queries = ['decidim', 'organization', 'metrics']

        query_string = ''

        for query in queries:
            with open('queries/{}.graphql'.format(query)) as graphql_file:
                graphql_query = graphql_file.read()

            query_string += graphql_query

        return query_string
