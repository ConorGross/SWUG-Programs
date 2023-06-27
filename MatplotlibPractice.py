import matplotlib.pyplot as plt


fig, ax = plt.subplots()

twin1 = ax.twinx() #create twin axes for second data set


# placed on the right by twinx above.


p1, = ax.plot([0, 1, 2], [0, 1, 2], "b-", label="Density") #plot first data set
p2, = twin1.plot([0, 1, 2], [0, 3, 2], "r-", label="Temperature") #plot second data set


ax.set_xlim(0, 2) #set limits for axis x
ax.set_ylim(0, 2) #set limits for data 1 y
twin1.set_ylim(0, 4) #set limits for data 2 y


ax.set_xlabel("Distance")
ax.set_ylabel("Density")
twin1.set_ylabel("Temperature")


ax.yaxis.label.set_color(p1.get_color())
twin1.yaxis.label.set_color(p2.get_color())


tkw = dict(size=4, width=1.5)
ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
ax.tick_params(axis='x', **tkw)

ax.legend(handles=[p1, p2])

plt.show()
