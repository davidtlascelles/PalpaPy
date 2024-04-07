# Palpa Py Library

This Python library provides an interface to the [Palpa pantillisuus service](https://extra.palpa.fi/pantillisuus).
This service allows users to check the deposit value of beverage containers
using the EAN barcode from the beverage container.

## Installation

You can install the library via pip:

```sh
pip install palpa-py
```

## Usage
-----

To use the library, first import the `PalpaPy` class. You can optionally also
import the `Locale` enum and/or the `InvalidEANInputError`.

```python
from palpa_py import PalpaPy, Locale, InvalidEANInputError
```

Then, initialize the `PalpaPy` object with the necessary parameters:

```python
ean_code = 7340131601954
palpa = PalpaPy(ean_code)
```

Optionally, you can specify Finnish or Swedish to change the language of the
responses from the service. The library will also change localization to the
requested language where possible. You can specify the language using the
`Locale` enum, or by using the `str` or `int` representations of
the locale.

```python
# Set the language using the Locale enum
palpa = PalpaPy(ean_code, Locale.FI)

# Set the language using the str abbreviation of the locales
palpa = PalpaPy(ean_code, "sv")

# Set the language using the int value associated with the locale
palpa = PalpaPy(ean_code, 1)
```

You can access all information provided from the service using the `str`
representation of the `PalpaPy` object

```python
print(palpa)
```

<details>
<summary>Output</summary>

    EAN: 7340131601954
    Message: The beverage package is registered to PALPAs return system.
    Name: NOCCO Focus Raspberry Blast
    Recycling: Can
    Deposit (str): 0,15 €
    Deposit (float): 0.15
    Type: APPROVED_OR_CONDITIONAL_NOT_34

</details>

## Contributing

Contributions are welcome! If you find any bugs or want to suggest improvements,
please [open an issue](https://github.com/davidtlascelles/PalpaPy/issues) or submit a pull request.

## License

This library is licensed under the GNU General Public License. See the `LICENSE` file for more details.

## Credits

Special thanks to Palpa for providing the deposit value lookup service.

