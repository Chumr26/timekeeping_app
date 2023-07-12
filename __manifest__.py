# -*- coding: utf-8 -*-
{
    'name': "Sản lượng",

    'summary': """
        Chấm công nhân công và cập nhật sản lượng""",

    'author': "T4tek",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Timekeeping',
    'version': '16.0.1.0.0',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['product', 'mail', 'stock', 'hr'],#, 'sale'

    # always loaded
    'data': [
        'security/timekeeping_security.xml',
        'security/ir.model.access.csv',
        'views/timekeeping_menu.xml',
        'views/timekeeping_view.xml',
        'views/many_view.xml',
        'views/employee.xml',
        'views/stock_edit.xml',
    ],
}
