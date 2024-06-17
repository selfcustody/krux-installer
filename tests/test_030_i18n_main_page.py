from unittest import TestCase
from src.i18n import T


class TestI18nMainScreen(TestCase):

    # Version
    def test_translate_version_af_za(self):
        msg = T("Version", locale="af_ZA.UTF-8", module="main_screen")
        self.assertEqual(msg, "Weergawe")

    def test_translate_version_en_us(self):
        msg = T("Version", locale="en_US.UTF-8", module="main_screen")
        self.assertEqual(msg, "Version")

    def test_translate_version_es_es(self):
        msg = T("Version", locale="es_ES.UTF-8", module="main_screen")
        self.assertEqual(msg, "Versión")

    def test_translate_version_fr_fr(self):
        msg = T("Version", locale="fr_FR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Version")

    def test_translate_version_it_it(self):
        msg = T("Version", locale="it_IT.UTF-8", module="main_screen")
        self.assertEqual(msg, "Versione")

    def test_translate_version_pt_br(self):
        msg = T("Version", locale="pt_BR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Versão")

    def test_translate_version_ru_ru(self):
        msg = T("Version", locale="ru_RU.UTF-8", module="main_screen")
        self.assertEqual(msg, "Версия")

    # Device
    def test_translate_device_af_za(self):
        msg = T("Device", locale="af_ZA.UTF-8", module="main_screen")
        self.assertEqual(msg, "Toestel")

    def test_translate_device_en_us(self):
        msg = T("Device", locale="en_US.UTF-8", module="main_screen")
        self.assertEqual(msg, "Device")

    def test_translate_device_es_es(self):
        msg = T("Device", locale="es_ES.UTF-8", module="main_screen")
        self.assertEqual(msg, "Dispositivo")

    def test_translate_device_fr_fr(self):
        msg = T("Device", locale="fr_FR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Appareil")

    def test_translate_device_it_it(self):
        msg = T("Device", locale="it_IT.UTF-8", module="main_screen")
        self.assertEqual(msg, "Dispositivo")

    def test_translate_device_pt_br(self):
        msg = T("Device", locale="pt_BR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Dispositivo")

    def test_translate_device_ru_ru(self):
        msg = T("Device", locale="ru_RU.UTF-8", module="main_screen")
        self.assertEqual(msg, "Устройство")

    # Select a new one
    def test_translate_select_a_new_one_af_za(self):
        msg = T("select a new one", locale="af_ZA.UTF-8", module="main_screen")
        self.assertEqual(msg, "kies 'n nuwe een")

    def test_translate_select_a_new_one_en_us(self):
        msg = T("select a new one", locale="en_US.UTF-8", module="main_screen")
        self.assertEqual(msg, "select a new one")

    def test_translate_select_a_new_one_es_es(self):
        msg = T("select a new one", locale="es_ES.UTF-8", module="main_screen")
        self.assertEqual(msg, "seleccione uno nuevo")

    def test_translate_select_a_new_one_fr_fr(self):
        msg = T("select a new one", locale="fr_FR.UTF-8", module="main_screen")
        self.assertEqual(msg, "sélectionnez-en un nouveau")

    def test_translate_select_a_new_one_it_it(self):
        msg = T("select a new one", locale="it_IT.UTF-8", module="main_screen")
        self.assertEqual(msg, "selezionane uno nuovo")

    def test_translate_select_a_new_one_pt_br(self):
        msg = T("select a new one", locale="pt_BR.UTF-8", module="main_screen")
        self.assertEqual(msg, "selecione um novo")

    def test_translate_select_a_new_one_ru_ru(self):
        msg = T("select a new one", locale="ru_RU.UTF-8", module="main_screen")
        self.assertEqual(msg, "выберите новый")

    # Flash
    def test_translate_flash_en_us(self):
        msg = T("Flash", locale="en_US.UTF-8", module="main_screen")
        self.assertEqual(msg, "Update firmware")

    def test_translate_flash_es_es(self):
        msg = T("Flash", locale="es_ES.UTF-8", module="main_screen")
        self.assertEqual(msg, "Programar el firmware")

    def test_translate_flash_fr_fr(self):
        msg = T("Flash", locale="fr_FR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Programmer le firmware")

    def test_translate_flash_it_it(self):
        msg = T("Flash", locale="it_IT.UTF-8", module="main_screen")
        self.assertEqual(msg, "Programmare il firmware")

    def test_translate_flash_pt_br(self):
        msg = T("Flash", locale="pt_BR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Programar firmware")

    def test_translate_flash_ru_ru(self):
        msg = T("Flash", locale="ru_RU.UTF-8", module="main_screen")
        self.assertEqual(msg, "Запрограммировать прошивку")

    # Wipe
    def test_translate_wipe_en_us(self):
        msg = T("Wipe", locale="en_US.UTF-8", module="main_screen")
        self.assertEqual(msg, "Wipe device")

    def test_translate_wipe_es_es(self):
        msg = T("Wipe", locale="es_ES.UTF-8", module="main_screen")
        self.assertEqual(msg, "Limpiar dispositivo")

    def test_translate_wipe_fr_fr(self):
        msg = T("Wipe", locale="fr_FR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Effacer l'appareil")

    def test_translate_wipe_it_it(self):
        msg = T("Wipe", locale="it_IT.UTF-8", module="main_screen")
        self.assertEqual(msg, "Spegnere il dispositivo")

    def test_translate_wipe_pt_br(self):
        msg = T("Wipe", locale="pt_BR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Limpar dispositivo")

    def test_translate_wipe_ru_ru(self):
        msg = T("Wipe", locale="ru_RU.UTF-8", module="main_screen")
        self.assertEqual(msg, "Стереть устройство")

    # Settings
    def test_translate_settings_en_us(self):
        msg = T("Settings", locale="en_US.UTF-8", module="main_screen")
        self.assertEqual(msg, "Settings")

    def test_translate_settings_es_es(self):
        msg = T("Settings", locale="es_ES.UTF-8", module="main_screen")
        self.assertEqual(msg, "Ajustes")

    def test_translate_settings_fr_fr(self):
        msg = T("Settings", locale="fr_FR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Paramètres")

    def test_translate_settings_it_it(self):
        msg = T("Settings", locale="it_IT.UTF-8", module="main_screen")
        self.assertEqual(msg, "Configurazioni")

    def test_translate_settings_pt_br(self):
        msg = T("Settings", locale="pt_BR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Configurações")

    def test_translate_wije_ru_ru(self):
        msg = T("Settings", locale="ru_RU.UTF-8", module="main_screen")
        self.assertEqual(msg, "Настройки")

    # About
    def test_translate_about_en_us(self):
        msg = T("About", locale="en_US.UTF-8", module="main_screen")
        self.assertEqual(msg, "About")

    def test_translate_about_es_es(self):
        msg = T("About", locale="es_ES.UTF-8", module="main_screen")
        self.assertEqual(msg, "Acerca de")

    def test_translate_about_fr_fr(self):
        msg = T("About", locale="fr_FR.UTF-8", module="main_screen")
        self.assertEqual(msg, "À propos")

    def test_translate_about_it_it(self):
        msg = T("About", locale="it_IT.UTF-8", module="main_screen")
        self.assertEqual(msg, "Informazioni")

    def test_translate_about_pt_br(self):
        msg = T("About", locale="pt_BR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Sobre")

    def test_translate_about_ru_ru(self):
        msg = T("About", locale="ru_RU.UTF-8", module="main_screen")
        self.assertEqual(msg, "Об установщике")

    # Fetching data from
    def test_translate_fetching_data_from_en_us(self):
        msg = T("Fetching data from", locale="en_US.UTF-8", module="main_screen")
        self.assertEqual(msg, "Fetching data from")

    def test_translate_fetching_data_from_es_es(self):
        msg = T("Fetching data from", locale="es_ES.UTF-8", module="main_screen")
        self.assertEqual(msg, "Obteniendo datos de")

    def test_translate_fetching_data_from_fr_fr(self):
        msg = T("Fetching data from", locale="fr_FR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Récupérer des données depuis")

    def test_translate_fetching_data_from_it_it(self):
        msg = T("Fetching data from", locale="it_IT.UTF-8", module="main_screen")
        self.assertEqual(msg, "Recupero dati da")

    def test_translate_fetching_data_from_pt_br(self):
        msg = T("Fetching data from", locale="pt_BR.UTF-8", module="main_screen")
        self.assertEqual(msg, "Buscando dados de")

    def test_translate_fetching_data_from_ru_ru(self):
        msg = T("Fetching data from", locale="ru_RU.UTF-8", module="main_screen")
        self.assertEqual(msg, "Получение данных из")
