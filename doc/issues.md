# Known issues to be resolved

## factory.py
1. PET: Units are hard-coded as BQML
1. PET: CountSource is hardcoded as EMISSION
1. PET: Determine CollimatorType from Inveon header
1. PET: DecayCorrection, need to distinguish between START and ADMIN
1. PET: CorrectedImage, need to review
1. PET: PatientGantryRelationship is hard coded
1. PET: ImageType is hard coded in create_pet_image_module
1. PET: RescaleIntercept and RescaleSlope are hard coded in create_pet_image_module
1. PET: ImageType is hard coded in create_enhanced_pet_image_module
1. PET: AcquisitionDuration is hard coded in create_enhanced_pet_image_module
1. PET: Other hard coded values in create_enhanced_pet_image_module
1. CT: create_enhanced_ct_image_module is not complete
1. create_patient_module uses "" for patient_name, patient_id, patient_dob, patient_sex
1. create_image_pixel_module makes many assumptions about pixel configuration
1. create_image_pixel_module assumes input data are 2-byte integers, ignores floats

## dicom.py
1. fill_pixel_measures_sequence has hard coded values
1. fill_frame_content_sequence has hard coded values
1. fill_unassigned_per_frame_converted_attributes_sequence hars hard coded values
1. fill_pixel_measures_sequence has hard coded values
1. fill_frame_content_sequence has hard coded values
1. fill_unassigned_per_frame_converted_attributes_sequence has hard coded values
1. fill_ct_image_frame_type_sequence has hard coded values
1. fill_pet_frame_type_sequence has hard coded values
1. fill_plane_orientation_sequence has hard coded values
1. fill_plane_position_sequence has hard coded values and has a weird way of creating an empty Dataset
1. MultiframeDimensionModule constructor has hard coded values
1. Change all consructors that compute ImageType to take a single string. Let the factory figure this out.
1. EnhancedCTImageModule constructor needs work



## General
1. Need a review of String / Integer variables. We are inconsistent in usage
1. Need a way to add subject information (Name, ID, DOB, Sex) from the command line
1. Standard CT and PET need minor review. The enhanced and legacy enhanced images need major review.
1. Bonus points for handling multi-subject data per the DICOM Standard
1. Review the name of the package. The Github project is pixi-inveon, and that matches other PIXI software. We have a package name that is inveondicom.
1. No provision yet for handling NM images as opposed to PET
1. Need a review of how slice location is calculated.