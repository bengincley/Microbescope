from MicrobeScope import controls
import argparse
import time


parser = argparse.ArgumentParser(description='Gather input parameters for MicrobeScope run')

parser.add_argument('-f', '--sample_frequency', help='number of samples per hour', type=int,
                    choices=range(1, 48), nargs='?', const=2)
parser.add_argument('-s', '--save_images', help='save images to file?', type=bool)
parser.add_argument('-f', '--logfile_name', help='Provide name for output logfile', type=str)

args = parser.parse_args()

try:
    print('Press CTRL+C to quit')
    while True:
        sample = controls.Sample(args.sample_frequency, args.logfile_name)
        sample.sample_run()
except KeyboardInterrupt:
    pass
