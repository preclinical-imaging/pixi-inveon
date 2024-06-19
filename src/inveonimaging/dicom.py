import pydicom
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset
from pydicom.sequence import Sequence
from pydicom.uid import UID

class PatientModule:
    def __init__(
        self,
        patient_name=None,
        patient_id=None,
        patient_dob=None,
        patient_sex=None):

        self.ds = Dataset()
        self.ds.PatientName = patient_name
        self.ds.PatientID   = patient_id
        self.ds.PatientBirthDate = patient_dob
        self.ds.PatientSex  = patient_sex

    def get_dataset(self):
        return self.ds

class GeneralStudyModule:
    def __init__(
        self,
        study_instance_uid = None,
        study_date         = None,
        study_time         = None,
        referring_physician_name = None,
        study_id           = None,
        accession_number   = None,
        study_description  = None):

        self.ds = Dataset()
        self.ds.StudyInstanceUID       = study_instance_uid
        self.ds.StudyDate              = study_date
        self.ds.StudyTime              = study_time
        self.ds.ReferringPhysicianName = referring_physician_name
        self.ds.StudyID                = study_id
        self.ds.AccessionNumber        = accession_number
        self.ds.StudyDescription       = study_description

    def get_dataset(self):
        return self.ds

class GeneralSeriesModule:
    def __init__(
        self,
        modality:str           = None,
        series_instance_uid    = None,
        laterality:str         = None,
        series_number:str      = None,
        series_date:str        = None,
        series_time:str        = None,
        series_description:str = None,
        patient_position:str   = None):
        """

        :type modality: str
        :type series_instance_uid: str
        :type laterality: str
        :type series_number: str
        :type series_date: str
        :type series_time: str
        :type series_description: str
        :type patient_position: str
        """
        self.ds = Dataset()
        self.ds.Modality = modality
        self.ds.SeriesInstanceUID = series_instance_uid
        if laterality is not None:
            self.ds.Laterality = laterality
        self.ds.SeriesDate = series_date
        self.ds.SeriesTime = series_time
        self.ds.SeriesNumber = series_number
        self.ds.SeriesDescription = series_description
        if patient_position is not None:
            self.ds.PatientPosition = patient_position

    def get_dataset(self):
        return self.ds


class PETSeriesModule:
    def __init__(
        self,
        series_date,
        series_time,
        units,
        counts_source,
        series_type,
        number_of_slices,
        decay_correction,
        corrected_image,
        collimator_type,
        number_of_time_slices
    ):

        self.ds = Dataset()
        self.ds.SeriesDate      = series_date
        self.ds.SeriesTime      = series_time
        self.ds.Units           = units
        self.ds.CountsSource    = counts_source
        self.ds.SeriesType      = series_type
        self.ds.NumberOfSlices  = int(number_of_slices)
        self.ds.DecayCorrection = decay_correction
        self.ds.CorrectedImage  = corrected_image
        self.ds.CollimatorType  = collimator_type
        if (number_of_time_slices is not None):
            self.ds.NumberOfTimeSlices = number_of_time_slices

    def get_dataset(self):
        return self.ds


class PETIsotopeModule:
    def __init__(
        self,
        radionuclide_code_dataset):

        self.ds = Dataset()

        ds = Dataset()
        ds.RadionuclideCodeSequence = Sequence([radionuclide_code_dataset])
        self.ds.RadiopharmaceuticalInformationSequence = Sequence([ds])

    def get_dataset(self):
        return self.ds

class NMPETPatientOrientation:
    def __init__(
        self,
        patient_orientation: Dataset,
        patient_gantry_relationship: Dataset
    ):

        self.ds = Dataset()
        self.ds.PatientOrientationCodeSequence = Sequence([patient_orientation])
        self.ds.PatientGantryRelationshipCodeSequence = Sequence([patient_gantry_relationship])

    def get_dataset(self):
        return self.ds


class FrameOfReferenceModule:
    def __init__(
        self,
        frame_of_reference_uid = None,
        position_reference_indicator = None):

        self.ds = Dataset()
        self.ds.FrameOfReferenceUID        = frame_of_reference_uid
        self.ds.PositionReferenceIndicator = position_reference_indicator

    def get_dataset(self):
        return self.ds
class GeneralEquipmentModule:
    def __init__(
        self,
        manufacturer=None,
        institution_name=None,
        software_versions=None,
        manufacturer_model_name=None):

        self.ds = Dataset()
        self.ds.Manufacturer = manufacturer
        self.ds.InstitutionName = institution_name
        self.ds.SoftwareVersions = software_versions
        self.ds.ManufacturerModelName = manufacturer_model_name

    def get_dataset(self):
        return self.ds

