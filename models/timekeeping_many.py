from odoo import fields, models#type:ignore


class Many(models.Model):
    _name = "timekeeping.many"
    _description = "Timekeeping Many"

    manager_id = fields.Many2one(
        "res.users",
        required=True,
        default=lambda s: s.env.user,
    )
    date = fields.Date(
        default=lambda s: fields.Date.today(),
    )
    line_ids = fields.One2many(
        "timekeeping.table",
        "worker_id",
        ondelete="cascade",
    )