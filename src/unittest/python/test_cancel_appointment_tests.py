"""Module for testing cancel_appointment method"""
import unittest
from unittest import TestCase
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_RF2_PATH, JSON_FILES_CANCEL_PATH

from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.patients_json_store import PatientsJsonStore
#from uc3m_care.storage.json_store import JsonStore


param_list_ok = [("test_ok_1.json", "Temporal", "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", "test_ok_1"),
                 ("test_ok_2.json", "Final", "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", "test_ok_2"),
                 ("test_ok_3.json", "Temporal", "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", "test_ok_3"),
                 ("test_ok_4.json", "Temporal", "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", "test_ok_4")]

param_list_nok = [("test_nok_1.json", "Error ", "test_nok_1"),
                  ("test_nok_2.json", "Error ", "test_nok_2"),
                  ("test_nok_3.json", "Error ", "test_nok_3"),
                  ("test_nok_4.json", "Error ", "test_nok_4"),
                  ("test_nok_5.json", "Error ", "test_nok_5"),
                  ("test_nok_6.json", "Error ", "test_nok_6"),
                  ("test_nok_7.json", "Error ", "test_nok_7"),
                  ("test_nok_8.json", "Error", "test_nok_8"),
                  ("test_nok_9.json", "Error ", "test_nok_9"),
                  ("test_nok_10.json", "Error ", "test_nok_10"),
                  ("test_nok_11.json", "Error ", "test_nok_11"),
                  ("test_nok_12.json", "Error ", "test_nok_12"),
                  ("test_no_ruta.json", "Error ", "test_nok_14"),
                  ("test_nok_15.json", "Error ", "test_nok_15")]

class TestCancelAppointment(TestCase):
    """Class for testing cancel_appointment"""

    @staticmethod
    @freeze_time("2022-03-08")
    def setup():
        """Method to prepare the stores"""
        file_store_patient = PatientsJsonStore()
        file_store_date = AppointmentsJsonStore()

        file_store_patient.delete_json_file()
        file_store_date.delete_json_file()

        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        date = "2022-03-18"
        # Añadimos los pacientes y las citas en los stores
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima", "Regular",
                                          "+34123456789", "6")
        my_manager.get_vaccine_date(file_test, date)

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax", "Family",
                                          "+34333456789", "7")
        file_test = JSON_FILES_RF2_PATH + "test_ok_2.json"
        my_manager.get_vaccine_date(file_test, date)

    @freeze_time("2022-03-08")
    def test_cancel_appointment_ok_parameter(self):
        """test_ok 1-4. Tests validos de la funcion cancel_appointment (parametrizados)"""
        my_manager = VaccineManager()
        for file_name, cancel_type, expected_value, test_id in param_list_ok:
            with self.subTest(test=test_id):
                # Preparamos los stores
                self.setup()
                file_store_date = AppointmentsJsonStore()
                file_test = JSON_FILES_CANCEL_PATH + file_name
                # Comprobamos que el método devuelve la date_signature correcta
                value = my_manager.cancel_appointment(file_test)
                self.assertEqual(value, expected_value)
                # Buscamos en store_date la date_signature de la cita
                appointment_item = file_store_date.find_item(expected_value)
                found = False
                # si encontramos la date_signature
                if appointment_item is not None:
                    # comprobamos si el cancelation_type es el esperado
                    if appointment_item["_VaccinationAppointment__cancelation_type"] == cancel_type:
                        found = True
                # Comprobamos que se ha modificado el cancelation_type correctamente
                self.assertTrue(found)
                # Mostramos el id del test que se ha ejecutado
                print(test_id)

    @freeze_time("2022-03-08")
    def test_cancel_appointment_nok_parameter(self):
        """test_nok 1-12, 14-15. Tests no validos de la funcion cancel_appointment (parametrizados)"""
        my_manager = VaccineManager()
        for file_name, expected_value, test_id in param_list_nok:
            with self.subTest(test=test_id):
                # Preparamos los stores
                self.setup()
                file_store_date = AppointmentsJsonStore()
                file_test = JSON_FILES_CANCEL_PATH + file_name
                # Leemos el fichero store_date original
                hash_original = file_store_date.data_hash()
                # Comprobamos que el método devuelve la excepcion esperada
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(file_test)
                self.assertEqual(c_m.exception.message, expected_value)
                # Volvemos a leer el fichero store_date para comparar
                hash_new = file_store_date.data_hash()
                # Comprobamos que el fichero store_date no haya cambiado
                self.assertEqual(hash_new, hash_original)
                # Mostramos el id del test que se ha ejecutado
                print(test_id)

    @freeze_time("2022-03-08")
    def test_cancel_appointment_nok_13(self):
        """test_nok_13. Los datos introducidos son correctos pero store_date no cambia"""
        my_manager = VaccineManager()
        # Preparamos los stores
        self.setup()
        file_store_date = AppointmentsJsonStore()
        file_test = JSON_FILES_CANCEL_PATH + "test_ok_1.json"
        # Cancelamos la cita de vacunacion del paciente
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        # Leemos el fichero store_date
        hash_original = file_store_date.data_hash()
        # Volvemos a intentar cancelar la cita
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        # Comprobamos que el método devuelve la excepcion esperada
        self.assertEqual(c_m.exception.message, "cita ya cancelada anteriormente")
        # Volvemos a leer el fichero store_date para comparar
        hash_new = file_store_date.data_hash()
        # Comprobamos que el fichero store_date no haya cambiado
        self.assertEqual(hash_new, hash_original)



if __name__ == '__main__':
    unittest.main()
