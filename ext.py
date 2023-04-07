import json
import matplotlib.pyplot as plt
import sys
# import datetime

# def getTime(time):
#     hour = datetime.datetime.fromtimestamp(time/1000.0).hour
#     if 5 <= hour and hour < 11:
#         return 0
#     elif 11 <= hour and hour < 16:
#         return 1
#     elif 16 <= hour and hour < 21:
#         return 2
#     else:
#         return 3

# def getTopApps(user_event_dict):
#     app_dict = dict()
#     for app in user_event_dict:
#         for event_type in app:
#             for event in app[event_type]:
#                 app_dict[app[event_type][event]] = app_dict.get(app[event_type][event], 0) + 1

#     app_dict = {k: v for k, v in sorted(app_dict.items(), key=lambda item: item[1], reverse=True)}
#     return app_dict

def listToXY(series):
    # start = series[0] // 60000
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


f = open("data1.json", "r")
data = f.read()

data1 = json.loads(data)

f = open("data1.json", "r")
data = f.read()

data2 = json.loads(data)

def getEvents(datas, types):
    result = list()

    for data in datas:
        for t in types:
            result += list(data.get(sys.argv[1], dict()).get("events", dict()).get(sys.argv[2], dict()).get(t, dict()).values())

    return result

launches = getEvents([data1, data2], ["Launched", "Notif clicked"])
scrolls = getEvents([data1, data2], ["Scrolled"])
clicks = getEvents([data1, data2], ["Clicked"])
notifs = getEvents([data1, data2], ["Notif received"])


# axes = plt.subplot()
# axes.set_xticks([0, 1, 2, 3])
# axes.set_xticklabels(["Morning", "Afternoon", "Evening", "Night"])

f1, x1, y1 = listToXY(notifs)
f2, x2, y2 = listToXY(clicks)
print(len(x1), len(x2))
y1 = [250 for y in y1]
# print(x1)

t = 0
result = dict()

while t < len(x1):
    
    for i in range(15):
        result[x1[t]] = result.get(x1[t], 0) + f2.get(x1[t] + i, 0)

    t = t + 1

X = list(result.keys())
Y = list(result.values())

plt.bar(x1, y1, color = "yellow", width=20)
# plt.bar(x2, y2, color = "blue", width=1)
plt.plot(x2, y2, color = "blue", marker = 'o')
plt.plot(X, Y, color = "red", marker = 'o')
# plt.scatter(x1, y1)
plt.show()




