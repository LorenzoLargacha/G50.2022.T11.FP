"""Module for testing cancel_appointment method"""
import unittest
from unittest import TestCase
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_RF2_PATH, JSON_FILES_CANCEL_PATH

from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.patients_json_store import PatientsJsonStore
from uc3m_care.storage.json_store import JsonStore


param_list_ok = [("test_ok_1.json","Temporal", "JSON Decode Error - Wrong JSON Format"),
                 ("test_ok_2.json", "Final", "JSON Decode Error - Wrong JSON Format"),
                 ("test_ok_3.json", "Temporal", "JSON Decode Error - Wrong JSON Format"),
                 ("test_ok_4.json", "Temporal", "JSON Decode Error - Wrong JSON Format")]

param_list_nok = [("test_nok_1.json","Error "),
                  ("test_nok_2.json", "Error "),
                  ("test_nok_3.json", "Error "),
                  ("test_nok_4.json", "Error "),
                  ("test_nok_5.json", "Error "),
                  ("test_nok_6.json", "Error "),
                  ("test_nok_7.json", "Error "),
                  ("test_nok_8.json", "Error"),
                  ("test_nok_9.json", "Error "),
                  ("test_nok_10.json", "Error "),
                  ("test_nok_11.json", "Error "),
                  ("test_nok_13.json", "Error "),
                  ("test_nok_14.json", "Error ")]

class TestCancelAppointment(TestCase):
    """Class for testing cancel_appointment"""
    @staticmethod
    @freeze_time("2022-03-08")
    def setup():
        """first prepare the stores"""

        file_store_patient = PatientsJsonStore()
        file_store_date = AppointmentsJsonStore()

        file_store_date.delete_json_file()
        file_store_patient.delete_json_file()
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        date = "2022-03-18"
        # add patient and date in the store
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

    def test_cancel_appointment_ok_parameter(self):
        """test ok parametrizado"""
        my_manager = VaccineManager()
        for file_name, type, expected_value in param_list_ok:
            with self.subTest(test=file_name):
                # preparamos los stores
                self.setup()
                file_store_date = AppointmentsJsonStore()
                file_test = JSON_FILES_CANCEL_PATH + file_name
                # Comprobamos que devuelve la date_signature correcta
                value = my_manager.cancel_appointment(file_test)
                self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
                # Buscamos en store_date el tipo de cancelación
                appointment_item = file_store_date.find_item("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1")
                found = False
                if appointment_item is not None:
                    if appointment_item["_VaccinationAppointment__cancelation_type"] == type:
                        found = True
                # Comprobamos que se ha cambiado correctamente
                self.assertTrue(found)
            print(file_name)

    def test_cancel_appointment_nok_parameter(self):
        """test no ok parametrizado"""
        my_manager = VaccineManager()
        for file_name, expected_value in param_list_nok:
            with self.subTest(test=file_name):
                self.setup()
                file_store_date = AppointmentsJsonStore()
                # read the file
                hash_original = file_store_date.data_hash()
                file_test = JSON_FILES_CANCEL_PATH + file_name
                # check the method
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(file_test)
                self.assertEqual(c_m.exception.message, expected_value)
                # read the file again to compare
                hash_new = file_store_date.data_hash()
                self.assertEqual(hash_new, hash_original)
            print(file_name)

    def test_cancel_appointment_nok_12(self):
        """test no ok: los datos introducidos son correctos pero store_date no cambia"""
        my_manager = VaccineManager()
        # preparamos los stores
        self.setup()
        #terminar...



if __name__ == '__main__':
    unittest.main()
