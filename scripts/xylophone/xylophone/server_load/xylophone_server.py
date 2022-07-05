#/usr/bin/env python

from xylophone.client import XyloClient
from xylonote_list import xylonote_list
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Partiture.txt')
parser.add_argument('-o', help='Xylophone ID')
args = parser.parse_args()



def main():
    xylo_list = xylonote_list(args.i)
    client = XyloClient(host=args.o, port = 8080)
    client.load(xylo_list)
    client.play()


if __name__ == '__main__':
    main()