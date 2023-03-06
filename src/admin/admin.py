from sqladmin import ModelView

from models import Currency, Order


class CurrencyAdmin(ModelView, model=Currency):
    column_list = [Currency.id, Currency.symbol]
    form_excluded_columns = [Currency.id, Currency.last_update]


class OrderAdmin(ModelView, model=Order):
    can_edit = False
    can_create = False
    can_delete = False
    column_list = [Order.currency, Order.price, Order.amount, Order.created_at]
