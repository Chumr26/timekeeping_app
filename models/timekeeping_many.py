from odoo import fields, models#type:ignore


class Many(models.Model):
    _name = "timekeeping.many"
    _description = "Timekeeping Many"

    date = fields.Date(
        default= fields.Date.today()
    )
    line_ids = fields.One2many(
        "timekeeping.table",
        "worker_id",
        ondelete="cascade",
    )