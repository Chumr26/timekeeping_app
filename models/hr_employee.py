from odoo import models, fields, api  # type:ignore
from odoo.exceptions import ValidationError  # type:ignore


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    position_selection = [
        ('position_1', 'Quản lý'),
        ('position_2', 'Nhân viên kho'),
        ('position_3', 'Nhân viên bán hàng'),
        ('position_4', 'Thợ in'),
    ]
    job_title_1 = fields.Selection(
        position_selection,
        string="Chức vụ",
        required=True,
    )