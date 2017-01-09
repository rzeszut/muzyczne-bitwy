from flask import Blueprint
from random import shuffle

ROMAN_MONTHS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']

def to_roman(month):
    return ROMAN_MONTHS[month - 1]

def jinja2_utilities():
    def format_date(date):
        return '{} {}'.format(date.day, to_roman(date.month))

    return {
        'format_date': format_date
    }

def shuffled(lst):
    l = list(lst)
    shuffle(l)
    return l

