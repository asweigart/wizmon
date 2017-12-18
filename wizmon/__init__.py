# wizmon: A Python module to implement logic to handle wizard money.
# By Al Sweigart al@inventwithpython.com

"""
This module was made as an educational example of Pythonic OOP. As such, all
the "NOTE:" comments aren't meant for code maintainability but rather as
teaching notes for people reading the code.


Design decisions:

- WizardMoney objects are mutable, and therefore don't have a hash and can't
  be used as keys in dictionaries.
- The == operator treats an object of 29 knuts as equal to an object of 1
  sickle, though these objects would have different hashes.
- Galleons, sickles, and knuts have abbreviates of lowercase g, s, and k.
- The abbreviations come after the numeric amount, e.g. 5g for 5 galleons.
- You can use integers (or int()-compatible values) for the constructor or
  galleons/sickles/knuts properties, like '5g' or '4s, 0g, 10k'.
- We will call strings like '5g' "quantity strings" in this module. They are
  delimited by commas, have whitespace trimmed, and the g/s/k abbreviation
  must be lowercase and follow directly behind the number. They can have
  a negative sign, e.g. '-5s' is negative five sickles.
- The quantity string '5g, 5g' will represent the quantity '10g'
- WizardMoney can be subclassed, but it's not really set up that way. See the
  "NOTE:" explanation in the parse() function.
- The constructor accepts only int values or whole number floats.
- Because we only deal with whole numbers for the units, all division is
  floor division.

Example Usage:
See the docstring for the WizardMoney class for example usage.

Trivia:
The dragot and sprink are wizarding currency used in the United States. These
are unsupported by the WizardMoney class.
"""

# Some constants for this currency:
KNUTS_PER_SICKLE= 29
SICKLES_PER_GALLEON = 17
KNUTS_PER_GALLEON = SICKLES_PER_GALLEON * KNUTS_PER_SICKLE

# NOTE: I thought about using these constants, but then reconsidered since it
# might be more confusing to see a variable than a simple string like 'k' or
# 'g', so I took these out. (Normally commented-out code would not exist in
# a module like this.)
# G = 'g'
# S = 's'
# K = 'k'

def parse(quantityStr):
    """TODO quantityStr can be str, tuple, or iterable

    >>> parse('5g')
    WizardMoney(galleons=5, sickles=0, knuts=0)
    >>> parse('2s')
    WizardMoney(galleons=0, sickles=2, knuts=0)
    >>> parse('10k')
    WizardMoney(galleons=0, sickles=0, knuts=10)
    >>> parse('5g,10k')
    WizardMoney(galleons=5, sickles=0, knuts=10)
    >>> parse('5g, 10k')
    WizardMoney(galleons=5, sickles=0, knuts=10)
    >>> parse('-5g, 10k')
    WizardMoney(galleons=-5, sickles=0, knuts=10)
    >>> parse(10)
    WizardMoney(galleons=0, sickles=0, knuts=10)
    >>> parse('5g, 10')
    WizardMoney(galleons=5, sickles=0, knuts=10)
    >>> parse('5g, 5g, 5g')
    WizardMoney(galleons=15, sickles=0, knuts=0)
    >>> parse('3g, 3g, -5g')
    WizardMoney(galleons=1, sickles=0, knuts=0)
    """

    # NOTE: We could have made this a static method but I decided not to because there's no reason to subclass WizardMoney. TODO

    # NOTE: Originally I made this function so that the WizardMoney constructor
    # could accept different units for its arguments, like
    # WizardMoney(galleons='34s') which would be equivalent to
    # WizardMoney(galleons=2). This was far too complex, so I removed that
    # feature but thought to keep parse().

    # TODO - because parse() creates WizardMoney objects and the WizardMoney ctor uses parse, I needed to split out this logic into a helper function
    if type(quantityStr) == str:
        # ...a string like '5g, 2k'.
        # NOTE: TODO we use a geneartor expression with tuple()
        quantities = tuple((q.strip() for q in quantityStr.split(',')))
    elif type(quantityStr) == int:
        # ...an int (in which case we assume it is for knuts).
        return WizardMoney(0, 0, quantityStr)
    else:
        raise TypeError('quantityStr must be str, int, or WizardMoney')

    # NOTE: Originally I thought this function should also handle iterables
    # of '5g'-type of strings (or ints or WizardMoney objects), but decided
    # that was adding too much functionality here. If the user wants that,
    # they can just pass the individual items to parse() themselves. It's
    # enough that we handle comma-delimited strings like '5g, 10s' (which
    # we only do because that is the format returned by __str__()).

    # NOTE: Originally I also thought that parse() should accept WizardMoney
    # objects. This made sense if parse() accepted iterables of values
    # (and this would be an easy way to sum a series of WizardMoney objects)
    # but now that parse() only takes a single value, we would just return
    # a copy of the WizardMoney object passed in. This seemed silly, so I
    # took out this feature.

    # Set up the counters.
    galleons = 0
    sickles = 0
    knuts = 0

    for quantity in quantities:
        # At this point, the quantity should be a string like '5g', '10k', '-4s', or '3'.
        if not quantity.endswith(('g', 's', 'k')):
            try:
                int(quantity) # a string no units is fine (we assume it is in knuts)
                quantity += 'k' # add the knuts unit abbreviation to the end
            except ValueError:
                raise ValueError("Quantity '{quantity}' must end with 'g', 's', 'k', or no units")

        units = quantity[-1]
        try:
            quantity = int(quantity[:-1]) # remove the units, convert the rest to int
        except ValueError:
            raise ValueError("Quantity '{quantity}' must be a str of a number that ends with 'g', 's', or 'k'")

        if units == 'g':
            galleons += quantity
        elif units == 's':
            sickles += quantity
        elif units == 'k':
            knuts += quantity

    return WizardMoney(galleons, sickles, knuts)