class EnhancedGeneralEquipmentModule:
    def __init__(
        self,
        manufacturer=None,
        manufacturer_model_name=None,
        device_serial_number=None,
        software_versions=None):

        self.ds = Dataset()
        self.ds.Manufacturer = manufacturer
        self.ds.ManufacturerModelName = manufacturer_model_name
        self.ds.DeviceSerialNumber = device_serial_number
        self.ds.SoftwareVersions = software_versions


    def get_dataset(self):
        return self.ds


class GeneralAcquisitionModule:
    def __init__(
        self):

        self.ds = Dataset()
    def get_dataset(self):
        return self.ds

class GeneralImageModule:
    def __init__(
        self,
        instance_number,
        image_comments):

        self.ds = Dataset()
        self.ds.InstanceNumber = instance_number
        self.ds.ImageComments  = image_comments

    def get_dataset(self):
        return self.ds

class ImagePlaneModule:
    def __init__(
        self,
        pixel_spacing_row,
        pixel_spacing_col,
        image_orientation_patient,
        image_position_patient,
        slice_thickness):

        self.ds = Dataset()
        self.ds.PixelSpacing = pixel_spacing_row + "\\" + pixel_spacing_col
        self.ds.ImageOrientationPatient = image_orientation_patient
        self.ds.ImagePositionPatient    = image_position_patient
        self.ds.SliceThickness          = slice_thickness

    def get_dataset(self):
        return self.ds

class ImagePixelModule:
    def __init__(
        self,
        samples_per_pixel,
        photometric_interpretation,
        rows,
        columns,
        bits_allocated,
        bits_stored,
        high_bit,
        pixel_representation,
        pixel_data):

        self.ds = Dataset()

        self.ds.SamplesPerPixel     = samples_per_pixel
        self.ds.PhotometricInterpretation = photometric_interpretation
        self.ds.Rows                = int(rows)
        self.ds.Columns             = int(columns)
        self.ds.BitsAllocated       = bits_allocated
        self.ds.BitsStored          = bits_stored
        self.ds.HighBit             = high_bit
        self.ds.PixelRepresentation = pixel_representation
        if (pixel_data is not None):
            self.ds.PixelData           = pixel_data

    def get_dataset(self):
        return self.ds

class ContrastBolusModule:
    def __init__(
        self):

        self.ds = Dataset()
    def get_dataset(self):
        return self.ds


class EnhancedContrastBolusModule:
    def __init__(
        self):

        self.ds = Dataset()
    def get_dataset(self):
        return self.ds


class MultiframeFunctionalGroupsModule:
    def __init__(
        self,
        modality,
        content_date     = None,
        content_time     = None,
        number_of_frames = None,
        frame_content_list = None):

        self.ds = Dataset()

        self.ds.InstanceNumber = 1
        self.ds.ContentDate    = content_date
        self.ds.ContentTime    = content_time
        self.ds.NumberOfFrames = number_of_frames
        if (modality == "CT"):
            self.ds.SharedFunctionalGroupsSequence   = Sequence([self.fill_shared_functional_groups_sequence_ct()])
        else:
            self.ds.SharedFunctionalGroupsSequence = Sequence([self.fill_shared_functional_groups_sequence_pet()])
        self.ds.PerFrameFunctionalGroupsSequence = Sequence(self.fill_per_frame_functional_groups_sequence(frame_content_list))

    def fill_shared_functional_groups_sequence_ct(self):
        d = Dataset()
        d.PixelMeasuresSequence     = Sequence([self.fill_pixel_measures_sequence()])
        d.CTImageFrameTypeSequence  = Sequence([self.fill_ct_image_frame_type_sequence()])
        d.PlaneOrientationSequence  = Sequence([self.fill_plane_orientation_sequence()])
        d.PlanePositionSequence     = Sequence([self.fill_plane_position_sequence()])
        return d

    def fill_shared_functional_groups_sequence_pet(self):
        d = Dataset()
        d.PixelMeasuresSequence     = Sequence([self.fill_pixel_measures_sequence()])
        d.PETFrameTypeSequence      = Sequence([self.fill_pet_frame_type_sequence()])
        d.PlaneOrientationSequence  = Sequence([self.fill_plane_orientation_sequence()])
        d.PlanePositionSequence     = Sequence([self.fill_plane_position_sequence()])
        return d

    def fill_per_frame_functional_groups_sequence(self, frame_content_list):

        functional_groups_list = []

        for index in range(len(frame_content_list)):
            d = Dataset()
            d.FrameContentSequence = Sequence([self.fill_frame_content_sequence(index+1, frame_content_list[index])])
            d.UnassignedPerFrameConvertedAttributesSequence = Sequence([self.fill_unassigned_per_frame_converted_attributes_sequence(index+1,frame_content_list[index])])
            functional_groups_list.append(d)

        return functional_groups_list

    def fill_pixel_measures_sequence(self):
        dataset = Dataset()
        dataset.PixelSpacing = "1\\1"
        dataset.SliceThickness = "0.05"
        dataset.SpacingBetweenSlices = "0.05"

        return dataset

    def fill_frame_content_sequence(self, index, frame_content):
        dataset = Dataset()

        # TODO
