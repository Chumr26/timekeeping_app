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
        default=lambda self: fields.Date.today(),
        string="Ngày",
    )
    company_id = fields.Many2one(
        "res.company",
        required=True,
        string="Xưởng",
    )

    @api.onchange('company_id')
    def _onchange_company_id(self):
        self.line_ids = False