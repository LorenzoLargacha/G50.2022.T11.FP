"""Module """

from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appointment import VaccinationAppointment

from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.parser.cancelation_json_parser import CancelationJsonParser
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.attribute.attribute_cancelation_type import CancelationType
from uc3m_care.data.attribute.attribute_reason import Reason

class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # pylint: disable=invalid-name
    class __VaccineManager:
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        def request_vaccination_id (self, patient_id,
                                    name_surname,
                                    registration_type,
                                    phone_number,
                                    age):
            """Register the patinent into the patients file"""
            my_patient = VaccinePatientRegister(patient_id,
                                                    name_surname,
                                                    registration_type,
                                                    phone_number,
                                                    age)

            my_patient.save_patient()
            return my_patient.patient_sys_id

        def get_vaccine_date (self, input_file, date):
            """Gets an appointment for a registered patient"""
            my_sign = VaccinationAppointment.create_appointment_from_json_file(input_file, date)
            #save the date in store_date.json
            my_sign.save_appointment()
            return my_sign.date_signature

        def vaccine_patient(self, date_signature):
            """Register the vaccination of the patient"""
            appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)
            return appointment.register_vaccination()

        def cancel_appointment(self, input_file):
            """Cancel a vaccination appointment"""
            pass

            # Intentamos abrir el fichero de entrada, validamos las keys y guardamos sus datos
            cancelation_parser = CancelationJsonParser(input_file)

            # Comprobamos la estructura del fichero JSON
            # Si la solicitud de cancelacion no se encuentra en el fichero lanzamos una excepcion
            if len(cancelation_parser.json_content) == 0:
                raise VaccineManagementException("La solicitud no se encontro en el archivo de solicitudes JSON")

            # Comprobamos que solo haya una solicitud de cancelacion con tres keys
            if not len(cancelation_parser.json_content) == 3:
                raise VaccineManagementException("Estructura JSON incorrecta")

            # Obtenemos los valores del diccionario y los validamos
            date_signature = DateSignature(cancelation_parser.json_content[cancelation_parser.DATE_SIGNATURE_KEY]).value
            cancelation_type = CancelationType(cancelation_parser.json_content[cancelation_parser.CANCELATION_TYPE_KEY]).value
            reason = Reason(cancelation_parser.json_content[cancelation_parser.REASON_KEY]).value

            # Buscamos la cita en store_date, y si existe creamos un objeto tipo VaccinationAppoinment
            appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)

            # Modificamos el status de la cita en el objeto y en el fichero store_date
            appointment.modify_appointment_status(cancelation_type)


    instance = None

    def __new__ ( cls ):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()
        return VaccineManager.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)
