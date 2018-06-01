from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_webdriver(type=webdriver.Firefox, executable_path=None, download_dir='', log_dir='', marionette=False,
                  marionette_port=0):
    '''
    Gets the webdriver object depending on the type set.
    :param type: RemoteWebDriver - type of the WebDriver, allowed: Firefox, Chrome, Ie
    :param executable_path: str - path of the webdriver executable
    :param download_dir: str - path of the download directory
    :param log_dir: str - path of the logfile
    :param marionette: bool - used only for Firefox; True for Selenium 3; False for Selenium 2
    :param marionette_port: int|None - if marionette enabled, set a port (if not None)
    :return: WebDriver object
    '''
    if type == webdriver.Firefox:
        return get_firefox(executable_path=executable_path, download_dir=download_dir, log_dir=log_dir,
                           marionette=marionette, marionette_port=marionette_port)
    elif type == webdriver.Chrome:
        return get_chrome(download_dir=download_dir, log_dir=log_dir)
    elif type == webdriver.Ie:
        return get_ie(download_dir=download_dir, log_dir=log_dir)
    return None


def get_ie(download_dir='', log_dir=''):
    '''
    Stub for getting Internet Explorer WebDriver.
    :param download_dir: str - path of the download directory
    :param log_dir: str - path of the logfile
    :return: WebDriver object
    '''
    return webdriver.Ie()


def get_chrome(download_dir='', log_dir=''):
    '''
    Stub for getting Chrome WebDriver
    :param download_dir: str - path of the download directory
    :param log_dir: str - path of the logfile
    :return: WebDriver object
    '''
    return webdriver.Chrome()


def get_firefox(executable_path=None, download_dir='', log_dir='', marionette=False, marionette_port=0):
    '''
    Returns a Firefox WebDriver that accepts untrusted certificates, will no ask to resume from crashes,
    does not use cache, uses specified download directory and logfile, downloads files automatically.
    :param executable_path: str - path of the webdriver executable
    :param download_dir: str - path of the download directory
    :param log_dir: str - path of the logfile
    :param marionette: bool - False to use Selenium 2, True for Selenium 3
    :param marionette_port: int|None - if marionette enabled, set a port (if not None)
    :return: WebDriver object
    '''
    # New firefox profile
    profile = webdriver.FirefoxProfile()

    # Accept untrusted certs and untrusted issuers (testing systems usually don't have trusted certs)
    profile.accept_untrusted_certs = True
    profile.default_preferences['webdriver_assume_untrusted_issuer'] = False
    profile.assume_untrusted_cert_issuer = False

    # Disable safe mode
    profile.set_preference('toolkit.startup.max_resumed_crashes', '-1')
    # Disable cache
    profile.set_preference('network.http.use-cache', False)
    # Disable other caches
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)

    # Set download dir and don't ask for confirmation
    profile.set_preference("browser.download.folderList", 2)

    profile.set_preference("browser.download.dir", download_dir)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream, application/xml')

    # Disable automatic update check
    profile.set_preference("app.update.auto", False)
    profile.set_preference("app.update.enabled", False)

    # Set the logfile
    profile.set_preference("webdriver.log.file", log_dir)

    # Get the capabilities and set SSL parameters
    capabilities = DesiredCapabilities().FIREFOX
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True
    capabilities['handleAlerts'] = True
    capabilities['marionette'] = marionette  # Uncomment this line to use Selenium 3 with Firefox <=47
    if marionette and marionette_port is not None:
        profile.set_preference("marionette.port", marionette_port)

    # Save preferences
    profile.update_preferences()

    # Start Firefox with our profile and capabilities and return the WebDriver
    return webdriver.Firefox(
        executable_path=executable_path,
        firefox_profile=profile, capabilities=capabilities)
