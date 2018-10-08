#!/usr/bin/env python3
import argparse
import os
import sys


def subtract_minutes(minued_date_time, subtrahend_minutes):
    date_time_parts = minued_date_time.split('-')
    hours, minutes = int(date_time_parts[3]), int(date_time_parts[4])

    prev_minutes = minutes - subtrahend_minutes
    prev_hours = hours
    if prev_minutes < 0:
        prev_minutes = 60 + prev_minutes
        prev_hours -= 1

    residual_date_time = '{y}-{M}-{d}-{H}-{m}'.format(y=date_time_parts[0], M=date_time_parts[1], d=date_time_parts[2],
                                                      H=prev_hours, m=prev_minutes)
    return residual_date_time


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='N min aggregator')
    parser.add_argument('-i', help='input dir')
    parser.add_argument('-o', help='output dir')
    parser.add_argument('-t', help='datetime in `yyyy-MM-dd-HH-mm`')
    parser.add_argument('-d', type=int, help='interval length in minutes')
    parser.add_argument('-n', type=int, help='number of intervals')
    args = vars(parser.parse_args(sys.argv[1:]))

    date_time = args['t']
    date_time_intervals = [date_time]
    for i in range(1, args['n']):
        prev_date_time = subtract_minutes(date_time_intervals[i - 1], args['d'])
        date_time_intervals.append(prev_date_time)

    input_dirs = ['{dir}/{dt_prefix}'.format(dir=args['i'], dt_prefix=dt.replace('-', '/'))
                  for dt in date_time_intervals]

    for input_dir in input_dirs:
        if not os.path.exists(input_dir):
            raise Exception('Input path {} doesn`t exist'.format(input_dir))

    output_path = '{base_dir}/{dt_prefix}'.format(base_dir=args['o'], dt_prefix=date_time.replace('-', '/'))
    os.makedirs(output_path, exist_ok=True)
    with open('{output_path}/_SUCCESS'.format(output_path=output_path), 'a'):
        pass
