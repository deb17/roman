from browser import document

inp_roman = document.select('#roman')[0]
inp_decimal = document.select('#decimal')[0]
err_roman = document.select('#error-roman')[0]
err_decimal = document.select('#error-decimal')[0]

map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
exceptions = {'CD': 'no', 'CM': 'no',
              'XL': 'no', 'XC': 'no',
              'IV': 'no', 'IX': 'no'}


def roman_to_decimal(r):

    d = 0
    prev = ''

    if (r.count('M') > 4 or
        r.count('C') > 4 or
        r.count('X') > 4 or
        r.count('D') > 1 or
        r.count('L') > 1 or
        r.count('V') > 1 or
            r.count('I') > 3):
        raise ValueError('Invalid Roman numeral.')

    if ('MMMM' in r or
        'CCCC' in r or
            'XXXX' in r):
        raise ValueError('Invalid Roman numeral.')

    for c in r:
        if prev:
            if map[prev] < map[c]:
                chars = prev + c
                if chars in exceptions:
                    if exceptions[chars] == 'yes':
                        raise ValueError('Invalid Roman numeral.')
                    else:
                        for key in exceptions:
                            exceptions[key] = 'yes'
                            if key == chars:
                                break
                else:
                    raise ValueError('Invalid Roman numeral.')
        if (prev + c) in exceptions:
            d += map[c] - 2 * map[prev]
        else:
            d += map[c]

        prev = c

    if d > 3999:
        raise ValueError('Invalid Roman numeral.')

    return d


def decimal_to_roman(d):

    r = ''

    thou = d // 1000

    r += 'M' * thou

    hund = d // 100 % 10

    if hund < 4:
        r += 'C' * hund
    elif hund == 4:
        r += 'CD'
    elif hund == 5:
        r += 'D'
    elif hund < 9:
        r += 'D' + 'C' * (hund-5)
    else:
        r += 'CM'

    tens = d // 10 % 10

    if tens < 4:
        r += 'X' * tens
    elif tens == 4:
        r += 'XL'
    elif tens == 5:
        r += 'L'
    elif tens < 9:
        r += 'L' + 'X' * (tens-5)
    else:
        r += 'XC'

    units = d % 10

    if units < 4:
        r += 'I' * units
    elif units == 4:
        r += 'IV'
    elif units == 5:
        r += 'V'
    elif units < 9:
        r += 'V' + 'I' * (units-5)
    else:
        r += 'IX'

    return r


def decimal(e):

    value = e.target.value
    clear_errors()

    if not value:
        inp_roman.value = ''
    else:
        try:
            num = int(value)
            if num not in range(4000):
                raise ValueError(
                    'Input should be positive and less than 4000.')
            else:
                inp_roman.value = decimal_to_roman(num)
        except ValueError as e:
            err_decimal.text = str(e)
            inp_roman.value = ''


def roman(e):

    value = e.target.value
    clear_errors()

    if not value:
        inp_decimal.value = ''
    else:
        try:
            for c in value:
                if c.upper() not in map:
                    raise ValueError('Invalid Roman numeral.')
            inp_decimal.value = roman_to_decimal(value.upper())
        except ValueError as e:
            err_roman.text = str(e)
            inp_decimal.value = ''


def clear_errors():

    err_roman.text = ''
    err_decimal.text = ''


inp_roman.bind('input', roman)
inp_decimal.bind('input', decimal)
