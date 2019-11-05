""" Computing configuration representation """

from __future__ import division, print_function
import argparse
import logmuse
import logging
import os
import sys
import pandas as pd
import numpy as np
import random
from _version import __version__

_LOGGER = logging.getLogger(__name__)


chroms = ['chr'+str(num) for num in list(range(1, 23)) + ['X', 'Y']]
chrom_lens = [247249719, 242951149, 199501827, 191273063, 180857866, 170899992, 158821424, 146274826, 140273252, 135374737, 134452384, 132349534, 114142980, 106368585, 100338915, 88827254, 78774742, 76117153, 63811651, 62435964, 46944323, 49691432, 154913754, 57772954]


class _VersionInHelpParser(argparse.ArgumentParser):
    def format_help(self):
        """ Add version information to help text. """
        return "version: {}\n".format(__version__) + \
               super(_VersionInHelpParser, self).format_help()


def build_argparser():
    """
    Builds argument parser.

    :return argparse.ArgumentParser
    """

    banner = "%(prog)s - randomize BED files"
    additional_description = "\n..."

    parser = _VersionInHelpParser(
            description=banner,
            epilog=additional_description)

    parser.add_argument(
            "-V", "--version",
            action="version",
            version="%(prog)s {v}".format(v=__version__))

    parser.add_argument(
            "-b", "--bedfile", required=True,
            help="File path to bed file.")

    parser.add_argument(
            "-d", "--droprate", type=float, default=0.0,
            help="Droprate parameter")

    parser.add_argument(
            "-a", "--addrate", type=float, default=0.0,
            help="Addrate parameter")

    parser.add_argument(
            "--addmean", type=float, default=320.0,
            help="Mean add region length")

    parser.add_argument(
            "--addstdev", type=float, default=30.0,
            help="Stdev add length")

    parser.add_argument(
            "-p", "--shiftrate", type=float, default=0.0,
            help="Shift prob.")

    parser.add_argument(
            "--shiftmean", type=float, default=0.0,
            help="Mean shift")

    parser.add_argument(
            "--shiftstdev", type=float, default=150.0,
            help="Stdev shift")

    parser.add_argument(
            "-c", "--cutrate", type=float, default=0.0,
            help="Cut prob.")

    parser.add_argument(
            "-m", "--mergerate", type=float, default=0.0,
            help="Merge prob. WARNING: will likely create regions that are thousands of base pairs long")

    parser.add_argument(
            "-o", "--outputfile", type=str,
            help="output file name (including extension). if not specified, will default to bedshifted_{originalname}.bed")


    return parser


