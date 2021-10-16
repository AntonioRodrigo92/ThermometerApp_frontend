from bson import SON
from django.shortcuts import render
import json
from datetime import datetime, timedelta
import pymongo


def all_reads(request):
    coll = get_collection()
    labels_raw = []
    temp_raw = []
    hum_raw = []

    for doc in coll:
        labels_raw.append(doc["timestamp"].strftime("%H:%M:%S"))
        temp_raw.append(doc["temperature"])
        hum_raw.append(doc["humidity"])

    labels = ','.join(labels_raw)
    values_temp = json.dumps(temp_raw)
    values_hum = json.dumps(hum_raw)

    context = {
        'labels': labels,
        'values_temp': values_temp,
        'values_hum': values_hum,
    }
    return render(request, 'all_reads.html', context)


def last_24h(request):
    coll = get_collection()
    last_day = get_last_day_readings(coll)
    labels_raw = []
    temp_raw = []
    hum_raw = []

    for doc in last_day:
        labels_raw.append(doc["_id"]["hour"])
        temp_raw.append(doc["avgTemperature"])
        hum_raw.append(doc["avgHumidity"])

    labels = labels_raw
    values_temp = json.dumps(temp_raw)
    values_hum = json.dumps(hum_raw)

    context = {
        'labels': labels,
        'values_temp': values_temp,
        'values_hum': values_hum,
    }
    return render(request, 'last_24h.html', context)


def last_hour(request):
    coll = get_collection()
    last_hour_r = get_last_hour_readings(coll)
    labels_raw = []
    temp_raw = []
    hum_raw = []

    for doc_h in last_hour_r:
        labels_raw.append(doc_h["timestamp"].strftime("%H:%M:%S"))
        temp_raw.append(doc_h["temperature"])
        hum_raw.append(doc_h["humidity"])

    labels = ','.join(labels_raw)
    values_temp = json.dumps(temp_raw)
    values_hum = json.dumps(hum_raw)

    context = {
        'labels': labels,
        'values_temp': values_temp,
        'values_hum': values_hum,
    }
    return render(request, 'last_hour.html', context)


def render_specific_day(request):
    coll = get_collection()
    td = datetime.now()
    last_day = td.strftime("%Y-%m-%d")
    first_dt = get_first_measure(coll).strftime("%Y-%m-%d")

    labels_raw = []
    temp_raw = []
    hum_raw = []

    if request.method == 'GET':
        year = int(td.strftime("%Y"))
        month = int(td.strftime("%m"))
        day = int(td.strftime("%d"))
        last_day_readings = get_specific_day_readings(coll, datetime(year, month, day))
        for read in last_day_readings:
            labels_raw.append(read["_id"]["hour"])
            temp_raw.append(read["avgTemperature"])
            hum_raw.append(read["avgHumidity"])

        labels = labels_raw
        values_temp = json.dumps(temp_raw)
        values_hum = json.dumps(hum_raw)

        context = {
            'calendar_today': last_day,
            'calendar_first_day': first_dt,
            'calendar_last_day': last_day,

            'labels': labels,
            'values_temp': values_temp,
            'values_hum': values_hum,
        }
    else:
        selected_date = request.POST['select_date']
        selected_date_arr = request.POST['select_date'].split('-')
        year = int(selected_date_arr[0])
        month = int(selected_date_arr[1])
        day = int(selected_date_arr[2])
        selected_day_readings = get_specific_day_readings(coll, datetime(year, month, day))
        for read in selected_day_readings:
            labels_raw.append(read["_id"]["hour"])
            temp_raw.append(read["avgTemperature"])
            hum_raw.append(read["avgHumidity"])

        labels = labels_raw
        values_temp = json.dumps(temp_raw)
        values_hum = json.dumps(hum_raw)

        context = {
            'calendar_today': selected_date,
            'calendar_first_day': first_dt,
            'calendar_last_day': last_day,

            'labels': labels,
            'values_temp': values_temp,
            'values_hum': values_hum,
        }
    return render(request, 'specific_date.html', context)


