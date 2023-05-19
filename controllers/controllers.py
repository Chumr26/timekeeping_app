# -*- coding: utf-8 -*-
# from odoo import http


# class TimekeepingApp(http.Controller):
#     @http.route('/timekeeping_app/timekeeping_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/timekeeping_app/timekeeping_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('timekeeping_app.listing', {
#             'root': '/timekeeping_app/timekeeping_app',
#             'objects': http.request.env['timekeeping_app.timekeeping_app'].search([]),
#         })

#     @http.route('/timekeeping_app/timekeeping_app/objects/<model("timekeeping_app.timekeeping_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('timekeeping_app.object', {
#             'object': obj
#         })
