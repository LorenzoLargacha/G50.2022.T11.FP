"""Tests for singleton patter"""
import unittest
from uc3m_care import VaccineManager
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
from uc3m_care.storage.patients_json_store import PatientsJsonStore
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore

param_list = [VaccineManager(), VaccinationJsonStore(),
              PatientsJsonStore(), AppointmentsJsonStore()]


class MyTestCase(unittest.TestCase):
    """Tests for singleton pattern"""
    def test_parametrized_singleton(self):
        """testing singleton for VaccineManager, PatientsJsonStore, AppointmentsJsonStore and VaccinationJsonStore"""
        for singleton_class in param_list:
            vm1 = singleton_class
            vm2 = singleton_class
            vm3 = singleton_class
            vm4 = singleton_class

            self.assertEqual(id(vm1), id(vm2))
            self.assertEqual(id(vm1), id(vm3))
            self.assertEqual(id(vm1), id(vm4))


if __name__ == '__main__':
    unittest.main()
