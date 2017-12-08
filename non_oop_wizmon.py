# The Non-OOP code for some "wizard money"-related functions.

# 29 knuts == 1 sickle
# 17 sickles == 1 galleon

"""
Example Usage:

myMoney = getWizardMoney(2, 10, 5)
yourMoney = getWizardMoney(knuts=25)

print(addWizardMoney(myMoney, yourMoney))
print(multiplyWizardMoney(myMoney, 2))
print(converToKnuts(myMoney))
"""

GALLEONS = 'galleons'
SICKLES = 'sickles'
KNUTS = 'knuts'

def getWizardMoney(galleons=0, sickles=0, knuts=0):
    return {GALLEONS: galleons, SICKLES: sickles, KNUTS: knuts}

def copyWizardMoney(wizMon):
    return {GALLEONS: wizMon[GALLEONS], SICKLES: wizMon[SICKLES], KNUTS: wizMon[KNUTS]}
    # alternatively we could have used `import copy; return copy.copy(wizMon)`

def addWizardMoney(a, b):
    return getWizardMoney(a[GALLEONS] + b[GALLEONS],
                          a[SICKLES] + b[SICKLES],
                          a[KNUTS] + b[KNUTS])

def multiplyWizardMoney(wizMon, n):
    return getWizardMoney(wizMon[GALLEONS] * n,
                          wizMon[SICKLES] * n,
                          wizMon[KNUTS] * n)

def convertToKnuts(wizMon):
    result = copyWizardMoney(wizMon)

    result[KNUTS] += (result[GALLEONS] * 17 * 29) + (result[SICKLES] * 29)
    result[GALLEONS] = 0 # all galleons were converted to knuts
    result[SICKLES] = 0 # all sickles were converted to knuts

    return result

def convertToSickles(wizMon):
    result = copyWizardMoney(wizMon)

    result[SICKLES] += result[GALLEONS] * 17 # convert galleons to sickles
    result[GALLEONS] = 0 # all galleons were converted to sickles

    result[SICKLES] += result[KNUTS] // 29 # convert knuts to sickles
    result[KNUTS] %= 29 # (some knuts may be remaining)

    return result

def convertToGalleons(wizMon):
    result = copyWizardMoney(wizMon)

    result[GALLEONS] += (result[KNUTS] // (29 * 17)) + (result[SICKLES] // 17) # convert all knuts and sickles to galleons
    result[SICKLES] %= 17
    result[KNUTS] %= (29 * 17)

    return result

def getValue(wizMon):
    return convertToKnuts(wizMon)[KNUTS]
