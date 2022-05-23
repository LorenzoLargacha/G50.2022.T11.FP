"""Module vaccine_manager"""
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appointment import VaccinationAppointment


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    class __VaccineManager:
        def __init__(self):
            pass

        def request_vaccination_id(self, patient_id: str,
                                   name_surname: str,
                                   registration_type: str,
                                   phone_number: str,
                                   age: str) -> str:
            """Register the patient into the patients file"""
            my_patient = VaccinePatientRegister(patient_id,
                                                name_surname,
                                                registration_type,
                                                phone_number,
                                                age)

            my_patient.save_patient()
            return my_patient.patient_sys_id

        def get_vaccine_date(self, input_file: str, date: str) -> str:
            """Gets an appointment for a registered patient"""
            my_sign = VaccinationAppointment.create_appointment_from_json_file(input_file, date)
            # save the date in store_date.json
            my_sign.save_appointment()
            return my_sign.date_signature

        def vaccine_patient(self, date_signature: str) -> True:
            """Register the vaccination of the patient"""
            appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)
            return appointment.register_vaccination()

        def cancel_appointment(self, input_file: str) -> str:
            """Cancel a vaccination appointment"""
            # Modificamos el appointment_status
            appointment = VaccinationAppointment.modify_appointment_from_json_file(input_file)
            # Modificamos la cita en store_date
            appointment.modify_store_date()
            return appointment.date_signature


    instance = None

    def __new__(cls):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()
        return VaccineManager.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
