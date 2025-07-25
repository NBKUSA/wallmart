from iso8583.iso8583 import ISO8583
from iso8583.specs import default_ascii as spec
from datetime import datetime
import random

def generate_iso8583_request(pan, expiry, cvv, amount, txn_type="00"):
    iso = ISO8583(spec=spec)
    iso.set_mtI("0200")  # Financial transaction request
    iso.set_bit(2, pan)
    iso.set_bit(3, "000000")
    iso.set_bit(4, f"{int(amount):012}")
    iso.set_bit(7, datetime.now().strftime("%m%d%H%M%S"))
    iso.set_bit(11, str(random.randint(100000, 999999)))
    iso.set_bit(12, datetime.now().strftime("%H%M%S"))
    iso.set_bit(13, datetime.now().strftime("%m%d"))
    iso.set_bit(14, expiry)
    iso.set_bit(22, "051")
    iso.set_bit(25, "00")
    iso.set_bit(41, "TERM001")
    iso.set_bit(42, "MERCHANT001")
    iso.set_bit(39, txn_type)

    msg, _ = iso.get_network_request()
    return msg

def generate_iso8583_response(txn_id, field39="00"):
    iso = ISO8583(spec=spec)
    iso.set_mtI("0210")  # Response message
    iso.set_bit(11, txn_id)
    iso.set_bit(39, field39)
    iso.set_bit(41, "TERM001")
    iso.set_bit(42, "MERCHANT001")

    msg, _ = iso.get_network_response()
    return msg
