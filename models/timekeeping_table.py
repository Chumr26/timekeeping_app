from odoo import models, fields, api
from datetime import datetime, timedelta


class Timekeeping(models.Model):
    _name = "timekeeping.table"
    _description = "Timekeeping"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    partner_id = fields.Many2one(
        "res.partner",
        delegate=True,
        ondelete="cascade",
        required=True,
        track_visibility="always",
    )
    product_id = fields.Many2one("product.product", required=True, track_visibility="always",)
    quantity = fields.Integer(track_visibility="always")
    date = fields.Date(default=lambda self: fields.Date.today(), track_visibility="always",)
    pay = fields.Float(compute="_compute_pay", store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)

    @api.depends("product_id.list_price", "quantity")
    def _compute_pay(self):
        for product in self:
            product.pay = product.product_id.list_price * product.quantity

    #update quantity onhand
    @api.onchange("quantity")
    def _onchange_quantity(self):
        quant = self.env["stock.quant"].search(
            [("product_id", "=", self.product_id.id)], limit=1)
        if quant:
            total_quantity = quant.quantity + self.quantity
            quant.write({"quantity": total_quantity})