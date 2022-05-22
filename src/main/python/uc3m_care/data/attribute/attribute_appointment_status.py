"""Classs for the attribute AppointmentStatus"""
from uc3m_care.data.attribute.attribute import Attribute


#pylint: disable=too-few-public-methods
class AppointmentStatus(Attribute):
    """Class for the attribute AppointmentStatus"""
    _validation_pattern = r"(Active|Cancelled Temporal|Cancelled Final)"
    _validation_error_message = "Cancelation status is not valid"
