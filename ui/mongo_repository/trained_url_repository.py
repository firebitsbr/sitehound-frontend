from collections import OrderedDict

import pymongo
from bson import ObjectId

from ui.singleton import Singleton


def get_seeds_urls_to_label_dao(workspace_id, page_size, sources, relevances, categories, keyword_source_type, last_id, last_source):

    and_condition_list = []
    #sources
    if len(sources) > 0:
        source_search_conditions = []
        for source in sources:
            if source == "searchengine":
                source_search_conditions.append({'crawlEntityType': "BING"})
                source_search_conditions.append({'crawlEntityType': "GOOGLE"})
            elif source == "tor":
                source_search_conditions.append({'crawlEntityType': "TOR"})
            elif source == "imported":
                source_search_conditions.append({'crawlEntityType': "MANUAL"})
            elif source == "deepdeep":
                source_search_conditions.append({'crawlEntityType': "DD"})
            else:
                print("no valid source was provided:" + source)

        source_search_object = {'$or': source_search_conditions}
        and_condition_list.append(source_search_object)


    #relevances
    if len(relevances) > 0:
        relevances_search_conditions = []
        for relevance in relevances:
            if relevance == "unset":
                relevances_search_conditions.append({'relevant': {"$exists": False}})
            else:
                relevances_search_conditions.append({"$and": [{'relevant': relevance}, {'relevant': {"$exists": True}}]})

        relevances_search_object = {'$or': relevances_search_conditions}
        and_condition_list.append(relevances_search_object)


    #page_types
    if len(categories) > 0:
        categories_search_conditions = []
        for category in categories:
            categories_search_conditions.append({'categories': category})

        categories_search_object = {'$or': categories_search_conditions}
        and_condition_list.append(categories_search_object)

    page_search_object = {}
    if last_id is not None and last_source is not None:
        #even bigger from same source, or any from other source
        page_search_object = {'$or': [
            {"$and": [{"_id": {"$gt": ObjectId(last_id)}}, {"crawlEntityType": last_source}]},
            {"crawlEntityType": {"$ne": last_source}}
        ]}
        and_condition_list.append(page_search_object)

    deleted_search_object = {'deleted': {"$exists": False}}
    and_condition_list.append(deleted_search_object)

    workspace_search_object = {'workspaceId': workspace_id}
    and_condition_list.append(workspace_search_object)


    sort_dict = OrderedDict()
    sort_dict['order'] = 1
    sort_dict['_id'] = 1

    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()

    res = collection.aggregate([
        { "$project" : {
            '_id':1, 'host':1, 'crawlEntityType':1, 'url':1, 'title':1, 'relevant':1, 'workspaceId':1, 'deleted':1,
            "order" : {
                "$cond" : {
                    "if": { "$eq" : ["$crawlEntityType", "DD"] }, "then" : 1,
                    "else": { "$cond" : {
                        "if": { "$eq" : ["$crawlEntityType", "TOR"] }, "then" : 2,
                        "else": {"$cond": {
                            "if": {"$eq": ["$crawlEntityType", "GOOGLE"]}, "then": 3,
                            "else": {"$cond": {
                                "if": {"$eq": ["$crawlEntityType", "BING"]}, "then": 4,
                                "else": 5
                            }}
                        }}
                    }}
                }
            }}
        },
        {"$match" : {'$and': and_condition_list}},
        {"$sort" : sort_dict },
        {"$limit" : page_size },
        {"$project" : {'_id':1, 'host':1, 'crawlEntityType':1, 'url':1, 'title':1, 'relevant':1, 'order': 1} }
    ])

    docs = list(res["result"])
    return docs


