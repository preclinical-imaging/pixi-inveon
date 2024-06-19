import os
import argparse
from inveonimaging.inveon import InveonImage
from inveonimaging.factory import Factory


def find_img_files(input_folder: str):
    rtn = []
    for f in os.listdir(input_folder):
        full_path = os.path.join(input_folder, f)
        if os.path.isfile(full_path):
            filename, file_extension = os.path.splitext(full_path)
            if (file_extension == ".img"):
                rtn.append(full_path)
                expected_hdr_file = f"{full_path}.hdr"
                if not os.path.isfile(expected_hdr_file):
                    raise Exception(f"We found this .img file {full_path} with no corresponding .hdr file")

            elif (file_extension == ".hdr"):
                expected_img_file = filename
                if not os.path.isfile(expected_img_file):
                    raise Exception(f"We found this .hdr file {full_path} with no corresponding .img file")

            else:
                raise Exception(
                    f"File {full_path} found with file extension {file_extension}. This program expects only .img and .hdr files in the folder")
        else:
            raise Exception(f"This program does not support nested folders {full_path}")

    return rtn


# Arguments:
#              Input Inveon .img file (with an appropriate .hdr file)
#              Output folder for DICOM files

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Inveon native .img/.hdr file to DICOM original")
    parser.add_argument("InveonFolder",                     help="Path to Inveon .hdr/.img file(s)")
    parser.add_argument("OutputFolder",                     help="Path to output folder for DICOM files")
    parser.add_argument('-c', '--ct',    dest='ct_prefix',  help="Prefix for a CT file")
    parser.add_argument('-p', '--pet',   dest='pet_prefix', help="Prefix for a PET file")
    parser.add_argument('-f', '--file',                     help="Name of output file for multiframe output")
    parser.add_argument('-l', '--legacyconverted', action='store_true')
    parser.add_argument('-m', '--multiframe',      action='store_true')
    args = parser.parse_args()

    factory = Factory()
    factory.generate_study_instance_uid()
    factory.add_file_prefix("CT",  args.ct_prefix)
    factory.add_file_prefix("PxT",  args.pet_prefix)

    img_files = find_img_files(args.InveonFolder)
    for f in img_files:
        series_number = factory.get_series_number()

        inveon_image: InveonImage = InveonImage("unknown", f).parse_header()
        output_folder: str = os.path.join(args.OutputFolder, str(series_number))
        if (args.multiframe) :
            print(f"Multiframe {f} {output_folder}")
            factory.convert_to_multiframe(inveon_image, output_folder, args.file)
        
        elif (args.legacyconverted):
            print (f"Legacy Converted {f} {output_folder}")
            factory.convert_to_legacy_converted_multiframe(inveon_image, output_folder, args.file)
        else:
            print (f"Standard SOP classes, single frame {f} {output_folder}")
            factory.convert_to_standard_images(inveon_image, output_folder)
        
        factory.increment_series_number()

#    if (args.multiframe) :
#        print("Multiframe")
#        factory.convert_to_multiframe(inveon_image, args.OutputFolder, args.file)
#
#    elif (args.legacyconverted):
#        print ("Legacy Converted")
#        factory.convert_to_legacy_converted_multiframe(inveon_image, args.OutputFolder, args.file)
#    else:
#        print ("Standard SOP classes, single frame")
#        factory.convert_to_standard_images(inveon_image, args.OutputFolder)




