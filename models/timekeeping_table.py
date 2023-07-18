from odoo import models, fields, api  # type:ignore
from odoo.exceptions import ValidationError  # type:ignore
from dateutil.relativedelta import relativedelta
from datetime import date
import calendar


class Timekeeping(models.Model):
    _name = "timekeeping.table"
    _description = "Timekeeping"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    order_id = fields.Many2one(
        "sale.order",
        string="Đơn hàng",
    )
    order_line_id = fields.Many2one(
        "sale.order.line",
        track_visibility="always",
        string="Mã hàng",
    )
    employee_id = fields.Many2one(
        "hr.employee",
        delegate=True,
        ondelete="cascade",
        required=True,
        track_visibility="always",
        string="Nhân viên",
    )

    company_id = fields.Many2one(
        "res.company",
        string="Xưởng",
    )
    list_price = fields.Float(
        string='Đơn giá',
        readonly=True,
        related='order_line_id.product_id.list_price',
        groups='timekeeping_app.timekeeping_group_manager'
    )
    quantity = fields.Integer(
        track_visibility="always",
        string="Số lượng",
    )
    date = fields.Date(
        default=lambda self: fields.Date.today(),
        track_visibility="always",
        string="Ngày",
    )
    # field này dùng cho filter
    quarter = fields.Integer(
        compute="_compute_date_filter",
        store=True
    )
    # field này dùng cho filter
    # year = fields.Integer(
    #     compute="_compute_date_filter",
    #     store=True
    # )
    pay = fields.Float(
        compute="_compute_pay",
        store=True,
        string="Thành tiền",
        groups='timekeeping_app.timekeeping_group_manager'
    )
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id.id
    )
    location_id = fields.Many2one(
        "stock.location",
        default=8,
    )
    worker_id = fields.Many2one(
        "timekeeping.many",
        ondelete="cascade",
    )
    image_1920 = fields.Image(
        string="Ảnh",
        related='order_line_id.product_id.image_1920',
    )
    reason = fields.Many2one(
        "timekeeping.reason",
        string="Lý do"
    )
    note = fields.Char(
        string="Ghi chú",
        widget="textarea",
    )

    @api.constrains('date')
    def _check_date(self):
        for rec in self:
            if rec.order_id and rec.date < rec.order_id.date_order.date():
                raise ValidationError("Invalid date!")

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError("Not allow positive number!")

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            self.company_id = self.employee_id.company_id.id

    @api.depends("order_line_id.product_id.list_price", "quantity")
    def _compute_pay(self):
        for product in self:
            product.pay = product.order_line_id.product_id.list_price * product.quantity

    # update quantity onhand
    @ api.onchange("quantity")
    def _onchange_quantity(self):
        if self.quantity != 0:
            quant = self.env["stock.quant"].search(
                [("product_id", "=", self.order_line_id.product_id.id)], limit=1)
            if self._origin.id and quant:
                total_quantity = quant.quantity - self._origin.quantity + self.quantity
                quant.write({"quantity": total_quantity})
            elif quant:
                total_quantity = quant.quantity + self.quantity
                quant.write({"quantity": total_quantity})
            else:
                self.env["stock.quant"].create({
                    "product_id": self.order_line_id.product_id.id,
                    "quantity": self.quantity,
                    "location_id": self.location_id.id
                })

    @api.onchange('order_id')
    def _onchange_order_id(self):
        # Clear the values of dependent fields
        if self.order_id:
            self.order_line_id = False
            self.quantity = False
            self.reason = False
            self.image_1920 = False
            self.note = ""

    @api.onchange('company_id')
    def _onchange_company_id(self):
        # Clear the values of dependent fields
        if self._context.get('params', {}).get('model') == 'timekeeping.table':
            if self.company_id:
                self.employee_id = False

    # @api.depends("date")
    # def _compute_date_filter(self):
    #     for rc in self:
    #         rc.quarter = (rc.date.month - 1) // 3 + 1
    #         rc.year = rc.date.year