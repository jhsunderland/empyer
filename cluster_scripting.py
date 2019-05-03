#!/usr/bin/python
import os
import glob
import re
import numpy as np
import empyer
import argparse



# This program is designed to take a diffraction signal, convert the signal to polar coordinates and then output
# the angular correlation and power spectrum.

"""
OPTIONS:
-d = cwd :directory
-f = cwd :output filename
-p : prismatic param file
-b = 2 : beamsize

"""


def correlation(signal_file):
    ds = empyer.load(signal_file, signal_type='diffraction_signal')
    file_name = os.path.splitext(signal_file)[0]
    ps = ds.calculate_polar_spectrum()
    ps.save(filename=file_name+'_polar.hdf5', overwrite=True)
    acs = ps.autocorrelation()
    acs.save(filename=file_name + '_angular.hdf5', overwrite=True)
    pow_s = acs.get_power_spectrum()
    pow_s.save(filename=file_name+'_angularPower.hdf5', overwrite=True)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d",
                        "--directory",
                        type=str,
                        help="input directory")
    args = parser.parse_args()

    if not args.directory:
        args.directory = os.getcwd()
    if os.path.isdir(args.directory):
        files = glob.glob(args.directory+"/*.hdf5")
    else:
        files = [args.directory]
    print(files)

    for f in files:
        correlation(f)
