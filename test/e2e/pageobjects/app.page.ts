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

  private __select_device_page__: string;
  private __select_device_page_maixpy_m5stickv_button__: string;
  private __select_device_page_maixpy_amigo_button__: string;
  private __select_device_page_maixpy_bit_button__: string;
  private __select_device_page_maixpy_dock_button__: string;
  private __select_device_page_maixpy_back_button__: string;
  private __select_device_page_maixpy_m5stickv_text__: string;
  private __select_device_page_maixpy_amigo_text__: string;
  private __select_device_page_maixpy_bit_text__: string;
  private __select_device_page_maixpy_dock_text__: string;
  private __select_device_page_maixpy_back_text__: string;

  private __select_version_page__: string;
  private __select_version_page_selfcustody_button__: string;
  private __select_version_page_selfcustody_text__: string;
  private __select_version_page_odudex_button__: string;
  private __select_version_page_odudex_text__: string;
  private __select_version_page_back_button__: string;
  private __select_version_page_back_text__: string;

  private __github_octocat_checker_logo__: string;

  private __download_official_release_zip_page__: string;
  private __download_official_release_zip_title__: string;
  private __download_official_release_zip_subtitle__: string;
  private __download_official_release_zip_progress__: string;

  private __checking_release_zip_msg__: string;
  private __not_found_release_zip_msg__: string;
  private __found_release_zip_msg__: string;

  private __checking_release_zip_sha256_txt_msg__: string;
  private __not_found_release_zip_sha256_txt_msg__: string;
  private __found_release_zip_sha256_txt_msg__: string;

  private __download_official_release_zip_sha256_txt_page__: string;
  private __download_official_release_zip_sha256_txt_page_title__: string;
  private __download_official_release_zip_sha256_txt_page_subtitle__: string;
  private __download_official_release_zip_sha256_txt_page_progress__: string;

  private __checking_release_zip_sig_msg__: string;
  private __not_found_release_zip_sig_msg__: string;
  private __found_release_zip_sig_msg__: string;

  private __download_official_release_zip_sig_page__: string;
  private __download_official_release_zip_sig_title__: string;
  private __download_official_release_zip_sig_subtitle__: string;
  private __download_official_release_zip_sig_progress__: string;

  private __checking_release_pem_msg__: string;
  private __not_found_release_pem_msg__: string;
  private __found_release_pem_msg__: string;
  
  private __download_official_release_pem_page__: string;
  private __download_official_release_pem_title__: string;
  private __download_official_release_pem_subtitle__: string;
  private __download_official_release_pem_progress__: string;
  
  private __warning_download_page__: string;
  private __warning_already_downloaded_text__ : string;
  private __warning_download_proceed_button__: string;
  private __warning_download_proceed_button_text__: string;
  private __warning_download_show_details_button__: string;
  private __warning_download_show_details_button_text__: string;
  private __warning_download_again_button__: string
  private __warning_download_again_button_text__: string;
  private __warning_download_back_button__: string;
  private __warning_download_back_button_text__: string;
  private __warning_already_downloaded_overlay__: string;
  private __warning_already_downloaded_overlay_title__: string;
  private __warning_already_downloaded_overlay_subtitle__: string;
  private __warning_already_downloaded_overlay_text_remote__: string;
  private __warning_already_downloaded_overlay_text_local__: string;
  private __warning_already_downloaded_overlay_text_whatdo__: string;
  private __warning_already_downloaded_overlay_button_close__: string

  private __check_verify_official_release_page__: string;
  private __check_verify_official_release_len_sassaman_is_using_openssl__: string;

  private __verified_official_release_page__: string
  private __verified_official_release_page_sha256_integrity_title__: string;
  
  private __verified_official_release_page_sha256_integrity_txt__: string; 
  private __verified_official_release_page_sha256_integrity__: string;
  private __verified_official_release_page_signature_title__: string;
  private __verified_official_release_page_signature_command__: string;
  private __verified_official_release_page_signature_result__: string;
  private __verified_official_release_page_back_button__: string;

  
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

    this.__select_device_page__ = 'div#select-device-page';
    this.__select_device_page_maixpy_m5stickv_button__ = 'div#select-device-page-maixpy_m5stickv-button'
    this.__select_device_page_maixpy_amigo_button__ = 'div#select-device-page-maixpy_amigo-button'
    this.__select_device_page_maixpy_bit_button__ = 'div#select-device-page-maixpy_bit-button' 
    this.__select_device_page_maixpy_dock_button__ = 'div#select-device-page-maixpy_dock-button' 
    this.__select_device_page_maixpy_back_button__ = 'div#select-device-page-back-button'
    this.__select_device_page_maixpy_m5stickv_text__ = 'div#select-device-page-maixpy_m5stickv-text' 
    this.__select_device_page_maixpy_amigo_text__ = 'div#select-device-page-maixpy_amigo-text'  
    this.__select_device_page_maixpy_bit_text__ = 'div#select-device-page-maixpy_bit-text'  
    this.__select_device_page_maixpy_dock_text__ = 'div#select-device-page-maixpy_dock-text'  
    this.__select_device_page_maixpy_back_text__ = 'div#select-device-page-back-text' 

    this.__select_version_page__ = 'div#select-version-page';
    this.__select_version_page_selfcustody_button__ = 'div#select-version-page-selfcustody-krux-releases-tag-v24-03-0-button'
    this.__select_version_page_back_button__ = 'div#select-version-page-back-button'
    this.__select_version_page_odudex_button__ = 'div#select-version-page-odudex-krux-binaries-button'
    this.__select_version_page_selfcustody_text__ = 'div#select-version-page-selfcustody-krux-releases-tag-v24-03-0-text'
    this.__select_version_page_odudex_text__ = 'div#select-version-page-odudex-krux-binaries-text'
    this.__select_version_page_back_text__ = 'div#select-version-page-back-text'

    this.__github_octocat_checker_logo__ = 'pre#github-octocat-checker-logo'

    this.__download_official_release_zip_page__ = 'div#download-official-release-zip-page'
    this.__download_official_release_zip_title__ = 'div#download-official-release-zip-page-title'
    this.__download_official_release_zip_subtitle__ = 'div#download-official-release-zip-page-subtitle'
    this.__download_official_release_zip_progress__ = 'div#download-official-release-zip-page-progress'

    this.__checking_release_zip_msg__ = 'pre#checking-v24-03-0-krux-v24-03-0-zip'
    this.__not_found_release_zip_msg__ = 'pre#v24-03-0-krux-v24-03-0-zip-not-found'
    this.__found_release_zip_msg__ = 'pre#v24-03-0-krux-v24-03-0-zip-found'

    this.__checking_release_zip_sha256_txt_msg__ = 'pre#checking-v24-03-0-krux-v24-03-0-zip-sha256-txt'
    this.__not_found_release_zip_sha256_txt_msg__ = 'pre#v24-03-0-krux-v24-03-0-zip-sha256-txt-not-found'
    this.__found_release_zip_sha256_txt_msg__ = 'pre#v24-03-0-krux-v24-03-0-zip-sha256-txt-found'

    this.__download_official_release_zip_sha256_txt_page__ = 'div#download-official-release-zip-sha256-txt-page'
    this.__download_official_release_zip_sha256_txt_page_title__ = 'div#download-official-release-zip-sha256-txt-page-title'
    this.__download_official_release_zip_sha256_txt_page_subtitle__ = 'div#download-official-release-zip-sha256-txt-page-subtitle'
    this.__download_official_release_zip_sha256_txt_page_progress__ = 'div#download-official-release-zip-sha256-txt-page-progress'

    this.__checking_release_zip_sig_msg__ = 'pre#checking-v24-03-0-krux-v24-03-0-zip-sig'
    this.__not_found_release_zip_sig_msg__ = 'pre#v24-03-0-krux-v24-03-0-zip-sig-not-found'
    this.__found_release_zip_sig_msg__ = 'pre#v24-03-0-krux-v24-03-0-zip-sig-found'

    this.__download_official_release_zip_sig_page__ = 'div#download-official-release-zip-sig-page'
    this.__download_official_release_zip_sig_title__ = 'div#download-official-release-zip-sig-page-title'
    this.__download_official_release_zip_sig_subtitle__ = 'div#download-official-release-zip-sig-page-subtitle'
    this.__download_official_release_zip_sig_progress__ = 'div#download-official-release-zip-sig-page-progress'

    this.__download_official_release_pem_page__ = 'div#download-official-release-pem-page'
    this.__download_official_release_pem_title__ = 'div#download-official-release-pem-page-title'
    this.__download_official_release_pem_subtitle__ = 'div#download-official-release-pem-page-subtitle' 
    this.__download_official_release_pem_progress__ = 'div#download-official-release-pem-page-progress'
  
    this.__checking_release_pem_msg__ = 'pre#checking-main-selfcustody-pem'
    this.__not_found_release_pem_msg__ = 'pre#main-selfcustody-pem-not-found'
    this.__found_release_pem_msg__ = 'pre#main-selfcustody-pem-found'

    this.__warning_download_page__ = 'div#warning-download-page'
    this.__warning_already_downloaded_text__ = 'div#warning-already-downloaded-text'
    this.__warning_download_proceed_button__ = 'div#warning-download-proceed-button'
    this.__warning_download_proceed_button_text__ = 'div#warning-download-proceed-button-text'
    this.__warning_download_again_button__ = 'div#warning-download-again-button'
    this.__warning_download_again_button_text__ = 'div#warning-download-again-button-text'
    this.__warning_download_show_details_button__ = 'div#warning-download-show-details-button'
    this.__warning_download_show_details_button_text__ = 'div#warning-download-show-details-button-text'
    this.__warning_download_back_button__ = 'div#warning-download-back-button'
    this.__warning_download_back_button_text__ = 'div#warning-download-back-button-text'
    this.__warning_already_downloaded_overlay__ = 'div#warning-already-downloaded-overlay'
    this.__warning_already_downloaded_overlay_title__ = 'div#warning-already-downloaded-overlay-title'
    this.__warning_already_downloaded_overlay_subtitle__ = 'div#warning-already-downloaded-overlay-subtitle'
    this.__warning_already_downloaded_overlay_text_remote__ = 'div#warning-already-downloaded-overlay-text-remote'
    this.__warning_already_downloaded_overlay_text_local__ = 'div#warning-already-downloaded-overlay-text-local'
    this.__warning_already_downloaded_overlay_text_whatdo__ = 'div#warning-already-downloaded-overlay-text-whatdo'
    this.__warning_already_downloaded_overlay_button_close__ = 'div#warning-already-downloaded-overlay-button-close'

    this.__check_verify_official_release_page__ = 'div#check-verify-official-release-page'
    this.__check_verify_official_release_len_sassaman_is_using_openssl__ = 'pre#check-verify-official-release-len-sassaman-is-using-openssl'
    
    this.__verified_official_release_page__ = 'div#verified-official-release-page'
    this.__verified_official_release_page_sha256_integrity_title__ = 'div#verified-official-release-page-sha256-integrity-title'
    this.__verified_official_release_page_sha256_integrity_txt__ = 'div#verified-official-release-page-sha256-integrity-v24-03-0-krux-v24-03-0-zip-sha256-txt' 
    this.__verified_official_release_page_sha256_integrity__ = 'div#verified-official-release-page-sha256-integrity-v24-03-0-krux-v24-03-0-zip'
    this.__verified_official_release_page_signature_title__ = 'div#verified-official-release-page-signature-title'
    this.__verified_official_release_page_signature_command__ = 'span#verified-official-release-page-signature-command'
    this.__verified_official_release_page_signature_result__ = 'span#verified-official-release-page-signature-result'
    this.__verified_official_release_page_back_button__ = 'div#verified-official-release-page-back-button'
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

  get selectDevicePage () {
    return $(this.__select_device_page__)
  }

  get selectMaixpyM5StickVButton () {
    return $(this.__select_device_page_maixpy_m5stickv_button__)
  }

  get selectMaixpyAmigoButton () {
    return $(this.__select_device_page_maixpy_amigo_button__)
  }

  get selectMaixpyBitButton () {
    return $(this.__select_device_page_maixpy_bit_button__)
  }

  get selectMaixpyDockButton () {
    return $(this.__select_device_page_maixpy_dock_button__)
  }

  get selectBackButton () {
    return $(this.__select_device_page_maixpy_back_button__)
  }

  get selectMaixpyM5StickVText () {
    return $(this.__select_device_page_maixpy_m5stickv_text__)
  }

  get selectMaixpyAmigoText () {
    return $(this.__select_device_page_maixpy_amigo_text__)
  }

  get selectMaixpyBitText () {
    return $(this.__select_device_page_maixpy_bit_text__)
  }

  get selectMaixpyDockText () {
    return $(this.__select_device_page_maixpy_dock_text__)
  }

  get selectBackText () {
    return $(this.__select_device_page_maixpy_back_text__)
  }

  get selectVersionPage () {
    return $(this.__select_version_page__)
  }

  get selectVersionSelfcustodyButton () {
    return $(this.__select_version_page_selfcustody_button__)
  }

  get selectVersionOdudexButton () {
    return $(this.__select_version_page_odudex_button__)
  }

  get selectVersionBackButton () {
    return $(this.__select_version_page_back_button__)
  }

  get selectVersionSelfcustodyText () {
    return $(this.__select_version_page_selfcustody_text__)
  }

  get selectVersionOdudexText () {
    return $(this.__select_version_page_odudex_text__)
  }

  get selectVersionBackText () {
    return $(this.__select_version_page_back_text__)
  }

  get githubOctocatCheckerLogo () {
    return $(this.__github_octocat_checker_logo__)
  }


  get checkingReleaseZipMsg () {
    return $(this.__checking_release_zip_msg__)
  }

  get notFoundReleaseZipMsg () {
    return $(this.__not_found_release_zip_msg__)
  }

  get foundReleaseZipMsg () {
    return $(this.__found_release_zip_msg__)
  }

  get downloadOfficialReleaseZipPage () {
    return $(this.__download_official_release_zip_page__)
  }

  get downloadOfficialReleaseZipTitle () {
    return $(this.__download_official_release_zip_title__)
  }

  get downloadOfficialReleaseZipSubtitle () {
    return $(this.__download_official_release_zip_subtitle__)
  }

  get downloadOfficialReleaseZipProgress () {
    return $(this.__download_official_release_zip_progress__)
  }

  get warningDownloadPage () {
    return $(this.__warning_download_page__)
  }

  get warningAlreadyDownloadedText() {
    return $(this.__warning_already_downloaded_text__)
  }

  get warningDownloadProceedButton () {
    return $(this.__warning_download_proceed_button__)
  }

  get warningDownloadProceedButtonText () {
    return $(this.__warning_download_proceed_button_text__)
  }

  get warningDownloadAgainButton () {
    return $(this.__warning_download_again_button__)
  }

  get warningDownloadAgainButtonText () {
    return $(this.__warning_download_again_button_text__)
  }

  get warningDownloadShowDetailsButton () {
    return $(this.__warning_download_show_details_button__)    
  }

  get warningDownloadShowDetailsButtonText () {
    return $(this.__warning_download_show_details_button_text__)    
  }

  get warningDownloadBackButton () {
    return $(this.__warning_download_back_button__)
  }

  get warningDownloadBackButtonText () {
    return $(this.__warning_download_back_button_text__)
  }

  get warningAlreadyDownloadedOverlay () {
    return $(this.__warning_already_downloaded_overlay__)
  }

  get warningAlreadyDownloadedOverlayTitle () {
    return $(this.__warning_already_downloaded_overlay_title__)
  }

  get warningAlreadyDownloadedOverlaySubtitle () {
    return $(this.__warning_already_downloaded_overlay_subtitle__)
  }

  get warningAlreadyDownloadedOverlayTextRemote () {
    return $(this.__warning_already_downloaded_overlay_text_remote__)
  }

  get warningAlreadyDownloadedOverlayTextLocal () {
    return $(this.__warning_already_downloaded_overlay_text_local__)
  }

  get warningAlreadyDownloadedOverlayTextWhatdo () {
    return $(this.__warning_already_downloaded_overlay_text_whatdo__)
  }

  get warningAlreadyDownloadedOverlayButtonClose () {
    return $(this.__warning_already_downloaded_overlay_button_close__)
  }

  get checkingReleaseZipSha256txtMsg () {
    return $(this.__checking_release_zip_sha256_txt_msg__)
  }

  get notFoundReleaseZipSha256txtMsg () {
    return $(this.__not_found_release_zip_sha256_txt_msg__)
  }

  get foundReleaseZipSha256txtMsg () {
    return $(this.__found_release_zip_sha256_txt_msg__)
  }

  get downloadOfficialReleaseZipSha256txtPage () {
    return $(this.__download_official_release_zip_sha256_txt_page__)
  }

  get downloadOfficialReleaseZipSha256txtPageTitle () {
    return $(this.__download_official_release_zip_sha256_txt_page_title__)
  }

  get downloadOfficialReleaseZipSha256txtPageSubtitle () {
    return $(this.__download_official_release_zip_sha256_txt_page_subtitle__)
  }

  get downloadOfficialReleaseZipSha256txtPageProgress () {
    return $(this.__download_official_release_zip_sha256_txt_page_progress__)
  }

  get checkingReleaseZipSigMsg () {
    return $(this.__checking_release_zip_sig_msg__)
  }

  get notFoundReleaseZipSigMsg () {
    return $(this.__not_found_release_zip_sig_msg__)
  }

  get foundReleaseZipSigMsg () {
    return $(this.__found_release_zip_sig_msg__)
  }

  get downloadOfficialReleaseZipSigPage () {
    return $(this.__download_official_release_zip_sig_page__)
  }

  get downloadOfficialReleaseZipSigTitle () {
    return $(this.__download_official_release_zip_sig_title__)
  }

  get downloadOfficialReleaseZipSigSubtitle () {
    return $(this.__download_official_release_zip_sig_subtitle__)
  }

  get downloadOfficialReleaseZipSigProgress () {
    return $(this.__download_official_release_zip_sig_progress__)
  }

  get downloadOfficialReleasePemPage () {
    return $(this.__download_official_release_pem_page__)
  }

  get downloadOfficialReleasePemTitle () {
    return $(this.__download_official_release_pem_title__)
  }

  get downloadOfficialReleasePemSubtitle () {
    return $(this.__download_official_release_pem_subtitle__)
  }

  get downloadOfficialReleasePemProgress () {
    return $(this.__download_official_release_pem_page__)
  }

  get checkingReleasePemMsg () {
    return $(this.__checking_release_pem_msg__)
  }
  
  get notFoundReleasePemMsg () {
    return $(this.__not_found_release_pem_msg__)
  }

  get foundReleasePemMsg () {
    return $(this.__found_release_pem_msg__)
  }

  get checkVerifyOfficialReleasePage () {
    return $(this.__check_verify_official_release_page__)
  }

  get checkVerifyOfficialReleaseLenSassamanIsUsingOpenssl (){
    return $(this.__check_verify_official_release_len_sassaman_is_using_openssl__)
  }

  get verifiedOfficialReleasePage () {
    return $(this.__verified_official_release_page__)
  }

  get verifiedOfficialReleasePageSha2256IntegrityTitle () {
    return $(this.__verified_official_release_page_sha256_integrity_title__)
  }
  
  get verifiedOfficialReleasePageSha2256IntegritySha256txt () {
    return $(this.__verified_official_release_page_sha256_integrity_txt__)
  }

  get verifiedOfficialReleasePageSha2256IntegritySha256 () {
    return $(this.__verified_official_release_page_sha256_integrity__)
  }

  get verifiedOfficialReleasePageSignatureTitle () {
    return $(this.__verified_official_release_page_signature_title__)
  }
  
  get verifiedOfficialReleasePageSignatureCommand () {
    return $(this.__verified_official_release_page_signature_command__)
  }
  
  get verifiedOfficialReleasePageSignatureResult () {
    return $(this.__verified_official_release_page_signature_result__)
  }

  get verifiedOfficialReleasePageBackButton () {
    return $(this.__verified_official_release_page_back_button__)
  }
  
}

module.exports = App
