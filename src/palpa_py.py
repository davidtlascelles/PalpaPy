'''Library for retrieving beverage container deposit value'''
import logging

from bs4 import BeautifulSoup
from requests import Session

from src.palpa_locale import Locale

class InvalidEANInputError(Exception):
    '''Exception when EAN entry produces a `null` response from the service due to invalid entry'''

class PalpaPy:
    '''Retrieves the deposit value and other metadata associated with the given EAN code.

    ### Parameters
    `ean` : `int`
        The EAN code from a beverage container
    `locale` : `int|str|Locale`, optional
        The desired localization language for the responses from the service. The library also will
        adapt to this requested localization when possible. By default, Locale.EN

    ### Raises
    `TypeError`
        If the EAN input is not an `int`, a `TypeError` is raised
    `TypeError`
        If the requested locale is not an `int`, `str`, or `Locale`, a `TypeError` is raised
    `ValueError`
        If the requested `int` or `str` locale is not valid, a `ValueError` is raised
    `InvalidEANInputError`
        If the EAN input is not a valid EAN in the Palpa service, an `InvalidEANInputError` is raised
    '''

    host = 'extra.palpa.fi'
    origin = 'https://' + host
    endpoint = 'pantillisuus'

    CSRF_TOKEN_ATTR = 'data-essi-csrf-token'

    def __init__(self, ean: int, locale: 'int|str|Locale' = Locale.EN) -> None:
        # Create a logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.__logger = logging.getLogger(self.__class__.__name__)

        # Configure locale
        self.locale: Locale = self.__normalize_locale_enum(locale)
        self.__logger.debug("Locale: %s", self.locale.name)

        # Sanitize EAN input
        if not isinstance(ean, int):
            raise TypeError(self.locale.ean_type_error())
        self.ean: int = ean
        self.__logger.info(self.locale.checking_ean_code(self.ean))

        # Fetch deposit value and set remaining attributes
        payload: dict = self.__get_deposit_value()

        self.message: str = payload['message']
        self.name: str = payload['name']
        self.recycling: str = payload['recycling']
        self.deposit_str: str = payload['deposit']
        self.deposit: float = float(self.deposit_str.strip('€ ').replace(',', '.'))
        self.type: str = payload['type']

    def __get_deposit_value(self) -> dict:
        '''Fetch the deposit value from the service

        ### Returns
        `dict`
            The `payLoad` dict from the JSON response

        ### Raises
        `InvalidEANInput`
            If the service returns a `null` `payLoad`, the `message` 
        '''
        # Create session to get valid cookie and CSRF token
        session = Session()

        # Before making request, get the webpage to parse CSRF token
        get_response = session.get(f'{self.origin}/{self.endpoint}')

        # Load webpage
        soup: BeautifulSoup = BeautifulSoup(get_response.text, 'html.parser')

        # Find the x_csrf_token
        x_csrf_token = soup.body.attrs[self.CSRF_TOKEN_ATTR]

        # Change the locale if not using the default
        if self.locale != Locale.FI:
            self.__logger.debug(self.locale.set_locale_cookies())
            # Making a GET request to the /locale/<language> endpoint with the language abbreviation of
            # the desired locale will store the desired locale in the session cookies
            session.get(f'{self.origin}/locale/{self.locale.name}', headers=self.headers)

        # Add the CSRF token to the headers
        headers = self.headers
        headers.update({'X-CSRF-TOKEN': x_csrf_token})

        # Make request
        self.__logger.debug(self.locale.fetch_deposit_information())
        post_response = session.post(f'{self.origin}/{self.endpoint}', headers=headers, json=self.data)

        # Handle invalid entry
        if post_response.json()['payLoad'] is None:
            raise InvalidEANInputError(post_response.json()['message'])

        return post_response.json()['payLoad']

    def __normalize_locale_enum(self, locale: 'int|str|Locale') -> Locale:
        '''Normalizes the provided locale (which can be int, str, or Locale) into a Locale enum

        ### Parameters
        `locale` : `int|str|Locale`
            Input locale, not sanitized

        ### Returns
        `Locale`
            Sanitized locale as an enum

        ### Raises
        `ValueError`
            If the provided `int` or `str` does not correspond with a valid `Locale`, a `ValueError` is raised
        `TypeError`
            If the provided locale is not an `int`, `str`, or `Locale`, a `TypeError` is raised
        '''

        # If a Locale enum is used, no sanitization is needed
        if isinstance(locale, Locale):
            return locale

        # Int and str inputs need to be sanitized against a dynamically generated list of int values or str names
        if isinstance(locale, int):
            if locale not in [l.value for l in Locale]:
                valid_values = [locale.value for locale in Locale]
                raise ValueError(f"Invalid locale argument (int). Please use a valid argument: {valid_values}")
            return Locale(locale)

        if isinstance(locale, str):
            locale.upper()
            if locale.upper() not in [l.name for l in Locale]:
                valid_names = [locale.name for locale in Locale]
                raise ValueError(f"Invalid locale argument (str). Please use a valid argument: {valid_names}")
            return Locale[locale.upper()]

        # Handle case if incorrect type is provided
        raise TypeError("Invalid locale argument type. Please use an int, str, or Locale.")

    @property
    def data(self) -> dict:
        '''Dynamically generate the EAN data payload for the request to the service'''
        return {'ean': str(self.ean)}

    @property
    def headers(self) -> dict:
        '''Request headers to be used in the requests to the service'''
        return {
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host': self.host,
            'Origin': self.origin,
            'Referer': f'{self.origin}/{self.endpoint}',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def __repr__(self) -> str:
        return '\n'.join([
            f"EAN: {self.ean}",
            f"Message: {self.message}",
            f"Name: {self.name}",
            f"Recycling: {self.recycling}",
            f"Deposit (str): {self.deposit_str}",
            f"Deposit (float): {self.deposit}",
            f"Type: {self.type}"
        ])
