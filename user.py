import json
import csv
#code is used to get different csv files based on event type for each user and app both simultaneously 
def get_events(data):
    events = set()
    for user in data:
        if 'events' in data[user]:
            for app in data[user]['events']:
                for event_type in data[user]['events'][app]:
                    events.add(event_type)
    return events

def get_top_events(event_type, data):
    app_dict = dict()
    for user in data:
        if 'events' in data[user]:
            for app_k, app_v in data[user]['events'].items():
                for type_k, type_v in app_v.items():
                    if type_k == event_type:
                        app_dict[app_k] = app_dict.get(app_k, 0) + len(type_v)
    app_dict = {k: v for k, v in sorted(app_dict.items(), key=lambda item: item[1], reverse=True)}
    return app_dict

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User ID', 'App', 'Count'])
        for user in data:
            for app, count in data[user].items():
                writer.writerow([user, app, count])

# Read data from JSON file
with open('data1.json') as f:
    data = json.load(f)

events = get_events(data)

for event_type in events:
    event_data = {}
    for user in data:
        if 'events' in data[user]:
            top_events = get_top_events(event_type, {user: data[user]})
            event_data[user] = top_events
    write_to_csv(event_data, f'{event_type}.csv')
