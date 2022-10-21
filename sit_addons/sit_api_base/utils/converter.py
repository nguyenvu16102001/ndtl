# -*- coding: utf-8 -*- 


from odoo import _, fields
from pytz import timezone
import datetime
from dateutil.parser import parse
import pytz
import logging, traceback
_logger = logging.getLogger(__name__)

class APIConverter(object):
    def __init__(self):
        self.default_date_format = '%d-%m-%Y'

    def get_formatted_date(self, date, date_format='%d-%m-%Y', tz='Asia/Ho_Chi_Minh'):

        target_tz = timezone(tz)

        utc_dt = parse(date)
        date_tz = utc_dt.astimezone(target_tz)
        return date_tz.strftime(date_format)