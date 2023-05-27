from odoo import models, fields, api #type:ignore


class Timekeeping(models.Model):
    _name = "timekeeping.table"
    _description = "Timekeeping"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    partner_id = fields.Many2one(
        "res.partner",
        delegate=True,
        ondelete="cascade",
        required=True,
        track_visibility="always",)
    product_id = fields.Many2one(
        "product.product", required=True, track_visibility="always",)
    quantity = fields.Float(track_visibility="always")
    date = fields.Date(default=lambda self: fields.Date.today(),
                       track_visibility="always",)
    pay = fields.Float(compute="_compute_pay", store=True)
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id.id)
    location_id = fields.Many2one("stock.location", default=8)
    worker_id = fields.Many2one(
        "timekeeping.many",
        required=True,
        ondelete="cascade",
    )

    @api.depends("product_id.list_price", "quantity")
    def _compute_pay(self):
        for product in self:
            product.pay = product.product_id.list_price * product.quantity

    # update quantity onhand
    @api.onchange("quantity")
    def _onchange_quantity(self):
        if self.quantity != 0:
            quant = self.env["stock.quant"].search(
                [("product_id", "=", self.product_id.id)], limit=1)
            if self._origin.id and quant:
                total_quantity = quant.quantity - self._origin.quantity + self.quantity
                quant.write({"quantity": total_quantity})
            elif quant:
                total_quantity = quant.quantity + self.quantity
                quant.write({"quantity": total_quantity})
            else:
                self.env["stock.quant"].create({
                    "product_id": self.product_id.id,
                    "quantity": self.quantity,
                    "location_id": self.location_id.id
                })
