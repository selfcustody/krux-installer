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

  constructor () {
    this.__app__ = '#app'
    this.__main__ = '#app>div>main'
    this.__logo__ = "pre#krux-installer-logo"
    this.__loading_data_msg__ = 'pre#loading-data-from-storage'
    this.__verifying_openssl_msg__ = 'pre#verifying-openssl'
    this.__openssl_for_linux_found__ = 'pre#openssl-for-linux-found'
    this.__openssl_for_darwin_found__ = 'pre#openssl-for-darwin-found'
    this.__openssl_for_win32_found__ = 'pre#openssl-for-win32-found'
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

}

module.exports = App
