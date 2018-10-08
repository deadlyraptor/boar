from flask import Blueprint

filters = Blueprint('filters', __name__)


@filters.app_template_filter()
def datetimeformat(value, format='%m/%d/%y'):
    return value.strftime(format)


@filters.app_template_filter()
def format_currency(value):
    return f'${value:,}'


@filters.app_template_filter()
def format_percentage(value):
    return f'{value/100:.1%}'
