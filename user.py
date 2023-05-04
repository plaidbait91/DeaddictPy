import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_events(data):
    events = set()
    
    for d in data: 
        for user in d:
            if 'events' in d[user]:
                for app in d[user]['events']:
                    for event_type in d[user]['events'][app]:
                        events.add(event_type)
    return events

def get_apps(data, threshold):
    apps = dict()
    user_count = dict()

    for d in data:
        for user in d:
            for app_k, app_v in d[user].get('events', {}).items():
                user_count[app_k] = user_count.get(app_k, 0) + 1
                for type_k, type_v in app_v.items():
                    for event in type_v:
                        apps[app_k] = apps.get(app_k, 0) + 1

    apps = {k : v for k, v in apps.items() if v > threshold and user_count[k] > 5}
    return apps

# def get_top_events(event_type, user, range):
#     app_dict = dict()
    
#     for d in data:
#         if 'events' in d.get(user, {}).keys():
#             for app_k, app_v in d.get(user, {})['events'].items():
#                 for type_k, type_v in app_v.items():
#                     if type_k == event_type:
#                         for _, event in type_v.items():
#                             if event > range[0] and event < range[1]:
#                                 app_dict[app_k] = app_dict.get(app_k, 0) + 1

#     app_dict = {k: v for k, v in sorted(app_dict.items(), key=lambda item: item[1], reverse=True)}
#     return app_dict

def byTime(rng, user, range):
    count = 0
    
    for d in data:
        for app_k, app_v in d.get(user, {}).get('events', {}).items():
            for type_k, type_v in app_v.items():
                for _, event in type_v.items():
                    time = event % day
                    if event > range[0] and event < range[1] and time > rng[0] and time < rng[1]:
                        count += 1

    return count

def byEvent(event_type, user, range):
    count = 0
    
    for d in data:
        for app_k, app_v in d.get(user, {}).get('events', {}).items():
            for type_k, type_v in app_v.items():
                if type_k == event_type:
                    for _, event in type_v.items():
                        if event > range[0] and event < range[1]:
                            count += 1

    return count

def byApp(app, user, range):
    count = 0
    
    for d in data:
        for app_k, app_v in d.get(user, {}).get('events', {}).items():
            if app_k == app:
                for type_k, type_v in app_v.items():
                    for _, event in type_v.items():
                        if event > range[0] and event < range[1]:
                            count += 1

    return count

def byEventApp(app, event, user, range):
    count = 0
    
    for d in data:
        for app_k, app_v in d.get(user, {}).get('events', {}).items():
            if app_k == app:
                for type_k, type_v in app_v.items():
                    if type_k == event_type:
                        for _, event in type_v.items():
                            if event > range[0] and event < range[1]:
                                count += 1

    return count

def byUnlocks(dummy, user, range):
    count = 0
    
    for d in data:
        for _, x in d.get(user, {}).get('unlocks', {}).items():
            count += 1

    return count

# def write_to_csv(data, filename):
#     with open(filename, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['User ID', 'App', 'Count'])
#         for user in data:
#             for app, count in data[user].items():
#                 writer.writerow([user, app, count])

def csv_generate(filename, func, *axis):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User ID', 'Day 1-10', 'Day 10-20', 'Day 20-30', 'Day 30-40', 'Day 40-50'])
        for user in keys:
            row = [user]
            for i in range(5):
                rng = [start + day * i * 10, start + day * (i + 1) * 10]
                count = func(*axis, user, rng)
                row.append(count)
            writer.writerow(row)
    
# Read data from JSON file
with open('data1.json') as f:
    data1 = json.load(f)

with open('data2.json') as f:
    data2 = json.load(f)

data = [data1, data2]

events = get_events(data)
apps = get_apps(data, 200)
keys = set().union(*data)

start = 1677609000000
day = 1000 * 60 * 60 * 24

    
# df = pd.read_csv("./csv/com,reddit,frontpage.csv")
# df = pd.read_csv("./csv/com,instagram,android.csv")
df = pd.read_csv("./csv/com,instagram,android_Scrolled.csv")

# ranges = [(0, day / 4), (day / 4, day / 2), (day / 2, day * 3 / 4), (day * 3 / 4, day)]
# for i, rng in enumerate(ranges):
#     csv_generate(f'./csv/{i}.csv', byTime, rng)

# for event_type in events:
#     for app in apps:
#         csv_generate(f'./csv/{app}_{event_type}.csv', byEventApp, app, event_type)

# for event_type in events:
#     csv_generate(f'./csv/{event_type}.csv', byEvent, event_type)

# for app in apps:
#     csv_generate(f'./csv/{app}.csv', byApp, app)

# csv_generate('./new_csv/unlocks.csv', byUnlocks, 0)
# df = pd.read_csv("./new_csv/unlocks.csv")
df = df.replace(0, np.nan)
for interval in df.columns[1:]:
    med = df[interval].median()
    mad = (df[interval] - df[interval].mean()).abs().mean()

    df[interval] = [0.6745 * (x - med) / mad if not np.isnan(x) else np.nan for x in df[interval]]
        
grp1 = ["145",
"112",
"164",
"169",
"195",
"176",
"febEv5ejT_q-qpHYWIstzH",
"fuF_HzIMS3yTIVS-QiTO64",
"dG3EunBVQPWeWRQsGrk6PL",
"eR8YD1lZTrywe2pJM4pqTY",
"ecxeoOeJT22cee3zmzNnv3",
"eRx9i8oVS5mLrJ7_JbpbdJ",]

# F = ["112",
# "142",
# "164",
# "146",
# "111",
# "febEv5ejT_q-qpHYWIstzH",
# ]

# M = df["User ID"].tolist()
# M = list(filter(lambda x: x not in F, M))

grp2 = df["User ID"].tolist()
grp2 = list(filter(lambda x: x not in grp1, grp2))

add_df = df[df["User ID"].isin(grp1)]
norm_df = df[df["User ID"].isin(grp2)]

intervals = ["Day 1-10", "Day 10-20", "Day 20-30", "Day 30-40", "Day 40-50"]
for interval in intervals:
    df.to_csv("./csv/test.csv", index=False)
    plt.scatter(add_df["User ID"], add_df[interval], marker="x", label="Addicted")
    plt.scatter(norm_df["User ID"], norm_df[interval], marker="o", label="Normal")
    # plt.scatter(df["User ID"], df["Day 1-10"], label="Days 1-10")
    # plt.scatter(df["User ID"], df["Day 10-20"])
    # plt.scatter(df["User ID"], df["Day 20-30"], label="Days 20-30")
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.xticks([]) 
    # plt.scatter(df["User ID"], df["Day 30-40"])
    plt.show()

