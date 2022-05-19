"""Classs for the attribute Date"""
from datetime import datetime
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class AppointmentDate(Attribute):
    """Classs for the attribute Date"""
    _validation_error_message = "wrong date format"

    def _validate(self, attr_value):
        """overrides the validate method to include the valiation of the appointment date"""
        try:
            appointment_date = datetime.fromisoformat(attr_value)
        except ValueError as val_er:
            raise VaccineManagementException(self._validation_error_message) from val_er

        appointment_time_stamp = datetime.timestamp(appointment_date)
        appointment_days = (appointment_time_stamp/3600)/24

        today_time_stamp = datetime.timestamp(datetime.utcnow())
        today_days = (today_time_stamp/3600)/24

        if appointment_days <= today_days:
            raise VaccineManagementException("date should be after today")

        return appointment_time_stamp