class WizardMoney:
    """A class to represent an amount of wizard money and handle the currency-related conversion math. TODO

    >>> amt = WizardMoney(5, 2, 10)
    >>> amt
    WizardMoney(galleons=5, sickles=2, knuts=10)
    >>> str(amt)
    '5g, 2s, 10k'
    >>> amt.galleons
    5
    >>> amt.sickles
    2
    >>> amt.knuts
    10
    >>> amt.knuts = 1000  # We can change any of the units.
    >>> amt
    WizardMoney(galleons=5, sickles=2, knuts=1000)
    >>> amt.asGalleons()  # Get a new object, with as many units converted to Galleons as possible.
    WizardMoney(galleons=7, sickles=2, knuts=14)
    >>> amt.asSickles()
    WizardMoney(galleons=0, sickles=121, knuts=14)
    >>> amt.asKnuts()
    WizardMoney(galleons=0, sickles=0, knuts=3523)
    >>> amt.value
    3523
    >>> amt
    WizardMoney(galleons=5, sickles=2, knuts=1000)
    >>> amt.convertToGalleons()  # Modify the object in-place to convert units to Galleons.
    >>> amt
    WizardMoney(galleons=7, sickles=2, knuts=14)  # We still have 2 sickles and 14 knuts left over.
    >>> amt.convertToSickles()
    >>> amt
    WizardMoney(galleons=0, sickles=121, knuts=14)
    >>> amt.convertToKnuts()
    >>> amt
    WizardMoney(galleons=0, sickles=0, knuts=3523)
    >>> amt.convertToGalleons()
    >>> amt
    WizardMoney(galleons=7, sickles=0, knuts=72)  # Note that the sickles have previously been converted to knuts.
    >>> amt.value  # Note that the value is the same as before.
    3523
    """

    def __init__(self, galleons=0, sickles=0, knuts=0):
        # NOTE: Originally I thought it would be nice to be able to pass
        # amounts in other units for each argument, like
        # WizardMoney(galleons='34s') which would be equivalent to
        # WizardMoney(galleons=2). But this turned into a nightmare of
        # complexity so I abandoned this idea.

        # NOTE: I also originally thought that automatically converting
        # values to ints was a good idea, but then reconsidered since
        # 4.9 would convert to 4. The compromise is that the constructor
        # can accept floats, but only if they are whole numbers.

        # If the galleons parameter is a string like '5g, 2s', we parse it.
        # We'll then ignore any sickles and knuts keyword arguments that
        # were originally passed in.
        if type(galleons) == str:
            parsedWizMon = parse(galleons)

            galleons = parsedWizMon.galleons
            sickles = parsedWizMon.sickles
            knuts = parsedWizMon.knuts

        if type(galleons) != int or (type(galleons) == float and galleons % 1 != 0):
            # NOTE: One of the reasons for making a class is to have
            # better error messages than the defaults. We don't want a
            # generic "invalid literal for int()" message.
            raise ValueError('galleons must be int or whole number float')

        if type(sickles) != int or (type(sickles) == float and sickles % 1 != 0):
            raise ValueError('sickles must be int or whole number float')

        if type(knuts) != int or (type(knuts) == float and knuts % 1 != 0):
            raise ValueError('knuts must be int or whole number float')

        self._galleons = int(galleons)
        self._sickles = int(sickles)
        self._knuts = int(knuts)

        self._iter_units_ptr = None # Used for the iterator protocol. See __iter__() and __next__()


    def asKnuts(self):
        """Converts the """
        knuts = self._knuts + (self._galleons * KNUTS_PER_GALLEON) + (self._sickles * KNUTS_PER_SICKLE)
        return WizardMoney(0, 0, knuts)


    def asSickles(self):
        sickles = self._sickles + (self._galleons * SICKLES_PER_GALLEON) + (self._knuts // KNUTS_PER_SICKLE)
        knuts = self._knuts % KNUTS_PER_SICKLE # (some knuts may be remaining)
        return WizardMoney(0, sickles, knuts)


    def asGalleons(self):
        galleons = self._galleons + (self._knuts // (KNUTS_PER_GALLEON)) + (self._sickles // SICKLES_PER_GALLEON)
        sickles = self._sickles % SICKLES_PER_GALLEON
        knuts = self._knuts % KNUTS_PER_GALLEON
        return WizardMoney(galleons, sickles, knuts)


    def convertToKnuts(self):
        self._knuts += (self._galleons * KNUTS_PER_GALLEON) + (self._sickles * KNUTS_PER_SICKLE)
        self._galleons = 0
        self._sickles = 0


    def convertToSickles(self):
        self._sickles += (self._galleons * SICKLES_PER_GALLEON) + (self._knuts // KNUTS_PER_SICKLE)
        self._knuts %= KNUTS_PER_SICKLE # (some knuts may be remaining)
        self._galleons = 0


    def convertToGalleons(self):
        self._galleons += (self._knuts // (KNUTS_PER_GALLEON)) + (self._sickles // SICKLES_PER_GALLEON)
        self._sickles %= SICKLES_PER_GALLEON
        self._knuts %= KNUTS_PER_GALLEON


    def convert(self):
        # First, convert as much to Galleons as possible:
        self.convertToGalleons()
        # Then, convert any remaining Knuts to Sickles:
        self._sickles = self._knuts // KNUTS_PER_SICKLE
        self._knuts %= KNUTS_PER_SICKLE


    @property
    def galleons(self):
        return self._galleons


    @galleons.setter
    def galleons(self, value):
        if type(value) != int or (type(value) == float and value % 1 != 0):
            raise ValueError('galleons must be int or whole number float')
        self._galleons = int(value)


    @galleons.deleter
    def galleons(self):
        self._galleons = 0


    @property
    def sickles(self):
        return self._sickles


    @sickles.setter
    def sickles(self, value):
        if type(value) != int or (type(value) == float and value % 1 != 0):
            raise ValueError('sickles must be int or whole number float')
        self._galleons = int(value)


    @sickles.deleter
    def sickles(self):
        self._sickles = 0


    @property
    def knuts(self):
        return self._knuts


    @knuts.setter
    def knuts(self, value):
        if type(value) != int or (type(value) == float and value % 1 != 0):
            raise ValueError('knuts must be int or whole number float')
        self._knuts = int(value)


    @knuts.deleter
    def knuts(self):
        self._knuts = 0


    @property
    def value(self):
        return (self._galleons * KNUTS_PER_GALLEON) + (self._sickles * KNUTS_PER_SICKLE) + self._knuts


    @value.setter
    def value(self, value):
        raise Exception('value attribute is read-only') # TODO what is the right exception for this?


    def __repr__(self):
        className = type(self).__name__
        return f'{className}(galleons={self._galleons}, sickles={self._sickles}, knuts={self._knuts})'


    def __str__(self):
        return f'{self._galleons}g, {self._sickles}s, {self._knuts}k'


    def __add__(self, other):
        if type(other) in (str, int, float):
            other = parse(other) # other is now a WizardMoney object.

        return WizardMoney(other._galleons + self._galleons, other._sickles + self._sickles, other._knuts + self._knuts)



    def __radd__(self, other):
        return self.__add__(other) # NOTE: Addition is commutative, so let's just reuse the code in __add__().


    def __iadd__(self, other):
        if type(other) in (str, int, float):
            other = parse(other) # other is now a WizardMoney object.

        self._galleons += other._galleons
        self._sickles += other._sickles
        self._knuts += other._knuts


    def __neg__(self):
        return WizardMoney(-self._galleons, -self._sickles, -self._knuts)


    def __sub__(self, other):
        if type(other) in (str, int, float):
            other = parse(other) # other is now a WizardMoney object.

        return self.__add__(-other) # NOTE: We can reuse the logic in __neg__() and __add__() here.


    def __rsub__(self, other):
        if type(other) in (str, int, float):
            other = parse(other) # other is now a WizardMoney object.

        return other.__add__(-self) # NOTE: We can reuse the logic in __neg__() and __add__() here.


    def __isub__(self, other):
        pass


    def __mul__(self, other):
        if type(other) != int or (type(other) == float and other % 1 != 0):
            raise ValueError('multiplier must be int or whole number float')

        return WizardMoney(self._galleons * other, self._sickles * other, self._knuts * other)


    def __rmul__(self, other):
        return self.__mul__(other) # NOTE: Multiplication is commutative, so let's just reuse the code in __add__().


    def __imul__(self, other):
        pass


    def __floordiv__(self, other):
        # TODO - converts to knuts first
        return WizardMoney(0, 0, self.value // other)


    def __ifloordiv__(self, other):
        value = self.value
        self._galleons = 0
        self._sickles = 0
        self._knuts = value // other


    def __truediv__(self, other):
        # The design decision was that all division is floor division.
        return self.__floordiv__(other)


    def __itruediv__(self, other):
        # The design decision was that all division is floor division.
        self.__ifloordiv__(other)


    def __mod__(self, other):
        # TODO - converts to knuts first
        return WizardMoney(0, 0, self.value % other)


    def __divmod__(self, other):
        return (self.__floordiv__(other), self.__mod__(other))


    def __pow__(self, other):
        if type(other) != int or (type(other) == float and other % 1 != 0):
            raise ValueError('exponent must be int or whole number float')
        return WizardMoney(self._galleons ** other, self._sickles ** other, self._knuts ** other)


    def __ipow__(self, other):
        pass

    """
    # NOTE: This was the old design of the iterator protocol for WizardMoney.
    # Then I realized it was easier just to make an iterator based on the tuple
    # of strings like ('5g', '2s', '10k').


    def __iter__(self):
        self._iter_units_ptr = 'g'
        return self


    def __next__(self):
        if self._iter_units_ptr == 'g':
            self._iter_units_ptr = 's'
            return str(self._galleons) + 'g'
        elif self._iter_units_ptr == 's':
            self._iter_units_ptr = 'k'
            return str(self._sickles) + 's'
        elif self._iter_units_ptr == 'k':
            self._iter_units_ptr = None
            return str(self._knuts) + 'k'
        else:
            raise StopIteration
    """


    def __iter__(self):
        # NOTE: Letting iter() do all the work for us makes this a simple
        # one-liner. But it doesn't really have as much educational value
        # for someone reading this code
        return iter((str(self._galleons) + 'g',
                     str(self._sickles) + 's',
                     str(self._knuts) + 'k'))