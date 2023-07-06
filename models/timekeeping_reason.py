from odoo import models, fields  # type:ignore


class Reason(models.Model):
    _name = "timekeeping.reason"
    _description = "Reason"

    reason = fields.Char()

    def name_get(self):
        result = []
        for record in self:
            display_name = record.reason  # Customize the display name based on your requirements
            result.append((record.id, display_name))
        return result