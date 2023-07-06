from odoo import models, fields, api  # type:ignore
from odoo.exceptions import ValidationError  # type:ignore


class Timekeeping(models.Model):
    _name = "timekeeping.table"
    _description = "Timekeeping"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    employee_id = fields.Many2one(
        "hr.employee",
        delegate=True,
        ondelete="cascade",
        required=True,
        track_visibility="always",
        string="Nhân viên",
    )

    partner_id = fields.Many2one(
        "res.partner",
        # required=True,
        track_visibility="always",
        string="Khách hàng",
    )

    company_id = fields.Many2one(
        "res.company",
        required=True,
        string="Xưởng",
    )
    # product_id = fields.Many2one('product.template', string='Product')
    list_price = fields.Float(string='Đơn giá', related='order_line_id.product_id.list_price',
                              readonly=True, groups='timekeeping_app.timekeeping_group_manager')
    order_line_id = fields.Many2one(
        "sale.order.line",
        track_visibility="always",
        string="Sản phẩm",
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
    pay = fields.Float(
        compute="_compute_pay",
        store=True,
        string="Thành tiền",
        groups='timekeeping_app.timekeeping_group_manager'
    )
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id.id)
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
    )
    note = fields.Char(
        string="Ghi chú",
        widget="textarea",
    )
    order_id = fields.Many2one(
        "sale.order",
        string="Đơn hàng",
        # domain="[('partner_id', '=', partner_id)]"
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

    @api.constrains('employee_id', 'company_id', 'partner_id')
    def _check_partner_company(self):
        for record in self:
            if record.employee_id and record.partner_id:
                if record.employee_id.company_id != record.partner_id.company_id:
                    raise ValidationError(
                        "Selected partner must belong to the selected company.")
            elif record.employee_id and not record.partner_id:
                if record.employee_id.company_id != record.company_id:
                    raise ValidationError(
                        "Selected employee must belong to the selected company.")

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.employee_id:
            self.company_id = self.employee_id.company_id.id

    @ api.depends("order_line_id.product_id.list_price", "quantity")
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
        self.order_line_id = False
        self.quantity = False
        self.reason = False
        self.image_1920 = False
        self.note = False

    # @api.onchange('company_id')
    # def _onchange_company_id(self):
    #     # Clear the values of dependent fields
    #     self.employee_id = False