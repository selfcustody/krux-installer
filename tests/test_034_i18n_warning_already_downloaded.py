from unittest import TestCase
from src.i18n import T


class TestI18nWarningBetaScreen(TestCase):

    # Assets already downloaded
    def test_translate_assets_af_za(self):
        msg = T(
            "Assets already downloaded",
            locale="af_ZA.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Bates wat reeds afgelaai is")

    def test_translate_assets_en_us(self):
        msg = T(
            "Assets already downloaded",
            locale="en_US.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Assets already downloaded")

    def test_translate_assets_es_es(self):
        msg = T(
            "Assets already downloaded",
            locale="es_ES.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Recursos ya descargados")

    def test_translate_assets_versions_fr_fr(self):
        msg = T(
            "Assets already downloaded",
            locale="fr_FR.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Ressources déjà téléchargées")

    def test_translate_assets_versions_it_it(self):
        msg = T(
            "Assets already downloaded",
            locale="it_IT.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Risorse già scaricate")

    def test_translate_assets_versions_pt_br(self):
        msg = T(
            "Assets already downloaded",
            locale="pt_BR.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Arquivos já baixados")

    def test_translate_assets_versions_ru_ru(self):
        msg = T(
            "Assets already downloaded",
            locale="ru_RU.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Ресурсы уже загружены")

    # Do you want to proceed with the same file or do you want to download it again?
    def test_translate_proceed_af_za(self):
        msg = T(
            "Do you want to proceed with the same file or do you want to download it again?",
            locale="af_ZA.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(
            msg, "Wil jy voortgaan met dieselfde lêer of wil jy dit weer aflaai?"
        )

    def test_translate_proceed_en_us(self):
        msg = T(
            "Do you want to proceed with the same file or do you want to download it again?",
            locale="en_US.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(
            msg,
            "Do you want to proceed with the same file or do you want to download it again?",
        )

    def test_translate_proceed_es_es(self):
        msg = T(
            "Do you want to proceed with the same file or do you want to download it again?",
            locale="es_ES.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(
            msg,
            "¿Quieres continuar con el mismo archivo o quieres descargarlo nuevamente?",
        )

    def test_translate_proceed_versions_fr_fr(self):
        msg = T(
            "Do you want to proceed with the same file or do you want to download it again?",
            locale="fr_FR.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(
            msg,
            "Voulez-vous continuer avec le même fichier ou souhaitez-vous le télécharger à nouveau?",
        )

    def test_translate_proceed_versions_it_it(self):
        msg = T(
            "Do you want to proceed with the same file or do you want to download it again?",
            locale="it_IT.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(
            msg, "Vuoi procedere con l'ultimo file o come scaricare il nuovo file?"
        )

    def test_translate_proceed_versions_pt_br(self):
        msg = T(
            "Do you want to proceed with the same file or do you want to download it again?",
            locale="pt_BR.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(
            msg,
            "Você quer proceder com o mesmo arquivo ou quer fazer o download dele novamente?",
        )

    def test_translate_proceed_versions_ru_ru(self):
        msg = T(
            "Do you want to proceed with the same file or do you want to download it again?",
            locale="ru_RU.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(
            msg, "Хотите продолжить с последним файлом или как загрузить новый файл?"
        )

    # Download again
    def test_translate_again_af_za(self):
        msg = T(
            "Download again",
            locale="af_ZA.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Laai weer af")

    def test_translate_again_en_us(self):
        msg = T(
            "Download again",
            locale="en_US.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Download again")

    def test_translate_again_es_es(self):
        msg = T(
            "Download again",
            locale="es_ES.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Descargar de nuevo")

    def test_translate_again_fr_fr(self):
        msg = T(
            "Download again",
            locale="fr_FR.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Télécharger à nouveau")

    def test_translate_again_it_it(self):
        msg = T(
            "Download again",
            locale="it_IT.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Scarica di nuovo")

    def test_translate_again_pt_br(self):
        msg = T(
            "Download again",
            locale="pt_BR.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Baixe novamente")

    def test_translate_again_ru_ru(self):
        msg = T(
            "Download again",
            locale="ru_RU.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Скачать еще раз")

    # Proceed with current file
    def test_translate_current_af_za(self):
        msg = T(
            "Proceed with current file",
            locale="af_ZA.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Gaan voort met\ndie huidige lêer")

    def test_translate_current_en_us(self):
        msg = T(
            "Proceed with current file",
            locale="en_US.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Proceed with current file")

    def test_translate_current_es_es(self):
        msg = T(
            "Proceed with current file",
            locale="es_ES.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Continuar con el archivo actual")

    def test_translate_current_fr_fr(self):
        msg = T(
            "Proceed with current file",
            locale="fr_FR.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Passer au fichier actuel")

    def test_translate_current_it_it(self):
        msg = T(
            "Proceed with current file",
            locale="it_IT.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Procedi con il file corrente")

    def test_translate_current_pt_br(self):
        msg = T(
            "Proceed with current file",
            locale="pt_BR.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Proceda com o arquivo atual")

    def test_translate_current_ru_ru(self):
        msg = T(
            "Proceed with current file",
            locale="ru_RU.UTF-8",
            module="warning_already_downloaded_screen",
        )
        self.assertEqual(msg, "Продолжить работу\nс текущим файлом")
