import os
import argparse
from inveonimaging.inveon import InveonImage
from inveonimaging.factory import Factory


def find_img_files(input_folder: str, ignore_all_extra_files: bool, ignore_specific_extra_files: list):
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
                raiseException = True
                ignore_specific_extra_files_msg = ""
                if (ignore_specific_extra_files):
                    ignore_specific_extra_files_msg = ", ".join(ignore_specific_extra_files)
                    if file_extension in ignore_specific_extra_files:
                        raiseException = False
                if ignore_all_extra_files:
                    raiseException = False
                if (raiseException):                
                    raise Exception(
                        f"File {full_path} found with file extension {file_extension}. This program expects only {ignore_specific_extra_files_msg} .img and .hdr  files in the folder")
        else:
            raise Exception(f"This program does not support nested folders {full_path}")

    return rtn

def construct_overrides(my_parser:argparse.Namespace) -> {}:
    overrides = {}
    overrides["patient_name"] = my_parser.patient_name
    overrides["patient_id"]   = my_parser.patient_id
    overrides["patient_birthdate"] = my_parser.patient_birthdate
    overrides["patient_sex"] = my_parser.patient_sex

    return overrides

# Arguments:
#              Input Inveon .img file (with an appropriate .hdr file)
#              Output folder for DICOM files

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Inveon native .img/.hdr file to DICOM original")
    parser.add_argument("InveonFolder",                                      help="Path to Inveon .hdr/.img file(s)")
    parser.add_argument("OutputFolder",                                      help="Path to output folder for DICOM files")
    parser.add_argument('-C', '--codetable',        dest='code_table',       help="JSON file with code table")
    parser.add_argument('-c', '--ct',               dest='ct_prefix',        help="Prefix for a CT file")
    parser.add_argument('-p', '--pet',              dest='pet_prefix',       help="Prefix for a PET file")
    parser.add_argument('-f', '--file',                                      help="Name of output file for multiframe output")
    parser.add_argument('-l', '--legacyconverted', action='store_true')
    parser.add_argument('-m', '--multiframe',      action='store_true')
    parser.add_argument('-s', '--studydescription', dest='study_description', help="Set DICOM StudyDescription")
    parser.add_argument(      '--patientname',      dest='patient_name',      help="Set DICOM PatientName")
    parser.add_argument(      '--patientid',        dest='patient_id',        help="Set DICOM PatientID")
    parser.add_argument(      '--patientdob',       dest='patient_birthdate', help="Set DICOM PatientBirthDate")
    parser.add_argument(      '--patientsex',       dest='patient_sex',       help="Set DICOM PatientSex")
    parser.add_argument(      '--ignoreAllExtraFiles', action='store_true', dest='ignore_all_extra_files',       help="Ignore presence of all files with extension other than .img and .hdr")
    parser.add_argument(      '--ignoreFileWithExt',  action='append', dest='ignore_specific_extra_files',       help="Ignore presence of files with specific extension other than .img and .hdr")

    args = parser.parse_args()
    overrides = construct_overrides(args)

    factory = Factory()
    if (args.code_table is not None):
        factory.import_code_table_file(args.code_table)

    factory.generate_study_instance_uid()
    factory.add_file_prefix("CT",  args.ct_prefix)
    factory.add_file_prefix("PT",  args.pet_prefix)


    study_description = None
    if (args.study_description is not None):
        study_description = args.study_description

    img_files = find_img_files(args.InveonFolder, args.ignore_all_extra_files, args.ignore_specific_extra_files)
    for f in img_files:
        series_number = factory.get_series_number()

        inveon_image: InveonImage = InveonImage(study_description, f).parse_header()
        output_folder: str = os.path.join(args.OutputFolder, str(series_number), "DICOM")
        if (args.multiframe) :
#            print(f"Multiframe {f} {output_folder}")
            factory.convert_to_multiframe(inveon_image, output_folder, args.file)
        
        elif (args.legacyconverted):
#            print (f"Legacy Converted {f} {output_folder}")
            factory.convert_to_legacy_converted_multiframe(inveon_image, output_folder, args.file)
        else:
#            print (f"Standard SOP classes, single frame {f} {output_folder}")
            factory.convert_to_standard_images(inveon_image, overrides, output_folder)
        
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




