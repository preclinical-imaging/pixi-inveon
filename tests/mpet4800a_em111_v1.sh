#!/bin/sh

 BASE=`dirname $0`
 CODE_TABLE=$BASE/../src/codes/DICOM-CID-4020.json

 export PYTHONPATH=/opt/software-projects/XNAT/PIXI/Inveon-to-DICOM/pixi-inveon/src

 INPUT_FOLDER=/opt/datasets/SAI_WUSTL/Sample_Inveon_DICOM/test_1
 OUTPUT_FOLDER=/tmp/test_1/single_frame

 ARGS="-c CT- -p PET- --codetable $CODE_TABLE --patientname mpet4800a_em111_v1.pet --patientid mpet4800a_em111_v1.pet"
 rm -rf $OUTPUT_FOLDER

 echo python3 -m inveonimaging.inveonFolder2DICOM $ARGS $INPUT_FOLDER $OUTPUT_FOLDER
      python3 -m inveonimaging.inveonFolder2DICOM $ARGS $INPUT_FOLDER $OUTPUT_FOLDER

 echo ""


