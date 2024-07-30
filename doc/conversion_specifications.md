# Specifications for Inveon to DICOM Conversion

## CT Image

## PET Image



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

### PWR Multi-Gated Acqusition
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

| Keyword  | Value | Mapped Value         |
|----------|-------|----------------------|
| model    |    0  | unknown              |
| model    | 2000  | Primate              |
| model    | 2001  | Rodent               |
| model    | 2002  | microPET2            |
| model    | 2500  | Focus_220            |
| model    | 2501  | Focus_120            |
| model    | 3000  | mCAT                 |
| model    | 3500  | mCATII               |
| model    | 4000  | mSPECT               |
| model    | 5000  | Inveon_Dedicated_PET |
| model    | 5001  | Inveon_MM_Platform   |
| model    | 6000  | MR_PET_Head_Insert   |
| model    | 8000  | Tuebingen_PET_MR     |
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
 - TODO

### General Reference
 - None

 ### Image Plane
 - TODO

### Image Pixel
 - TODO

### Device
 - None

### Specimen
 - None

### PET Image
 - TODO

### VOI LUT
 - None

### Acquisition Context
 - None

### SOP Common
 - TODO

### Common Instance Reference
 - TODO