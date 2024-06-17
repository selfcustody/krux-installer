from unittest import TestCase
from src.i18n import T


class TestI18nMainScreen(TestCase):

    # Setup
    def test_translate_setup_af_za(self):
        msg = T("Setup", locale="af_ZA.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Stel")

    def test_translate_setup_en_us(self):
        msg = T("Setup", locale="en_US.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Setup")

    def test_translate_setup_es_es(self):
        msg = T("Setup", locale="es_ES.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Configuración")

    def test_translate_setup_fr_fr(self):
        msg = T("Setup", locale="fr_FR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Configuration")

    def test_translate_setup_it_it(self):
        msg = T("Setup", locale="it_IT.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Configura")

    def test_translate_setup_pt_br(self):
        msg = T("Setup", locale="pt_BR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Configurando")

    def test_translate_setup_ru_ru(self):
        msg = T("Setup", locale="ru_RU.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Настройка")

    # for
    def test_translate_for_af_za(self):
        msg = T("for", locale="af_ZA.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "vir")

    def test_translate_for_en_us(self):
        msg = T("for", locale="en_US.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "for")

    def test_translate_for_es_es(self):
        msg = T("for", locale="es_ES.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "para")

    def test_translate_for_fr_fr(self):
        msg = T("for", locale="fr_FR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "pour")

    def test_translate_for_it_it(self):
        msg = T("for", locale="it_IT.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "per")

    def test_translate_for_pt_br(self):
        msg = T("for", locale="pt_BR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "para")

    def test_translate_for_ru_ru(self):
        msg = T("for", locale="ru_RU.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "для")

    # Checking
    def test_translate_checking_af_za(self):
        msg = T("Checking", locale="af_ZA.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Kontroleer")

    def test_translate_checking_en_us(self):
        msg = T("Checking", locale="en_US.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Checking")

    def test_translate_checking_es_es(self):
        msg = T("Checking", locale="es_ES.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Comprobación")

    def test_translate_checking_fr_fr(self):
        msg = T("Checking", locale="fr_FR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Vérification")

    def test_translate_checking_it_it(self):
        msg = T("Checking", locale="it_IT.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Verifica")

    def test_translate_checking_pt_br(self):
        msg = T("Checking", locale="pt_BR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Checando")

    def test_translate_checking_ru_ru(self):
        msg = T("Checking", locale="ru_RU.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Проверка")

    # permissions for
    def test_translate_permissions_for_af_za(self):
        msg = T("permissions for", locale="af_ZA.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "groeptoestemmings vir")

    def test_translate_permissions_for_en_us(self):
        msg = T("permissions for", locale="en_US.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "permissions for")

    def test_translate_permissions_for_es_es(self):
        msg = T("permissions for", locale="es_ES.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "permissos para")

    def test_translate_permissions_for_fr_fr(self):
        msg = T("permissions for", locale="fr_FR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "des autorisations pour")

    def test_translate_permissions_for_it_it(self):
        msg = T("permissions for", locale="it_IT.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "delle autorizzazioni per")

    def test_translate_permissions_for_pt_br(self):
        msg = T("permissions for", locale="pt_BR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "permissiões para")

    def test_translate_permissions_for_ru_ru(self):
        msg = T("permissions for", locale="ru_RU.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "Разрешения для")

    # WARNING
    def test_translate_warning_for_af_za(self):
        msg = T("WARNING", locale="af_ZA.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "WAARSKUWING")

    def test_translate_warning_for_en_us(self):
        msg = T("WARNING", locale="en_US.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "WARNING")

    def test_translate_warning_for_es_es(self):
        msg = T("WARNING", locale="es_ES.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "ADVERTENCIA")

    def test_translate_warning_for_fr_fr(self):
        msg = T("WARNING", locale="fr_FR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "AVERTISSEMENT")

    def test_translate_warnnig_for_it_it(self):
        msg = T("WARNING", locale="it_IT.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "AVVERTIMENTO")

    def test_translate_warning_for_pt_br(self):
        msg = T("WARNING", locale="pt_BR.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "AVISO")

    def test_translate_warning_for_ru_ru(self):
        msg = T("WARNING", locale="ru_RU.UTF-8", module="greetings_screen")
        self.assertEqual(msg, "ПРЕДУПРЕЖДЕНИЕ")

    # This is first run of KruxInstaller in
    def test_translate_first_run_af_za(self):
        msg = T(
            "This is first run of KruxInstaller in",
            locale="af_ZA.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(msg, "Dit is die eerste lopie van KruxInstaller in")

    def test_translate_first_run_en_us(self):
        msg = T(
            "This is first run of KruxInstaller in",
            locale="en_US.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(msg, "This is first run of KruxInstaller in")

    def test_translate_first_run_es_es(self):
        msg = T(
            "This is first run of KruxInstaller in",
            locale="es_ES.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(msg, "Esta es la primera ejecución de KruxInstaller no")

    def test_translate_first_run_fr_fr(self):
        msg = T(
            "This is first run of KruxInstaller in",
            locale="fr_FR.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg, "Il s'agit de la première exécution de KruxInstaller dans"
        )

    def test_translate_first_run_it_it(self):
        msg = T(
            "This is first run of KruxInstaller in",
            locale="it_IT.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(msg, "Questa è la prima esecuzione di KruxInstaller in")

    def test_translate_first_run_pt_br(self):
        msg = T(
            "This is first run of KruxInstaller in",
            locale="pt_BR.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(msg, "Esta é a primeira execução do KruxInstaller no")

    def test_translate_first_run_ru_ru(self):
        msg = T(
            "This is first run of KruxInstaller in",
            locale="ru_RU.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(msg, "Это первый запуск KruxInstaller в")

    # and it appears that you do not have privileged access to make flash procedures
    def test_translate_and_it_appears_af_za(self):
        msg = T(
            "and it appears that you do not have privileged access to make flash procedures",
            locale="af_ZA.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "en dit blyk dat u nie bevoorregte toegang het om flitsprosedures te maak nie",
        )

    def test_translate_and_it_appears_en_us(self):
        msg = T(
            "and it appears that you do not have privileged access to make flash procedures",
            locale="en_US.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "and it appears that you do not have privileged access to make flash procedures",
        )

    def test_translate_and_it_appears_es_es(self):
        msg = T(
            "and it appears that you do not have privileged access to make flash procedures",
            locale="es_ES.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "y parece que no tiene acceso privilegiado para realizar procedimientos flash",
        )

    def test_translate_and_it_appears_fr_fr(self):
        msg = T(
            "and it appears that you do not have privileged access to make flash procedures",
            locale="fr_FR.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "et il semble que vous n'ayez pas d'accès privilégié pour effectuer des procédures flash",
        )

    def test_translate_and_it_appears_it_it(self):
        msg = T(
            "and it appears that you do not have privileged access to make flash procedures",
            locale="it_IT.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "e sembra che tu non disponga di un accesso privilegiato per effettuare procedure flash",
        )

    def test_translate_and_it_appears_pt_br(self):
        msg = T(
            "and it appears that you do not have privileged access to make flash procedures",
            locale="pt_BR.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "e parece que você não tem acesso privilegiado para realizar procedimentos de flash",
        )

    def test_translate_and_it_appears_ru_ru(self):
        msg = T(
            "and it appears that you do not have privileged access to make flash procedures",
            locale="ru_RU.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "и оказывается, что у вас нет привилегированного доступа для выполнения процедур прошивки",
        )

    # To proceed, click in the screen and a prompt will ask for your password
    def test_translate_to_proceed_af_za(self):
        msg = T(
            "To proceed, click in the screen and a prompt will ask for your password",
            locale="af_ZA.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg, "Om voort te gaan, klik op die skerm en 'n aanwysing vra u wagwoord"
        )

    def test_translate_to_proceed_en_us(self):
        msg = T(
            "To proceed, click in the screen and a prompt will ask for your password",
            locale="en_US.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "To proceed, click in the screen and a prompt will ask for your password",
        )

    def test_translate_to_proceed_es_es(self):
        msg = T(
            "To proceed, click in the screen and a prompt will ask for your password",
            locale="es_ES.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "Para continuar, haga clic en la pantalla y un mensaje le pedirá su contraseña",
        )

    def test_translate_to_proceed_fr_fr(self):
        msg = T(
            "To proceed, click in the screen and a prompt will ask for your password",
            locale="fr_FR.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "Pour continuer, cliquez sur l'écran et une invite vous demandera votre mot de passe",
        )

    def test_translate_to_proceed_it_it(self):
        msg = T(
            "To proceed, click in the screen and a prompt will ask for your password",
            locale="it_IT.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg,
            "Per procedere, fai clic sullo schermo e ti verrà chiesto di inserire la password",
        )

    def test_translate_to_proceed_pt_br(self):
        msg = T(
            "To proceed, click in the screen and a prompt will ask for your password",
            locale="pt_BR.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg, "para proceder, clique na tela e um prompt irá solicitar sua senha"
        )

    def test_translate_to_proceed_ru_ru(self):
        msg = T(
            "To proceed, click in the screen and a prompt will ask for your password",
            locale="ru_RU.UTF-8",
            module="greetings_screen",
        )
        self.assertEqual(
            msg, "Чтобы продолжить, нажмите на экране, и появится запрос на ввод пароля"
        )
