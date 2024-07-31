# Specifications for Inveon to DICOM Conversion

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
 - TODO

### Patient Study
 - TODO

### Clinical Trial Study
 - None

### General Series
 - TODO

### Clinical Trial Series
 - None

### Frame of Reference

| Attribute Name               | Tag         | Conversion                      |
|------------------------------|-------------|---------------------------------|
| Frame of Reference UID       | (0020,0052) | generated (see TODO below)      |
| Position Reference Indicator | (0020,1040) | ""                              |

TODO: Need to harmonize generated UID across the PET and CT scans and make sure the same Frame of Reference is used. Today, these are separate, so no automatic registration is possible.

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
| Attribute Name              | Tag         | Conversion                           |
|-----------------------------|-------------|--------------------------------------|
| Pixel Spacing               | (0028,0030) | from pixel_size_x and pixel_size_y   |
| Image Orientation (Patient) | (0020,0037) | from subject_orientation. See below. |
| Image Position (Patient)    | (0020,0032) | from pixel_size_z                    |
| Slice Thickness             | (0018,0050) | pixel_size_z                         |

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

### Image Pixel

| Attribute Name              | Tag         | Conversion     |
|-----------------------------|-------------|----------------|
| Samples per Pixel           | (0028,0002) |      1         |
| Photometric Interpretation  | (0028,0004) | MONOCHROME2    |
| Rows                        | (0028,0010) | y_dimension    |
| Columns                     | (0028,0011) | x_dimension    |
| Bits Allocated              | (0028,0100) |     16  (1)    |
| Bits Stored                 | (0028,0101) |     16         |
| High Bit                    | (0028,0102) |     15         |
| Pixel Representation        | (0028,0103) |      1  (2)    |
| Pixel Data                  | (7FE0,0010) | from .img file |

Notes:
1. All pixels converted to 16 bit integers if not already in that format. For example, floating point values are converted.
2. Pixel Representation is 2's complement

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
| 1.2.840.10008.5.1.4.1.1.128.1 | Legacy Converted Enhanced PET |
| 1.2.840.10008.5.1.4.1.1.130   | Enhanced PET                  |
| 1.2.840.10008.5.1.4.1.1.2     | CT
| 1.2.840.10008.5.1.4.1.1.2.1   | Enhanced CT                   |
| 1.2.840.10008.5.1.4.1.1.2.2   | Legacy Converted Enhanced CT  |

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

### CT Image (Module)

### Multi-energy CT Image

### Overlay Plane
 - None

### VOI LUT

### Common Instance Reference





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
See https://dicom.nema.org/medical/dicom/current/output/html/part16.html#sect_CID_4020

| isotope | Code Value | Coding Scheme | Code Meaning |
|---------|------------|---------------|--------------|
| F-18    | C-111A1    | SNM3          | ^18^Fluorine |

TODO:
1. We use the value from isotope here. There is also a header field for injected_compound. How should that be used?

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
| 0 - Unknown subject orientation  | No code    |
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