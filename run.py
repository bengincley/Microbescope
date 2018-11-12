from MicrobeScope import controls
import argparse
import time


parser = argparse.ArgumentParser(description='Gather input parameters for MicrobeScope run')

parser.add_argument('-f', '--sample_frequency', help='number of samples per hour', type=int,
                    choices=range(1, 48), nargs='?', const=2)
parser.add_argument('-s', '--save_images', help='save images to file?', type=bool)

args = parser.parse_args()
frequency = args.sample_frequency

try:
    print('Press CTRL+C to quit')
    count = 0
    while True:
        loop_time = time.time()
        while (time.time()-loop_time) < 10 and count < 2000:
                count += main()
                print(count)
        while (time.time()-loop_time) < 10:
            time.sleep(0.1)
        count = 0
except KeyboardInterrupt:
    pass