#        dataset.InStackPositionNumber    = index
        dataset.FrameReferenceDateTime   = "202405201200"
        dataset.FrameAcquisitionDateTime = "202405201200"
        dataset.FrameAcquisitionDuration = 100
        dataset.FrameAcquisitionNumber   = index

        return dataset

    def fill_unassigned_per_frame_converted_attributes_sequence(self, index, frame_content):
        dataset = Dataset()

        dataset.DistanceSourceToDetector = 400.
        dataset.DistanceSourceToPatient  = 380.
        dataset.FilterType               = "None"
        dataset.RevolutionTime           = 99
        dataset.InstanceNumber           = index

        return dataset


    def fill_ct_image_frame_type_sequence(self):
        dataset = Dataset()
        dataset.FrameType                       = "ORIGINAL\\PRIMARY\\WHOLE_BODY\\NONE"
        dataset.PixelPresentation               = "MONOCHROME"
        dataset.VolumetricProperties            = "VOLUME"
        dataset.VolumeBasedCalculationTechnique = "NONE"

        return dataset

    def fill_pet_frame_type_sequence(self):
        dataset = Dataset()
        dataset.FrameType                       = "ORIGINAL\\PRIMARY\\WHOLE_BODY\\NONE"
        dataset.PixelPresentation               = "MONOCHROME"
        dataset.VolumetricProperties            = "VOLUME"
        dataset.VolumeBasedCalculationTechnique = "NONE"

        return dataset


    def fill_plane_orientation_sequence(self):
        dataset = mergeDatasets()
        dataset.ImageOrientationPatient = "-1\\0\\0\\0\\-1\\0"

        return dataset


    def fill_plane_position_sequence(self):
        dataset = mergeDatasets()
        dataset.ImagePositionPatient = "20.037376\\20.037224\\-109.937187"

        return dataset

    def get_dataset(self):
        return self.ds

class MultiframeDimensionModule:
    def __init__(
        self):

        self.ds = Dataset()

        dimension_org_sequence = Dataset()
        ## TODO
        dimension_org_sequence.DimensionOrganizationUID = "1.2.3.4"

        self.ds.DimensionOrganizationSequence = Sequence([dimension_org_sequence])
        self.ds.DimensionOrganizationType     = "3D"

    def get_dataset(self):
        return self.ds


class AcquisitionContextModule:
    def __init__(self):

        self.ds = Dataset()
        self.ds.AcquisitionContextSequence = Sequence([])

    def get_dataset(self):
        return self.ds


class CTImageModule:
    def __init__(
        self,
        image_type_1       = None,
        image_type_2       = None,
        image_type_3       = None,
        rescale_intercept  = None,
        rescale_slope      = None,
        kvp                = None,
        dist_source_to_det = None,
        dist_source_to_pat = None,
        xray_tube_current  = None,
        acquisition_number = None,
        convolution_kernel = None):

        self.ds = Dataset()

        self.ds.ImageType         = image_type_1 + "\\" + image_type_2 + "\\" + image_type_3
        self.ds.RescaleIntercept  = rescale_intercept
        self.ds.RescaleSlope      = rescale_slope
        self.ds.KVP               = kvp
        if (xray_tube_current != None):
            self.ds.XRayTubeCurrent = xray_tube_current

        if (dist_source_to_det != None):
            self.ds.DistanceSourceToDetector = dist_source_to_det

        if (dist_source_to_pat != None):
            self.ds.DistanceSourceToPatient = dist_source_to_pat

        self.ds.AcquisitionNumber = acquisition_number
        self.ds.ConvolutionKernel = convolution_kernel[:16]

    def get_dataset(self):
        return self.ds

