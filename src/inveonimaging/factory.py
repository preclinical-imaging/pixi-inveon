from pathlib import Path
import os
import pydicom
from pydicom.sequence import Sequence
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from pydicom.uid import generate_uid, UID
from inveonimaging.inveon import InveonImage
from inveonimaging.dicom import PatientModule, GeneralStudyModule, GeneralEquipmentModule, \
    EnhancedGeneralEquipmentModule, \
    GeneralSeriesModule, FrameOfReferenceModule, GeneralAcquisitionModule, \
    GeneralImageModule, ImagePlaneModule, ImagePixelModule, MultiframeFunctionalGroupsModule, \
    MultiframeDimensionModule, ContrastBolusModule, SOPCommonModule, \
    AcquisitionContextModule, FrameContentItem, \
    PETSeriesModule, PETIsotopeModule, NMPETPatientOrientation, \
    PETImageModule, EnhancedPETImageModule, CTImageModule, EnhancedCTImageModule, \
    mergeDatasets, mergeDatasetsVerbose


class Factory:
    def __init__(
            self):
        self.study_instance_uid = None
        self.series_number      = 1
        self.instance_number    = 1
        self.file_prefix_map = {}

    def get_series_number(self) -> int:
        return self.series_number

    def get_instance_number(self) -> int:
        return self.instance_number

    def increment_series_number(self) -> None:
        self.series_number += 1

    def increment_instance_number(self) -> None:
        self.instance_number += 1
    def generate_study_instance_uid(self) -> None:
        self.study_instance_uid = generate_uid()

    def add_file_prefix(self, modality: str, prefix: str) -> None:
        self.file_prefix_map[modality] = prefix

    def get_file_prefix(self, modality: str) -> str:
        return self.file_prefix_map.get(modality, "")

    # These are three higher-level methods to convert one Inveon Image to DICOM files.
    # By calling the desired method, the user controls the output type. These include:
    #  Multiframe data (one DICOM file)
    #  Legacy Converted Multiframe data (one DICOM file)
    #  Standard Images (one DICOM file per slice/timepoint)
    def convert_to_multiframe(self, inveon_image: InveonImage, output_folder: str, file_name=None):
        modality_mapped = inveon_image.get_metadata_element("modality_mapped")
        if (modality_mapped == 'CT'):
            self.create_write_dicom_multiframe_ct(inveon_image, output_folder, file_name)
        else:
            self.create_write_dicom_multiframe_pet(inveon_image, output_folder, file_name)

        return None

    def convert_to_legacy_converted_multiframe(self, inveon_image: InveonImage, output_folder: str, file_name=None):
        modality_mapped = inveon_image.get_metadata_element("modality_mapped")
        if (modality_mapped == 'CT'):
            self.create_write_dicom_legacy_converted_multiframe_ct(inveon_image, output_folder, file_name)
        else:
            self.create_write_dicom_legacy_converted_multiframe_pet(inveon_image, output_folder, file_name)

        return None

    def convert_to_standard_images(self, inveon_image: InveonImage, output_folder: str):
        modality_mapped = inveon_image.get_metadata_element("modality_mapped")
        if (modality_mapped == 'CT'):
            self.create_write_dicom_files_ct(inveon_image, output_folder)
        else:
            self.create_write_dicom_files_pet(inveon_image, output_folder)

        return None

    def create_write_dicom_multiframe_ct(self, inveon_image: InveonImage, output_path: str, file_name=None):
        print(f"create_write_dicom_multiframe_ct {file_name}")
        ds = self.create_enhanced_ct_dataset(inveon_image)
        self.create_output_folder(output_path, False)
        self.write_dataset(ds, output_path, self.determine_filename(ds, file_name))
        return None

    def create_write_dicom_multiframe_pet(self, inveon_image: InveonImage, output_path: str, file_name=None):
        print(f"create_write_dicom_multiframe_pet {file_name}")
        ds = self.create_enhanced_pet_dataset(inveon_image)
        self.create_output_folder(output_path, False)
        self.write_dataset(ds, output_path, self.determine_filename(ds, file_name))
        return None

    def create_write_dicom_legacy_converted_multiframe_ct(self, inveon_image: InveonImage, output_path: str,
                                                          file_name=None):
        print(f"create_write_dicom_multiframe_ct {file_name}")
        ds = self.create_legacy_converted_enhanced_ct_dataset(inveon_image)
        self.create_output_folder(output_path, False)
        self.write_dataset(ds, output_path, self.determine_filename(ds, file_name))
        return None

    def create_write_dicom_legacy_converted_multiframe_pet(self, inveon_image: InveonImage, output_path: str,
                                                           file_name=None):
        print(f"create_write_dicom_multiframe_pet {file_name}")
        ds = self.create_legacy_converted_enhanced_pet_dataset(inveon_image)
        self.create_output_folder(output_path, False)
        self.write_dataset(ds, output_path, self.determine_filename(ds, file_name))
        return None

    def create_write_dicom_files_ct(self, inveon_image: InveonImage, output_path: str):

        self.create_output_folder(output_path, True)
        ct_common = self.create_ct_common_elements(inveon_image)

        z_dimension = int(inveon_image.get_metadata_element("z_dimension"))
        total_frames = int(inveon_image.get_metadata_element("total_frames"))
        frame_count = z_dimension * total_frames

        for index in range(frame_count):
            current_frame = index // z_dimension
            frame_ds = self.fill_ct_per_frame_data(inveon_image, current_frame, index)
            instance_ds = mergeDatasets(ct_common, frame_ds)
            self.write_dataset(instance_ds, output_path, self.determine_filename(instance_ds, None))

    def create_write_dicom_files_pet(self, inveon_image: InveonImage, output_path: str):

        self.create_output_folder(output_path, True)
        pet_common = self.create_pet_common_elements(inveon_image)

        z_dimension = int(inveon_image.get_metadata_element("z_dimension"))
        time_frames = int(inveon_image.get_metadata_element("time_frames"))
        frame_count = z_dimension * time_frames

        for time_index in range(time_frames):
            for frame_index in range(z_dimension):
                frame_ds = self.fill_pet_per_frame_data(inveon_image, time_index, frame_index)
                instance_ds = mergeDatasets(pet_common, frame_ds)
                self.write_dataset(instance_ds, output_path, self.determine_filename(instance_ds, None))

    #        for frame_index in range(frame_count):
    #            time_frame = frame_index // z_dimension
    #            print (f"{time_frame} {frame_index}")
    #
    #            frame_ds = self.fill_pet_per_frame_data(inveon_image, time_frame, frame_index)
    #            instance_ds = mergeDatasets(pet_common, frame_ds)
    #            self.write_dataset(instance_ds, output_path, self.determine_filename(instance_ds, None))

    def create_output_folder(self, folder: str, must_be_empty: bool) -> None:
        if (os.path.exists(folder)):
            if (not os.path.isdir(folder)):
                raise Exception(f"The item identified by {folder} exists, but it is not a folder")
            if (must_be_empty and (os.listdir(folder))):
                raise Exception(f"The item identified by {folder} exists, but it is not empty")
        else:
            os.makedirs(folder, 0o777, True)

    def determine_filename(self, ds: Dataset, file_name=None):
        if (file_name is None):
            modality = ds.Modality
            file_name = f"{self.get_file_prefix(modality)}{ds.InstanceNumber:06d}.dcm"
        return file_name

    def write_dataset(self, ds: Dataset, folder: str, file_name=None) -> None:
        file_meta = FileMetaDataset()
        file_meta.FileMetaInformationVersion = b'\x00\x01'
        file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
        file_meta.MediaStorageSOPInstanceUID = UID(ds.SOPInstanceUID)
        file_meta.ImplementationClassUID = UID("1.2.3.4")
        file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
        file_meta.FileMetaInformationGroupLength = 0

        file_dataset = FileDataset("", dataset=ds, file_meta=file_meta, preamble=b"\0" * 128)
        file_dataset.is_little_endian = True
        file_dataset.is_implicit_VR = False
        file_dataset.write_like_original = False
        file_dataset.save_as(f"{folder}/{file_name}")

    # Create the elements that are common to all CT slices
    # A.3 CT Image IOD
    # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_A.3
    def create_ct_common_elements(self, inveon_image: InveonImage) -> Dataset:

        # Patient
        patient = self.create_patient_module(inveon_image)
        clinical_trial_subject = None

        # Study
        general_study = self.create_general_study_module(inveon_image)
        patient_study = None
        clinical_trial_study = None

        # Series
        general_series = self.create_general_series_module(inveon_image)
        clinical_trial_series = None

        # Frame of Reference
        frame_of_reference = self.create_frame_of_reference_module(inveon_image)
        synchronization = None

        # Equipment
        general_equipment = self.create_general_equipment_module(inveon_image)

        # Acquisition
        general_acquisition = self.create_general_acquisition_module(inveon_image)

        # Image
        general_image = self.create_general_image_module(inveon_image)
        general_reference = None
        image_plane = self.create_image_plane_module(inveon_image)
        image_pixel = self.create_image_pixel_module(inveon_image, False)
        contrast_bolus = self.create_contrast_bolus_module(inveon_image)
        device = None
        specimen = None
        ct_image = self.create_ct_image_module(inveon_image)
        multi_energy_ct_image = None
        overlay_plane = None
        voi_lut = None
        sop_common = self.create_sop_common_module(inveon_image, "1.2.840.10008.5.1.4.1.1.2")
        common_instance_reference = None

        ds = mergeDatasets(patient,
                           clinical_trial_subject,

                           general_study,
                           patient_study,
                           clinical_trial_study,

                           general_series,
                           clinical_trial_series,

                           frame_of_reference,
                           synchronization,

                           general_equipment,

                           general_acquisition,

                           general_image,
                           general_reference,
                           image_plane,
                           image_pixel,
                           contrast_bolus,
                           device,
                           specimen,
                           ct_image,
                           multi_energy_ct_image,
                           overlay_plane,
                           voi_lut,
                           sop_common,
                           common_instance_reference)
        return ds

    # A.38.1.3 Enhanced CT Image IOD
    # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_A.38
    def create_enhanced_ct_dataset(self, inveon_image: InveonImage) -> Dataset:

        # Patient
        patient = self.create_patient_module(inveon_image)
        clinical_trial_subject = None
        # Study
        general_study = self.create_general_study_module(inveon_image)
        patient_study = None
        clinical_trial_study = None
        # Series
        general_series = self.create_general_series_module(inveon_image)
        ct_series = None
        clinical_trial_series = None

        # Frame of Reference
        frame_of_reference = self.create_frame_of_reference_module(inveon_image)
        synchronization = None

        # Equipment
        general_equipment = self.create_general_equipment_module(inveon_image)
        enhanced_gen_equip = self.create_enhanced_general_equipment_module(inveon_image)

        # Image
        image_pixel = self.create_image_pixel_module(inveon_image)
        enhanced_contrast_bolus = None
        multiframe_fctnl_grps = self.create_multiframe_functional_groups_module(inveon_image)
        multiframe_dimension = self.create_multiframe_dimension_module(inveon_image)
        cardiac_synchronization = None
        respiratory_synchronization = None
        supplemental_palette_color_lut = None
        acquisition_context = None
        device = None
        specimen = None
        enhanced_ct_image = self.create_enhanced_ct_image_module(inveon_image)
        enhanced_multi_energy_ct_acq = None
        icc_profile = None
        sop_common = self.create_sop_common_module(inveon_image, "1.2.840.10008.5.1.4.1.1.2.1")
        common_instance_reference = None
        frame_extraction = None

        ds = mergeDatasets(patient,
                           clinical_trial_subject,

                           general_study,
                           patient_study,
                           clinical_trial_study,

                           general_series,
                           ct_series,
                           clinical_trial_series,

                           frame_of_reference,
                           synchronization,

                           general_equipment,
                           enhanced_gen_equip,

                           image_pixel,
                           enhanced_contrast_bolus,
                           multiframe_fctnl_grps,
                           multiframe_dimension,
                           cardiac_synchronization,
                           respiratory_synchronization,
                           supplemental_palette_color_lut,
                           acquisition_context,
                           device,
                           specimen,
                           enhanced_ct_image,
                           enhanced_multi_energy_ct_acq,
                           icc_profile,
                           sop_common,
                           common_instance_reference,
                           frame_extraction)
        return ds

    # A.70 Legacy Converted Enhanced CT Image IOD
    # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_A.70
    def create_legacy_converted_enhanced_ct_dataset(self, inveon_image: InveonImage) -> Dataset:

        patient = self.create_patient_module(inveon_image)
        clin_trial_subject = None

        general_study = self.create_general_study_module(inveon_image)
        patient_study = None
        clin_trial_study = None

        general_series = self.create_general_series_module(inveon_image)
        ct_series = None
        clin_trial_series = None

        frame_of_reference = self.create_frame_of_reference_module(inveon_image)
        synchronization = None

        general_equipment = self.create_general_equipment_module(inveon_image)
        enhanced_gen_equip = self.create_enhanced_general_equipment_module(inveon_image)

        # These are at the Image level in the IOD definition
        image_pixel = self.create_image_pixel_module(inveon_image)
        contrast_bolus = self.create_contrast_bolus_module(inveon_image)
        enhanced_contrast_bolus = None
        multiframe_fctnl_grps = self.create_multiframe_functional_groups_module(inveon_image)
        multiframe_dimension = None
        cardiac_synchronization = None
        respiratory_synchronization = None
        acquisition_context = self.create_acquisition_context_module(inveon_image)
        device = None
        specimen = None
        enhanced_ct_image = self.create_enhanced_ct_image_module(inveon_image)
        sop_common = self.create_sop_common_module(inveon_image, "1.2.840.10008.5.1.4.1.1.2.2")
        common_instance_reference = None
        frame_extraction = None

        ds = mergeDatasets(patient,
                           clin_trial_subject,

                           general_study,
                           patient_study,
                           clin_trial_study,

                           general_series,
                           ct_series,
                           clin_trial_series,

                           frame_of_reference,
                           synchronization,

                           general_equipment,
                           enhanced_gen_equip,

                           image_pixel,
                           contrast_bolus,
                           enhanced_contrast_bolus,
                           multiframe_fctnl_grps,
                           multiframe_dimension,
                           cardiac_synchronization,
                           respiratory_synchronization,
                           acquisition_context,
                           device,
                           specimen,
                           enhanced_ct_image,
                           sop_common,
                           common_instance_reference,
                           frame_extraction)
        return ds

    # Create the elements that are common to all PET slices
    # A.21 Positron Emission Tomography Image IOD
    # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_A.21
    def create_pet_common_elements(self, inveon_image: InveonImage) -> Dataset:
        # Patient
        patient = self.create_patient_module(inveon_image)
        clinical_trial_subject = None

        # Study
        general_study = self.create_general_study_module(inveon_image)
        patient_study = None
        clinical_trial_study = None

        # Series
        general_series              = self.create_general_series_module(inveon_image)
        clinical_trial_series       = None
        pet_series                  = self.create_pet_series_module(inveon_image)
        pet_isotope                 = self.create_pet_isotope_module(inveon_image)
        pet_multi_gated_acquisition = None
        nm_pet_patient_orientation  = self.create_nm_patient_orientation_module(inveon_image)

        # Frame of Reference
        frame_of_reference = self.create_frame_of_reference_module(inveon_image)
        synchronization = None

        # Equipment
        general_equipment = self.create_general_equipment_module(inveon_image)

        # Acquisition
        general_acquisition = self.create_general_acquisition_module(inveon_image)

        # Image
        general_image = self.create_general_image_module(inveon_image)
        general_reference = None
        image_plane = self.create_image_plane_module(inveon_image)
        image_pixel = self.create_image_pixel_module(inveon_image)
        device = None
        specimen = None
        pet_image = self.create_pet_image_module(inveon_image)
        overlay_plane = None
        voi_lut = None
        acquisition_context = None
        sop_common = self.create_sop_common_module(inveon_image, "1.2.840.10008.5.1.4.1.1.128")
        common_instance_reference = None

        ds = mergeDatasets(patient,
                           clinical_trial_subject,

                           general_study,
                           patient_study,
                           clinical_trial_study,

                           general_series,
                           clinical_trial_series,
                           pet_series,
                           pet_isotope,
                           pet_multi_gated_acquisition,
                           nm_pet_patient_orientation,

                           frame_of_reference,
                           synchronization,

                           general_equipment,

                           general_acquisition,

                           general_image,
                           general_reference,
                           image_plane,
                           image_pixel,
                           device,
                           specimen,
                           pet_image,
                           overlay_plane,
                           voi_lut,
                           acquisition_context,
                           sop_common,
                           common_instance_reference)
        return ds

    # A.56.1 Enhanced PET Image IOD Description
    # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_A.56
    def create_enhanced_pet_dataset(self, inveon_image: InveonImage) -> Dataset:

        patient = self.create_patient_module(inveon_image)
        clin_trial_subject = None

        general_study = self.create_general_study_module(inveon_image)
        patient_study = None
        clin_trial_study = None

        # These are at the Series level in the IOD definition
        general_series = self.create_general_series_module(inveon_image)
        enhanced_pet_series = None
        clin_trial_series = None

        # These are at the Frame of Reference level in the IOD definition
        frame_of_reference = self.create_frame_of_reference_module(inveon_image)
        synchronization = None

        # These are at the Equipment level in the IOD definition
        general_equipment = self.create_general_equipment_module(inveon_image)
        enhanced_gen_equip = self.create_enhanced_general_equipment_module(inveon_image)

        # These are at the Image level in the IOD definition
        image_pixel = self.create_image_pixel_module(inveon_image)
        intervention = None
        acquisition_context = self.create_acquisition_context_module(inveon_image)
        multiframe_fctnl_grps = self.create_multiframe_functional_groups_module_pet(inveon_image)
        multiframe_dimension = None
        cardiac_synchronization = None
        respiratory_synchronization = None
        specimen = None
        enhanced_pet_image = self.create_enhanced_pet_image_module(inveon_image)

        sop_common = self.create_sop_common_module(inveon_image, "1.2.840.10008.5.1.4.1.1.128.1")
        common_instance_reference = None
        frame_extraction = None

        ds = mergeDatasets(patient,
                           clin_trial_subject,

                           general_study,
                           patient_study,
                           clin_trial_study,

                           general_series,
                           enhanced_pet_series,
                           clin_trial_series,

                           frame_of_reference,
                           synchronization,

                           general_equipment,
                           enhanced_gen_equip,

                           image_pixel,
                           intervention,
                           acquisition_context,
                           multiframe_fctnl_grps,
                           multiframe_dimension,
                           cardiac_synchronization,
                           respiratory_synchronization,
                           specimen,
                           enhanced_pet_image,
                           sop_common,
                           common_instance_reference,
                           frame_extraction)
        return ds

    # A.72 Legacy Converted Enhanced PET Image IOD
    # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#sect_A.72
    def create_legacy_converted_enhanced_pet_dataset(self, inveon_image: InveonImage) -> Dataset:

        patient = self.create_patient_module(inveon_image)
        clin_trial_subject = None

        general_study = self.create_general_study_module(inveon_image)
        patient_study = None
        clin_trial_study = None

        # These are at the Series level in the IOD definition
        general_series = self.create_general_series_module(inveon_image)
        enhanced_pet_series = None
        clin_trial_series = None

        # These are at the Frame of Reference level in the IOD definition
        frame_of_reference = self.create_frame_of_reference_module(inveon_image)
        synchronization = None

        # These are at the Equipment level in the IOD definition
        general_equipment = self.create_general_equipment_module(inveon_image)
        enhanced_gen_equip = self.create_enhanced_general_equipment_module(inveon_image)

        # These are at the Image level in the IOD definition
        image_pixel = self.create_image_pixel_module(inveon_image)
        intervention = None
        acquisition_context = self.create_acquisition_context_module(inveon_image)
        multiframe_fctnl_grps = self.create_multiframe_functional_groups_module_pet(inveon_image)
        multiframe_dimension = None
        cardiac_synchronization = None
        respiratory_synchronization = None
        specimen = None
        enhanced_pet_image = self.create_enhanced_pet_image_module(inveon_image)

        sop_common = self.create_sop_common_module(inveon_image, "1.2.840.10008.5.1.4.1.1.128.1")
        common_instance_reference = None
        frame_extraction = None

        ds = mergeDatasets(patient,
                           clin_trial_subject,

                           general_study,
                           patient_study,
                           clin_trial_study,

                           general_series,
                           enhanced_pet_series,
                           clin_trial_series,

                           frame_of_reference,
                           synchronization,

                           general_equipment,
                           enhanced_gen_equip,

                           image_pixel,
                           intervention,
                           acquisition_context,
                           multiframe_fctnl_grps,
                           multiframe_dimension,
                           cardiac_synchronization,
                           respiratory_synchronization,
                           specimen,
                           enhanced_pet_image,
                           sop_common,
                           common_instance_reference,
                           frame_extraction)
        return ds

    def fill_pet_per_frame_data(self, inveon_image: InveonImage, time_index: int, frame_index: int):
        z_dimension = int(inveon_image.get_metadata_element("z_dimension"))