class Bedshift(object):

    def readDF(self, bedfile_path):
        df = pd.read_csv(bedfile_path, sep='\t', header=None, usecols=[0,1,2])
        df[3] = 0 # column indicating which modifications were made
        return df.sort_values([0, 1]).reset_index(drop=True)


    def check_rate(self, rates):
        for rate in rates:
            if rate < 0 or rate > 1:
                _LOGGER.error("Rate must be between 0 and 1")
                sys.exit(1)


    def __shift(self, df, row, mean, stdev):
        theshift = int(np.random.normal(mean, stdev))

        start = df.loc[row][1]
        end = df.loc[row][2]

        df.at[row, 1] = start + theshift
        df.at[row, 2] = end + theshift
        df.at[row, 3] = 1.0

        return df


    def __drop(self, df, row):
        return df.drop(row)


    def __cut(self, df, row):
        chrom = df.loc[row][0]
        start = df.loc[row][1]
        end = df.loc[row][2]

        if end-start < 0:
            _LOGGER.error('ERROR: the end value of a region is less than the start value')
            sys.exit(1)
        thecut = int(np.random.normal((start+end)/2, (end - start)/6))
        if thecut <= start:
            thecut = start + 10
        if thecut >= end:
            thecut = end - 10

        new_segs = pd.DataFrame([[chrom, start, thecut, 2.0], [chrom, thecut, end, 2.0]])
        ''' may add in later, this makes the api confusing!
        # adjust the cut regions using the shift function
        new_segs = self.__shift(new_segs, 0, meanshift, stdevshift)
        new_segs = self.__shift(new_segs, 1, meanshift, stdevshift)
        '''
        new_segs[3] = 2.0
        df.loc[row] = new_segs.loc[0]
        return df.append(new_segs.loc[1], ignore_index=True)


    def __add(self, df, mean, stdev):
        chrom_index = random.randrange(len(chroms))
        chrom_num = chroms[chrom_index]
        start = random.randint(1, chrom_lens[chrom_index])
        end = min(start + max(int(np.random.normal(mean, stdev)), 20), chrom_lens[chrom_index])
        return df.append(pd.DataFrame([[chrom_num, start, end, 3.0]]), ignore_index=True)


    def __merge(self, df, row):
        # check if the regions being merged are on the same chromosome
        if row + 1 not in df.index or df.loc[row][0] != df.loc[row+1][0]:
            return df

        chrom = df.loc[row][0]
        start = df.loc[row][1]
        end = df.loc[row+1][2]
        df = self.__drop(df, row)
        df.loc[row+1] = [chrom, start, end, 4.0]
        return df


    def add(self, df, addrate, addmean, addstdev):
        self.check_rate([addrate])
        rows = df.shape[0]
        for _ in range(rows):
            if random.random() < addrate:
                df = self.__add(df, addmean, addstdev) # added rows display a 3
        return df


    def shift(self, df, shiftrate, shiftmean, shiftstdev):
        self.check_rate([shiftrate])
        rows = df.shape[0]
        for i in range(rows):
            if random.random() < shiftrate:
                df = self.__shift(df, i, shiftmean, shiftstdev) # shifted rows display a 1
        return df


    def cut(self, df, cutrate):
        self.check_rate([cutrate])
        rows = df.shape[0]
        for i in range(rows):
            if random.random() < cutrate:
                df = self.__cut(df, i) # cut rows display a 2
        return df.reset_index(drop=True)


    def merge(self, df, mergerate):
        self.check_rate([mergerate])
        rows = df.shape[0]
        i = 0
        while i < rows:
            if random.random() < mergerate:
                df = self.__merge(df, i) # merged rows display a 4
                i += 1
            i += 1
        return df.reset_index(drop=True)


    def drop(self, df, droprate):
        self.check_rate([droprate])
        rows = df.shape[0]
        for i in range(rows):
            if random.random() < droprate:
                df = self.__drop(df, i)
        return df


    def all_perturbations(self, df, addrate=0.0, addmean=320.0, addstdev=30.0, shiftrate=0.0, shiftmean=0.0, shiftstdev=150.0, cutrate=0.0, mergerate=0.0, droprate=0.0):
        self.check_rate([addrate, shiftrate, cutrate, mergerate, droprate])
        df = self.add(df, addrate, addmean, addstdev)
        df = self.shift(df, shiftrate, shiftmean, shiftstdev)
        df = self.cut(df, cutrate)
        df = self.merge(df, mergerate)
        df = self.drop(df, droprate)
        return df


    def write_csv(self, df, outfile_name):
        df.to_csv(outfile_name, sep='\t', header=False, index=False)




def main():
    """ Primary workflow """

    parser = logmuse.add_logging_options(build_argparser())
    args, remaining_args = parser.parse_known_args()
    global _LOGGER
    _LOGGER = logmuse.logger_via_cli(args)

    _LOGGER.info("welcome to bedshift")
    _LOGGER.info("Shifting file: '{}'".format(args.bedfile))
    msg = """Params:
                drop rate: {droprate}
                add rate: {addrate}
                add mean length: {addmean}
                add stdev: {addstdev}
                shift rate: {shiftrate}
                shift mean distance: {shiftmean}
                shift stdev: {shiftstdev}
                cut rate: {cutrate}
                merge rate: {mergerate}
                outputfile: {outputfile}
            """

    outfile = 'bedshifted_{}'.format(os.path.basename(args.bedfile)) if not args.outputfile else args.outputfile

    _LOGGER.info(msg.format(
        droprate=args.droprate,
        addrate=args.addrate,
        addmean=args.addmean,
        addstdev=args.addstdev,
        shiftrate=args.shiftrate,
        shiftmean=args.shiftmean,
        shiftstdev=args.shiftstdev,
        cutrate=args.cutrate,
        mergerate=args.mergerate,
        outputfile=args.outputfile))

    if not args.bedfile:
        parser.print_help()
        _LOGGER.error("No bedfile given")
        sys.exit(1)


    bedshifter = Bedshift()
    bedshifter.check_rate([args.addrate, args.shiftrate, args.cutrate, args.mergerate, args.droprate])

    df = bedshifter.readDF(args.bedfile)
    original_rows = df.shape[0]
    df = bedshifter.all_perturbations(df, args.addrate, args.addmean, args.addstdev, args.shiftrate, args.shiftmean, args.shiftstdev, args.cutrate, args.mergerate, args.droprate)

    _LOGGER.info('The output bedfile located in {} has {} lines. The original bedfile had {} lines.'.format(outfile, df.shape[0], original_rows))

    bedshifter.write_csv(df, outfile)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        _LOGGER.error("Program canceled by user!")
        sys.exit(1)


