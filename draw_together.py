import sys
import matplotlib.pyplot as plt
from draw_util import Log

num_filenames = (len(sys.argv)-1)/2
filenames = sys.argv[1:1+num_filenames]
legends = sys.argv[1+num_filenames:]
logs = [Log.load(filename) for filename in filenames]
handles = []
for log in logs:
    log.sort()
    for i, time in enumerate(log.time_list):
        if time > 0.45:
            break
    log.time_list[i:], log.value_list[i:] = [],[]
    handles.append(log.draw())
plt.legend(handles, legends, loc=4)
plt.show()


