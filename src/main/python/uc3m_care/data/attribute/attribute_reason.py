"""Classs for the attribute FullName"""
from uc3m_care.data.attribute.attribute import Attribute


class Reason(Attribute):
    """Classs for the attribute FullName"""
    _validation_pattern = r".{2,100}"
    _validation_error_message = "Reason is not valid"
