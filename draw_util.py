import json
import matplotlib.pyplot as plt
class Log:
    def __init__(self, time_list = [], value_list = []):
        self.time_list = time_list
        self.value_list = value_list
    def update(self, time, value):
        self.time_list.append(time)
        self.value_list.append(value)
    def dump(self, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps({'time_list': self.time_list,
                'value_list': self.value_list}))
    def draw(self):
        plt.plot(self.time_list, self.value_list)
        plt.xlabel('time(s)')
        plt.ylabel('average reward')
        plt.show()

if __name__ == "__main__":
    import sys

    log_filename = sys.argv[1]
    with open(log_filename, 'r') as f:
        log_dict = json.loads(f.read())
    log = Log(log_dict['time_list'], log_dict['value_list'])
    log.draw()