#        instance_number = (time_index * z_dimension) + frame_index + 1


        ds = Dataset()
        ds.InstanceNumber = self.get_instance_number()
        self.increment_instance_number()

        ds.SOPInstanceUID = generate_uid()

        image_plane_module = self.create_image_plane_module(inveon_image, frame_index)
        image_pixel_module = self.create_image_pixel_module(inveon_image, True, False)
        pet_image_module   = self.create_pet_image_module(inveon_image, time_index, frame_index)
        return mergeDatasets(image_plane_module, image_pixel_module, pet_image_module, ds)

    def fill_ct_per_frame_data(self, inveon_image: InveonImage, current_frame: int, index: int) -> Dataset:
        z = current_frame * index
        acquisition_number = index + 1
#        instance_number = index + 1

#        z_dimension = int(inveon_image.get_metadata_element("z_dimension"))

#        in_frame_index = index % z_dimension

        ds = Dataset()
        ds.InstanceNumber = self.get_instance_number()
        self.increment_instance_number()

        ds.SOPInstanceUID = generate_uid()

        image_plane_module = self.create_image_plane_module(inveon_image, index)
        image_pixel_module = self.create_image_pixel_module(inveon_image, True, False)
        return mergeDatasets(image_plane_module, image_pixel_module, ds)

    def create_patient_module(self, inveon_image: InveonImage) -> PatientModule:

        # TODO Replace with real values
        patient_name = ""
        patient_id   = ""
        patient_dob  = ""
        patient_sex  = ""

        m = PatientModule(patient_name,patient_id,patient_dob,patient_sex)
        return m

    def create_general_study_module(self, inveon_image: InveonImage) -> GeneralStudyModule:
        study_instance_uid = generate_uid() if self.study_instance_uid is None else self.study_instance_uid
        study_date = inveon_image.get_metadata_element("scan_time_date")
        study_time = inveon_image.get_metadata_element("scan_time_time")
        referring_phys = inveon_image.get_metadata_element("investigator")
        study_id = "Study-ID"
        accession_number = ""
        study_description = inveon_image.get_metadata_element("study")

        m = GeneralStudyModule(study_instance_uid,
                               study_date,
                               study_time,
                               referring_phys,
                               study_id,
                               accession_number,
                               study_description)
        return m

    def create_general_series_module(self, inveon_image: InveonImage) -> GeneralSeriesModule:
        modality_mapped = inveon_image.get_metadata_element("modality_mapped")
        # Need to convert what INVEON thinks of as Modality to what DICOM thinks
        the_map = {"CT": "CT", "PET": "PT", "SPECT": "NM"}
