"""Contains the class Vaccination Appointment"""
from datetime import datetime
import hashlib
from freezegun import freeze_time
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.attribute.attribute_appointment_status import AppointmentStatus
from uc3m_care.data.attribute.attribute_appointment_date import AppointmentDate
from uc3m_care.data.attribute.attribute_cancelation_type import CancelationType
from uc3m_care.data.attribute.attribute_reason import Reason
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser
from uc3m_care.parser.cancelation_json_parser import CancelationJsonParser


class VaccinationAppointment:
    """Class representing an appointment  for the vaccination of a patient"""
    def __init__(self, patient_sys_id: str, patient_phone_number: str,
                 date: str, appointment_status="Active") -> None:
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_sys_id = PatientSystemId(patient_sys_id).value
        patient = VaccinePatientRegister.create_patient_from_patient_system_id(
            self.__patient_sys_id)
        self.__patient_id = patient.patient_id
        self.__phone_number = PhoneNumber(patient_phone_number).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        self.__appointment_date = AppointmentDate(date).value
        self.__date_signature = self.vaccination_signature
        self.__appointment_status = AppointmentStatus(appointment_status).value


    def __signature_string(self) -> str:
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appointment_date.__str__() + "}"

    @property
    def patient_id(self) -> str:
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value) -> None:
        self.__patient_id = value

    @property
    def patient_sys_id(self) -> str:
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id

    @patient_sys_id.setter
    def patient_sys_id(self, value) -> None:
        self.__patient_sys_id = value

    @property
    def phone_number(self) -> str:
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: str) -> None:
        self.__phone_number = PhoneNumber(value).value

    @property
    def vaccination_signature(self) -> str:
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self) -> float:
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value: float) -> None:
        self.__issued_at = value

    @property
    def appointment_date(self) -> float:
        """Returns the vaccination date"""
        return self.__appointment_date

    @property
    def date_signature(self) -> str:
        """Returns the SHA256 """
        return self.__date_signature

    @property
    def appointment_status(self) -> str:
        """Property that represents the appointment_status of an appointment"""
        return self.__appointment_status

    def save_appointment(self) -> None:
        """saves the appointment in the appointments store"""
        appointments_store = AppointmentsJsonStore()
        appointments_store.add_item(self)

    @classmethod
    def get_appointment_from_date_signature(cls, date_signature: str):
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = AppointmentsJsonStore()
        appointment_record = appointments_store.find_item(DateSignature(date_signature).value)
        if appointment_record is None:
            raise VaccineManagementException("date_signature is not found")
        freezer = freeze_time(
            datetime.fromtimestamp(appointment_record["_VaccinationAppointment__issued_at"]))
        freezer.start()
        # Obtenemos la fecha de la cita y la convertimos de timestamp a string
        appointment_date_str = datetime.fromtimestamp(
            appointment_record["_VaccinationAppointment__appointment_date"]).strftime("%Y-%m-%d")
        appointment = cls(appointment_record["_VaccinationAppointment__patient_sys_id"],
                          appointment_record["_VaccinationAppointment__phone_number"],
                          appointment_date_str,
                          appointment_record["_VaccinationAppointment__appointment_status"])
        freezer.stop()
        return appointment

    @classmethod
    def create_appointment_from_json_file(cls, json_file: str, date: str):
        """returns the vaccination appointment for the received input json file"""
        appointment_parser = AppointmentJsonParser(json_file)
        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY],
            appointment_parser.json_content[appointment_parser.CONTACT_PHONE_NUMBER_KEY],
            date)
        return new_appointment

    def is_valid_today(self) -> True:
        """returns true if today is the appointment's date"""
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(self.appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")
        return True

    def register_vaccination(self) -> True:
        """register the vaccine administration"""
        if self.is_valid_today():
            # Comprobamos que la cita no haya sido cancelada
            if self.appointment_status != "Active":
                raise VaccineManagementException(
                    "La cita para la que se intenta vacunar ha sido cancelada")
            vaccination_log_entry = VaccinationLog(self.date_signature)
            vaccination_log_entry.save_log_entry()
        return True

    @classmethod
    def modify_appointment_from_json_file(cls, input_file: str):
        """returns the vaccination appointment object for the input_file received
        and modifies the appointment_status"""
        # Intentamos abrir el fichero de entrada, validamos las keys y guardamos sus datos
        cancelation_parser = CancelationJsonParser(input_file)
        # Comprobamos que solo haya una solicitud de cancelacion con tres keys
        if not len(cancelation_parser.json_content) == 3:
            raise VaccineManagementException("Estructura JSON incorrecta")
        # Obtenemos los valores del diccionario y los validamos
        date_signature = DateSignature(
            cancelation_parser.json_content[cancelation_parser.DATE_SIGNATURE_KEY]).value
        cancelation_type = CancelationType(
            cancelation_parser.json_content[cancelation_parser.CANCELATION_TYPE_KEY]).value
        Reason(cancelation_parser.json_content[cancelation_parser.REASON_KEY])
        # Buscamos la cita en store_date, y si existe creamos un objeto tipo VaccinationAppoinment
        appointment = cls.get_appointment_from_date_signature(date_signature)
        # Modificamos el status de la cita en el objeto y en el fichero store_date
        appointment.modify_appointment_status(cancelation_type)
        return appointment

    def modify_appointment_status(self, cancelation_type: str) -> None:
        """Modifica el status de la cita en el objeto VaccinationAppoinment"""
        # Comprobamos si la fecha de la cita recibida ya ha pasado
        appointment_days = (self.__appointment_date / 3600) / 24
        today_time_stamp = datetime.timestamp(datetime.utcnow())
        today_days = (today_time_stamp / 3600) / 24
        if appointment_days < today_days:
            raise VaccineManagementException("La fecha de la cita recibida ya ha pasado")

        # Comprobamos si ya se ha administrado la vacuna
        vaccination_store = VaccinationJsonStore()
        if vaccination_store.find_item(self.__date_signature) is not None:
            raise VaccineManagementException("Ya se ha administrado la vacuna")

        # Si la cita esta activa
        if self.__appointment_status == "Active":
            # Se puede cancelar de forma Temporal o Final
            if cancelation_type == "Temporal":
                self.__appointment_status = "Cancelled Temporal"
            elif cancelation_type == "Final":
                self.__appointment_status = "Cancelled Final"
        # Si la cita esta cancelada de forma Temporal
        elif self.__appointment_status == "Cancelled Temporal":
            # Si era Temporal se puede cancelar como Final
            if cancelation_type == "Final":
                self.__appointment_status = "Cancelled Final"
            # Si se intenta volver a cancelar como Temporal lanzamos una excepcion
            elif cancelation_type == "Temporal":
                raise VaccineManagementException("Cita ya cancelada de forma Temporal")
        # Si la cita esta cancelada de forma Final lanzamos una excepcion
        elif self.__appointment_status == "Cancelled Final":
            raise VaccineManagementException("Cita ya cancelada de forma Final")

    def modify_store_date(self) -> None:
        """Modifica el status de la cita en store_date"""
        appointments_store = AppointmentsJsonStore()
        appointments_store.update_item(self, self.__date_signature)
