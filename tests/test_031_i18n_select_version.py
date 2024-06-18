from unittest import TestCase
from src.i18n import T


class TestI18nSelectVersionScreen(TestCase):

    # Old versions
    def test_translate_old_versions_af_za(self):
        msg = T("Old versions", locale="af_ZA.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Ou weergawes")

    def test_translate_old_versions_en_us(self):
        msg = T("Old versions", locale="en_US.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Old versions")

    def test_translate_old_versions_es_es(self):
        msg = T("Old versions", locale="es_ES.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Versiones antiguas")

    def test_translate_old_versions_fr_fr(self):
        msg = T("Old versions", locale="fr_FR.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Anciennes versions")

    def test_translate_old_versions_it_it(self):
        msg = T("Old versions", locale="it_IT.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Vecchie versioni")

    def test_translate_old_versions_pt_br(self):
        msg = T("Old versions", locale="pt_BR.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Versões antigas")

    def test_translate_old_versions_ru_ru(self):
        msg = T("Old versions", locale="ru_RU.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Старые версии")

    # Back
    def test_translate_back_af_za(self):
        msg = T("Back", locale="af_ZA.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Terug")

    def test_translate_back_en_us(self):
        msg = T("Back", locale="en_US.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Back")

    def test_translate_back_es_es(self):
        msg = T("Back", locale="es_ES.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Volver")

    def test_translate_back_versions_fr_fr(self):
        msg = T("Back", locale="fr_FR.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Retour")

    def test_translate_back_versions_it_it(self):
        msg = T("Back", locale="it_IT.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Indietro")

    def test_translate_back_versions_pt_br(self):
        msg = T("Back", locale="pt_BR.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Voltar")

    def test_translate_back_versions_ru_ru(self):
        msg = T("Back", locale="ru_RU.UTF-8", module="select_version_screen")
        self.assertEqual(msg, "Вернуться")