#        series_number_map = {"CT": "1", "PET": "2", "SPECT": "3"}
        modality = "OT"

        if (modality_mapped in the_map):
            modality = the_map[modality_mapped]

        series_number = str(self.series_number)

        series_instance_uid = generate_uid()
        laterality = ""
        series_date = inveon_image.get_metadata_element("scan_time_date")
        series_time = inveon_image.get_metadata_element("scan_time_time")
        series_description = inveon_image.get_metadata_element("acquisition_mode_mapped")
        subject_orientation_mapped = inveon_image.get_metadata_element("subject_orientation_mapped")
        patient_position = None

        if modality != "PT" and subject_orientation_mapped != None and subject_orientation_mapped != "":
            patient_position = subject_orientation_mapped

        m = GeneralSeriesModule(modality, series_instance_uid, laterality, series_number, series_date, series_time,
                                series_description, patient_position)
        return m

    def create_pet_series_module(self, inveon_image: InveonImage) -> PETSeriesModule:
        series_date = inveon_image.get_metadata_element("scan_time_date")
        series_time = inveon_image.get_metadata_element("scan_time_time")
        units = "BQML"
        ## TODO
        counts_source = "EMISSION"
        series_type = self.calculate_SeriesType(inveon_image)
        number_of_slices = inveon_image.get_metadata_element("z_dimension")
        decay_correction = self.calculate_DecayCorrection(inveon_image)
        corrected_image = self.calculate_CorrectedImage(inveon_image)
        # TODO Can we determine this from metadata?
        collimator_type = ""
        number_of_time_slices = self.calculate_NumberOfTimeSlices(inveon_image)

        m = PETSeriesModule(series_date, series_time, units, counts_source, series_type,
                            number_of_slices, decay_correction, corrected_image, collimator_type,
                            number_of_time_slices)

        return m

    def calculate_SeriesType(self, inveon_image: InveonImage) -> str:
        acquisition_mode = inveon_image.get_metadata_element("acquisition_mode")
        match acquisition_mode:
            case "3":
                return "DYNAMIC\\IMAGE"
            case _:
                raise Exception(
                    f"Do not have code to calculate SeriesType when acquisition_mode is {acquisition_mode}")

    # TODO Review
    #  Need to distinguish between "START" and "ADMIN"
    def calculate_DecayCorrection(self, inveon_image: InveonImage) -> str:
        decay_correction_applied = inveon_image.get_metadata_element("decay_correction_applied")
        if (decay_correction_applied is not None and decay_correction_applied != "0"):
            return "START"
        else:
            return "NONE"

    # TODO Review all calculations
    def calculate_CorrectedImage(self, inveon_image: InveonImage) -> str:
        rtn = ""
        delimiter = ""

        normalization_applied = inveon_image.get_metadata_element("normalization_applied")
        if normalization_applied is not None and normalization_applied != "0":
            rtn = f"{rtn}{delimiter}NORM"
            delimiter = "\\"

        attenuation_applied = inveon_image.get_metadata_element("attenuation_applied")
        if attenuation_applied is not None and attenuation_applied != "0":
            rtn = f"{rtn}{delimiter}ATTN"
            delimiter = "\\"

        scatter_correction = inveon_image.get_metadata_element("scatter_correction")
        if scatter_correction is not None and scatter_correction != "0":
            rtn = f"{rtn}{delimiter}SCAT"
            delimiter = "\\"

        decay_correction_applied = inveon_image.get_metadata_element("decay_correction_applied")
        if decay_correction_applied is not None and decay_correction_applied != "0":
            rtn = f"{rtn}{delimiter}DECY"
            delimiter = "\\"

        deadtime_correction_applied = inveon_image.get_metadata_element("deadtime_correction_applied")
        if deadtime_correction_applied is not None and deadtime_correction_applied != "0":
            rtn = f"{rtn}{delimiter}DTIM"
            delimiter = "\\"

        return rtn

    def calculate_NumberOfTimeSlices(self, inveon_image: InveonImage) -> int | None:
        series_type = self.calculate_SeriesType(inveon_image)
        if not series_type.startswith("DYNAMIC"):
            return None

        time_frames = inveon_image.get_metadata_element("time_frames")
        if time_frames is not None:
            return int(time_frames)
        else:
            return None

    def create_frame_of_reference_module(self, inveon_image: InveonImage) -> FrameOfReferenceModule:
        frame_of_reference_uid = generate_uid()
        position_reference_indicator = ""

        m = FrameOfReferenceModule(
            frame_of_reference_uid,
            position_reference_indicator
        )
        return m

    def create_pet_isotope_module(self, inveon_image: InveonImage) -> PETIsotopeModule:
        radionuclide_code_dataset = self.calculate_RadionuclideCodeSequence(inveon_image)
        m = PETIsotopeModule(radionuclide_code_dataset)

        return m


    def calculate_RadionuclideCodeSequence(self, inveon_image: InveonImage) -> Dataset :

       isotope = inveon_image.get_metadata_element("isotope")
       ds      = Dataset()
       if isotope == "F-18":
           ds.CodeValue              = "C-111A1"
           ds.CodingSchemeDesignator = "SNM3"
           ds.CodeMeaning            = "^18^Fluorine"

       return ds


    def create_nm_patient_orientation_module(self, inveon_image: InveonImage) -> NMPETPatientOrientation:
        patient_orientation = Dataset()
        patient_orientation.CodeValue              = "102538003"
        patient_orientation.CodingSchemeDesignator = "SCT"
        patient_orientation.CodeMeaning            = "Recumbent"

        # TODO Fix hard coded
        patient_gantry_relationship = Dataset()
        patient_gantry_relationship.CodeValue              = "102541007"
        patient_gantry_relationship.CodingSchemeDesignator = "SCT"
        patient_gantry_relationship.CodeMeaning            = "feet-first"

        m = NMPETPatientOrientation(patient_orientation, patient_gantry_relationship)

        return m


    def create_general_equipment_module(self, inveon_image: InveonImage) -> GeneralEquipmentModule:
        manufacturer = inveon_image.get_metadata_element("manufacturer")
        if not manufacturer:
            manufacturer = "Siemens"
        institution = inveon_image.get_metadata_element("institution")
        version = "header " + inveon_image.get_metadata_element(
            "version") + "\\" + "reconstruction " + inveon_image.get_metadata_element("recon_version")
        mfr_model_name = inveon_image.get_metadata_element("model_mapped") + ":" + inveon_image.get_metadata_element(
            "modality_configuration_mapped")

        m = GeneralEquipmentModule(manufacturer, institution, version, mfr_model_name)
        return m

    def create_enhanced_general_equipment_module(self, inveon_image: InveonImage) -> GeneralEquipmentModule:
        manufacturer = inveon_image.get_metadata_element("manufacturer")
        if not manufacturer:
            manufacturer = "Siemens"

        mfr_model_name = inveon_image.get_metadata_element("model_mapped") + ":" + inveon_image.get_metadata_element(
            "modality_configuration_mapped")
        version = "header " + inveon_image.get_metadata_element(
            "version") + "\\" + "reconstruction " + inveon_image.get_metadata_element("recon_version")
        device_serial_number = "2024.01.01"

        m = EnhancedGeneralEquipmentModule(manufacturer, mfr_model_name, device_serial_number, version)
        return m

    def create_general_acquisition_module(self, inveon_image: InveonImage) -> GeneralAcquisitionModule:
        #        manufacturer = inveon_image.get_metadata_element("manufacturer")

        m = GeneralAcquisitionModule()
        return m

    def create_general_image_module(self, inveon_image: InveonImage) -> GeneralImageModule:
        image_comments = inveon_image.get_metadata_element("ImageComments")
        modality_mapped = inveon_image.get_metadata_element("modality_mapped")

