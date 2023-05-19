from odoo import models, fields, api
from datetime import datetime, timedelta

class Timekeeping(models.Model):
    _name = "timekeeping.table"
    _description = "Timekeeping"

    user_id = fields.Many2one("res.partner", string="User")
    product_id = fields.Many2one(
        "product.product", string="Product", required=True)
    quantity = fields.Integer(string="Quantity")
    date = fields.Date(default=lambda self: fields.Date.today())
    pay = fields.Float(string="Pay", compute="_compute_pay", store=True)

    @api.depends("product_id.list_price", "quantity")
    def _compute_pay(self):
        for product in self:
            product.pay = product.product_id.list_price * product.quantity