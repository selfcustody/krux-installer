const { $ } = require('@wdio/globals')

class App {

  private __app__: string;
  private __main__: string;
  private __logo__: string;
  private __loading_data_msg__: string;
  private __verifying_openssl_msg__: string;
  private __openssl_for_linux_found__: string;
  private __openssl_for_darwin_found__: string;
  private __openssl_for_win32_found__: string;
  private __main_page__: string;
  private __main_page_click_message_text__: string;
  private __main_page_select_device_button__: string;
  private __main_page_select_version_button__: string;
  private __main_page_select_device_text__: string;
  private __main_page_select_version_text__: string;
  private __main_page_flash_button__: string;
  private __main_page_flash_text__: string;

  constructor () {
    this.__app__ = '#app'
    this.__main__ = '#app>div>main'
    this.__logo__ = "pre#krux-installer-logo"
    this.__loading_data_msg__ = 'pre#loading-data-from-storage'
    this.__verifying_openssl_msg__ = 'pre#verifying-openssl'
    this.__openssl_for_linux_found__ = 'pre#openssl-for-linux-found'
    this.__openssl_for_darwin_found__ = 'pre#openssl-for-darwin-found'
    this.__openssl_for_win32_found__ = 'pre#openssl-for-win32-found'
    this.__main_page__ = '#main-page'
    this.__main_page_click_message_text__ = 'div#main-click-message-text'
    this.__main_page_select_device_button__ = 'div#main-page-select-device-button'
    this.__main_page_select_version_button__ = 'div#main-page-select-version-button'
    this.__main_page_select_device_text__ = 'div#main-page-select-device-text'
    this.__main_page_select_version_text__ = 'div#main-page-select-version-text'
    this.__main_page_flash_button__ = 'div#main-page-flash-button'
    this.__main_page_flash_text__ = 'div#main-page-flash-text'
    
  }

  get title () {
    return $('head>title')
  }

  get app () {
    return $(this.__app__)
  }

  get main () {
    return $(this.__main__)
  }

  get logo () {
    return $(this.__logo__)
  }

  get loadingDataMsg () {
    return $(this.__loading_data_msg__)
  }

  get verifyingOpensslMsg () {
    return $(this.__verifying_openssl_msg__)
  }

  get opensslForLinuxFound () {
    return $(this.__openssl_for_linux_found__)
  }

  get opensslForDarwinFound () {
    return $(this.__openssl_for_darwin_found__)
  }

  get opensslForWin32Found () {
    return $(this.__openssl_for_win32_found__)
  }

  get mainPage () {
    return $(this.__main_page__)
  }

  get mainClickMessageText () {
    return $(this.__main_page_click_message_text__)
  }

  get mainSelectDeviceButton () {
    return $(this.__main_page_select_device_button__)
  }

  get mainSelectVersionButton () {
    return $(this.__main_page_select_version_button__)
  }

  get mainSelectFlashButton () {
    return $(this.__main_page_flash_button__)
  }

  get mainSelectDeviceText () {
    return $(this.__main_page_select_device_text__)
  }

  get mainSelectVersionText () {
    return $(this.__main_page_select_version_text__)
  }

  get mainSelectFlashText () {
    return $(this.__main_page_flash_text__)
  }
}

module.exports = App
