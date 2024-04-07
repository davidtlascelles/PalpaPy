'''Unit tests for PalpaPy'''
import logging
from contextlib import AbstractContextManager
from typing import Any
from unittest import TestCase

from src.palpa_py import InvalidEANInputError, Locale, PalpaPy


class TestPalpa(TestCase):
    '''Test suite for PalpaPy'''

    __base_response_component = {
        'ean': 7340131601954,
        'name': 'NOCCO Focus Raspberry Blast',
        'deposit_str': '0,15 €',
        'deposit': 0.15,
        'type': 'APPROVED_OR_CONDITIONAL_NOT_34'
    }

    __fi_response_component = {
        'locale': Locale.FI,
        'message': 'Juomapakkaus on rekisteröity PALPAn pantilliseen palautusjärjestelmään.',
        'recycling': 'Tölkki'
    }

    __sv_response_component = {
        'locale': Locale.SV,
        'message': 'Dryckesförpackningen hör till PALPAs retursystem.',
        'recycling': 'Burk'
    }

    __en_response_component = {
        'locale': Locale.EN,
        'message': 'The beverage package is registered to PALPAs return system.',
        'recycling': 'Can'
    }

    @property
    def expected_response_fi(self) -> dict:
        '''Combines the Finnish localized responses with the base to create the full response'''
        response_dict = self.__base_response_component
        response_dict.update(self.__fi_response_component)
        return response_dict

    @property
    def expected_response_sv(self) -> dict:
        '''Combines the Swedish localized responses with the base to create the full response'''
        response_dict = self.__base_response_component
        response_dict.update(self.__sv_response_component)
        return response_dict

    @property
    def expected_response_en(self) -> dict:
        '''Combines the English localized responses with the base to create the full response'''
        response_dict = self.__base_response_component
        response_dict.update(self.__en_response_component)
        return response_dict

    def setUp(self):
        print("Executing unittest:", self._testMethodName)
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.ean = self.__base_response_component['ean']

    def subTest(self, msg: Any = ..., **params: Any) -> AbstractContextManager[None]:
        print("  Executing subtest:",msg)
        return super().subTest(msg, **params)

    def test_enum_en_locale(self):
        '''Tests that querying a valid EAN code with the English `Locale` enum works'''
        palpa = PalpaPy(self.ean, Locale.EN)
        self.assertDictEqual(vars(palpa), vars(palpa) | self.expected_response_en)

    def test_str_sv_lowercase_locale(self):
        '''Tests that querying a valid EAN code with the Swedish lowercase `str` locale works'''
        palpa = PalpaPy(self.ean, 'sv')
        self.assertDictEqual(vars(palpa), vars(palpa) | self.expected_response_sv)

    def test_str_fi_uppercase_locale(self):
        '''Tests that querying a valid EAN code with the Finnish uppercase `str` locale works'''
        palpa = PalpaPy(self.ean, 'FI')
        self.assertDictEqual(vars(palpa), vars(palpa) | self.expected_response_fi)

    def test_int_en_locale(self):
        '''Tests that querying a valid EAN code with the English `int` locale works'''
        palpa = PalpaPy(self.ean, 2)
        self.assertDictEqual(vars(palpa), vars(palpa) | self.expected_response_en)

    def test_invalid_type_ean(self):
        '''
        Tests that the correct `TypeError` is raised when using invalid type for the EAN code.
        All supported locales are tested in subTests
        '''
        for locale in Locale:
            with self.subTest(f"{locale.name} locale"):
                with self.assertRaises(TypeError) as context:
                    PalpaPy(str(self.ean), locale)

                self.assertEqual(str(context.exception), locale.ean_type_error())

    def test_invalid_type_locale(self):
        '''Tests that the correct `TypeError` is raised when an invalid type for the locale is used'''
        with self.assertRaises(TypeError) as context:
            PalpaPy(self.ean, 2.0)

        self.assertEqual(str(context.exception), 'Invalid locale argument type. Please use an int, str, or Locale.')

    def test_invalid_ean_input(self):
        '''
        Tests that the correct `InvalidEANInputError` is raised when an invalid EAN code is entered.
        All supported locales are tested in subTests
        '''
        for locale in Locale:
            if locale == Locale.EN:
                expected_error = "Check the barcode numbers"
            elif locale == Locale.SV:
                expected_error = "Kontrollera nummerserien"
            elif locale == Locale.FI:
                expected_error = "Tarkistahan, että syötit numerosarjan oikein."
            with self.subTest(f"{locale.name} locale"):
                with self.assertRaises(InvalidEANInputError) as context:
                    PalpaPy(123, locale)

                self.assertEqual(str(context.exception), expected_error)

    def test_invalid_value_ean(self):
        '''Tests that the correct `ValueError` is raised when an invalid `str` or `int` locale is entered'''
        with self.subTest("Invalid int locale"):
            with self.assertRaises(ValueError) as context:
                PalpaPy(self.ean, -1)

            self.assertEqual(
                str(context.exception),
                'Invalid locale argument (int). Please use a valid argument: [0, 1, 2]'\
            )

        with self.subTest("Invalid str locale"):
            with self.assertRaises(ValueError) as context:
                PalpaPy(self.ean, 'test')

            self.assertEqual(
                str(context.exception),
                "Invalid locale argument (str). Please use a valid argument: ['FI', 'SV', 'EN']"
            )

    def test_repr(self):
        '''Tests that the string representation of the `PalpaPy` object is correct'''
        palpa = PalpaPy(self.ean)
        expected = '\n'.join([
            f"EAN: {palpa.ean}",
            f"Message: {palpa.message}",
            f"Name: {palpa.name}",
            f"Recycling: {palpa.recycling}",
            f"Deposit (str): {palpa.deposit_str}",
            f"Deposit (float): {palpa.deposit}",
            f"Type: {palpa.type}"
        ])

        self.assertEqual(str(palpa), expected)
