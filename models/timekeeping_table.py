from odoo import models, fields, api
from datetime import timedelta

class Timekeeping(models.Model):
    _name = "timekeeping.table"
    _description = "Timekeeping"

    user_id = fields.Many2one("res.partner", string="User")
    product_id = fields.Many2one(
        "product.product", string="Product", required=True)
    quantity = fields.Integer(string="Quantity")
    date = fields.Date(default=lambda self: fields.Date.today())
    pay = fields.Float(string="Pay", compute="_compute_pay")   

    @api.depends("product_id.standard_price","quantity")
    def _compute_pay(self):
        for product in self:
            product.pay = product.product_id.standard_price * product.quantity

    # @api.model
    # def _search_this_week(self, operator, value):
    #     current_date = fields.Date.today()
    #     start_of_week = current_date - timedelta(days=current_date.weekday())
    #     end_of_week = start_of_week + timedelta(days=6)
    #     return [('date', '>=', start_of_week.strftime('%Y-%m-%d')), ('date', '<=', end_of_week.strftime('%Y-%m-%d'))]
    
    # # Register the search filter
    # _searchable = [
    #     (_search_this_week, 'This Week'),
    # ]
