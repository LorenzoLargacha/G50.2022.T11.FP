"""Module cancelation_json_parser"""
from uc3m_care.parser.json_parser import JsonParser


class CancelationJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of cancel_appointment"""
    BAD_DATE_SIGNATURE_LABEL_ERROR = "Bad label date_signature"
    BAD_CANCELATION_TYPE_LABEL_ERROR = "Bad label cancelation_type"
    BAD_REASON_LABEL_ERROR = "Bad label reason"
    DATE_SIGNATURE_KEY = "date_signature"
    CANCELATION_TYPE_KEY = "cancelation_type"
    REASON_KEY = "reason"

    _JSON_KEYS = [DATE_SIGNATURE_KEY, CANCELATION_TYPE_KEY, REASON_KEY]
    _ERROR_MESSAGES = [BAD_DATE_SIGNATURE_LABEL_ERROR,
                       BAD_CANCELATION_TYPE_LABEL_ERROR, BAD_REASON_LABEL_ERROR]
