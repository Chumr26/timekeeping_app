from xml.dom import ValidationErr
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
        default=lambda self: fields.Date.today(),
        track_visibility="always",
        string="Ngày",
        
        )

    company_id = fields.Many2one(
        # 'res.company',
        related='line_ids.company_id',
        readonly=False,
        required=True,
        
    )
