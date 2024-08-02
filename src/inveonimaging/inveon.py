import datetime


class InveonFrame:
    def __init__(
            self,
            frame_number:str):
        self.frame_number = frame_number
        self.metadata = {}

    def get_metadata_element(self, element_name) -> str:
        rtn = ""

        if (self.metadata[element_name] != None):
            rtn = self.metadata[element_name]

        return rtn

class InveonImage:
    def __init__(
            self,
            name:str,
            base_path=None):
        self.name = name
        self.base_path     = base_path
        self.metadata      = {}
        self.metadata["ImageComments"] = None
        self.frames        = {}
        self.current_frame = None
        self.pixel_fh      = None

    def get_pixel_fh(self):
        if (not self.pixel_fh):
            self.pixel_fh = open(self.base_path, 'rb')

        return self.pixel_fh

    def close_pixel_file(self):
        if (self.pixel_fh):
            self.pixel_fh.close();
            self.pixel_fh = None

    def add_frame(self, frame_index:str, frame:InveonFrame):
        self.frames[frame_index] = frame

    def get_frame(self, frame_index:str):
        return self.frames[frame_index]

    def get_name(self) -> str:
        return self.name

    def set_base_path(self, base_path):
        self.base_path = base_path

    def get_base_path(self) -> str:
        return self.base_path

    def get_metadata_element(self, element_name) -> str:
        rtn = ""

        if (self.metadata[element_name] != None):
            rtn = self.metadata[element_name]

        return rtn


    def get_metadata(self):
        return self.metadata

    def get_frame_metadata_element(self, index:int, element_name:str) -> str:
        inveon_frame_instance = self.get_frame(str(index))
        return inveon_frame_instance.get_metadata_element(element_name)

    def parse_header(self, base_path=None):
        if (base_path != None):
            self.base_path = base_path
        hdr_path = f"{self.base_path}.hdr"

        with open(hdr_path) as file:
            while line := file.readline():
                if self.current_frame is None:
                    self.parse_header_line(line.rstrip())
                else:
                    self.parse_frame_header_line(line.rstrip())

        return self


    def parse_frame_header_line(self, line:str) -> None:
        if (line.startswith("#")):
            return

        tokens = line.split(" ")
        if (len(tokens) == 0):
            return

        if (tokens[0] == "frame"):
            self.current_frame = tokens[1]
            new_frame = InveonFrame(self.current_frame)
            self.add_frame(self.current_frame, new_frame)
            return

        frame = self.get_frame(self.current_frame)
        if (len(tokens) == 1):
            frame.metadata[tokens[0]] = ""

        elif (len(tokens) == 2):
            frame.metadata[tokens[0]] = tokens[1]

        else:
            frame.metadata[tokens[0]] = line

        self.add_frame(self.current_frame, frame)

    def parse_header_line(self, line:str) -> None:
        if (line.startswith("#")):
            return

        tokens = line.split(" ")
        if (len(tokens) == 0):
            return

        if (tokens[0] == "frame"):
            self.current_frame = tokens[1]
            new_frame = InveonFrame(self.current_frame)
            self.add_frame(self.current_frame, new_frame)
            return

        if (len(tokens) == 1):
            self.metadata[tokens[0]] = ""

        elif (len(tokens) == 2):
            self.metadata[tokens[0]] = tokens[1]
            self.process_mapped_elements(tokens[0], tokens[1])

        else:
            self.metadata[tokens[0]] = line
            self.process_multi_token_elements(tokens[0], line)


    def process_mapped_elements(self, token:str, value:str) -> None:
        coded_elements = {"model": "CODED_MODEL", "modality": "CODED_MODALITY",
                          "modality_configuration": "CODED_MODALITY_CONFIGURATION",
                          "acquisition_mode": "CODED_ACQUISITION_MODE",
                          "recon_algorithm": "CODED_RECON_ALGORITHM",
                          "subject_orientation": "CODED_SUBJECT_ORIENTATION"
                          }
        if (token in coded_elements):
            code_table = {"model:0": "unknown",
                          "model:2000": "Primate",
                          "model:2001": "Rodent",
                          "model:2002": "microPET2",
                          "model:2500": "Focus_220",
                          "model:2501": "Focus_120",
                          "model:3000": "mCAT",
                          "model:3500": "mCATII",
                          "model:4000": "mSPECT",
                          "model:5000": "Inveon_Dedicated_PET",
                          "model:5001": "Inveon_MM_Platform",
                          "model:6000": "MR_PET_Head_Insert",
                          "model:8000": "Tuebingen_PET_MR",
                          "modality:-1": "Unknown",
                          "modality:0": "PET",
                          "modality:1": "CT",
                          "modality:2": "SPECT",
                          "modality_configuration:0":    "Unknown",

                          # These are CT values
                          "modality_configuration:3000": "mCAT",
                          "modality_configuration:3500": "mCATII",
                          "modality_configuration:3600": "Inveon_MM_Std_CT",
                          "modality_configuration:3601": "Inveon_MM_HiRes_Std_CT",
                          "modality_configuration:3602": "Inveon_MM_Std_LFOV_CT",
                          "modality_configuration:3603": "Inveon_MM_HiRes_LFOV_CT",

                          # These are PET values
                          "modality_configuration:2000": "Primate",
                          "modality_configuration:2001": "Rodent",
                          "modality_configuration:2002": "microPET2",
                          "modality_configuration:2500": "Focus_220",
                          "modality_configuration:2501": "Focus_120",
                          "modality_configuration:5000": "Inveon_Dedicated_PET",
                          "modality_configuration:5500": "Inveon_MM_PET",

                          "acquisition_mode:0": "Unknown acquisition mode",
                          "acquisition_mode:1": "Blank acquisition",
                          "acquisition_mode:2": "Emission acquisition",
                          "acquisition_mode:3": "Dynamic acquisition",
                          "acquisition_mode:4": "Gated acquisition",
                          "acquisition_mode:5": "Continuous bed motion acquisition",
                          "acquisition_mode:6": "Singles transmission acquisition",
                          "acquisition_mode:7": "Windowed coincidence transmission acquisition",
                          "acquisition_mode:8": "Non-windowed coincidence transmission acquisition",
                          "acquisition_mode:9": "CT projection acquisition",
                          "acquisition_mode:10": "CT calibration acquisition",
                          "acquisition_mode:11": "SPECT planar projection acquisitio",
                          "acquisition_mode:12": "SPECT multi-projection acquisition",
                          "acquisition_mode:13": "SPECT calibration acquisition",
                          "acquisition_mode:14": "SPECT tomography normalization acquisition",
                          "acquisition_mode:15": "SPECT detector setup acquisition",
                          "acquisition_mode:16": "SPECT scout view acquisition",
                          "acquisition_mode:17": "SPECT planar normalization acquisition",

                          "recon_algorithm:0": "Unknown, or no, algorithm type",
                          "recon_algorithm:1": "Filtered Backprojection",
                          "recon_algorithm:2": "OSEM2d",
                          "recon_algorithm:3": "OSEM3d",
                          "recon_algorithm:4": "3D Reprojection",
                          "recon_algorithm:5": "Undefined",      # Undefined
                          "recon_algorithm:6": "OSEM3D/MAP",
                          "recon_algorithm:7": "MAPTR for transmission image",
                          "recon_algorithm:8": "MAP 3D reconstruction",
                          "recon_algorithm:9": "Feldkamp cone beam",

                          "subject_orientation:0": "",
                          "subject_orientation:1": "FFP",
                          "subject_orientation:2": "HFP",
                          "subject_orientation:3": "FFS",
                          "subject_orientation:4": "HFS",
                          "subject_orientation:5": "FFDR",
                          "subject_orientation:6": "HFDR",
                          "subject_orientation:7": "FFDL",
                          "subject_orientation:8": "HFDL",



                          }

            local_key = f"{token}:{value}"
            if (local_key in code_table):
                mapped_value = code_table[local_key];
                mapped_key = token + "_mapped";
                self.metadata[mapped_key] = code_table[local_key]


    def process_multi_token_elements(self, token:str, line:str) -> None:
        if (token == "scan_time"):
            self.process_scan_time(line)
        elif (token == "x_filter") :
            self.process_xyz_filter(line)
        elif (token == "y_filter"):
            self.process_xyz_filter(line)
        elif (token == "z_filter") :
            self.process_xyz_filter(line)

    def process_scan_time(self, line:str) -> None:
        month_map = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"}
        tokens = line.split(' ')
        day  = tokens[1]
        mon  = tokens[2]
        date = tokens[3]
        time = tokens[4]
        year = tokens[5]

        date_string = year + month_map[mon] + date.zfill(2)
        time_tokens = time.split(':')
        time_string = time_tokens[0] + time_tokens[1] + time_tokens[2]

        self.metadata["scan_time_date"] = date_string
        self.metadata["scan_time_time"] = time_string

    def process_xyz_filter(self, line:str) -> None:
        filter_map = {
            "x_filter:0": "No filter",
            "x_filter:1": "Ramp filter (backprojection) or no filter",
            "x_filter:2": "First-order Butterworth window",
            "x_filter:3": "Hanning window",
            "x_filter:4": "Hamming window",
            "x_filter:5": "Parzen window",
            "x_filter:6": "Shepp filter",
            "x_filter:7": "Second-order Butterworth window",

            "y_filter:0": "No filter",
            "y_filter:2": "First-order Butterworth window",
            "y_filter:3": "Hanning window",
            "y_filter:4": "Hamming window",
            "y_filter:5": "Parzen window",
            "y_filter:7": "Second-order Butterworth window",

            "z_filter:0": "No filter",
            "z_filter:2": "First-order Butterworth window",
            "z_filter:3": "Hanning window",
            "z_filter:4": "Hamming window",
            "z_filter:5": "Parzen window",
            "z_filter:7": "Second-order Butterworth window",
        }

        tokens       = line.split(' ')
        keyword      = tokens[0]
        filter_index = tokens[1]
        cutoff_value = tokens[2]

        local_key = keyword + ":" + filter_index
        if (local_key in filter_map):
            filter_name = filter_map[local_key]
            new_filter_comments = tokens[0] + ", " + filter_name + " cutoff, " + cutoff_value

            image_comments = self.metadata["ImageComments"]
            if (image_comments == None):
                image_comments = new_filter_comments
            else :
                image_comments = image_comments + "; " + new_filter_comments
            self.metadata["ImageComments"] = image_comments


