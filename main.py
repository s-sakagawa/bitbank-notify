import sys

from src import PostNotify


def main(arg):
    notify = PostNotify()
    if arg == 'ticker':
        notify.send_ticker()
    elif arg == 'asset':
        notify.send_asset()
    elif arg == 'orders':
        notify.send_orders()
    else:
        raise Exception


if __name__ == '__main__':
    args = sys.argv
    try:
        if len(args) != 2:
            raise ValueError('Invalid length of arguments')
        if (args[1] != 'ticker') & (args[1] != 'asset') & (args[1] != 'orders'):
            raise ValueError('Invalid arguments, expected ["ticker", "asset", "orders"]')
    except ValueError as e:
        print(e)
    else:
        main(args[1])