def render_month_overview(request):
    coll = get_collection()
    td = datetime.now()
    last_month = td.strftime("%Y-%m")
    first_month = get_first_measure(coll).strftime("%Y-%m")

    labels_raw = []
    temp_raw = []
    hum_raw = []

    if request.method == 'GET':
        year = int(td.strftime("%Y"))
        month = int(td.strftime("%m"))
        last_month_readings = get_month_overview(coll, month, year)
        for read in last_month_readings:
            labels_raw.append(read["_id"]["day"])
            temp_raw.append(read["avgTemperature"])
            hum_raw.append(read["avgHumidity"])

        labels = labels_raw
        values_temp = json.dumps(temp_raw)
        values_hum = json.dumps(hum_raw)

        context = {
            'calendar_today': last_month,
            'calendar_first_month': first_month,
            'calendar_last_month': last_month,

            'labels': labels,
            'values_temp': values_temp,
            'values_hum': values_hum,
        }
    else:
        selected_month = request.POST['select_date']
        selected_month_arr = request.POST['select_date'].split('-')
        year = int(selected_month_arr[0])
        month = int(selected_month_arr[1])
        selected_month_readings = get_month_overview(coll, month, year)
        for read in selected_month_readings:
            labels_raw.append(read["_id"]["day"])
            temp_raw.append(read["avgTemperature"])
            hum_raw.append(read["avgHumidity"])

        labels = labels_raw
        values_temp = json.dumps(temp_raw)
        values_hum = json.dumps(hum_raw)

        context = {
            'calendar_today': selected_month,
            'calendar_first_month': first_month,
            'calendar_last_month': last_month,

            'labels': labels,
            'values_temp': values_temp,
            'values_hum': values_hum,
        }
    return render(request, 'month_overview.html', context)


########################################################################################################################


def get_collection():
    try:
        client = pymongo.MongoClient("")
        client.server_info()
    except:
        client = pymongo.MongoClient("")
    database = client[""]
    collection = database.get_collection("").find()
    client.close()
    return collection


def get_last_day_readings(collection):
    documents = collection.collection.aggregate([
        {
            "$match": {
                "timestamp": {'$gte': datetime.now() - timedelta(hours=24)},
                "humidity": {'$gt': 0}
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$timestamp"},
                    "month": {"$month": "$timestamp"},
                    "day": {"$dayOfMonth": "$timestamp"},
                    "hour": {"$hour": "$timestamp"}
                },
                "avgTemperature": {"$avg": "$temperature"},
                "avgHumidity": {"$avg": "$humidity"},
            }
        },
        {
            "$sort": SON([("_id", 1)])
        }
    ])
    return documents


def get_last_hour_readings(collection):
    documents = collection.collection.aggregate(
        [{"$match": {"timestamp": {'$gte': datetime.now() - timedelta(hours=1)}}}])
    return documents


def get_specific_day_readings(collection, date):
    max_date = date + timedelta(days=1)
    documents = collection.collection.aggregate([
        {
            "$match": {
                "$and": [
                    {"timestamp": {'$gte': date}},
                    {"timestamp": {'$lt': max_date}},
                    {"humidity": {'$gt': 0}}
                ]
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$timestamp"},
                    "month": {"$month": "$timestamp"},
                    "day": {"$dayOfMonth": "$timestamp"},
                    "hour": {"$hour": "$timestamp"}
                },
                "avgTemperature": {"$avg": "$temperature"},
                "avgHumidity": {"$avg": "$humidity"},
            }
        },
        {
            "$sort": SON([("_id", 1)])
        }
    ])
    return documents


def get_first_measure(collection):
    doc = collection.collection.find().sort("timestamp", pymongo.ASCENDING).limit(1)[0]
    return doc["timestamp"]


# TODO - acabar
def get_month_overview(coll, month, year):
    initial_date = datetime(year, month, 1)
    if month == 12:
        final_date = datetime(year + 1, 1, 1)
    else:
        final_date = datetime(year, month + 1, 1)
    documents = coll.collection.aggregate([
        {
            "$match": {
                "$and": [
                    {"timestamp": {'$gte': initial_date}},
                    {"timestamp": {'$lt': final_date}},
                    {"humidity": {'$gt': 0}}
                ]
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$timestamp"},
                    "month": {"$month": "$timestamp"},
                    "day": {"$dayOfMonth": "$timestamp"},
                },
                "avgTemperature": {"$avg": "$temperature"},
                "avgHumidity": {"$avg": "$humidity"},
            }
        },
        {
            "$sort": SON([("_id", 1)])
        }
    ])
    return documents
