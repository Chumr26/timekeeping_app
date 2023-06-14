from odoo import fields, models#type:ignore


class Many(models.Model):
    _name = "timekeeping.many"
    _description = "Timekeeping Many"

    line_ids = fields.One2many(
        "timekeeping.table",
        "worker_id",
        ondelete="cascade",
    )
    date = fields.Date(related='line_ids.date',default=lambda self: fields.Date.today(),
        track_visibility="always",
        string="Ngày",)
