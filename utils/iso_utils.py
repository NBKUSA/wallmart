from pyiso8583.iso8583 import Iso8583
from pyiso8583.specs import default_ascii as spec
from datetime import datetime
import random

def generate_iso8583_request(pan, expiry, cvv, amount, txn_type="00"):
    iso = Iso8583(spec=spec)
    iso.set_mti("0200")  # Financial transaction request
    iso.set_bit(2, pan)
    iso.set_bit(3, "000000")
    iso.set_bit(4, f"{int(amount):012}")
    iso.set_bit(7, datetime.now().strftime("%m%d%H%M%S"))
    iso.set_bit(11, f"{random.randint(100000, 999999):06}")
    iso.set_bit(12, datetime.now().strftime("%H%M%S"))
    iso.set_bit(13, datetime.now().strftime("%m%d"))
    iso.set_bit(14, expiry)
    iso.set_bit(22, "051")  # POS Entry Mode
    iso.set_bit(25, "00")   # POS Condition Code
    iso.set_bit(41, "TERMID01")  # 8 characters max
    iso.set_bit(42, "MERCHANT000001")  # 15 characters max

    # NOTE: Field 39 is for responses — not valid in request
    # Do not include in request:
    # iso.set_bit(39, txn_type)

    msg, _ = iso.get_network_request()
    return msg


def generate_iso8583_response(txn_id, field39="00"):
    iso = Iso8583(spec=spec)
    iso.set_mti("0210")  # Response message
    iso.set_bit(11, txn_id)
    iso.set_bit(39, field39)
    iso.set_bit(41, "TERMID01")  # 8 characters
    iso.set_bit(42, "MERCHANT000001")  # 15 characters

    msg, _ = iso.get_network_response()
    return msg
