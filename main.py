'''Example uses of the PalpaPy class'''
# If desired, you can run the Install task to build and install the library from sources.
# from palpa_py import PalpaPy, Locale

# Alternatively, use the library from the sources directly
from src.palpa_py import PalpaPy, Locale

# Example EAN codes to check
ean_codes = [7340131601954, 7340131603231, 6415600550420]

print("Example using default locale (en)")
print(PalpaPy(ean_codes[0]), '\n')

print("Example using int locale constructor (0: fi)")
print(PalpaPy(ean_codes[0], 0), '\n')

print("Example using str locale constructor (sv)")
print(PalpaPy(ean_codes[0], 'sv'), '\n')

print("Example using enum locale constructor")
print(PalpaPy(ean_codes[0], Locale.FI), '\n')

print("Accumulating sum value")
s = sum(p.deposit for p in [PalpaPy(ean, Locale.EN) for ean in ean_codes])
print(f"Total value: {s:.2f}€")
