from backtest import backtest
import sys
import argparse

# NOTE: Realtime is not yet supported.

def main():
    parser = argparse.ArgumentParser(description='.')
    parser.add_argument("-b", "--backtest", help="specific ticker that will be plotted for, or use 'all' to backtest all data in folder datasets", action="store")
    parser.add_argument("-s", "--save", help="whether or not to save the figure", action="store_true")
    args = parser.parse_args()

    if(args.backtest != None):
        backtest(args.backtest, args.save)
    else:
        backtest()




if(__name__ == "__main__"):
    main()