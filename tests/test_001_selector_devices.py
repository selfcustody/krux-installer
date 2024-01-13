import os
import pytest
from unittest import TestCase
from unittest.mock import mock_open
from unittest.mock import patch

from kivy.cache import Cache
from src.utils.selector import set_device, get_device

class TestConstants(TestCase):

    @patch('kivy.cache.Cache.append')
    def test_cache_set_m5stickv_as_device(self, append_mock):
        set_device('m5stickv')
        self.assertEqual(Cache.append.call_count, 1)

    @patch('kivy.cache.Cache.append')
    def test_cache_set_amigo_tft_as_device(self, append_mock):
        set_device('amigo_tft')
        self.assertEqual(Cache.append.call_count, 1)
        
    @patch('kivy.cache.Cache.append')
    def test_cache_set_amigo_ips_as_device(self, append_mock):
        set_device('amigo_ips')
        self.assertEqual(Cache.append.call_count, 1)
        
    @patch('kivy.cache.Cache.append')
    def test_cache_set_amigo_ips_as_device(self, append_mock):
        set_device('dock')
        self.assertEqual(Cache.append.call_count, 1)
    
    @patch('kivy.cache.Cache.append')
    def test_cache_set_amigo_ips_as_device(self, append_mock):
        set_device('bit')
        self.assertEqual(Cache.append.call_count, 1)
        
    @patch('kivy.cache.Cache.append')
    def test_cache_set_yahboom_as_device(self, append_mock):
        set_device('yahboom')
        self.assertEqual(Cache.append.call_count, 1)
        
    @patch('kivy.cache.Cache.append', side_effect=ValueError(f"Device 'lilygo' is not valid"))
    def test_cache_raise_value_error(self, append_mock):
        with pytest.raises(ValueError) as exc:
            set_device('lilygo')
            self.assertEqual(exc.value.message, "Device 'lilygo' is not valid")
            self.assertEqual(Cache.append.call_count, 1)
        
    @patch('kivy.cache.Cache.get', return_value='m5stickv')
    def test_cache_get_m5stickv_as_device(self, get_mock):
        device = get_device()
        self.assertEqual(Cache.get.call_count, 1)
