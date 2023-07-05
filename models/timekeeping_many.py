from odoo import fields, models, api  # type:ignore


class Many(models.Model):
    _name = "timekeeping.many"
    _description = "Timekeeping Many"

    line_ids = fields.One2many(
        "timekeeping.table",
        "worker_id",
        required=True,
        ondelete="cascade",

    )
    date = fields.Date(
        related='line_ids.date',
        # default=lambda self: fields.Date.today(),
        string="Ngày",

    )

    company_id = fields.Many2one(
        related='line_ids.company_id',
        required=True,
    )
