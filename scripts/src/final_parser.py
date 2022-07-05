import argparse
import instrument

parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, help='Instrument.txt')
parser.add_argument('-p', type=str, help='Partiture.txt')
parser.add_argument('-ff', type=int, help='Frequency')
parser.add_argument ('-o', type=str, help= 'Output .wav')
args = parser.parse_args()

def main():
    instrument_ = instrument.Instrument(args.f, args.p, args.ff, args.o)
    instrument_.audio_wav()

if __name__ == '__main__':
    main()
