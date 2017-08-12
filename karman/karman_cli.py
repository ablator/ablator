import argparse
from time import sleep

from karman import Karman

parser = argparse.ArgumentParser(description='Request ablator functionality '
                                             'status from the command line.')

parser.add_argument("user", help="The user to request the functionality")
parser.add_argument("func_group_id", help="The functionality group to query")


parser.add_argument("--base_url", help="Where is the server?", default="http://localhost:8000/")
parser.add_argument(
    "-c", "--continuous",
    help="Request the value again and again", action
    ="store_true"
)
parser.add_argument(
    "-s", "--slow",
    help="Request the value every second", action
    ="store_true"
)

args = parser.parse_args()
karman = Karman(args.base_url)


if args.continuous:
    count = 0
    enabled_count = 0
    times = []
    while True:
        try:
            username = args.user + str(count)
            availability, elapsed_time = karman.which(
                username,
                args.func_group_id,
                return_statistics=True
            )
            print('{:06.5f} {:>16} {}'.format(elapsed_time, username, availability))
            if args.slow:
                sleep(1)

            # Statistics
            count += 1
            times.append(elapsed_time)
            if availability:
                enabled_count += 1
        except KeyboardInterrupt:
            average_response_time = sum(times) / float(len(times))
            result_string = '\nRequested {} functionalities, {} enabled. Avg time: {:f} seconds'
            print(result_string.format(count, enabled_count, average_response_time))
            exit(0)
else:
    availability = karman.which(args.user, args.func_group_id)
    print('User: {}'.format(args.user))
    print('Functionality Group: {}'.format(args.func_group_id))
    if availability and availability[0]:
        print('{}: {}'.format(availability))
    else:
        print('No availability for that user')
