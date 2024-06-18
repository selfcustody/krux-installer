from unittest import TestCase
from src.i18n import T


class TestI18nWarningBetaScreen(TestCase):

    # WARNING
    def test_translate_warning_af_za(self):
        msg = T("WARNING", locale="af_ZA.UTF-8", module="warning_beta_screen")
        self.assertEqual(msg, "WAARSKUWING")

    def test_translate_warning_en_us(self):
        msg = T("WARNING", locale="en_US.UTF-8", module="warning_beta_screen")
        self.assertEqual(msg, "WARNING")

    def test_translate_warning_es_es(self):
        msg = T("WARNING", locale="es_ES.UTF-8", module="warning_beta_screen")
        self.assertEqual(msg, "ADVERTENCIA")

    def test_translate_warning_versions_fr_fr(self):
        msg = T("WARNING", locale="fr_FR.UTF-8", module="warning_beta_screen")
        self.assertEqual(msg, "AVERTISSEMENT")

    def test_translate_warning_versions_it_it(self):
        msg = T("WARNING", locale="it_IT.UTF-8", module="warning_beta_screen")
        self.assertEqual(msg, "AVVERTIMENTO")

    def test_translate_warning_versions_pt_br(self):
        msg = T("WARNING", locale="pt_BR.UTF-8", module="warning_beta_screen")
        self.assertEqual(msg, "ADVERTÊNCIA")

    def test_translate_warning_versions_ru_ru(self):
        msg = T("WARNING", locale="ru_RU.UTF-8", module="warning_beta_screen")
        self.assertEqual(msg, "ПРЕДУПРЕЖДЕНИЕ")

    # This is our test repository
    def test_translate_repo_af_za(self):
        msg = T(
            "This is our test repository",
            locale="af_ZA.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(msg, "Dit is ons toetsbewaarplek")

    def test_translate_repo_en_us(self):
        msg = T(
            "This is our test repository",
            locale="en_US.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(msg, "This is our test repository")

    def test_translate_repo_es_es(self):
        msg = T(
            "This is our test repository",
            locale="es_ES.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(msg, "Este es nuestro repositorio de pruebas")

    def test_translate_repo_versions_fr_fr(self):
        msg = T(
            "This is our test repository",
            locale="fr_FR.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(msg, "Ceci est notre référentiel de tests")

    def test_translate_repo_versions_it_it(self):
        msg = T(
            "This is our test repository",
            locale="it_IT.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(msg, "Questo è il nostro repository di testare")

    def test_translate_repo_versions_pt_br(self):
        msg = T(
            "This is our test repository",
            locale="pt_BR.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(msg, "Este é nosso repositório de testes")

    def test_translate_repo_versions_ru_ru(self):
        msg = T(
            "This is our test repository",
            locale="ru_RU.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(msg, "Это наш тестовый репозиторий")

    # These are unsigned binaries for the latest and most experimental features
    def test_translate_unsigned_af_za(self):
        msg = T(
            "These are unsigned binaries for the latest and most experimental features",
            locale="af_ZA.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg,
            "Dit is ongetekende binaries vir die nuutste en mees eksperimentele kenmerke",
        )

    def test_translate_unsigned_en_us(self):
        msg = T(
            "These are unsigned binaries for the latest and most experimental features",
            locale="en_US.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg,
            "These are unsigned binaries for the latest and most experimental features",
        )

    def test_translate_unsigned_es_es(self):
        msg = T(
            "These are unsigned binaries for the latest and most experimental features",
            locale="es_ES.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg,
            "Estos son binarios sin firmar para las funciones más recientes y experimentales",
        )

    def test_translate_unsigned_versions_fr_fr(self):
        msg = T(
            "These are unsigned binaries for the latest and most experimental features",
            locale="fr_FR.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg,
            "Ce sont des binaires non signés pour les fonctionnalités\nles plus récentes et les plus expérimentales",
        )

    def test_translate_unsigned_versions_it_it(self):
        msg = T(
            "These are unsigned binaries for the latest and most experimental features",
            locale="it_IT.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg,
            "Questi sono file binari non firmati per le funzionalità più recenti e sperimentali",
        )

    def test_translate_unsigned_versions_pt_br(self):
        msg = T(
            "These are unsigned binaries for the latest and most experimental features",
            locale="pt_BR.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg,
            "Estes são binários não assinados das últimas e mais experimentais características",
        )

    def test_translate_unsigned_versions_ru_ru(self):
        msg = T(
            "These are unsigned binaries for the latest and most experimental features",
            locale="ru_RU.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg,
            "Это неподписанные двоичные\nфайлы для новейших и наиболее экспериментальных функций",
        )

    # and it's just for trying new things and providing feedback.
    def test_translate_feedback_af_za(self):
        msg = T(
            "and it's just for trying new things and providing feedback.",
            locale="af_ZA.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg, "en dit is net om nuwe dinge te probeer en terugvoer te gee."
        )

    def test_translate_feedback_en_us(self):
        msg = T(
            "and it's just for trying new things and providing feedback.",
            locale="en_US.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg, "and it's just for trying new things and providing feedback"
        )

    def test_translate_feedback_es_es(self):
        msg = T(
            "and it's just for trying new things and providing feedback.",
            locale="es_ES.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(msg, "y es sólo para probar cosas nuevas y dar opinión.")

    def test_translate_feedback_versions_fr_fr(self):
        msg = T(
            "and it's just for trying new things and providing feedback.",
            locale="fr_FR.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg,
            "et c'est juste pour essayer de nouvelles choses et fournir des commentaires.",
        )

    def test_translate_feedback_versions_it_it(self):
        msg = T(
            "and it's just for trying new things and providing feedback.",
            locale="it_IT.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(msg, "ed è solo per provare cose nuove e fornire feedback.")

    def test_translate_feedback_versions_pt_br(self):
        msg = T(
            "and it's just for trying new things and providing feedback.",
            locale="pt_BR.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg, "e serve apenas para experimentar coisas novas e fornecer opiniões."
        )

    def test_translate_feedback_versions_ru_ru(self):
        msg = T(
            "and it's just for trying new things and providing feedback.",
            locale="ru_RU.UTF-8",
            module="warning_beta_screen",
        )
        self.assertEqual(
            msg,
            "и это просто для того, чтобы попробовать\nчто-то новое и оставить отзыв",
        )
