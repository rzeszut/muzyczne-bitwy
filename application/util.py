from flask import Blueprint
from random import shuffle
import rome

def jinja2_utilities():
    def format_date(date):
        return '{} {}'.format(date.day, rome.Roman(date.month))

    return {
        'format_date': format_date
    }

def shuffled(lst):
    l = list(lst)
    shuffle(l)
    return l

