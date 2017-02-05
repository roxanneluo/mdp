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
    import subprocess as sp

    """
    log_filename = sys.argv[1]
    with open(log_filename, 'r') as f:
        log_dict = json.loads(f.read())
    log = Log(log_dict['time_list'], log_dict['value_list'])
    log.draw()
    """

    max_iter = int(sys.argv[1]) # max for -i
    num_play = sys.argv[2] # -k: number of simulating the computed policy
    algorithm = sys.argv[3] # -a
    log_filename = sys.argv[4]

    reward_split_str = 'AVERAGE RETURNS FROM START STATE:' 
    time_split_str = 'PLANNING TIME:'
    iter_start, iter_step = 0, 10
    cmd = ['python', 'gridworld.py','-t', 
            '-g', 'BigGrid', '-q', '-w', '35',
            '-a', algorithm, '-k', num_play,
            '-i', None]

    log = Log()
    for num_iter in range(iter_start, max_iter, iter_step):
        cmd[-1] = str(num_iter)
        result = sp.check_output(cmd).split('\n')
        print(num_iter, result)
        # assume the time print is always in line 0 and reward print in line[-1]
        time = float(result[0].split(time_split_str)[-1])
        reward = float(result[-4].split(reward_split_str)[-1])
        log.update(time, reward)
        plt.close()
    print('done run')
    log.dump(log_filename)
    print('done dump')
    log.draw()
