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
    help="Request the value every second", action
    ="store_true"
)

args = parser.parse_args()
karman = Karman(args.base_url)


def which():
    print("{}: {}".format(
        args.func_group_id,
        karman.which(args.user, args.func_group_id)
    ))

if args.continuous:
    while True:
        try:
            which()
            sleep(1)
        except KeyboardInterrupt:
            print('Bye')
            exit(0)
else:
    which()
