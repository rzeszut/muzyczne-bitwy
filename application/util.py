import rome

from application import app

@app.context_processor
def jinja2_utilities():
    def format_date(date):
        return '{} {}'.format(date.day, rome.Roman(date.month))

    return {
        'format_date': format_date
    }