#        instance_number = 99
#        instance_number_map = {"CT": "101", "PET": "102", "SPECT": "103"}
#
#        if (modality_mapped in instance_number_map):
#            instance_number = instance_number_map[modality_mapped]

        instance_number = self.get_instance_number()
        self.increment_instance_number()

        m = GeneralImageModule(instance_number, image_comments)
        return m

    def create_image_plane_module(self, inveon_image: InveonImage, index=0) -> ImagePlaneModule:
        pixel_spacing_row = inveon_image.get_metadata_element("pixel_size_y")
        pixel_spacing_col = inveon_image.get_metadata_element("pixel_size_x")
        image_orientation_patient = self.calculate_ImageOrientationPatient(inveon_image)
        image_position_patient = self.calculate_ImagePositionPatient(inveon_image, index)
        slice_thickness = inveon_image.get_metadata_element("pixel_size_z")

        m = ImagePlaneModule(
            pixel_spacing_row,
            pixel_spacing_col,
            image_orientation_patient,
            image_position_patient,
            slice_thickness
        )
        return m

    def calculate_ImageOrientationPatient(self, inveon_image: InveonImage) -> str:
        subject_orientation = inveon_image.get_metadata_element("subject_orientation")
        rtn = ""
        match subject_orientation:
            case "0":
                return ""
            case "3":
                return "-1\\0\\0\\0\\1\\0"
            case _:
                raise Exception(
                    f"Do not have code to calculate ImageOrientationPatient when subject_orientation is {subject_orientation}")

    def calculate_ImagePositionPatient(self, inveon_image: InveonImage, index: int) -> str:
        z_position = float(inveon_image.get_metadata_element("pixel_size_z")) * index
        return f"0\\0\\{z_position:.6f}"

    def create_image_pixel_module(self, inveon_image: InveonImage, include_pixels=True,
                                  include_all_pixels=True) -> ImagePixelModule:
        # TODO Fix hard coding
        # TODO Fix assumption that data from Inveon is 2 byte integer
        samples_per_pixel = 1
        photometric_interpretation = "MONOCHROME2"
        rows = inveon_image.get_metadata_element("y_dimension")
        columns = inveon_image.get_metadata_element("x_dimension")
        bits_allocated = 16
        bits_stored = 16
        high_bit = 15
        pixel_representation = 1

        pixel_data = None
        if (include_pixels):
            fh = inveon_image.get_pixel_fh();
            if (include_all_pixels):
                pixel_data = bytes(fh.read())
                inveon_image.close_pixel_file();
            else:
                pixel_data = bytes(fh.read(int(rows) * int(columns) * 2))

        m = ImagePixelModule(
            samples_per_pixel,
            photometric_interpretation,
            rows,
            columns,
            bits_allocated,
            bits_stored,
            high_bit,
            pixel_representation,
            pixel_data)

        return m

    def create_multiframe_functional_groups_module(self, inveon_image: InveonImage) -> ImagePixelModule:
        content_date = inveon_image.get_metadata_element("scan_time_date")
        content_time = inveon_image.get_metadata_element("scan_time_time")
        number_of_frames = int(inveon_image.get_metadata_element("z_dimension"))

        frame_acquisition_date_time = f"{content_date}{content_time}"

        frame_content_list = []
        for index in range(number_of_frames):
            frame_content_list.append(FrameContentItem(index + 1, frame_acquisition_date_time))

        m = MultiframeFunctionalGroupsModule(
            "CT",
            content_date,
            content_time,
            number_of_frames,
            frame_content_list)

        return m

    def create_multiframe_functional_groups_module_pet(self, inveon_image: InveonImage) -> ImagePixelModule:
        content_date = inveon_image.get_metadata_element("scan_time_date")
        content_time = inveon_image.get_metadata_element("scan_time_time")
        number_of_frames = int(inveon_image.get_metadata_element("z_dimension"))

        frame_acquisition_date_time = f"{content_date}{content_time}"

        frame_content_list = []
        for index in range(number_of_frames):
            frame_content_list.append(FrameContentItem(index + 1, frame_acquisition_date_time))

        m = MultiframeFunctionalGroupsModule(
            "PET",
            content_date,
            content_time,
            number_of_frames,
            frame_content_list)

        return m

    def create_acquisition_context_module(self, inveon_image: InveonImage) -> ImagePixelModule:

        m = AcquisitionContextModule()

        return m

    def create_multiframe_dimension_module(self, inveon_image: InveonImage) -> MultiframeDimensionModule:

        m = MultiframeDimensionModule()

        return m

    def create_contrast_bolus_module(self, inveon_image: InveonImage) -> ContrastBolusModule:
        #        manufacturer = inveon_image.get_metadata_element("manufacturer")

        m = ContrastBolusModule()
        return m

    def create_ct_image_module(self, inveon_image: InveonImage) -> CTImageModule:
        kvp = inveon_image.get_metadata_element("ct_xray_voltage")

        ct_source_to_detector = inveon_image.get_metadata_element("ct_source_to_detector")
        if (ct_source_to_detector != None and ct_source_to_detector != ""):
            distance_source_to_detector = float(ct_source_to_detector) * 10  # Convert from cm to mm
        else:
            distance_source_to_detector = None

        ct_source_to_crot = inveon_image.get_metadata_element("ct_source_to_crot")
        if (ct_source_to_crot != None and ct_source_to_crot != ""):
            distance_source_to_patient = float(ct_source_to_crot) * 10  # Convert from cm to mm
        else:
            distance_source_to_patient = None

        # XRay Tube Current is expressed in mA in the DICOM Standard but in uA in Inveon files
        # If we calculate 0 mA, then we will set the xray_tube_current to None so that it is
        # not included in the DICOM image
        ct_anode_current = inveon_image.get_metadata_element("ct_anode_current")
        if (ct_anode_current != None and ct_anode_current != ""):
            xray_tube_current = int(int(ct_anode_current) / 1000)
            if (xray_tube_current == 0):
                xray_tube_current = None
        else:
            xray_tube_current = None

        recon_algorithm = inveon_image.get_metadata_element("recon_algorithm_mapped")

        image_type_1 = "ORIGINAL"
        image_type_2 = "PRIMARY"
        image_type_3 = "AXIAL"

        rescale_intercept = 0
        rescale_slope = 1
        acquisition_number = "1"
        m = CTImageModule(
            image_type_1,
            image_type_2,
            image_type_3,
            rescale_intercept,
            rescale_slope,
            kvp,
            distance_source_to_detector,
            distance_source_to_patient,
            xray_tube_current,
            acquisition_number,
            recon_algorithm)
        return m

    def create_enhanced_ct_image_module(self, inveon_image: InveonImage) -> EnhancedCTImageModule:
        image_type_1 = "ORIGINAL"
        image_type_2 = "PRIMARY"
        image_type_3 = "VOLUME"
        image_type_4 = "NONE"

        acquisition_date_time = "202405141200"
        acquisition_duration = 45

        # C.8.16.2 Common CT/MR and Photoacoustic Image Description Macro
        # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.8-131
        pixel_representation = "MONOCHROME"
        volumetric_properties = "VOLUME"
        volume_based_calculation_technique = "NONE"

        kvp = inveon_image.get_metadata_element("ct_xray_voltage")

        ct_source_to_detector = inveon_image.get_metadata_element("ct_source_to_detector")
        if (ct_source_to_detector != None and ct_source_to_detector != ""):
            distance_source_to_detector = float(ct_source_to_detector) * 10  # Convert from cm to mm
        else:
            distance_source_to_detector = None

        ct_source_to_crot = inveon_image.get_metadata_element("ct_source_to_crot")
        if (ct_source_to_crot != None and ct_source_to_crot != ""):
            distance_source_to_patient = float(ct_source_to_crot) * 10  # Convert from cm to mm
        else:
            distance_source_to_patient = None

        ct_anode_current = inveon_image.get_metadata_element("ct_anode_current")
        if (ct_anode_current != None and ct_anode_current != ""):
            xray_tube_current = int(int(ct_anode_current) / 1000)
        else:
            xray_tube_current = None

        recon_algorithm = inveon_image.get_metadata_element("recon_algorithm_mapped")

        # TODO

        content_qualification = "RESEARCH"

        rescale_intercept = 0
        rescale_slope = 1
        acquisition_number = "1"
        burned_in_annotation = "NO"
        lossy_image_compression = "00"
        presentation_lut_shape = "IDENTITY"

        m = EnhancedCTImageModule(
            image_type_1,
            image_type_2,
            image_type_3,
            image_type_4,
            acquisition_date_time,
            acquisition_duration,
            pixel_representation,
            volumetric_properties,
            volume_based_calculation_technique,

            content_qualification,
            rescale_intercept,
            rescale_slope,
            kvp,
            distance_source_to_detector,
            distance_source_to_patient,
            xray_tube_current,
            acquisition_number,
            burned_in_annotation,
            lossy_image_compression,
            presentation_lut_shape,
            recon_algorithm)
        return m

    # index: Frame index from 0 to a small number
    def create_pet_image_module(self, inveon_image: InveonImage, time_index=0, frame_index=0) -> EnhancedCTImageModule:

        # TODO fix these, all
        image_type = "ORIGINAL\\PRIMARY"
        rescale_intercept = "0"
        rescale_slope = "1.217"

        # These are OK
        frame_reference_time = self.calculate_FrameReferenceTime(inveon_image, time_index)
        image_index = self.calculate_ImageIndex(inveon_image, time_index, frame_index)
        acquisition_date = inveon_image.get_metadata_element("scan_time_date")
        acquisition_time = inveon_image.get_metadata_element("scan_time_time")
        actual_frame_duration = self.calculate_ActualFrameDuration(inveon_image, time_index, frame_index)
        decay_factor = self.calculate_DecayFactor(inveon_image, time_index)

        m = PETImageModule(
            image_type,
            rescale_intercept,
            rescale_slope,
            frame_reference_time,
            image_index,
            acquisition_date,
            acquisition_time,
            actual_frame_duration,
            decay_factor
        )
        return m

    def calculate_FrameReferenceTime(self, inveon_image: InveonImage, index: int) -> str:
        frame_start = float(inveon_image.get_frame_metadata_element(index, "frame_start"))
        frame_duration = float(inveon_image.get_frame_metadata_element(index, "frame_duration"))
        return str(1000 * (frame_start + frame_duration / 2))

    def calculate_ImageIndex(self, inveon_image: InveonImage, time_index: int, frame_index: int) -> int:
        z_dimension = int(inveon_image.get_metadata_element("z_dimension"))
        return (time_index * z_dimension) + frame_index + 1

    def calculate_ActualFrameDuration(self, inveon_image: InveonImage, time_index: int, frame_index: int) -> int:
        frame_duration = inveon_image.get_frame_metadata_element(time_index, "frame_duration")
        return int(float(frame_duration) * 1000)

    def calculate_DecayFactor(self, inveon_image: InveonImage, time_index) -> str:
        return inveon_image.get_frame_metadata_element(time_index, "decay_correction")

    def create_enhanced_pet_image_module(self, inveon_image: InveonImage) -> EnhancedCTImageModule:

        # TODO fix these, all
        image_type_1 = "ORIGINAL"
        image_type_2 = "PRIMARY"
        image_type_3 = "VOLUME"
        image_type_4 = "NONE"

        acquisition_date_time = inveon_image.get_metadata_element("scan_time_date")

        # TODO fix
        acquisition_duration = 45

        # C.8.16.2 Common CT/MR and Photoacoustic Image Description Macro
        # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.8-131
        # TODO fix hard coded values
        pixel_representation = "MONOCHROME"
        volumetric_properties = "VOLUME"
        volume_based_calculation_technique = "NONE"

        content_qualification = "RESEARCH"
        presentation_lut_shape = "IDENTITY"

        m = EnhancedPETImageModule(
            image_type_1,
            image_type_2,
            image_type_3,
            image_type_4,
            acquisition_date_time,
            acquisition_duration,
            pixel_representation,
            volumetric_properties,
            volume_based_calculation_technique,
            content_qualification,
            presentation_lut_shape)

        return m

    def create_sop_common_module(self, inveon_image: InveonImage, sop_class_uid: str) -> SOPCommonModule:
        #        manufacturer = inveon_image.get_metadata_element("manufacturer")

        m = SOPCommonModule(sop_class_uid, generate_uid())
        return m
