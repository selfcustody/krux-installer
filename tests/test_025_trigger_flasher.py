from unittest import TestCase
from unittest.mock import patch
from src.utils.flasher.trigger_flasher import TriggerFlasher
from .shared_mocks import MockListPorts


class TestTriggerFlasher(TestCase):

    def test_init(self):
        f = TriggerFlasher()
        self.assertEqual(f.ktool.killProcess, False)
        self.assertEqual(f.ktool.loader, None)
        self.assertEqual(f.ktool.print_callback, None)

    @patch("src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts)
    def test_detect_port_amigo(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="amigo")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")
    
    @patch("src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts)
    def test_detect_port_amigo_tft(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="amigo")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")
        
    @patch("src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts)
    def test_detect_port_amigo_ips(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="amigo")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")

    @patch("src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts)
    def test_detect_port_m5stickv(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="m5stickv")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")
    
    @patch("src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts)
    def test_detect_port_bit(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="m5stickv")
        mock_grep.assert_called_once_with("0403")
        self.assertEqual(f.board, "goE")
    
    @patch("src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts)
    def test_detect_port_dock(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="dock")
        mock_grep.assert_called_once_with("7523")
        self.assertEqual(f.board, "dan")
    
    @patch("src.utils.flasher.trigger_flasher.list_ports.grep", new_callable=MockListPorts)
    def test_detect_port_yahboom(self, mock_grep):
        f = TriggerFlasher()
        f.detect_ports(device="yahboom")
        mock_grep.assert_called_once_with("7523")
        self.assertEqual(f.board, "goE")
    

