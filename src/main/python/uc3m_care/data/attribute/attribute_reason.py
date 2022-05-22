"""Classs for the attribute FullName"""
from uc3m_care.data.attribute.attribute import Attribute

#pylint: disable=too-few-public-methods
class Reason(Attribute):
    """Classs for the attribute FullName"""
    #_validation_pattern = r"^(?=^.{2,100}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
    #_validation_pattern = r"^(?=^.{2,100}$)"
    _validation_pattern = r".{2,100}"
    #_validation_pattern = "^[A-Za-z0-9_-]*$"
    _validation_error_message = "Reason is not valid"
