import json
import matplotlib.pyplot as plt
import csv

def listToXY(series):
    start = 0
    s_dict = dict()

    for t in series:
        t_val = t // 60000 - start
        s_dict[t_val] = s_dict.get(t_val, 0) + 1

    x = list(s_dict.keys())
    x.sort()
    f = {i: s_dict[i] for i in x}
    y = list(f.values())

    return (f, x, y)


def getTopApps(user, data):
    app_dict = dict()

    for app_k, app_v in data[user]["events"].items():
        for type_k, type_v in app_v.items():
            for event in type_v:
                app_dict[app_k] = app_dict.get(app_k, 0) + 1

    app_dict = {k: v for k, v in sorted(app_dict.items(), key=lambda item: item[1], reverse=True)}
    return app_dict


def getTopEvents(user, data):
    app_dict = dict()

    for app_k, app_v in data[user]["events"].items():
        for type_k, type_v in app_v.items():
            for event in type_v:
                app_dict[type_k] = app_dict.get(type_k, 0) + 1

    app_dict = {k: v for k, v in sorted(app_dict.items(), key=lambda item: item[1], reverse=True)}
    return app_dict


def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['App', 'Count'])
        for app, count in data.items():
            writer.writerow([app, count])


# Read data from JSON file
with open('data1.json') as f:
    data = json.load(f)

# Generate CSV files for each user
for user in data:
    top_apps = getTopApps(user, data)
    top_events = getTopEvents(user, data)
## issue- Users with non integer usernames are not shown

    write_to_csv(top_apps, f'top_apps_{str(user)}.csv')
    write_to_csv(top_events, f'top_events_{str(user)}.csv')
