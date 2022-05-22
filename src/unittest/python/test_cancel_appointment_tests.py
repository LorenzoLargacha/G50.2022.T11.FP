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
                 ("test_ok_4.json", "Temporal", "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", "test_ok_4"),
                 ("test_ok.json", "Temporal", "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", "test_ok_5"),
                 ("test_no_comillas12.json", "Temporal", "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", "test_ok_6")]

param_list_nok = [("test_modif_valor1.json", "Error ", "test_nok_1"),
                  ("test_nok_2.json", "Error ", "test_nok_2"),
                  ("test_nok_3.json", "Error ", "test_nok_3"),
                  ("test_nok_4.json", "Error ", "test_nok_4"),
                  ("test_nok_5.json", "Error ", "test_nok_5"),
                  ("test_modif_valor2.json", "Error ", "test_nok_6"),
                  ("test_nok_7.json", "Error ", "test_nok_7"),
                  ("test_nok_8.json", "Error", "test_nok_8"),
                  ("test_nok_9.json", "Error ", "test_nok_9"),
                  ("test_modif_valor3.json", "Error ", "test_nok_10"),
                  ("test_nok_11.json", "Error ", "test_nok_11"),
                  ("test_nok_12.json", "Error ", "test_nok_12"),
                  ("test_no_ruta.json", "File is not found", "test_nok_14"),
                  ("test_no_comillas3.json", "Error ", "test_nok_15"),
                  ("test_fichero_vacio.json", "Error ", "test_nok_16"),
                  ("test_doble_contenido.json", "Error ", "test_nok_17"),
                  ("test_no_llave_ini.json", "Error ", "test_nok_18"),
                  ("test_doble_llave_ini.json", "Error ", "test_nok_19"),
                  ("test_modif_llave_ini.json", "Error ", "test_nok_20"),
                  ("test_no_datos.json", "Error ", "test_nok_21"),
                  ("test_doble_datos.json", "Error ", "test_nok_22"),
                  ("test_no_llave_fin.json", "Error ", "test_nok_23"),
                  ("test_doble_llave_fin.json", "Error ", "test_nok_24"),
                  ("test_modif_llave_fin.json", "Error ", "test_nok_25"),
                  ("test_no_campo1.json", "Error ", "test_nok_26"),
                  ("test_doble_campo1.json", "Error ", "test_nok_27"),
                  ("test_no_separador1.json", "Error ", "test_nok_28"),
                  ("test_doble_separador1.json", "Error ", "test_nok_29"),
                  ("test_modif_separador1.json", "Error ", "test_nok_30"),
                  ("test_no_campo2.json", "Error ", "test_nok_31"),
                  ("test_doble_campo2.json", "Error ", "test_nok_32"),
                  ("test_no_separador2.json", "Error ", "test_nok_33"),
                  ("test_doble_separador2.json", "Error ", "test_nok_34"),
                  ("test_modif_separador2.json", "Error ", "test_nok_35"),
                  ("test_no_campo3.json", "Error ", "test_nok_36"),
                  ("test_doble_campo3.json", "Error ", "test_nok_37"),
                  ("test_no_etiqueta_dato1.json", "Error ", "test_nok_38"),
                  ("test_doble_etiqueta_dato1.json", "Error ", "test_nok_39"),
                  ("test_no_igualdad1.json", "Error ", "test_nok_40"),
                  ("test_doble_igualdad1.json", "Error ", "test_nok_41"),
                  ("test_modif_igualdad1.json", "Error ", "test_nok_42"),
                  ("test_no_valor_dato1.json", "Error ", "test_nok_43"),
                  ("test_doble_valor_dato1.json", "Error ", "test_nok_44"),
                  ("test_no_etiqueta_dato2.json", "Error ", "test_nok_45"),
                  ("test_doble_etiqueta_dato2.json", "Error ", "test_nok_46"),
                  ("test_no_igualdad2.json", "Error ", "test_nok_47"),
                  ("test_doble_igualdad2.json", "Error ", "test_nok_48"),
                  ("test_modif_igualdad2.json", "Error ", "test_nok_49"),
                  ("test_no_valor_dato2.json", "Error ", "test_nok_50"),
                  ("test_doble_valor_dato2.json", "Error ", "test_nok_51"),
                  ("test_no_etiqueta_dato3.json", "Error ", "test_nok_52"),
                  ("test_doble_etiqueta_dato3.json", "Error ", "test_nok_53"),
                  ("test_no_igualdad3.json", "Error ", "test_nok_54"),
                  ("test_doble_igualdad3.json", "Error ", "test_nok_55"),
                  ("test_modif_igualdad3.json", "Error ", "test_nok_56"),
                  ("test_no_valor_dato3.json", "Error ", "test_nok_57"),
                  ("test_doble_valor_dato3.json", "Error ", "test_nok_58"),
                  ("test_no_comillas1.json", "Error ", "test_nok_59"),
                  ("test_doble_comillas1.json", "Error ", "test_nok_60"),
                  ("test_modif_comillas1.json", "Error ", "test_nok_61"),
                  ("test_no_valor_etiqueta1.json", "Error ", "test_nok_62"),
                  ("test_doble_valor_etiqueta1.json", "Error ", "test_nok_63"),
                  ("test_modif_valor_etiqueta1.json", "Error ", "test_nok_64"),
                  ("test_no_comillas2.json", "Error ", "test_nok_65"),
                  ("test_doble_comillas2.json", "Error ", "test_nok_66"),
                  ("test_modif_comillas2.json", "Error ", "test_nok_67"),
                  ("test_doble_comillas3.json", "Error ", "test_nok_68"),
                  ("test_modif_comillas3.json", "Error ", "test_nok_69"),
                  ("test_no_valor1.json", "Error ", "test_nok_70"),
                  ("test_doble_valor1.json", "Error ", "test_nok_71"),
                  ("test_no_comillas4.json", "Error ", "test_nok_72"),
                  ("test_doble_comillas4.json", "Error ", "test_nok_73"),
                  ("test_modif_comillas4.json", "Error ", "test_nok_74"),
                  ("test_no_comillas5.json", "Error ", "test_nok_75"),
                  ("test_doble_comillas5.json", "Error ", "test_nok_76"),
                  ("test_modif_comillas5.json", "Error ", "test_nok_77"),
                  ("test_no_valor_etiqueta2.json", "Error ", "test_nok_78"),
                  ("test_doble_valor_etiqueta2.json", "Error ", "test_nok_79"),
                  ("test_modif_valor_etiqueta2.json", "Error ", "test_nok_80"),
                  ("test_no_comillas6.json", "Error ", "test_nok_81"),
                  ("test_doble_comillas6.json", "Error ", "test_nok_82"),
                  ("test_modif_comillas6.json", "Error ", "test_nok_83"),
                  ("test_no_comillas7.json", "Error ", "test_nok_84"),
                  ("test_doble_comillas7.json", "Error ", "test_nok_85"),
                  ("test_modif_comillas7.json", "Error ", "test_nok_86"),
                  ("test_no_valor2.json", "Error ", "test_nok_87"),
                  ("test_doble_valor2.json", "Error ", "test_nok_88"),
                  ("test_no_comillas8.json", "Error ", "test_nok_89"),
                  ("test_doble_comillas8.json", "Error ", "test_nok_90"),
                  ("test_modif_comillas8.json", "Error ", "test_nok_91"),
                  ("test_no_comillas9.json", "Error ", "test_nok_92"),
                  ("test_doble_comillas9.json", "Error ", "test_nok_93"),
                  ("test_modif_comillas9.json", "Error ", "test_nok_94"),
                  ("test_no_valor_etiqueta3.json", "Error ", "test_nok_95"),
                  ("test_doble_valor_etiqueta3.json", "Error ", "test_nok_96"),
                  ("test_modif_valor_etiqueta3.json", "Error ", "test_nok_97"),
                  ("test_no_comillas10.json", "Error ", "test_nok_98"),
                  ("test_doble_comillas10.json", "Error ", "test_nok_99"),
                  ("test_modif_comillas10.json", "Error ", "test_nok_100"),
                  ("test_no_comillas11.json", "Error ", "test_nok_101"),
                  ("test_doble_comillas11.json", "Error ", "test_nok_102"),
                  ("test_modif_comillas11.json", "Error ", "test_nok_103"),
                  ("test_no_valor3.json", "Error ", "test_nok_104"),
                  ("test_no_comillas12.json", "Error ", "test_nok_105"),
                  ("test_doble_comillas12.json", "Error ", "test_nok_106"),
                  ("test_modif_comillas12.json.json", "Error ", "test_nok_107"),
                  ("test_nok_108.json.json", "Error ", "test_nok_108")]


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
        """test_ok 1-6. Tests validos de la funcion cancel_appointment (parametrizados)"""
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
                    # comprobamos si el appointment_status es el esperado
                    if appointment_item["_VaccinationAppointment__appointment_status"] == cancel_type:
                        found = True
                # Comprobamos que se ha modificado el appointment_status correctamente
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
    def test_nok_13(self):
        """test_nok_13. Los datos introducidos son correctos pero store_date no cambia.
        Cancelamos una misma cita dos veces seguidas de forma Temporal"""
        my_manager = VaccineManager()
        # Preparamos los stores
        self.setup()
        file_store_date = AppointmentsJsonStore()
        file_test = JSON_FILES_CANCEL_PATH + "test_ok_1.json"
        expected_value = "Cita ya cancelada de forma Temporal"
        # Cancelamos la cita de vacunacion del paciente
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        # Leemos el fichero store_date
        hash_original = file_store_date.data_hash()
        # Volvemos a intentar cancelar la cita
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        # Comprobamos que el método devuelve la excepcion esperada
        self.assertEqual(c_m.exception.message, expected_value)
        # Volvemos a leer el fichero store_date para comparar
        hash_new = file_store_date.data_hash()
        # Comprobamos que el fichero store_date no haya cambiado
        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_nok_109_no_store_date(self):
        """test_nok_109. Se produce un error de procesamiento interno cuando el fichero store_date no existe"""
        my_manager = VaccineManager()
        # Borramos los stores
        file_store_patient = PatientsJsonStore()
        file_store_date = AppointmentsJsonStore()
        file_store_patient.delete_json_file()
        file_store_date.delete_json_file()

        file_test = JSON_FILES_CANCEL_PATH + "test_ok_1.json"
        expected_value = "Fichero store_date no creado"

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

    @freeze_time("2022-03-08")
    def test_ok_110_temporal_final_cancels(self):
        """test_nok_110. Los datos introducidos son correctos y store_date cambia.
        Cancelamos una cita de forma Temporal en primer lugar, y posteriormente de forma Final"""
        my_manager = VaccineManager()
        # Preparamos los stores
        self.setup()
        file_store_date = AppointmentsJsonStore()
        expected_value = "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c"
        # Cancelamos la cita de vacunacion del paciente de forma Temporal
        file_test = JSON_FILES_CANCEL_PATH + "test_ok_1.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, expected_value)
        # Cancelamos la cita de vacunacion del paciente de forma Final
        file_test = JSON_FILES_CANCEL_PATH + "test_ok_2.json"
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, expected_value)
        # Buscamos en store_date la date_signature de la cita
        appointment_item = file_store_date.find_item(expected_value)
        found = False
        # si encontramos la date_signature
        if appointment_item is not None:
            # comprobamos si el appointment_status es el esperado
            if appointment_item["_VaccinationAppointment__appointment_status"] == "Final":
                found = True
        # Comprobamos que se ha modificado el appointment_status correctamente
        self.assertTrue(found)

    @freeze_time("2022-03-08")
    def test_nok_111_final_temporal_cancels(self):
        """test_nok_111. Los datos introducidos son correctos pero store_date no cambia.
        Intentamos cancelar una cita de forma Temporal,
        que ya se había cancelado antes de forma Final"""
        my_manager = VaccineManager()
        # Preparamos los stores
        self.setup()
        file_store_date = AppointmentsJsonStore()
        file_test = JSON_FILES_CANCEL_PATH + "test_ok_2.json"
        expected_value = "Cita ya cancelada anteriormente de forma Final"
        # Cancelamos la cita de vacunacion del paciente de forma final
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        # Leemos el fichero store_date
        hash_original = file_store_date.data_hash()
        # Volvemos a intentar cancelar la cita
        file_test = JSON_FILES_CANCEL_PATH + "test_ok_1.json"
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        # Comprobamos que el método devuelve la excepcion esperada
        self.assertEqual(c_m.exception.message, expected_value)
        # Volvemos a leer el fichero store_date para comparar
        hash_new = file_store_date.data_hash()
        # Comprobamos que el fichero store_date no haya cambiado
        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_nok_112_final_final_cancels(self):
        """test_nok_112. Los datos introducidos son correctos pero store_date no cambia.
        Intentamos cancelar una cita de forma Final,
        que ya se había cancelado antes de forma Final"""
        my_manager = VaccineManager()
        # Preparamos los stores
        self.setup()
        file_store_date = AppointmentsJsonStore()
        file_test = JSON_FILES_CANCEL_PATH + "test_ok_2.json"
        expected_value = "Cita ya cancelada anteriormente de forma Final"
        # Cancelamos la cita de vacunacion del paciente de forma final
        value = my_manager.cancel_appointment(file_test)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        # Leemos el fichero store_date
        hash_original = file_store_date.data_hash()
        # Volvemos a intentar cancelar la cita de forma Final
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        # Comprobamos que el método devuelve la excepcion esperada
        self.assertEqual(c_m.exception.message, expected_value)
        # Volvemos a leer el fichero store_date para comparar
        hash_new = file_store_date.data_hash()
        # Comprobamos que el fichero store_date no haya cambiado
        self.assertEqual(hash_new, hash_original)


if __name__ == '__main__':
    unittest.main()
