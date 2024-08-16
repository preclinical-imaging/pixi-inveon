# Specifications for Inveon to DICOM Conversion

## Items Not Addressed.
1. Siemens documentation indicates they produce NM images, but we do not know how to identify/distinguish NM from PET data.

1. CT: Will not support Multi-Energy CT.

1. PET: Will not support gated studies.

1. PET and CT: Will not syncrhonize the x,y,z positions and use a common Frame of Reference between the series.

## Open Issues (Priority Order)
### Larger Issues

1. PET: Need to translate float pixel values to 16 bit integers for DICOM.
   - Method is under review by Richard Laforest

1. CT, PET: Image Orientation (Patient) (0020,0037) is defined as: *The direction cosines of the first row and the first column with respect to the patient. *. This should be mapped from subject_orientation. I do not know the mapping.

1. CT, PET: Image Position (Patient) (0020,0032) contains the X,Y,Z position of a plane. With help from Richard Laforest, we empirically derived the equations for these three values. This is described below. This could use review, especially in the context of different orientations of the mouse subjects. We especially need to review why we had to reverse the sign on the x and y position calculations.

1. PET: Inveon header has values for isotope and injected_compound. We are using isotope to create a coded entry in the Radionuclide Code Sequence. How should we use injected_compound?

1. CT: Do we want to add the Siemens private data for CT? It is described in their Conformance Statement.

1. CT: Do we want to add the Siemens private data for PET? It is described in their Conformance Statement.

### Smaller Issues
1. PET: Decay Correction (0054,1102) can take on the values NONE, START, ADMIN. What is in the Inveon header that map to the correct values?

1. PET: Is decay_correction the right value to use for DICOM Decay Factor (0054,1321)?

