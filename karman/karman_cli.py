import argparse
from time import sleep

from karman import Karman

parser = argparse.ArgumentParser(description='Request ablator functionality '
                                             'status from the command line.')

parser.add_argument("user", help="The user to request the feature")
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


def which(user):
    print("{}: {}".format(
        user,
        karman.which(user, args.func_group_id)
    ))

if args.continuous:
    count = 0
    while True:
        try:
            which(args.user+str(count))
            if args.slow:
                sleep(1)
            count += 1
        except KeyboardInterrupt:
            print('\nRequested {} functionalities'.format(count))
            exit(0)
else:
    which(args.user)
