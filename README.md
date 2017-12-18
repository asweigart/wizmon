# wizmon
A Python module for handling the wizard money in Harry Potter. This is an OOP teaching example.

# Examples

    >>> amt = WizardMoney(galleons=5, sickles=2, knuts=10)
    >>> amt
    WizardMoney(galleons=5, sickles=2, knuts=10)
    >>> amt.asKnuts()
    WizardMoney(galleons=0, sickles=0, knuts=2533)
    >>> amt
    WizardMoney(galleons=5, sickles=2, knuts=10)
    >>> amt.convertToKnuts()
    >>> amt
    WizardMoney(galleons=0, sickles=0, knuts=2533)
    >>>
    >>> amt + WizardMoney(5, 0, 0)
    WizardMoney(galleons=5, sickles=0, knuts=2533)
    >>> WizardMoney(5, 100, 0) - WizardMoney(0, 25, 3)
    WizardMoney(galleons=5, sickles=75, knuts=-3)
    >>>
    >>> amt = WizardMoney(galleons=5, sickles=2, knuts=10)
    >>> amt * 10
    WizardMoney(galleons=50, sickles=20, knuts=100)