1. PET: The mapping table from isotope to the code value in Radionuclide Code Sequence needs to be completed. This one mapping exists:
   - F-18 --> (C-111A1, SNM3, ^18^Fluorine)
   - See [CID 4020 PET Radionuclide](https://dicom.nema.org/medical/dicom/current/output/html/part16.html#sect_CID_4020) for the list of coded values. We do not know the values that can be entered in the scanner for isotope.

1. CT, PET: Some code exists for Enhanced CT and Enhanced PET. That should be removed, and we should focus on traditional CT and PET images.

1. PET Review the computed value for Image Index (0054,1330)

1. CT, PET: Review how the values for Image Type (0008,0008) are determined.

1. CT, PET: Current software accepts Patient/Subject Name, ID, DOB, Sex from command line. These values are available in the header, but is there a standard format so we can populate the DICOM header properly
   - subject_date_of_birth
   - subject_sex
   - subject_identifier
   - subject_genus
   - subject_phenotype

1. CT, PET: Patient Study Module. Nothing is included today.
  - What is the format of subject_age so we can place this in the DICOM metadata?
  - Do we want to map subject_length into the DICOM metadata (Patient's Size 0010,1020)
  - Do we want to map subject_weight into the DICOM metadata (Patient's Weight 0010,1030)



## Common to All Modalities
The modules below are common to CT and PET and are listed separately to avoid duplication.

### Patient
| Attribute Name        | Tag         | Conversion         |
|-----------------------|-------------|--------------------|
| Patient's Name        | (0010,0010) | From command line  |
| Patient ID            | (0010,0020) | From command line  |
| Patient's Birth Date  | (0010,0030) | From command line  |
| Patient's Sex         | (0010,0040) | From command line  |

Notes:
1. We are not supporting multi-animal DICOM files (hotel sessions)
2. We chose to accept the four demographic fields from the command line. We could grab one or more values from the Inveon header and maintain command line overrides.
3. These fields are listed in the sample Inveon header files we have. We do not know if any format conversions are necessary.
   - subject_date_of_birth
   - subject_sex
   - subject_identifier
   - subject_genus

TODO:
1. Review what demographic fields could be pulled from the Inveon header
2. As part of the review, determine if any format conversions are needed to satisfy the DICOM Standard.

### Clinical Trial Subject
 - None

### General Study
| Attribute Name             | Tag         | Conversion                             |
|----------------------------|-------------|----------------------------------------|
| Study Instance UID         | (0020,000D) | generated                              |
| Study Date                 | (0008,0020) | from scan_time_date                    |
| Study Time                 | (0008,0030) | from scan_time_date                    |
| Referring Physician's Name | (0008,0090) | investigator                           |
| Study ID                   | (0020,0010) | study_identifier (first 16 characters) |
| Accession Number           | (0008,0050) | ""                                     |
| Study Description          | (0008,1030) | study                                  |

### Patient Study
Consider:
 - Patient's Age
 - Patient's Weight
 - Patient's Size

### Clinical Trial Study
 - None

### General Series
| Attribute Name        | Tag         | Conversion                                |
|-----------------------|-------------|-------------------------------------------|
| Modality              | (0008,0060) | from modality, see table below            |
| Series Instance UID   | (0020,000E) | generated                                 |
| Series Number         | (0020,0011) | increments from 1                         |
| Laterality            | (0020,0060) | ""                                        |
| Series Date           | (0008,0021) | from scan_time_date                       |
| Series Time           | (0008,0031) | from scan_time_date                       |
| Series Description    | (0008,103E) | from acquisition mode, see table below    |
| Patient Position      | (0018,5100) | from subject_orientation, see table below |
| Operators' Name       | (0008,1070) | operator                                  |

Mapping table from Inveon values to DICOM values
| Keyword                | Value | Mapped Value                                      |
|------------------------|-------|---------------------------------------------------|
| modality               |    0  | PT                                                |
| modality               |    1  | CT                                                |
| acquisition_mode       |    0  | Unknown acquisition mode                          |
| acquisition_mode       |    1  | Blank acquisition                                 |
| acquisition_mode       |    2  | Emission acquisition                              |
| acquisition_mode       |    3  | Dynamic acquisition                               |
| acquisition_mode       |    4  | Gated acquisition                                 |
| acquisition_mode       |    5  | Continuous bed motion acquisition                 |
| acquisition_mode       |    6  | Singles transmission acquisition                  |
| acquisition_mode       |    7  | Windowed coincidence transmission acquisition     |
| acquisition_mode       |    8  | Non-windowed coincidence transmission acquisition |
| acquisition_mode       |    9  | CT projection acquisition                         |
| acquisition_mode       |   10  | CT calibration acquisition                        |
| acquisition_mode       |   11  | SPECT planar projection acquisitio                |
| acquisition_mode       |   12  | SPECT multi-projection acquisition                |
| acquisition_mode       |   13  | SPECT calibration acquisition                     |
| acquisition_mode       |   14  | SPECT tomography normalization acquisition        |
| acquisition_mode       |   15  | SPECT detector setup acquisition                  |
| acquisition_mode       |   16  | SPECT scout view acquisition                      |
| acquisition_mode       |   17  | SPECT planar normalization acquisition            |
| subject_orientation    |    0  | ""                                                |
| subject_orientation    |    1  | FFP                                               |
| subject_orientation    |    2  | HFP                                               |
| subject_orientation    |    3  | FFS                                               |
| subject_orientation    |    4  | HFS                                               |
| subject_orientation    |    5  | FFDR                                              |
| subject_orientation    |    6  | HFDR                                              |
| subject_orientation    |    7  | FFDL                                              |
| subject_orientation    |    8  | HFDL                                              |



### Clinical Trial Series
 - None

### Frame of Reference

| Attribute Name               | Tag         | Conversion                      |
|------------------------------|-------------|---------------------------------|
| Frame of Reference UID       | (0020,0052) | generated (see Note below)      |
| Position Reference Indicator | (0020,1040) | ""                              |

Note: We generate seprate Frame of Reference UIDs for CT and PET series. There is no attempt to harmonize the Frames of Reference.

### Synchronization
 - None

### General Equipment

| Attribute Name               | Tag         | Conversion                                       |
|------------------------------|-------------|--------------------------------------------------|
| Manufacturer                 | (0008,0070) | from manufacturer, else "Siemens"                |
| Institution Name             | (0008,0080) | from institution                                 |
| Software Versions            | (0018,1020) | from version and recon_version                   |
| Manufacturer's Model Name    | (0008,1090) | from model and modality configuration. see below |

The value for Manufacturer's Model Name is of the form model:modality_configuration per the following mapping table:

| Keyword                | Value | Mapped Value         |
|------------------------|-------|----------------------|
| model                  |    0  | unknown              |
| model                  | 2000  | Primate              |
| model                  | 2001  | Rodent               |
| model                  | 2002  | microPET2            |
| model                  | 2500  | Focus_220            |
| model                  | 2501  | Focus_120            |
| model                  | 3000  | mCAT                 |
| model                  | 3500  | mCATII               |
| model                  | 4000  | mSPECT               |
| model                  | 5000  | Inveon_Dedicated_PET |
| model                  | 5001  | Inveon_MM_Platform   |
| model                  | 6000  | MR_PET_Head_Insert   |
| model                  | 8000  | Tuebingen_PET_MR     |
| modality_configuration |    0 | Unknown                 |
| modality_configuration | 3000 | mCAT                    |
| modality_configuration | 3500 | mCATII                  |
| modality_configuration | 3600 | Inveon_MM_Std_CT        |
| modality_configuration | 3601 | Inveon_MM_HiRes_Std_CT  |
| modality_configuration | 3602 | Inveon_MM_Std_LFOV_CT   |
| modality_configuration | 3603 | Inveon_MM_HiRes_LFOV_CT |
| modality_configuration | 2000 | Primate                 |
| modality_configuration | 2001 | Rodent                  |
| modality_configuration | 2002 | microPET2               |
| modality_configuration | 2500 | Focus_220               |
| modality_configuration | 2501 | Focus_120               |
| modality_configuration | 5000 | Inveon_Dedicated_PET    |
| modality_configuration | 5500 | Inveon_MM_PET           |

For example: Inveon_MM_Platform:Inveon_MM_PET

### General Acquisition
| Attribute Name               | Tag         | Conversion                    |
|------------------------------|-------------|-------------------------------|
| Acquisition Date             | (0008,0022) | from scan_time_date           |
| Acquisition Time             | (0008,0032) | from scan_time_date           |

### General Image
| Attribute Name               | Tag         | Conversion                    |
|------------------------------|-------------|-------------------------------|
| Instance Number              | (0020,0013) | increments from 1             |
| Image Comments               | (0020,4000) | from x_filter, y_filter, z_filter. See below |

The Image Comments element is created by combining values for x_filter, y_filter and z_filter. Up to three values are concatenated according to the values for x_filter, y_filter and z_filter from the Inveon header.

| Filter index | Description                               |
|--------------|-------------------------------------------|
|       0      | No filter                                 |
|       1      | Ramp filter (backprojection) or no filter |
|       2      | First-order Butterworth window            |
|       3      | Hanning window                            |
|       4      | Hamming window                            |
|       5      | Parzen window                             |
|       6      | Shepp filter                              |
|       7      | Second-order Butterworth window           |

### General Reference
 - None

 ### Image Plane
| Attribute Name              | Tag         | Conversion                              |
|-----------------------------|-------------|-----------------------------------------|
| Pixel Spacing               | (0028,0030) | from pixel_size_x and pixel_size_y      |
| Image Orientation (Patient) | (0020,0037) | from subject_orientation. See below.    |
| Image Position (Patient)    | (0020,0032) | see below                               |
| Slice Thickness             | (0018,0050) | pixel_size_z                            |
| Slice Location              | (0020,1041) | Z component of Image Position (Patient) |

Mapping Inveon subject_orientation to DICOM Image Orientation Patient
| subject_orientation              | DICOM Image Orientation Patient |
|----------------------------------|---------------------------------|
| 0 - Unknown subject orientation  | ""                              |
| 1 - Feet first, prone            |                                 |
| 2 - Head first, prone            |                                 |
| 3 - Feet first, supine           | -1\0\0\0\1\0                    |
| 4 - Head first, supine           |                                 |
| 5 - Feet first, right            |                                 |
| 6 - Head first, right            |                                 |
| 7 - Feet first, left             |                                 |
| 8 - Head first, left             |                                 |

TODO: Review the values for DICOM Subject Orientation and how they relate to Inveon subject_orientation.

####  Calculating X, Y, Z positions of the image plane
   - Variables below
      - $var refers to a local variable
      - {variable} refer to named variables of the same name in the Inveon header file. We take one liberty (next item)
   - The value image_ref_shift is defined as "Image reference shift (X, Y, Z), in mm, applied to data set (float float float)". In the notation below, we will use image_ref_shift(x) to indicate the shift in the x position with similar notation for y and z.
   - All calculations are in mm
   - These are the names of the variables we use from the Inveon header
      - image_ref_shift
      - pixel_size_x, pixel_size_y, pixel_size_z
      - x_dimension, y_dimension, z_dimension
   - See note after the equations about open issues

    $x_delta = {image_shift_ref(x)}
    $y_delta = {image_shift_ref(y)}
    $y_delta = {image_shift_ref(y)}
    
    $x_position =    (({x_dimension}/2-1) / 2 * {pixel_size_x}) - x_delta
    $y_position =  -((({y_dimension}/2-1) / 2 * {pixel_size_y}) - y_delta)

    $index: Ranges from 0 to number of slices - 1
    $z_position = (($index + .5 - z_dimension/2) * pixel_size_z) + z_delta

Notes on x, y, z positions
1. Equations for determining x, y, z positions were developed empirically and then compared to output produced by the Inveon workstation.
2. Equations do not take into consider any orientation information (HFS, FFS, etc.) that is found in the header information.
3. We especially need to review why we had to reverse the sign on the x and y position calculations.


### Image Pixel

| Attribute Name              | Tag         | Conversion         |
|-----------------------------|-------------|--------------------|
| Samples per Pixel           | (0028,0002) |      1             |
| Photometric Interpretation  | (0028,0004) | MONOCHROME2        |
| Rows                        | (0028,0010) | y_dimension        |
| Columns                     | (0028,0011) | x_dimension        |
| Bits Allocated              | (0028,0100) |     16  (1)        |
| Bits Stored                 | (0028,0101) |     16             |
| High Bit                    | (0028,0102) |     15             |
| Pixel Representation        | (0028,0103) |      1  (2)        |
| Pixel Data                  | (7FE0,0010) | from .img file (3) |

Notes:
1. All pixels converted to 16 bit integers if not already in that format. For example, floating point values are converted.
2. Pixel Representation is 2's complement
3. See calculations below

#### Image Pixel Calculations
The header variable data_type defines the format of the pixel data in the .img file. The software derives the pixel data as follows:

    switch data_type:
      case 2:     // 2-byte integer - Intel style
        read/return 2 byte integers as they exist in the file

      case 4:    // 4-byte float - Intel style
        convert float to integer; see below

      all others: (0, 1 3, 5, 6 7)
        raise exception

This describes the conversion of floating point data to 2-byte integers. We assume that we only get 4-byte float inputs for PET data. That assumption needs to be reviews.

Variables below
   - $var refers to a local variable
   - {variable} refer to named variables of the same name in the Inveon header file.
   - These are the names of the variables we use from the Inveon header
      - x_dimension, y_dimension
      - scale_factor
      - calibraton_factor
      - isotope_branching_fraction
      - maximum (conditioned on the time frame you are in)

    $max_scaled = {maximum} * {calibration_factor} * {scale_factor} / {isotope_branching_fraction} * 37
    $pixel_scale = {calibration_factor} * {scale_factor} / {isotope_branching_fraction} * 37 * (32767 / {max_scaled})
    $float_pixels = array of floating point pixel values

    for $i = 0 to float_pixels.lengh - 1:
      $int_pixel[$i] = $float_pixel[$i] * $pixel_scale
    done
    return $int_pixel (array of integer pixels)


### Device
 - None

### Specimen
 - None

### SOP Common
| Attribute Name       | Tag         | Conversion              |
|----------------------|-------------|-------------------------|
| SOP Class UID        | (0008,0016) | see table below         |
| SOP Instance UID     | (0008,0018) | generated per image     |

Table of supported SOP Class UIDs:
| SOP Class UID                 | Storage SOP Class Name        |
|-------------------------------|-------------------------------|
| 1.2.840.10008.5.1.4.1.1.128   | PET                           |
| 1.2.840.10008.5.1.4.1.1.2     | CT                            |


### Overlay Plane
 - None

### VOI LUT
 - TODO

### Common Instance Reference
 - None


## CT Image

See *Common to All Modalities* section for items not specific to CT. These modules are described above:

| DICOM IE           | Module                    | Usage |
|--------------------|---------------------------|-------|
| Patient            | Patient                   |   M   |
| Patient            | Clinical Trial Subject    |   U   |
| Study              | General Study             |   M   |
| Study              | Patient Study             |   U   |
| Study              | Clinical Trial Study      |   U   |
| Series             | General Series            |   M   |
| Series             | Clinical Trial Series     |   U   |
| Frame of Reference | Frame of Reference        |   M   |
| Frame of Reference | Synchronization           |   C   |
| Equipment          | General Equipment         |   M   |
| Acquisition        | General Acquisition       |   M   |
| Image              | General Image             |   M   |
| Image              | General Reference         |   U   |
| Image              | Image Plane               |   M   |
| Image              | Image Pixel               |   M   |
| Image              | Device                    |   U   |
| Image              | Specimen                  |   U   |
| Image              | Overlay Plane             |   U   |
| Image              | VOI LUT                   |   U   |
| Image              | SOP Common                |   M   |
| Image              | Common Instance Reference |   U   |


### Contrast/Bolus
 - None

### CT Image (Module)
NB: The DICOM Standard repeats some elements in this module already defined in the Image Pixel Module. In these cases, we use the value "Image Pixel" in the Conversion column.

| Attribute Name              | Tag         | Conversion                      |
|-----------------------------|-------------|---------------------------------|
| Image Type                  | (0008,0008) | ORIGINAL\PRIMARY\AXIAL          |
| Samples per Pixel           | (0028,0002) | Image Pixel                     |
| Photometric Interpretation  | (0028,0004) | Image Pixel                     |
| Bits Allocated              | (0028,0100) | Image Pixel                     |
| Bits Stored                 | (0028,0101) | Image Pixel                     |
| High Bit                    | (0028,0102) | Image Pixel                     |
| Rescale Intercept           | (0028,1052) |       0                         |
| Rescale Slope               | (0028,1053) |       1                         |
| KVP                         | (0018,0060) | ct_xray_voltage                 |
| Acquisition Number          | (0020,0012) |       1                         |
| Distance Source to Detector | (0018,1110) | ct_source_to_detector * 10      |
| Distance Source to Patient  | (0018,1111) | ct_source_to_crot * 10          |
| X-Ray Tube Current          | (0018,1151) | ct_anode_current / 1000         |
| Convolution Kernel          | (0018,1210) | from recon_algorithm. see below |

The value for Convolution Kernel is mapped from the variable recon_algoritm per the following mapping table:

| Keyword                | Value | Mapped Value                   |
|------------------------|-------|--------------------------------|
| recon_algorithm        |   0   | Unknown, or no, algorithm type |
| recon_algorithm        |   1   | Filtered Backprojection        |
| recon_algorithm        |   2   | OSEM2d                         |
| recon_algorithm        |   3   | OSEM3d                         |
| recon_algorithm        |   4   | 3D Reprojection                |
| recon_algorithm        |   5   | Undefined                      |
| recon_algorithm        |   6   | OSEM3D/MAP                     |
| recon_algorithm        |   7   | MAPTR for transmission image   |
| recon_algorithm        |   8   | MAP 3D reconstruction          |
| recon_algorithm        |   9   | Feldkamp cone beam             |



### Multi-energy CT Image
 - None

TODO: Do we want to add the Siemens private data for CT? It is described in their Conformance Statement.

## PET Image

See *Common to All Modalities* section for items not specific to PET. These modules are described above:

| DICOM IE           | Module                    | Usage |
|--------------------|---------------------------|-------|
| Patient            | Patient                   |   M   |
| Patient            | Clinical Trial Subject    |   U   |
| Study              | General Study             |   M   |
| Study              | Patient Study             |   U   |
| Study              | Clinical Trial Study      |   U   |
| Series             | General Series            |   M   |
| Series             | Clinical Trial Series     |   U   |
| Frame of Reference | Frame of Reference        |   M   |
| Frame of Reference | Synchronization           |   C   |
| Equipment          | General Equipment         |   M   |
| Acquisition        | General Acquisition       |   M   |
| Image              | General Image             |   M   |
| Image              | General Reference         |   U   |
| Image              | Image Plane               |   M   |
| Image              | Image Pixel               |   M   |
| Image              | Device                    |   U   |
| Image              | Specimen                  |   U   |
| Image              | Overlay Plane             |   U   |
| Image              | VOI LUT                   |   U   |
| Image              | SOP Common                |   M   |
| Image              | Common Instance Reference |   U   |



### PET Series

| Attribute Name        | Tag         | Conversion                      |
|-----------------------|-------------|---------------------------------|
| Series Date           | (0008,0021) | from scan_date_time             |
| Series Time           | (0008,0031) | from scan_date_time             |
| Counts Source         | (0054,1002) | EMISSION                        |
| Series Type (Value 1) | (0054,1000) | acquisition_mode:2 -> STATIC <br/> acquisition_mode:3 -> DYNAMIC <br/> acquisition_mode:4 -> GATED <br/> acquisition_mode:5 -> FULL BODY |
| Series Type (Value 2) | (0054,1000) | file_type:5 -> IMAGE <br/>    |
| Series Type (example) | (0054,1000) | DYNAMIC\IMAGE                   |
| Number of Slices      | (0054,0081) | z_dimension                     |
| Corrected Image       | (0028,0051) | Values added when one or more of the following are not empty: <br/>normalization_applied -> NORM <br/>attenuation_applied -> ATTN <br/>scatter_correction -> SCAT <br/>decay_correction_applied -> DECY <br/>deadtime_correction_applied -> DTM |
| Decay Correction      | (0054,1102) | decay_correction_applied:(not 0) -> START <br/>else NONE</br>See TODO below |
| Collimator Type       | 0018,1181   | ""                              |

TODO: Decay Correction can have values other than START. Determine proper mapping.

### PET Isotope

| Attribute Name                           | Tag         | Conversion   |
|------------------------------------------|-------------|--------------|
| Radiopharmaceutical Information Sequence | (0054,0016) |              |
| >Radionuclide Code Sequence              | (0054,0300) |              |
| >>Code Value                             | (0008,0100) | from isotope |
| >>Coding Scheme Designator               | (0008,0102) |              |
| >>Code Meaning                           | (0008,0104) |              |

Map of isotope to Radionuclide Code Sequence.
See https://dicom.nema.org/medical/dicom/current/output/html/part16.html#sect_CID_4020 for the list of coded values. The table in the DICOM Standard does not define the mapping from the Inveon header (isotope) to the value in the table for CID 4020.

| isotope | Code Value | Coding Scheme | Code Meaning |
|---------|------------|---------------|--------------|
| F-18    | C-111A1    | SNM3          | ^18^Fluorine |

TODO:
1. We use the value from isotope here. There is also a header field for injected_compound. How should that be used?
1. Finish the mapping table from isotope to coded valule

### PET Multi-Gated Acqusition
 - None

### NM/PET Patient Orientation

| Attribute Name                            | Tag         | Conversion               |
|-------------------------------------------|-------------|--------------------------|
| Patient Orientation Code Sequence         | (0054,0410) |                          |
| >Code Value                               | (0008,0100) | 102538003                |
| >Coding Scheme Designator                 | (0008,0102) | SCT                      |
| >Code Meaning                             | (0008,0104) | Recumbent                |
| Patient Gantry Relationship Code Sequence | (0054,0410) |                          |
| >Code Value                               | (0008,0100) | from subject_orientation |
| >Coding Scheme Designator                 | (0008,0102) |                          |
| >Code Meaning                             | (0008,0104) |                          |

Map of subject_orientation to Patient Gantry Relationship Code Sequence.
See https://dicom.nema.org/medical/dicom/current/output/html/part16.html#sect_CID_21

| subject_orientation              | Code Value | Coding Scheme | Code Meaning |
|----------------------------------|------------|---------------|--------------|
| 0 - Unknown subject orientation  | No code    |               |              |
| 1 - Feet first, prone            | 102541007  | SCT           | feet-first   |
| 2 - Head first, prone            | 102540008  | SCT           | headfirst    |
| 3 - Feet first, supine           | 102541007  | SCT           | feet-first   |
| 4 - Head first, supine           | 102540008  | SCT           | headfirst    |
| 5 - Feet first, right            | 102541007  | SCT           | feet-first   |
| 6 - Head first, right            | 102540008  | SCT           | headfirst    |
| 7 - Feet first, left             | 102541007  | SCT           | feet-first   |
| 8 - Head first, left             | 102540008  | SCT           | headfirst    |


### PET Image (Module)
NB: The DICOM Standard repeats some elements in this module already defined in the Image Pixel Module. In these cases, we use the value "Image Pixel" in the Conversion column.

| Attribute Name              | Tag         | Conversion                               |
|-----------------------------|-------------|------------------------------------------|
| Image Type                  | (0008,0008) | ORIGINAL\PRIMARY                         |
| Samples per Pixel           | (0028,0002) | Image Pixel                              |
| Photometric Interpretation  | (0028,0002) | Image Pixel                              |
| Bits Allocated              | (0028,0100) | Image Pixel                              |
| Bits Stored                 | (0028,0101) | Image Pixel                              |
| High Bit                    | (0028,0102) | Image Pixel                              |
| Rescale Intercept           | (0028,1052) | 0                                        |
| Rescale Slope               | (0028,1053) | 1.217                                    |
| Frame Reference Time        | (0054,1300) | (frame_start + frame_duraction/2) * 1000 |
| Image Index                 | (0054,1330) | In Error                                 |
| Acquisition Date            | (0008,0022) | from scan_time_date                      |
| Acquisition Time            | (0008,0032) | from scan_time_date                      |
| Actual Frame Duration       | (0018,1242) | frame_duration * 1000                    |
| Decay Factor                | (0054,1321) | decay_correction                         |

 TODO:
 1. Review/repair hard-coded value for Image Type
 2. Review/repair hard-coded values for Rescale Intercept and Rescale Slope
 3. Review computed value for Image Index
 4. Is decay_correction the right value to use for DICOM Decay Factor (0054,1321)?

### VOI LUT
 - None

### Acquisition Context
 - None

TODO: Do we want to add the Siemens private data for PET? It is described in their Conformance Statement.


## NM Image
 - Currently, no conversion software