class EnhancedCTImageModule:
    def __init__(
            self,
            image_type_1,
            image_type_2,
            image_type_3,
            image_type_4,
            acquisition_date_time,
            acquisition_duration,
            pixel_representation,
            volumetric_properties,
            volume_based_calculation_technique,
            content_qualification=None,
            rescale_intercept=None,
            rescale_slope=None,
            kvp=None,
            dist_source_to_det=None,
            dist_source_to_pat=None,
            xray_tube_current=None,
            acquisition_number=None,
            burned_in_annotation=None,
            lossy_image_compression=None,
            presentation_lut_shape=None,
            convolution_kernel=None):

        self.ds = Dataset()

        self.ds.ImageType = image_type_1 + "\\" + image_type_2 + "\\" + image_type_3 + "\\" + image_type_4
        self.ds.AcquisitionDateTime = acquisition_date_time
        self.ds.AcquisitionDuration = acquisition_duration

        # C.8.16.2 Common CT/MR and Photoacoustic Image Description Macro
        # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.8-131
        self.ds.PixelPresentation               = pixel_representation
        self.ds.VolumetricProperties            = volumetric_properties
        self.ds.VolumeBasedCalculationTechnique = volume_based_calculation_technique

        self.ds.ContentQualification = content_qualification

        # TODO
        #self.ds.RescaleIntercept = rescale_intercept
        #self.ds.RescaleSlope = rescale_slope

        # TODO
        #self.ds.KVP = kvp
        # TODO
        #if (xray_tube_current != None):
        #    self.ds.XRayTubeCurrent = xray_tube_current

        # TODO
        #if (dist_source_to_det != None):
        #    self.ds.DistanceSourceToDetector = dist_source_to_det
        # TODO
        #if (dist_source_to_pat != None):
        #    self.ds.DistanceSourceToPatient = dist_source_to_pat

        self.ds.AcquisitionNumber     = acquisition_number
        self.ds.BurnedInAnnotation    = burned_in_annotation
        self.ds.LossyImageCompression = lossy_image_compression
        self.ds.PresentationLUTShape  = presentation_lut_shape
        # TODO
        #self.ds.ConvolutionKernel     = convolution_kernel[:16]

    def get_dataset(self):
        return self.ds


class PETImageModule:
    def __init__(
            self,
            image_type,
            rescale_intercept,
            rescale_slope,
            frame_reference_time,
            image_index: int,
            acquisition_date: str,
            acquisition_time: str,
            actual_frame_duration: str,
            decay_factor: str
            ):

        self.ds = Dataset()

        self.ds.ImageType           = image_type
        self.ds.RescaleIntercept    = rescale_intercept
        self.ds.RescaleSlope        = rescale_slope
        self.ds.FrameReferenceTime  = frame_reference_time
        self.ds.ImageIndex          = image_index
        self.ds.AcquisitionDate     = acquisition_date
        self.ds.AcquisitionTime     = acquisition_time
        self.ds.ActualFrameDuration = actual_frame_duration
        if (decay_factor is not None):
            self.ds.DecayFactor     = decay_factor


    def get_dataset(self):
        return self.ds

class EnhancedPETImageModule:
    def __init__(
            self,
            image_type_1,
            image_type_2,
            image_type_3,
            image_type_4,
            acquisition_date_time,
            acquisition_duration,
            pixel_representation,
            volumetric_properties,
            volume_based_calculation_technique,
            content_qualification=None,
            presentation_lut_shape=None
            ):

        self.ds = Dataset()

        self.ds.ImageType = image_type_1 + "\\" + image_type_2 + "\\" + image_type_3 + "\\" + image_type_4
        self.ds.AcquisitionDateTime = acquisition_date_time
        self.ds.AcquisitionDuration = acquisition_duration

        # C.8.16.2 Common CT/MR and Photoacoustic Image Description Macro
        # https://dicom.nema.org/medical/dicom/current/output/html/part03.html#table_C.8-131
        self.ds.PixelPresentation               = pixel_representation
        self.ds.VolumetricProperties            = volumetric_properties
        self.ds.VolumeBasedCalculationTechnique = volume_based_calculation_technique

        self.ds.ContentQualification = content_qualification
        self.ds.PresentationLUTShape = presentation_lut_shape

    def get_dataset(self):
        return self.ds



class SOPCommonModule:
    def __init__(
        self,
        sop_class_uid=None,
        sop_instance_uid=None):

        self.ds = Dataset()
        self.ds.SOPClassUID    = UID(sop_class_uid)
        self.ds.SOPInstanceUID = UID(sop_instance_uid)

    def get_dataset(self):
        return self.ds

class FrameContentItem:
    def __init__(
        self,
        frame_acquisition_number,
        frame_acquisition_date_time):

        self.ds = Dataset()
        self.ds.FrameAcquisitionNumber   = frame_acquisition_number
        self.ds.FrameAcquisitionDateTime = frame_acquisition_date_time

    def get_dataset(self):
        return self.ds

def mergeDatasets(*arguments) -> Dataset:
    ds = Dataset()
    for arg in arguments:
        if arg is not None:
            if (isinstance(arg, Dataset)):
                for elem in arg:
                    ds.add(elem)
            else:
                for elem in arg.get_dataset():
                    ds.add(elem)

    return ds

def mergeDatasetsVerbose(*arguments) -> Dataset:
    ds = Dataset()
    for dataset in arguments:
        if dataset is not None:
            print(dataset)
            for elem in dataset.get_dataset():
                print(elem)
                ds.add(elem)

    return ds