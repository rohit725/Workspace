from elasticsearch import Elasticsearch, helpers


es = Elasticsearch(['10.132.46.98:9200'])
doc = {
    "query": {
        "bool": {
            "must": [
                {
                    "match_all": {}
                },
                {
                    "match_phrase": {
                        "connection.destination.locality.keyword": {
                            "query": "public"
                        }
                    }
                },
                {
                    "range": {
                        "@timestamp": {
                            "gte": "now-72h",
                            "lte": "now",
                            "format": "epoch_millis"
                        }
                    }
                }
            ],
            "filter": [],
            "should": [],
            "must_not": []
        }
    }
}

results = helpers.scan(es, index="d3b6842d-naf-*",
                       preserve_order=True, query=doc, scroll='90m', request_timeout=60)

for item in results:
    print(item['_source'])
