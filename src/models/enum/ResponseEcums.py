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
    PROJECT_NOT_FOUND_ERROR = "project_not_found"
    INSERT_INTO_VECTORDB_ERROR = "insert_into_vectordb_error"
    INSERT_INTO_VECTORDB_SUCCESS = "insert_into_vectordb_success"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"
    RAG_ANSWER_ERROR = "rag_answer_error"
    RAG_ANSWER_SUCCESS = "rag_answer_success"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb_collection_retrieved"