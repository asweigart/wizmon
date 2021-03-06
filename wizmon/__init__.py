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
- The constructor accepts only int()-compatible values or quantity strings.
- Because we only deal with whole numbers for the units, all division is
  floor division.
- Because we only deal with whole numbers for the units, all math operations
  have the result rounded down, e.g. 6k * 3. =   20k, not 20.4k

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

def parse(quantity):
    """Parses a string of comma-delimited quantities of wizard money. A
    quantity is a number followed by the units g, s, or k for galleon,
    sickle, or knut. Negative signs are allowed but not commas, e.g. '-4g'
    is okay but not '1,000g'.

    The argument can also be an int or float, in which case this is the
    amount in knuts.

    Repeated units are summed together, e.g. '5g, 5g' is the same as '10g'.

    parse() returns a WizardMoney object with the total quantities from
    quantity.

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
    >>> parse(42)
    WizardMoney(galleons=0, sickles=0, knuts=42)
    >>> parse(42.0)
    WizardMoney(galleons=0, sickles=0, knuts=42)
    """

    # NOTE: We could have made this a static method but I decided not to because there's no reason to subclass WizardMoney. TODO

    # NOTE: Originally I made this function so that the WizardMoney constructor
    # could accept different units for its arguments, like
    # WizardMoney(galleons='34s') which would be equivalent to
    # WizardMoney(galleons=2). This was far too complex, so I removed that
    # feature but thought to keep parse().

    # TODO - because parse() creates WizardMoney objects and the WizardMoney ctor uses parse, I needed to split out this logic into a helper function
    if type(quantity) == str:
        # ...a string like '5g, 2k'.
        # NOTE: TODO we use a geneartor expression with tuple()
        quantities = tuple((q.strip() for q in quantity.split(',')))
    elif type(quantity) in (int, float):
        # ...an int or float (in which case we assume it is for knuts).
        return WizardMoney(0, 0, int(quantity))
    else:
        raise TypeError('quantity must be str, int, or float')

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
    """A class to represent an amount of wizard money and handle the currency-related conversion math.

    Examples:

    >>> amount = WizardMoney(5, 2, 10)
    >>> amount
    WizardMoney(galleons=5, sickles=2, knuts=10)
    >>> str(amount)
    '5g, 2s, 10k'
    >>> amount.galleons
    5
    >>> amount.sickles
    2
    >>> amount.knuts
    10
    >>> amount.knuts = 1000  # We can change any of the units.
    >>> amount
    WizardMoney(galleons=5, sickles=2, knuts=1000)

    >>> amt = WizardMoney(galleons=5, sickles=2, knuts=1000)
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
    >>> amt  # We still have 2 sickles and 14 knuts left over.
    WizardMoney(galleons=7, sickles=2, knuts=14)
    >>> amt.convertToSickles()
    >>> amt
    WizardMoney(galleons=0, sickles=121, knuts=14)
    >>> amt.convertToKnuts()
    >>> amt
    WizardMoney(galleons=0, sickles=0, knuts=3523)
    >>> amt.convertToGalleons()
    >>> amt
    WizardMoney(galleons=7, sickles=2, knuts=14)
    >>> amt.value  # Note that the value is the same as before.
    3523

    >>> checking = WizardMoney(1, 25, 35)
    >>> savings = WizardMoney(10, 0, 0)
    >>> checking + savings
    WizardMoney(galleons=11, sickles=25, knuts=35)
    >>> savings - checking
    WizardMoney(galleons=9, sickles=-25, knuts=-35)
    >>> checking * 2
    WizardMoney(galleons=2, sickles=50, knuts=70)
    >>> 2 * checking
    WizardMoney(galleons=2, sickles=50, knuts=70)
    """

    def __init__(self, galleons=0, sickles=0, knuts=0):
        """Constructor for a WizardMoney object. The initial quantities can
        be set by passing integer or floats for the galleons, sickles, and
        knuts keyword arguments. These arguments default to 0.

        Alternatively, you can also pass a single "quantity string" such
        as '5g' or '2s, -5k' as the first and only argument and the
        constructor will parse this amount. See the parse() function for
        more details.

        Examples:
        >>>
        """

        # NOTE: Originally I thought it would be nice to be able to pass
        # amounts in other units for each argument, like
        # WizardMoney(galleons='34s') which would be equivalent to
        # WizardMoney(galleons=2). But this turned into a nightmare of
        # complexity so I abandoned this idea.

        # If the galleons parameter is a string like '5g, 2s', we parse it.
        # We'll then ignore any sickles and knuts keyword arguments that
        # were originally passed in.
        if type(galleons) == str:
            parsedWizMon = parse(galleons)

            galleons = parsedWizMon.galleons
            sickles = parsedWizMon.sickles
            knuts = parsedWizMon.knuts

        if type(galleons) not in (int, float):
            # NOTE: One of the reasons for making a class is to have
            # better error messages than the defaults. We don't want a
            # generic "invalid literal for int()" message.
            raise ValueError('galleons must be compatible with int()')

        if type(sickles) not in (int, float):
            raise ValueError('sickles must be compatible with int()')

        if type(knuts) not in (int, float):
            raise ValueError('knuts must be compatible with int()')

        self._galleons = int(galleons)
        self._sickles = int(sickles)
        self._knuts = int(knuts)

        # NOTE: We no longer use this. See __iter__()
        #self._iter_units_ptr = None # Used for the iterator protocol. See __iter__() and __next__()


    def asKnuts(self):
        """Returns a new WizardMoney object with the same value as this
        object, except with all denominations coverted to knuts.

        Examples:

        >>> amt = WizardMoney(5, 2, 10)
        >>> amt.asKnuts()
        WizardMoney(galleons=0, sickles=0, knuts=2533)
        """
        knuts = self._knuts + (self._galleons * KNUTS_PER_GALLEON) + (self._sickles * KNUTS_PER_SICKLE)
        return WizardMoney(0, 0, knuts)


    def asSickles(self):
        """Returns a new WizardMoney object with the same value as this
        object, except with all denominations coverted to sickles. Any
        remaining change is left as knuts.

        Examples:

        >>> amt = WizardMoney(5, 2, 10)
        >>> amt.asSickles()
        WizardMoney(galleons=0, sickles=87, knuts=10)
        """
        sickles = self._sickles + (self._galleons * SICKLES_PER_GALLEON) + (self._knuts // KNUTS_PER_SICKLE)
        knuts = self._knuts % KNUTS_PER_SICKLE # (some knuts may be remaining)
        return WizardMoney(0, sickles, knuts)


    def asGalleons(self):
        """Returns a new WizardMoney object with the same value as this
        object, except with all denominations coverted to knuts. Any
        remaining change is left as sickles or knuts (though knuts are
        also converted to sickles.)

        Call this method if you want the value in the largest denominations possible.

        Examples:

        >>> amt = WizardMoney(5, 2, 10)
        >>> amt.asGalleons()
        WizardMoney(galleons=5, sickles=2, knuts=10)
        """
        sickles = self._sickles + (self._knuts // KNUTS_PER_SICKLE) # convert knuts to sickles
        knuts = self._knuts % KNUTS_PER_SICKLE # (some knuts may be remaining as change)

        galleons = self._galleons + (sickles // SICKLES_PER_GALLEON) # convert sickles to galleons
        sickles = sickles % SICKLES_PER_GALLEON # (some sickles may be remaining as change)

        return WizardMoney(galleons, sickles, knuts)


    def convertToKnuts(self):
        """Modifies the WizardMoney object in-place with the same value as this
        object, except with all denominations coverted to knuts.

        Examples:

        >>> amt = WizardMoney(5, 2, 10)
        >>> amt.convertToKnuts()
        >>> amt
        WizardMoney(galleons=0, sickles=0, knuts=2533)
        """
        self._knuts += (self._galleons * KNUTS_PER_GALLEON) + (self._sickles * KNUTS_PER_SICKLE)
        self._galleons = 0
        self._sickles = 0


    def convertToSickles(self):
        """Modifies the WizardMoney object in-place with the same value as this
        object, except with all denominations coverted to sickles. Any
        remaining change is left as knuts.

        Examples:

        >>> amt = WizardMoney(5, 2, 10)
        >>> amt.convertToSickles()
        >>> amt
        WizardMoney(galleons=0, sickles=87, knuts=10)
        """
        self._sickles += (self._galleons * SICKLES_PER_GALLEON) + (self._knuts // KNUTS_PER_SICKLE)
        self._knuts %= KNUTS_PER_SICKLE # (some knuts may be remaining as change)
        self._galleons = 0


    def convertToGalleons(self):
        """Modifies the WizardMoney object in-place with the same value as this
        object, except with all denominations coverted to knuts. Any
        remaining change is left as sickles or knuts (though knuts are
        also converted to sickles.)

        Call this method if you want the value in the largest denominations possible.

        Examples:

        >>> amt = WizardMoney(0, 200, 1000)
        >>> amt.convertToGalleons()
        >>> amt
        WizardMoney(galleons=13, sickles=13, knuts=14)
        """
        self._sickles += self._knuts // KNUTS_PER_SICKLE # convert knuts to sickles
        self._knuts %= KNUTS_PER_SICKLE # (some knuts may be remaining as change)

        self._galleons += self._sickles // SICKLES_PER_GALLEON # convert sickles to galleons
        self._sickles %= SICKLES_PER_GALLEON # (some sickles may be remaining as change)


    @property
    def galleons(self):
        """The "getter" for how many galleons are in this WizardMoney object.

        Examples:

        >>> amt = WizardMoney(5, 2, 10)
        >>> amt.galleons
        5
        >>> amt.galleons = 10
        >>> amt
        WizardMoney(galleons=10, sickles=2, knuts=10)
        >>> del amt.galleons
        >>> amt
        WizardMoney(galleons=0, sickles=2, knuts=10)
        """

        # NOTE: You need to put all doctests in the getter of a property.
        # The doctest module ignores any doctests in the setter or deleter.
        # Did you know this? I didn't. My tests passed even though there
        # was clearly a bug in it. Huh.
        return self._galleons


    @galleons.setter
    def galleons(self, value):
        """The "setter" for how many galleons are in this WizardMoney object."""
        try:
            self._galleons = int(value)
        except ValueError:
            raise ValueError('galleons must be compatible with int()')


    @galleons.deleter
    def galleons(self):
        """The "deleter" for galleons. Sets the galleons property to 0."""
        self._galleons = 0


    @property
    def sickles(self):
        """The "getter" for how many sickles are in this WizardMoney object.

        Examples:

        >>> amt = WizardMoney(5, 2, 10)
        >>> amt.sickles
        2
        >>> amt.sickles = 100
        >>> amt
        WizardMoney(galleons=5, sickles=100, knuts=10)
        >>> del amt.sickles
        >>> amt
        WizardMoney(galleons=5, sickles=0, knuts=10)
        """
        return self._sickles


    @sickles.setter
    def sickles(self, value):
        """The "setter" for how many sickles are in this WizardMoney object."""
        try:
            self._sickles = int(value)
        except:
            raise ValueError('sickles must be compatible with int()')


    @sickles.deleter
    def sickles(self):
        """The "deleter" for sickles. Sets the sickles property to 0."""
        self._sickles = 0


    @property
    def knuts(self):
        """The "getter" for how many knuts are in this WizardMoney object.

        Examples:

        >>> amt = WizardMoney(5, 2, 10)
        >>> amt.knuts
        10
        >>> amt.knuts = 100
        >>> amt
        WizardMoney(galleons=5, sickles=2, knuts=100)
        >>> del amt.knuts
        >>> amt
        WizardMoney(galleons=5, sickles=2, knuts=0)
        """
        return self._knuts


    @knuts.setter
    def knuts(self, value):
        """The "setter" for how many knuts are in this WizardMoney object."""
        try:
            self._knuts = int(value)
        except:
            raise ValueError('knuts must be compatible with int()')


    @knuts.deleter
    def knuts(self):
        """The "deleter" for knuts. Sets the knuts property to 0."""
        self._knuts = 0


    @property
    def value(self):
        """The read-only property for the total value of this WizardMoney
        object. (This is the same as the number of knuts it is worth.)

        Examples:

        >>> amt = WizardMoney(5, 2, 10)
        >>> amt.value
        2533
        """
        return (self._galleons * KNUTS_PER_GALLEON) + (self._sickles * KNUTS_PER_SICKLE) + self._knuts


    @value.setter
    def value(self, value):
        """The value property is read-only, so attempting to write to it
        results in an exception raised."""
        raise Exception('value attribute is read-only') # TODO what is the right exception for this?


    @value.deleter
    def value(self):
        """The value property is read-only, so attempting to write to it
        results in an exception raised."""
        raise Exception('value attribute is read-only') # TODO what is the right exception for this?


    def __repr__(self):
        """Returns the repr string, which is also a valid constructor call for this WizardMoney object.

        Examples:

        >>> amt = WizardMoney(2, 5, 10)
        >>> repr(amt)
        'WizardMoney(galleons=2, sickles=5, knuts=10)'
        >>> amt2 = eval(repr(amt))
        >>> amt2
        WizardMoney(galleons=2, sickles=5, knuts=10)
        """
        className = type(self).__name__
        return f'{className}(galleons={self._galleons}, sickles={self._sickles}, knuts={self._knuts})'


    def __str__(self):
        """Returns a string representation of the amount of galleons, sickles,
        and knuts in this WizardMoney object. The string is formatted like
        '5g, 0s, 10k'. Note that this string can be passed to parse() or the
        WizardMoney constructor.

        Examples:

        >>> amt = WizardMoney(2, 0, 10)
        >>> str(amt)
        '2g, 0s, 10k'
        """
        return f'{self._galleons}g, {self._sickles}s, {self._knuts}k'


    def __add__(self, other):
        """Overrides the + operator to add two WizardMoney objects to produce
        a new WizardMoney object with the sum amount.

        Integers floats can be added to WizardMoney objects, in which case it's
        assumed they represent knuts.

        Examples:

        >>> checking = WizardMoney(1, 25, 35)
        >>> savings = WizardMoney(10, 0, 0)
        >>> checking + savings
        WizardMoney(galleons=11, sickles=25, knuts=35)
        >>> checking + 5
        WizardMoney(galleons=1, sickles=25, knuts=40)
        """
        if type(other) in (str, int, float):
            other = parse(other) # other is now a WizardMoney object.

        if not isinstance(other, WizardMoney):
            raise TypeException('WizardMoney objects can only operate with int, floats, or other WizardMoney objects')

        return WizardMoney(other._galleons + self._galleons, other._sickles + self._sickles, other._knuts + self._knuts)


    def __radd__(self, other):
        """Overrides the + operator to add a WizardMoney object to an int
        or float.

        Examples:

        >>> checking = WizardMoney(1, 25, 35)
        >>> 5 + checking
        WizardMoney(galleons=1, sickles=25, knuts=40)
        """
        return self.__add__(other) # NOTE: Addition is commutative, so let's just reuse the code in __add__().


    def __iadd__(self, other):
        """Overrides the += operator to add an int, float, or WizardMoney
        object to this object.

        Examples:

        >>> amt = WizardMoney(0, 0, 5)
        >>> amt += 5
        >>> amt
        WizardMoney(galleons=0, sickles=0, knuts=10)
        >>> amt += WizardMoney(1, 0, 0)
        >>> amt
        WizardMoney(galleons=1, sickles=0, knuts=10)
        """
        if type(other) in (str, int, float):
            other = parse(other) # other is now a WizardMoney object.

        if not isinstance(other, WizardMoney):
            raise TypeException('WizardMoney objects can only operate with int, float, or another WizardMoney object')

        self._galleons += other._galleons
        self._sickles += other._sickles
        self._knuts += other._knuts

        return self


    def __neg__(self):
        """Overrides the - unary operator to negate the value of this object.

        Examples:

        >>> amt = WizardMoney(2, -5, 10)
        >>> -amt
        WizardMoney(galleons=-2, sickles=5, knuts=-10)
        """
        return WizardMoney(-self._galleons, -self._sickles, -self._knuts)


    def __sub__(self, other):
        """Overrides the - operator to subtract two WizardMoney objects to produce
        a new WizardMoney object with the difference amount.

        Integers and floats can be added to WizardMoney objects, in which case it's
        assumed they represent knuts.

        Examples:

        >>> WizardMoney(1, 25, 35) - WizardMoney(0, 35, 3)
        WizardMoney(galleons=1, sickles=-10, knuts=32)
        >>> WizardMoney(0, 35, 3) - 3
        WizardMoney(galleons=0, sickles=35, knuts=0)
        """
        if type(other) in (str, int, float):
            other = parse(other) # other is now a WizardMoney object.

        if not isinstance(other, WizardMoney):
            raise TypeException('WizardMoney objects can only operate with int, float, or another WizardMoney object')

        galleons = self._galleons - other._galleons
        sickles = self._sickles - other._sickles
        knuts = self._knuts - other._knuts

        return WizardMoney(galleons, sickles, knuts)

        #return self.__add__(-other) # NOTE: We CANNOT reuse the logic in __neg__() and __add__() here, since '25k' - '1s, 10k' should be '1s, -15k', but the negation logic would make it '-1s, 20k'


    def __rsub__(self, other):
        """Overrides the - operator to add a WizardMoney object to an int
        or float.

        Examples:

        >>> 500 - WizardMoney(1, 25, 35)
        WizardMoney(galleons=-1, sickles=-25, knuts=465)
        """
        if type(other) in (str, int, float):
            other = parse(other) # other is now a WizardMoney object.

        if not isinstance(other, WizardMoney):
            raise TypeException('WizardMoney objects can only operate with int, floats, or another WizardMoney object')

        galleons = other._galleons - self._galleons
        sickles = other._sickles - self._sickles
        knuts = other._knuts - self._knuts

        return WizardMoney(galleons, sickles, knuts)

        # return other.__add__(-self) # NOTE: We CANNOT reuse the logic in __neg__() and __add__() here, since '25k' - '1s, 10k' should be '1s, -15k', but the negation logic would make it '-1s, 20k'


    def __isub__(self, other):
        """Overrides the -= operator to subtract an int, float, or WizardMoney
        object to this object.

        Examples:

        >>> amt = WizardMoney(0, 0, 5)
        >>> amt -= 5
        >>> amt
        WizardMoney(galleons=0, sickles=0, knuts=0)
        >>> amt -= WizardMoney(1, 0, 0)
        >>> amt
        WizardMoney(galleons=-1, sickles=0, knuts=0)
        """
        if type(other) in (str, int, float):
            other = parse(other) # other is now a WizardMoney object.

        if not isinstance(other, WizardMoney):
            raise TypeException('WizardMoney objects can only operate with int, float, or another WizardMoney object')

        self._galleons -= other._galleons
        self._sickles -= other._sickles
        self._knuts -= other._knuts

        return self


    def __mul__(self, other):
        """Overrides the * operator to multiply this WizardMoney object to produce
        a new WizardMoney object with the product amount.

        When the WizardMoney object is multiplied by an int or a whole number
        float, the denominations are simply multiplied, e.g. WizardMoney(1, 2, 3) * 2
        results in WizardMoney(2, 4, 6).

        However, when a non-whole number float is multiplied with the
        WizardMoney object, the value of the WizardMoney object in knuts is
        what gets multiplied to ensure the most accurate product, since
        WizardMoney objects only contain integer quantities for its
        denominations.

        (As an explanation, imagine multiplying WizardMoney(galleons=1) by 1.5.
        The quantity of galleons gets rounded down back to 1, even though 1
        galleon multiplied by 1.5 would more accurately be 1 galleon, 8 sickles.
        This is why we use knuts and then call convertToGalleons(): it ends up
        being more accurate.)

        Examples:

        >>> WizardMoney(1, 25, 35) * 2
        WizardMoney(galleons=2, sickles=50, knuts=70)
        >>> WizardMoney(0, 35, 3) * -3
        WizardMoney(galleons=0, sickles=-105, knuts=-9)
        >>> WizardMoney(1, 25, 35) * 2.35
        WizardMoney(galleons=5, sickles=16, knuts=15)
        """
        if type(other) == int or (type(other) == float and other % 1 == 0):
            return WizardMoney(int(self._galleons * other), int(self._sickles * other), int(self._knuts * other))
        elif type(other) == float:
            result = WizardMoney(knuts=int(self.value * other))
            result.convertToGalleons()
            return result
        else:
            raise ValueError('WizardMoney objects can only be multiplied by an int or float')


    def __rmul__(self, other):
        """Overrides the * operator to multiply a WizardMoney object to an int
        or float.

        Examples:

        >>> 2 * WizardMoney(1, 25, 35)
        WizardMoney(galleons=2, sickles=50, knuts=70)
        >>> -3 * WizardMoney(0, 35, 3)
        WizardMoney(galleons=0, sickles=-105, knuts=-9)
        >>> 2.35 * WizardMoney(1, 25, 35)
        WizardMoney(galleons=5, sickles=16, knuts=15)
        """
        return self.__mul__(other) # NOTE: Multiplication is commutative, so let's just reuse the code in __add__().


    def __imul__(self, other):
        """Overrides the *= operator to subtract an int, float, or WizardMoney
        object to this object.

        Examples:

        >>> amt = WizardMoney(2, 3, 5)
        >>> amt *= 2
        >>> amt
        WizardMoney(galleons=4, sickles=6, knuts=10)
        """
        if type(other) == int or (type(other) == float and other % 1 == 0):
            self._galleons = int(self._galleons * other)
            self._sickles = int(self._sickles * other)
            self._knuts = int(self._knuts * other)
            return self
        elif type(other) == float:
            result = WizardMoney(knuts=int(self.value * other))
            result.convertToGalleons()
            return result
        else:
            raise ValueError('WizardMoney objects can only be multiplied by an int or float')



    def __floordiv__(self, other):
        """Overrides the // operator to divide this WizardMoney object by an
        int or float. The resulting value is the WizardMoney value in knuts
        divided by the other number, and then convertToGalleons() is called
        to redistribute the quantities across the denominations.

        This is done to get the most accurate division.

        Note that all division with WizardMoney objects is floor division.

        Examples:

        >>> amt = WizardMoney(2, 4, 6)
        >>> amt / 2
        WizardMoney(galleons=1, sickles=2, knuts=3)
        >>> amt.value / 2.5
        443.2
        >>> amt / 2.5
        WizardMoney(galleons=0, sickles=15, knuts=8)
        >>> (amt / 2.5).value
        443
        """

        if type(other) not in (int, float):
            raise ValueError('divisor must be int or float')

        result = WizardMoney(0, 0, int(self.value // other))
        result.convertToGalleons()
        return result


    def __ifloordiv__(self, other):
        """Overrides the //= operator.

        Examples:

        >>> amt = WizardMoney(2, 4, 6)
        >>> amt /= 2
        >>> amt
        WizardMoney(galleons=1, sickles=2, knuts=3)

        >>> amt = WizardMoney(2, 4, 6)
        >>> amt /= 2.35
        >>> amt
        WizardMoney(galleons=0, sickles=16, knuts=7)

        """
        value = self.value
        self._galleons = 0
        self._sickles = 0
        self._knuts = int(value // other)
        self.convertToGalleons()

        return self


    def __truediv__(self, other):
        """Overrides the / operator, which for WizardMoney operators acts the
        same as the // operator.

        Examples:

        >>> amt = WizardMoney(2, 4, 6)
        >>> amt / 2
        WizardMoney(galleons=1, sickles=2, knuts=3)
        >>> amt / 2.35
        WizardMoney(galleons=0, sickles=16, knuts=7)
        """
        return self.__floordiv__(other)


    def __itruediv__(self, other):
        """Overrides the /= operator, which for WizardMoney operators acts the
        same as the //= operator.

        Examples:

        >>> amt = WizardMoney(2, 4, 6)
        >>> amt /= 2
        >>> amt
        WizardMoney(galleons=1, sickles=2, knuts=3)

        >>> amt = WizardMoney(2, 4, 6)
        >>> amt /= 2.35
        >>> amt
        WizardMoney(galleons=0, sickles=16, knuts=7)
        """

        self.__ifloordiv__(other)
        return self


    def __mod__(self, other):
        """Overrides the % operator. The result has convertToGalleons() called
        on it to redistribute the quantity to all denominations.

        Examples:

        >>> amt = WizardMoney(2, 5, 10)
        >>> amt.value % 13
        10
        >>> amt % 13
        WizardMoney(galleons=0, sickles=0, knuts=10)
        """
        result = WizardMoney(0, 0, self.value % other)
        result.convertToGalleons()
        return result


    def __imod__(self, other):
        """Overrides the %= operator. The result has convertToGalleons() called
        on it to redistribute the quantity to all denominations.

        Examples:

        >>> amt = WizardMoney(2, 5, 10)
        >>> amt %= 13
        >>> amt
        WizardMoney(galleons=0, sickles=0, knuts=10)
        """
        self._knuts = self.value % other
        self._galleons = 0
        self._sickles = 0
        self.convertToGalleons()
        return self


    def __divmod__(self, other):
        """Overrides divmod() for WizardMoney objects.

        Examples:

        >>> amt = WizardMoney(2, 5, 10)
        >>> amt / 13
        WizardMoney(galleons=0, sickles=3, knuts=0)
        >>> amt % 13
        WizardMoney(galleons=0, sickles=0, knuts=10)
        >>> result = ((amt / 13) * 13 + (amt % 13))
        >>> result.convertToGalleons()
        >>> result
        WizardMoney(galleons=2, sickles=5, knuts=10)

        >>> divmod(amt, 13)
        (WizardMoney(galleons=0, sickles=3, knuts=0), WizardMoney(galleons=0, sickles=0, knuts=10))
        """
        return (self.__floordiv__(other), self.__mod__(other))


    def __pow__(self, other):
        """Overrides the ** operator. The result has convertToGalleons()
        called on it to redistribute the quantity to all denominations.

        Examples:

        >>> amt = WizardMoney(2, 5, 10)
        >>> amt ** 2
        WizardMoney(galleons=2640, sickles=12, knuts=13)
        >>> (amt ** 2).value
        1301881
        >>> amt.value ** 2
        1301881
        """
        if type(other) not in (int, float):
            raise ValueError('exponent must be int or float')

        result = WizardMoney(0, 0, int(self.value ** other))
        result.convertToGalleons()
        return result


    def __ipow__(self, other):
        """Overrides the **= operator.

        Examples:

        >>> amt = WizardMoney(2, 5, 10)
        >>> amt **= 2
        >>> amt
        WizardMoney(galleons=2640, sickles=12, knuts=13)
        """
        self._knuts = int(self.value ** other)
        self._galleons = 0
        self._sickles = 0
        self.convertToGalleons()

        return self


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
        """

        Examples:

        >>> amt = WizardMoney(2, 5, 10)
        >>> for i in amt: print(i)
        ...
        2g
        5s
        10k
        """

        # NOTE: Letting iter() do all the work for us makes this a simple
        # one-liner. But it doesn't really have as much educational value
        # for someone reading this code
        return iter((str(self._galleons) + 'g',
                     str(self._sickles) + 's',
                     str(self._knuts) + 'k'))
