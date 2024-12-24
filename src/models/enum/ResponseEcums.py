from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS ="file_validated_success"
    FILE_TYPE_NOT_SUPPORTED ="file_type not supported"
    FILE_SIZE_EXCEEDS = "file_size exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload success"
    FILE_UPLOAD_FAILED = "file_upload failed"
    PROCESSING_SUCCESS = "processing success"
    PROCESSING_FAILED = "processing failed"
    NO_FILES_ERROR = "not_found_files"
    FILE_ID_ERROR = "no_file_found_with_this_id"

