from unittest import TestCase
from unittest.mock import patch
from src.i18n import T


class TestI18nMainScreen(TestCase):

    # Setup
    @patch("src.i18n.Ai18n.translate")
    def test_translate(self, mock_translate):
        T("Setup", locale="af_ZA.UTF-8", module="greetings_screen")
        mock_translate.assert_called_once_with(
            "Setup", locale="af_ZA.UTF-8", module="greetings_screen"
        )

    # Setup
    @patch(
        "src.i18n.I18N_LOCALES", [{"name": "mo_MO.UTF-8", "file": "mo_MO.UTF-8.json"}]
    )
    @patch("src.i18n.Ai18n.translate")
    def test_fail_translate(self, mock_translate):
        with self.assertRaises(ValueError) as exc_info:
            T("Setup", locale="af_ZA.UTF-8", module="greetings_screen")

        self.assertEqual(
            str(exc_info.exception), "Locale 'af_ZA.UTF-8' not found in translations"
        )
        mock_translate.assert_not_called()
