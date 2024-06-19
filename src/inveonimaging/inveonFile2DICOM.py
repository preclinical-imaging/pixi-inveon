import subprocess
import argparse
from inveonimaging.inveon import InveonImage
from inveonimaging.factory import Factory

# Arguments:
#              Input Inveon .img file (with an appropriate .hdr file)
#              Output folder for DICOM files

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Inveon native .img/.hdr file to DICOM original")
    parser.add_argument("InveonImage",  help="Path to Inveon .img file")
    parser.add_argument("OutputFolder", help="Path to output folder for DICOM files")
    parser.add_argument('-f', '--file', help="Name of output file for multiframe output")
    parser.add_argument('-l', '--legacyconverted', action='store_true')
    parser.add_argument('-m', '--multiframe',      action='store_true')
    args = parser.parse_args()

    inveon_image = InveonImage("unknown", args.InveonImage).parse_header()
    factory = Factory()

    if (args.multiframe) :
        print("Multiframe")
        factory.convert_to_multiframe(inveon_image, args.OutputFolder, args.file)

    elif (args.legacyconverted):
        print ("Legacy Converted")
        factory.convert_to_legacy_converted_multiframe(inveon_image, args.OutputFolder, args.file)
    else:
        print ("Standard SOP classes, single frame")
        factory.convert_to_standard_images(inveon_image, args.OutputFolder)
