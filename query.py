from elasticsearch import Elasticsearch, helpers

client = Elasticsearch(HOST="http://localhost", PORT=9200)

INDEX = 'lyrics_metaphors_db_4'




def basic_search(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        }
    }
    return q


def search_with_field(query, field):
    q = {
        "query": {
            "match": {
                field: query
            }
        }
    }
    return q


def wild_card_search(query):
    q = {
        "query": {
            "wildcard": {
               "பாடல் வரிகள்": {
                    "value": query
                }
            }
        },
    }
    return q


def multi_match(query,fields, operator='or'):
    q = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        }
    }
    return q


def exact_search(query):
    q = {
        "query": {
            "multi_match": {
                "query": query,
                "type": "phrase"
            }
        }
    }
    return q


def process_query(query):
    # query based on our input
    if "?" in query:
        search_query = query.split('?')
        if search_query[1] == "பாடல் வரிகள்":
            query_body = search_with_field(search_query[0],'பாடல் வரிகள்')
        elif search_query[1] == "உருவகம்":
            query_body = multi_match(search_query[0],['உருவகம்_1', 'உருவகம்_2', 'உருவகம்_3'])
        elif search_query[1] == "மூலம்":
            query_body = multi_match(search_query[0],['மூலம்_1', 'மூலம்_2', 'மூலம்_3'])
        elif search_query[1] == "இலக்கு":
            query_body = multi_match(search_query[0],['இலக்கு_1', 'இலக்கு_2', 'இலக்கு_3'])
        elif search_query[1] == "பாடகர்" or search_query[1] == "பாடகர்கள்":
            query_body = search_with_field(search_query[0], "பாடகர்கள்")
        else:
            query_body = search_with_field(search_query[0],search_query[1])

    elif '''"''' in query:

        query_body = exact_search(query)

    elif '*' in query:

        query_body = wild_card_search(query)

    else:

        query_body = basic_search(query)
    return query_body


def search(query):
    query_body = process_query(query)
    print('Searching...')
    resp = client.search(index=INDEX, body=query_body)
    return resp
