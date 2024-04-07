'''Module for handling the localization options supported by the library'''
from enum import Enum


class Locale(Enum):
    '''Enumeration of the supported locales, with methods to access localized console messages'''
    FI = 0
    SV = 1
    EN = 2

    def ean_type_error(self) -> str:
        '''Returns localized error message for when the EAN code is provided as an incorrect type'''
        if self == Locale.FI:
            return "EAN-koodin on oltava int"
        if self == Locale.SV:
            return "EAN-koden måste vara en int"
        if self == Locale.EN:
            return "The EAN code must be an int"

    def checking_ean_code(self, ean: int) -> str:
        '''Returns localized status message for when the EAN code is being checked'''
        if self == Locale.FI:
            return f"EAN-koodin tarkistus: {ean}"
        if self == Locale.SV:
            return f"Kontrollerar EAN-kod: {ean}"
        if self == Locale.EN:
            return f"Checking EAN code: {ean}"

    def set_locale_cookies(self) -> str:
        '''Returns localized status message for when the locale is being set'''
        # No message for FI because it is the default
        if self == Locale.SV:
            return "Ställa in lokala cookies"
        if self == Locale.EN:
            return "Setting locale cookies"

    def fetch_deposit_information(self) -> str:
        '''Returns localized status message for when the service is being queried'''
        if self == Locale.FI:
            return "Haetaan talletustietoja"
        if self == Locale.SV:
            return "Hämtar insättningsinformation"
        if self == Locale.EN:
            return "Fetching deposit information"
