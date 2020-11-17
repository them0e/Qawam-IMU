#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#from matplotlib import style

#style.use('fivethirtyeight')

#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)

#def animate(i):
#    graph_data = open('example.txt','r').read()
#    lines = graph_data.split('\n')
#    xs = []
#    ys = []
#    for line in lines:
#        if len(line) > 1:
#            x, y = line.split(',')
#            xs.append(float(x))
#            ys.append(float(y))
#    ax1.clear()
#    ax1.plot(xs, ys)

#ani = animation.FuncAnimation(fig, animate, interval=1000)
#plt.show()

import matplotlib.pyplot as plt
import numpy as np

t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2*np.pi*t)
plt.plot(t, s)

plt.xlabel('time (s)')
plt.ylabel('voltage (mV)')
plt.title('About as simple as it gets, folks')
plt.grid(True)
plt.savefig("test.png")
plt.show()