def get_seeds_urls_all_labeled_dao(workspace_id, page_size, sources, relevances, last_id):

    and_condition_list = []

    if len(sources) > 0:
        source_search_conditions = []
        for source in sources:
            if source == "searchengine":
                source_search_conditions.append({'crawlEntityType': "BING"})
                source_search_conditions.append({'crawlEntityType': "GOOGLE"})
            elif source == "tor":
                source_search_conditions.append({'crawlEntityType': "TOR"})
            elif source == "imported":
                source_search_conditions.append({'crawlEntityType': "MANUAL"})
            elif source == "deepdeep":
                source_search_conditions.append({'crawlEntityType': "DD"})
            else:
                print("no valid source was provided:" + source)

        source_search_object = {'$or': source_search_conditions}
        and_condition_list.append(source_search_object)

    if len(relevances) > 0:
        relevances_search_conditions = []
        for relevance in relevances:
            if relevance == "unset":
                relevances_search_conditions.append({'relevant': {"$exists": False}})
            else:
                relevances_search_conditions.append({"$and": [{'relevant': relevance}, {'relevant': {"$exists": True}}]})

        relevances_search_object = {'$or': relevances_search_conditions}
        and_condition_list.append(relevances_search_object)

    if last_id:
        last_id_search_object = {"_id": {"$gt": ObjectId(last_id)}}
        and_condition_list.append(last_id_search_object)

    deleted_search_object = {'deleted': {"$exists": False}}
    and_condition_list.append(deleted_search_object)

    workspace_search_object = {'workspaceId': workspace_id}
    and_condition_list.append(workspace_search_object)

    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()
    res = collection.find({'$and': and_condition_list})\
        .sort('_id', pymongo.ASCENDING)\
        .limit(page_size)

    docs = list(res)
    return docs


def get_seeds_urls_keywords_results_dao(workspace_id, page_size, last_id):

    and_condition_list = []

    deleted_search_object = {'deleted': {"$exists": False}}
    and_condition_list.append(deleted_search_object)

    workspace_search_object = {'workspaceId': workspace_id}
    and_condition_list.append(workspace_search_object)

    if last_id:
        last_id_search_object = {"_id": {"$gt": ObjectId(last_id)}}
        and_condition_list.append(last_id_search_object)

    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()

    res = collection.find({'$and': and_condition_list})\
        .sort('_id', pymongo.ASCENDING)\
        .limit(page_size)

    docs = list(res)
    return docs


def get_seeds_udcs_by_workspace_dao(workspace_id):

    and_condition_list = []

    # source_search_conditions = []
    # if source == "searchengine":
    #     source_search_conditions.append({'crawlEntityType': "BING"})
    #     source_search_conditions.append({'crawlEntityType': "GOOGLE"})
    # elif source == "twitter":
    #     source_search_conditions.append({'crawlEntityType': "TWITTER"})
    # elif source == "tor":
    #     source_search_conditions.append({'crawlEntityType': "TOR"})
    # elif source == "imported":
    #     source_search_conditions.append({'crawlEntityType': "MANUAL"})
    # elif source == "deepdeep":
    #     source_search_conditions.append({'crawlEntityType': "DD"})
    # else:
    #     print("no valid source was provided:" + source)
    # source_search_object = {'$or': source_search_conditions}
    # and_condition_list.append(source_search_object)

    deleted_search_object = {'deleted': None}
    and_condition_list.append(deleted_search_object)

    workspace_search_object = {'workspaceId': workspace_id}
    and_condition_list.append(workspace_search_object)

    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()
    res = collection\
        .find({'$and': and_condition_list})\
        .distinct("udc")

    docs = list(res)
    return sorted(docs)


# def get_seeds_udcs_by_workspace_dao(workspace_id):
#     collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()
#     return list(collection.find({'workspaceId': workspace_id}))


' retrieves only the field url from the docs '


def get_seeds_urls_url(workspace_id):
    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()
    res = collection.find({'workspaceId': workspace_id}, {'_id': 0, 'url': 1})
    docs = list(res)
    return docs


