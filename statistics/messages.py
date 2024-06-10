import matplotlib as mpl
import csv

import matplotlib.pyplot as plt

with open('messages.csv', encoding="utf-8") as csvfile:
    t = []
    if csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        headers = next(reader)
        n = 0
        for i in reader:
            F = 1
            for j in range(len(t)):
                if t[j]["name"] == i[0] and t[j]["guild"] == i[1]:
                    t[j]["date"].append(i[2])
                    t[j]["messages"].append(int(i[3]))
                    F = 0
                    break
            if F:
                t.append({
                    "name": i[0],
                    "guild": i[1],
                    "date": [i[2]],
                    "messages": [int(i[3])]
                })
fig, ax = plt.subplots()
t.sort(key=lambda x: sum(x["messages"]), reverse=True)
print(t)
for i in [i if sum(i['messages']) > 200 else "" for i in t]:
    if i:
        if i["guild"] == "887981666805628939":
            x, y = i['date'], i['messages']
            if '10/06/24' in x:
                x, y = x[:-1], y[:-1]
            ax.plot(x, y, label=i["name"])
ax.legend()
ax.grid()
plt.show()