from unittest import TestCase
from src.i18n import T


class TestI18nVerifyStableZipScreen(TestCase):

    # Verifying integrity and authenticity
    def test_translate_verifying_af_za(self):
        msg = T(
            "Verifying integrity and authenticity",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verifieer integriteit en egtheid")

    def test_translate_verifying_en_us(self):
        msg = T(
            "Verifying integrity and authenticity",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verifying integrity and authenticity")

    def test_translate_verifying_es_es(self):
        msg = T(
            "Verifying integrity and authenticity",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verificación de la integridad y autenticidad")

    def test_translate_verifying_fr_fr(self):
        msg = T(
            "Verifying integrity and authenticity",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Vérification de l'intégrité et de l'authenticité")

    def test_translate_verifying_it_it(self):
        msg = T(
            "Verifying integrity and authenticity",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verifica dell'integrità e dell'autenticità")

    def test_translate_verifying_pt_br(self):
        msg = T(
            "Verifying integrity and authenticity",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verificando integridade e autenticidade")

    def test_translate_verifying_ru_ru(self):
        msg = T(
            "Verifying integrity and authenticity",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Проверка целостности и подлинности")

    # Integrity verification
    def test_translate_integrity_af_za(self):
        msg = T(
            "Integrity verification",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Integriteit verifikasie")

    def test_translate_integrity_en_us(self):
        msg = T(
            "Integrity verification",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Integrity verification")

    def test_translate_integrity_es_es(self):
        msg = T(
            "Integrity verification",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verificación de integridad")

    def test_translate_integrity_fr_fr(self):
        msg = T(
            "Integrity verification",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Vérification de l'intégrité")

    def test_translate_integrity_it_it(self):
        msg = T(
            "Integrity verification",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verifica dell'integrità")

    def test_translate_integrity_pt_br(self):
        msg = T(
            "Integrity verification",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verificação de integridade")

    def test_translate_integrity_ru_ru(self):
        msg = T(
            "Integrity verification",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Проверка целостности")

    # SUCCESS
    def test_translate_success_af_za(self):
        msg = T(
            "SUCCESS",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "SUKSES")

    def test_translate_success_en_us(self):
        msg = T(
            "SUCCESS",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "SUCCESS")

    def test_translate_success_es_es(self):
        msg = T(
            "SUCCESS",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "ÉXITO")

    def test_translate_success_fr_fr(self):
        msg = T(
            "SUCCESS",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "SUCCÈS")

    def test_translate_success_it_it(self):
        msg = T(
            "SUCCESS",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "SUCCESSO")

    def test_translate_success_pt_br(self):
        msg = T(
            "SUCCESS",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "SUCESSO")

    def test_translate_success_ru_ru(self):
        msg = T(
            "SUCCESS",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "УСПЕХ")

    # FAILED
    def test_translate_failed_af_za(self):
        msg = T(
            "FAILED",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "HET MISLUK")

    def test_translate_failed_en_us(self):
        msg = T(
            "FAILED",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "FAILED")

    def test_translate_failed_es_es(self):
        msg = T(
            "FAILED",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "FRACASADO")

    def test_translate_failed_fr_fr(self):
        msg = T(
            "FAILED",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "RATÉ")

    def test_translate_failed_it_it(self):
        msg = T(
            "FAILED",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "FALLITO")

    def test_translate_failed_pt_br(self):
        msg = T(
            "FAILED",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "FALHOU")

    def test_translate_failed_ru_ru(self):
        msg = T(
            "FAILED",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "НЕУДАВШИЙСЯ")

    # Authenticity verification
    def test_translate_auth_af_za(self):
        msg = T(
            "Authenticity verification",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verifikasie van egtheid")

    def test_translate_auth_en_us(self):
        msg = T(
            "Authenticity verification",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Authenticity verification")

    def test_translate_auth_es_es(self):
        msg = T(
            "Authenticity verification",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verificación de autenticidad")

    def test_translate_auth_fr_fr(self):
        msg = T(
            "Authenticity verification",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Vérification de l'authenticité")

    def test_translate_auth_it_it(self):
        msg = T(
            "Authenticity verification",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verifica dell'autenticità")

    def test_translate_auth_pt_br(self):
        msg = T(
            "Authenticity verification",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Verificação de autenticidade")

    def test_translate_auth_ru_ru(self):
        msg = T(
            "Authenticity verification",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Проверка подлинности")

    # GOOD
    def test_translate_good_af_za(self):
        msg = T(
            "GOOD",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "GOEIE")

    def test_translate_good_en_us(self):
        msg = T(
            "GOOD",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "GOOD")

    def test_translate_good_es_es(self):
        msg = T(
            "GOOD",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "BUENA")

    def test_translate_good_fr_fr(self):
        msg = T(
            "GOOD",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "BONNE")

    def test_translate_good_it_it(self):
        msg = T(
            "GOOD",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "BUONA")

    def test_translate_good_pt_br(self):
        msg = T(
            "GOOD",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "BOA")

    def test_translate_good_ru_ru(self):
        msg = T(
            "GOOD",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "ХОРОШАЯ")

    # BAD
    def test_translate_bad_af_za(self):
        msg = T(
            "BAD",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "SLEGTE")

    def test_translate_bad_en_us(self):
        msg = T(
            "BAD",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "BAD")

    def test_translate_bad_es_es(self):
        msg = T(
            "BAD",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "MALA")

    def test_translate_bad_fr_fr(self):
        msg = T(
            "BAD",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "MAUVAISE")

    def test_translate_bad_it_it(self):
        msg = T(
            "BAD",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "CATTIVA")

    def test_translate_bad_pt_br(self):
        msg = T(
            "BAD",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "MÁ")

    def test_translate_bad_ru_ru(self):
        msg = T(
            "BAD",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "НЕПРАВИЛЬНАЯ")

    # SIGNATURE
    def test_translate_sig_af_za(self):
        msg = T(
            "SIGNATURE",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "HANDTEKENING")

    def test_translate_sig_en_us(self):
        msg = T(
            "SIGNATURE",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "SIGNATURE")

    def test_translate_sig_es_es(self):
        msg = T(
            "SIGNATURE",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "FIRMA")

    def test_translate_sig_fr_fr(self):
        msg = T(
            "SIGNATURE",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "SIGNATURE")

    def test_translate_sig_it_it(self):
        msg = T(
            "SIGNATURE",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "FIRMA")

    def test_translate_sig_pt_br(self):
        msg = T(
            "SIGNATURE",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "ASSINATURA")

    def test_translate_sig_ru_ru(self):
        msg = T(
            "SIGNATURE",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "ПОДПИСЬ")

    # If you have openssl installed on your system
    def test_translate_openssl_af_za(self):
        msg = T(
            "If you have openssl installed on your system",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "As u openssl op u stelsel geïnstalleer het")

    def test_translate_openssl_en_us(self):
        msg = T(
            "If you have openssl installed on your system",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "If you have openssl installed on your system")

    def test_translate_openssl_es_es(self):
        msg = T(
            "If you have openssl installed on your system",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Si tiene openssl instalado en su sistema")

    def test_translate_openssl_fr_fr(self):
        msg = T(
            "If you have openssl installed on your system",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Si openssl est installé sur votre système")

    def test_translate_openssl_it_it(self):
        msg = T(
            "If you have openssl installed on your system",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Se hai openssl installato sul tuo sistema")

    def test_translate_openssl_pt_br(self):
        msg = T(
            "If you have openssl installed on your system",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Se você tiver o openssl instalado no seu sistema,")

    def test_translate_openssl_ru_ru(self):
        msg = T(
            "If you have openssl installed on your system",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Если в вашей системе установлен openssl")

    # you can check manually with the following command
    def test_translate_check_af_za(self):
        msg = T(
            "you can check manually with the following command",
            locale="af_ZA.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "U kan handmatig met die volgende opdrag kyk")

    def test_translate_check_en_us(self):
        msg = T(
            "you can check manually with the following command",
            locale="en_US.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "you can check with the following command")

    def test_translate_check_es_es(self):
        msg = T(
            "you can check manually with the following command",
            locale="es_ES.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "puede comprobarlo manualmente con el siguiente comando")

    def test_translate_check_fr_fr(self):
        msg = T(
            "you can check manually with the following command",
            locale="fr_FR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(
            msg, "vous pouvez vérifier manuellement avec la commande suivante"
        )

    def test_translate_check_it_it(self):
        msg = T(
            "you can check manually with the following command",
            locale="it_IT.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(
            msg, "è possibile controllare manualmente con il seguente comando"
        )

    def test_translate_check_pt_br(self):
        msg = T(
            "you can check manually with the following command",
            locale="pt_BR.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "você pode checar manualmente a com o seguinte commando")

    def test_translate_check_ru_ru(self):
        msg = T(
            "you can check manually with the following command",
            locale="ru_RU.UTF-8",
            module="verify_stable_zip_screen",
        )
        self.assertEqual(msg, "Вы можете проверить вручную с помощью следующей команды")
