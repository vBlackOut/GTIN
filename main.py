from lib.decorator import decorator_except_stringdigital
from random import sample, choices
import logging

logger = logging.getLogger(__name__)

class GTIN():

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s'
        )

    def debug(self, value, level=""):

        logger.setLevel(getattr(logging, level))

        if type(value) == bool:
            logger.propagate = value
        else:
            raise "Error of type debug bool required"
    '''
    Additionnal barcode calculate
    from : https://www.gs1.org/services/how-calculate-check-digit-manually
    '''
    @decorator_except_stringdigital
    def checkbarcode(self, value):

        lenght_barcode = len(value)

        if lenght_barcode == 8:
            lenght_barcode = (0, 8)
        elif lenght_barcode == 12:
            lenght_barcode = (0, 12)
        elif lenght_barcode == 13:
            lenght_barcode = (1, 13)
        elif lenght_barcode == 14:
            lenght_barcode = (0, 14)
        elif lenght_barcode == 17:
            lenght_barcode = (1, 17)
        elif lenght_barcode == 18:
            lenght_barcode = (0, 18)
        else:
            logger.debug('Error barcode "{}" lenght string == "{}" not in [8, 12, 13, 14, 17, 18] '.format(value, lenght_barcode))
            return False

        sum_digital = 0
        list_calcule_addition = []

        for i, digital in enumerate(value[:-1]):

            if i % 2 == lenght_barcode[0]:
                logger.debug("pos : {}, calcule : 3 * {} = {}".format(i, int(digital), int(digital)*3))
                list_calcule_addition.append(int(digital)*3)
            else:
                logger.debug("pos : {}, calcule : 1 * {} = {}".format(i, int(digital), int(digital)*1))
                list_calcule_addition.append(int(digital))

        sum_digital = sum(list_calcule_addition)
        logger.debug("list {} total {}".format(list_calcule_addition, sum_digital))

        calcule_checksum = self.calculechecksum(sum_digital) - sum_digital

        calcule_ten = (len(str(calcule_checksum)), str(calcule_checksum))

        if value[-calcule_ten[0]:] == calcule_ten[1]:
            logger.debug("string: {}, end: {}, calcule end: {}, len end: {}, return True".format(value, str(value)[-calcule_ten[0]:], calcule_checksum, calcule_ten[0]))
            return True
        else:
            logger.debug("string: {}, end: {}, calcule end: {}, len end: {}, return False".format(value, str(value)[-calcule_ten[0]:], calcule_checksum, calcule_ten[0]))
            return False

    def calculechecksum(self, value):
        value_ten = value % 10
        result = (10 - value_ten) + value

        if result == (value_ten + result):
            return value
        else:
            return result

    '''
    Generator barcode it's for generate barcode
    - lenght choice : lenght returned in list
    - number barcode : is define for number return barcode in list
    - return bar code :  just return all type True or False if define or None for all Type mixed True or False
    None it's for all type barcode returned.
    '''
    def generator_barcode(self, barcode_lenght, number_barcode, status_barcode=None):
        full_barcode = []

        for a in range(0, number_barcode):
            list_bar_code = []

            choice_bar_code = choices(barcode_lenght)[0]

            for i in range(0, choice_bar_code):
                bar_code_number = str(sample(range(0, 9), 1)[0])
                list_bar_code.append(bar_code_number)
            if self.checkbarcode("".join(list_bar_code)):
                full_barcode.append(("".join(list_bar_code), True))
            else:
                full_barcode.append(("".join(list_bar_code), False))

        if status_barcode != None and type(status_barcode) == bool:
            copy_full_bar_code = []
            for i, (code, status) in enumerate(full_barcode):
                if status is status_barcode:
                    copy_full_bar_code.append((code, status))
            full_barcode = copy_full_bar_code

        # retry if len == 0
        if len(full_barcode) <= 0:
            full_barcode = self.generator_barcode(barcode_lenght, number_barcode, status_barcode)

        return full_barcode

    def test_barcode(self, list_test):
        for test, expected in list_test:
            # is_valid_barcode(test)
            try:
                result = self.checkbarcode(test)
                logger.info("result '{}' return function: {} excepted return: {}".format(test, result, expected))
            except Exception as e:
                return "Failed: %s -> %s" % (test, e)
                raise
            if result != expected:
                return "Failed: %s -> expected %s got %s" % (test, expected, result)
                break
        else:
            return "Success"

if "__main__" == __name__:
    gtin = GTIN()
    gtin.debug(True, "INFO")

    test_cases = [
        ('6291041500213', True), # <--- example of the spec
        ('6291041500211', False), # <-- example with wrong check digit
        ('3124482010481', True),
        ('3124482010482', False),
        ('3124482010483', False),
        ('3124482010484', False),
        ('3124482010485', False),
        ('3124482010486', False),
        ('3124482010487', False),
        ('3124482010488', False),
        ('3124482010489', False),
        ('3124482010480', False),
        ('0167053164698', True),
        ('13033490913240', True),
        ('13033490913240.00', False),
        ('123456017450', True),
        ('12345670', True),
        ('000000000000000000000', False),
        ('00000000000000000000', False),
        ('0000000000000000000', False),
        ('000000000000000000', True),
        ('00000000000000000', True),
        ('0000000000000000', False),
        ('000000000000000', False),
        ('00000000000000', True),
        ('0000000000000', True),
        ('000000000000', True),
        ('00000000000', False),
        ('0000000000', False),
        ('000000000', False),
        ('00000000', True),
        ('0000000', False),
        ('000000', False),
        ('00000', False),
        ('0000', False),
        ('000', False),
        ('00', False),
        ('0', False),
        ('zerozerozerozero', False),
        ("I am not a GTIN!4", False),
        ('0000OOOO000000000', False),
        ('ßþéçíæL ĉĥâ®åCẗëR§ ΅œ’', False),
        ([0,0,0,0,0,0,0,0], False),
        (3124482010481, False),
    ]

    gtin.checkbarcode("3124482010481") # return True
    gtin.generator_barcode(barcode_lenght=[8,12,13,14,17,18], number_barcode=1000, status_barcode=True) # return generate test 1000 barcode, return just barcode of status True barcode of lenght variable 8-18
    print(gtin.test_barcode(test_cases)) # return Success
