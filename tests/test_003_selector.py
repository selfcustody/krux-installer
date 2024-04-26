from unittest import TestCase
from unittest.mock import MagicMock, patch, call
import requests
from src.utils.selector import Selector
from .shared_mocks import PropertyInstanceMock

MOCKED_EMPTY_API = []
MOCKED_WRONG_API = [
    {"author": "test"},
    {"author": "test"},
    {"author": "test"},
]
MOCKED_FOUND_API = [
    {"author": "test", "tag_name": "v0.0.1"},
    {"author": "test", "tag_name": "v0.1.0"},
    {"author": "test", "tag_name": "v1.0.0"},
]


class TestSelector(TestCase):

    @patch("src.utils.selector.requests")
    def test_init(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()

        mock_requests.get.assert_called_once_with(
            url="https://api.github.com/repos/selfcustody/krux/releases",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=10,
        )

        self.assertEqual(selector.releases[0], "v0.0.1")
        self.assertEqual(selector.releases[1], "v0.1.0")
        self.assertEqual(selector.releases[2], "v1.0.0")

    @patch("src.utils.selector.requests")
    def test_fail_init_empty_data(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_EMPTY_API
        mock_requests.get.return_value = mock_response

        with self.assertRaises(ValueError) as exc_info:
            Selector()

        self.assertEqual(
            str(exc_info.exception),
            "https://api.github.com/repos/selfcustody/krux/releases returned empty data",
        )

    @patch("src.utils.selector.requests")
    def test_fail_init_wrong_data(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_WRONG_API
        mock_requests.get.return_value = mock_response

        with self.assertRaises(KeyError) as exc_info:
            Selector()

        self.assertEqual(
            str(exc_info.exception), "\"Invalid key: 'tag_name' do not exist on api\""
        )

    @patch("src.utils.selector.requests")
    def test_fail_init_http_error_404(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            Selector()

        self.assertEqual(str(exc_info.exception), "HTTP error 404: None")

    @patch("src.utils.selector.requests")
    def test_fail_init_http_error_500(self, mock_requests):
        mock_response = MagicMock(status_code=500)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            Selector()

        self.assertEqual(str(exc_info.exception), "HTTP error 500: None")

    @patch("src.utils.selector.requests")
    def test_fail_init_timeout(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            Selector()

        self.assertEqual(str(exc_info.exception), "Timeout error: None")

    @patch("src.utils.selector.requests")
    def test_fail_init_http_connection_error(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.ConnectionError
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            Selector()

        self.assertEqual(str(exc_info.exception), "Connection error: None")

    @patch("src.utils.selector.requests")
    @patch("src.utils.selector.Selector.device", new_callable=PropertyInstanceMock)
    def test_set_device_m5stickv(self, mock_set, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.device = "m5stickv"
        mock_set.assert_has_calls([call(selector, None), call(selector, "m5stickv")])

    @patch("src.utils.selector.requests")
    @patch(
        "src.utils.selector.Selector.device",
        new_callable=PropertyInstanceMock,
        return_value="m5stickv",
    )
    def test_get_device_m5stickv(self, mock_get, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        self.assertEqual(selector.device, "m5stickv")
        mock_get.assert_has_calls([call(selector, None), call(selector)])

    @patch("src.utils.selector.requests")
    @patch("src.utils.selector.Selector.device", new_callable=PropertyInstanceMock)
    def test_set_device_amigo_tft(self, mock_set, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.device = "amigo_tft"
        mock_set.assert_has_calls([call(selector, None), call(selector, "amigo_tft")])

    @patch("src.utils.selector.requests")
    @patch(
        "src.utils.selector.Selector.device",
        new_callable=PropertyInstanceMock,
        return_value="amigo_tft",
    )
    def test_get_device_amigo_tft(self, mock_get, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        self.assertEqual(selector.device, "amigo_tft")
        mock_get.assert_has_calls([call(selector, None), call(selector)])

    @patch("src.utils.selector.requests")
    @patch("src.utils.selector.Selector.device", new_callable=PropertyInstanceMock)
    def test_set_device_amigo_ips(self, mock_set, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.device = "amigo_ips"
        mock_set.assert_has_calls([call(selector, None), call(selector, "amigo_ips")])

    @patch("src.utils.selector.requests")
    @patch(
        "src.utils.selector.Selector.device",
        new_callable=PropertyInstanceMock,
        return_value="amigo_ips",
    )
    def test_get_device_amigo_ips(self, mock_get, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        self.assertEqual(selector.device, "amigo_ips")
        mock_get.assert_has_calls([call(selector, None), call(selector)])

    @patch("src.utils.selector.requests")
    @patch("src.utils.selector.Selector.device", new_callable=PropertyInstanceMock)
    def test_set_device_dock(self, mock_set, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.device = "dock"
        mock_set.assert_has_calls([call(selector, None), call(selector, "dock")])

    @patch("src.utils.selector.requests")
    @patch(
        "src.utils.selector.Selector.device",
        new_callable=PropertyInstanceMock,
        return_value="dock",
    )
    def test_get_device_dock(self, mock_get, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        self.assertEqual(selector.device, "dock")
        mock_get.assert_has_calls([call(selector, None), call(selector)])

    @patch("src.utils.selector.requests")
    @patch("src.utils.selector.Selector.device", new_callable=PropertyInstanceMock)
    def test_set_device_bit(self, mock_set, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.device = "bit"
        mock_set.assert_has_calls([call(selector, None), call(selector, "bit")])

    @patch("src.utils.selector.requests")
    @patch(
        "src.utils.selector.Selector.device",
        new_callable=PropertyInstanceMock,
        return_value="bit",
    )
    def test_get_device_bit(self, mock_get, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        self.assertEqual(selector.device, "bit")
        mock_get.assert_has_calls([call(selector, None), call(selector)])

    @patch("src.utils.selector.requests")
    @patch("src.utils.selector.Selector.device", new_callable=PropertyInstanceMock)
    def test_set_device_yahboom(self, mock_set, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.device = "yahboom"
        mock_set.assert_has_calls([call(selector, None), call(selector, "yahboom")])

    @patch("src.utils.selector.requests")
    @patch(
        "src.utils.selector.Selector.device",
        new_callable=PropertyInstanceMock,
        return_value="yahboom",
    )
    def test_get_device_yahboom(self, mock_get, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        self.assertEqual(selector.device, "yahboom")
        mock_get.assert_has_calls([call(selector, None), call(selector)])

    @patch("src.utils.selector.requests")
    def test_fail_set_device(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        with self.assertRaises(ValueError) as exc_info:
            selector = Selector()
            selector.device = "mock"

        self.assertEqual(str(exc_info.exception), "Device 'mock' is not valid")

    @patch("src.utils.selector.requests")
    @patch("src.utils.selector.Selector.firmware", new_callable=PropertyInstanceMock)
    def test_set_firmware_official(self, mock_set, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.firmware = "v0.0.1"
        mock_set.assert_has_calls([call(selector, "v0.0.1")])

    @patch("src.utils.selector.requests")
    @patch(
        "src.utils.selector.Selector.firmware",
        new_callable=PropertyInstanceMock,
        return_value="v0.0.1",
    )
    def test_get_firmware_official(self, mock_get, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        self.assertEqual(selector.firmware, "v0.0.1")
        mock_get.assert_has_calls([call(selector, None), call(selector)])

    @patch("src.utils.selector.requests")
    @patch("src.utils.selector.Selector.firmware", new_callable=PropertyInstanceMock)
    def test_set_firmware_odudex(self, mock_set, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.firmware = "odudex/krux_binaries"
        mock_set.assert_has_calls(
            [call(selector, None), call(selector, "odudex/krux_binaries")]
        )

    @patch("src.utils.selector.requests")
    def test_fail_set_firmware_offical(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        with self.assertRaises(ValueError) as exc_info:
            selector = Selector()
            selector.firmware = "v0.0.111"

        self.assertEqual(str(exc_info.exception), "Firmware 'v0.0.111' is not valid")

    @patch("src.utils.selector.requests")
    def test_fail_set_firmware_odudex(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        with self.assertRaises(ValueError) as exc_info:
            selector = Selector()
            selector.firmware = "odudex/krux_mock"

        self.assertEqual(
            str(exc_info.exception), "Firmware 'odudex/krux_mock' is not valid"
        )


# class TestSelectorInit(TestCase):
#     def test_init (self, mock_logger):
#         mock_set_level = MagicMock()
#         mock_logger.setLevel = mock_set_level

#         Selector()
#         mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["info"])

#     @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
#     @patch("src.utils.trigger.Logger")
#     def test_init_loglevel_debug(self, mock_logger):
#         mock_set_level = MagicMock()
#         mock_logger.setLevel = mock_set_level

#         Selector()
#         mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["debug"])

#     @patch.dict(os.environ, {"LOGLEVEL": "warning"}, clear=True)
#     @patch("src.utils.trigger.Logger")
#     def test_init_loglevel_warning(self, mock_logger):
#         mock_set_level = MagicMock()
#         mock_logger.setLevel = mock_set_level

#         Selector()
#         mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["warning"])

#     @patch.dict(os.environ, {"LOGLEVEL": "error"}, clear=True)
#     @patch("src.utils.trigger.Logger")
#     def test_init_loglevel_error(self, mock_logger):
#         mock_set_level = MagicMock()
#         mock_logger.setLevel = mock_set_level

#         Selector()
#         mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["error"])

#     @patch.dict(os.environ, {"LOGLEVEL": "lol"}, clear=True)
#     def test_fail_init_loglevel_lol(self):
#         with self.assertRaises(KeyError) as exc_info:
#             Selector()

#         self.assertEqual(str(exc_info.exception), "'Not recognized LOGLEVEL: lol'")
