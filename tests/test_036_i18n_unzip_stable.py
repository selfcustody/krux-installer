from unittest import TestCase
from src.i18n import T


class TestI18nVerifyStableZipScreen(TestCase):

    # Flash update with
    def test_translate_flash_af_za(self):
        msg = T(
            "Flash update with",
            locale="af_ZA.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Flits opdatering met")

    def test_translate_flash_en_us(self):
        msg = T(
            "Flash update with",
            locale="en_US.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Flash update with")

    def test_translate_flash_es_es(self):
        msg = T(
            "Flash update with",
            locale="es_ES.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Actualización por flash con")

    def test_translate_flash_fr_fr(self):
        msg = T(
            "Flash update with",
            locale="fr_FR.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Programmer par flash avec")

    def test_translate_flash_it_it(self):
        msg = T(
            "Flash update with",
            locale="it_IT.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Programmazione flash con")

    def test_translate_flash_pt_br(self):
        msg = T(
            "Flash update with",
            locale="pt_BR.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Programar por flash com")

    def test_translate_flash_ru_ru(self):
        msg = T(
            "Flash update with",
            locale="ru_RU.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Программирование \nфлэш-памяти с помощью")

    # Airgap update with
    def test_translate_airgap_af_za(self):
        msg = T(
            "Airgap update with",
            locale="af_ZA.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Airgap-opdatering")

    def test_translate_airgap_en_us(self):
        msg = T(
            "Airgap update with",
            locale="en_US.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Airgap update with")

    def test_translate_airgap_es_es(self):
        msg = T(
            "Airgap update with",
            locale="es_ES.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Actualización por airgap con")

    def test_translate_airgap_fr_fr(self):
        msg = T(
            "Airgap update with",
            locale="fr_FR.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Programmer de manière airgap avec")

    def test_translate_airgap_it_it(self):
        msg = T(
            "Airgap update with",
            locale="it_IT.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Programmazione per airgap con")

    def test_translate_airgap_pt_br(self):
        msg = T(
            "Airgap update with",
            locale="pt_BR.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Programar de forma airgap com")

    def test_translate_airgap_ru_ru(self):
        msg = T(
            "Airgap update with",
            locale="ru_RU.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Программирование \nAirgap с помощью")

    # Unziping
    def test_translate_unziping_af_za(self):
        msg = T(
            "Unziping",
            locale="af_ZA.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Uitpak")

    def test_translate_unziping_en_us(self):
        msg = T(
            "Unziping",
            locale="en_US.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Extracting")

    def test_translate_unziping_es_es(self):
        msg = T(
            "Unziping",
            locale="es_ES.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Descomprimir")

    def test_translate_unziping_fr_fr(self):
        msg = T(
            "Unziping",
            locale="fr_FR.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Décompression de")

    def test_translate_unziping_it_it(self):
        msg = T(
            "Unziping",
            locale="it_IT.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Decompressione")

    def test_translate_unziping_pt_br(self):
        msg = T(
            "Unziping",
            locale="pt_BR.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Descomprimindo")

    def test_translate_unziping_ru_ru(self):
        msg = T(
            "Unziping",
            locale="ru_RU.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Декомпрессия")

    # Unziped
    def test_translate_unziped_af_za(self):
        msg = T(
            "Unziped",
            locale="af_ZA.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Uitgepak")

    def test_translate_unziped_en_us(self):
        msg = T(
            "Unziped",
            locale="en_US.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Extracted")

    def test_translate_unziped_es_es(self):
        msg = T(
            "Unziped",
            locale="es_ES.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Descomprimido")

    def test_translate_unziped_fr_fr(self):
        msg = T(
            "Unziped",
            locale="fr_FR.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Décompressé")

    def test_translate_unziped_it_it(self):
        msg = T(
            "Unziped",
            locale="it_IT.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Decompresso")

    def test_translate_unziped_pt_br(self):
        msg = T(
            "Unziped",
            locale="pt_BR.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Descomprimido")

    def test_translate_unziped_ru_ru(self):
        msg = T(
            "Unziped",
            locale="ru_RU.UTF-8",
            module="unzip_stable_screen",
        )
        self.assertEqual(msg, "Неупакованный")
