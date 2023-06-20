from xml.dom import ValidationErr
from odoo import fields, models,api#type:ignore


class Many(models.Model):
    _name = "timekeeping.many"
    _description = "Timekeeping Many"

    line_ids = fields.One2many(
        "timekeeping.table",
        "worker_id",
        ondelete="cascade",
    )
    date = fields.Date(
        related='line_ids.date',
        default=lambda self: fields.Date.today(),
        track_visibility="always",
        string="Ngày",)
    
    company_id = fields.Many2one(
        related='line_ids.company_id',
        string="Xưởng", 
        readonly = False, 
        required=True 
        )
    
  