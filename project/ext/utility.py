# -*- encoding: utf-8 -*-

import struct
import re

import jalali_converter


def multiple_replace(dic, text):
    pattern = "|".join(map(re.escape, dic.keys()))
    return re.sub(pattern, lambda m: dic[m.group()], str(text))


def perToEnglishNumber(userInput):
    dic = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
        }

    return multiple_replace(dic, userInput)


def correct_phone(phone):
    phone = perToEnglishNumber(phone)

    if phone.startswith('+'):
        phone = phone[1:]
    if phone.startswith('0'):
        return phone[1:]

    return phone


def from_gregorian_to_jalali(dt, format=u"%a، %d %b %Y ساعت %H:%M:%S"):
    if not dt:
        return dt

    return jalali_converter.datetime.fromgregorian(datetime=dt).strftime(format)


def add_be_af(data, added_str='*'):
    print added_str*100
    print data
    print added_str*100