def get_seeds_urls_categorized(workspace_id):
    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()
    relevant_urls_result = collection.find({'workspaceId': workspace_id, 'relevant': True, 'deleted': {'$exists': False}}, {'_id': 0, 'url': 1})
    relevant_urls = []
    for url_doc in relevant_urls_result:
        if 'url' in url_doc:
            relevant_urls.append(url_doc['url'])

    irrelevant_urls_result = collection.find({'relevant': False, 'deleted': {'$exists': False}}, {'_id': 0, 'url': 1})
    irrelevant_urls = []
    for url_doc in irrelevant_urls_result:
        if 'url' in url_doc:
            irrelevant_urls.append(url_doc['url'])

    return {'relevant': list(relevant_urls), 'irrelevant': list(irrelevant_urls)}






################ SAVE_CUSTOMIZE_SEEDS #########################

# def dao_insert_url(url, is_relevant):
#     extracted = extract_tld(url)
#     host = extracted.domain + '.' + extracted.suffix
#     update_object = {"host": host, "relevant": is_relevant}
#
#     collection = Singleton.getInstance().mongo_instance.get_current_seed_urls_collection()
#     collection.update({"url": url}, {'$set': update_object}, True)


def dao_update_relevance(url, obj):
    update_object = {}
    update_object['relevant'] = obj['relevant']
    collection = Singleton.getInstance().mongo_instance.get_current_seed_urls_collection()
    print "setting url %s to %s in collection %s" % (url, str(obj['relevant']), collection)
    collection.update({"url": url}, {'$set': update_object}, True)


def dao_update_relevanceByid(workspace_id, id, relevance, categories, udc):
    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()
    update_object= {}
    update_object['relevant'] = relevance
    update_object['categories'] = categories
    update_object['udc'] = udc
    collection.update({"_id": ObjectId(id)}, {'$set': update_object}, True)


def label(workspace_id, id, relevance):
    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()
    update_object= {}
    update_object['relevant'] = relevance
    collection.update({"_id": ObjectId(id)}, {'$set': update_object}, True)


def dao_delete_seed_url(workspace_id, id):
    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()
    update_object= {}
    update_object['deleted'] = True
    collection.update({"_id": ObjectId(id)}, {'$set': update_object}, True)


def dao_reset_results(workspace_id, source):

    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()

    source_search_conditions = []

    workspace_search_object = {'workspaceId': workspace_id}

    if source == "searchengine":
        source_search_conditions.append({'crawlEntityType': "BING"})
        source_search_conditions.append({'crawlEntityType': "GOOGLE"})
    elif source == "twitter":
        source_search_conditions.append({'crawlEntityType': "TWITTER"})
    elif source == "tor":
        source_search_conditions.append({'crawlEntityType': "TOR"})
    elif source == "imported":
        source_search_conditions.append({'crawlEntityType': "MANUAL"})
    elif source == "deepdeep":
        source_search_conditions.append({'crawlEntityType': "DD"})
    else:
        print("no valid source was provided:" + source)
        return
    source_search_object = {'$or': source_search_conditions}

    collection.remove({'$and': [workspace_search_object, source_search_object]})


def dao_aggregate_urls(workspace_id):

    and_search_conditions = []

    workspace_search_object = {'workspaceId': workspace_id}
    and_search_conditions.append(workspace_search_object)

    delete_search_object = {'deleted': {'$exists': False}}
    and_search_conditions.append(delete_search_object)

    source_search_object = {'$and': and_search_conditions}

    collection = Singleton.getInstance().mongo_instance.get_seed_urls_collection()

    try:
        res = collection.aggregate([

            # '$group': {'_id': '$crawlEntityType', "count": {"$sum": 1}}
            {'$match': source_search_object},
            {'$group': {'_id': {'crawlEntityType': '$crawlEntityType', 'relevant': '$relevant'}, "count": {"$sum": 1}}}
        ])
    except Exception as e:
        print e

    return res["result"]


