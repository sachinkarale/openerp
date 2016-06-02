# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009 Sharoon Thomas
#    Copyright (C) 2010-Today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

import base64
import logging

from openerp import netsvc
from openerp.osv import osv, fields
from openerp.osv import fields
from openerp import tools
from openerp.tools.translate import _
from urllib import urlencode, quote as quote

_logger = logging.getLogger(__name__)

class email_template(osv.osv):
    _inherit = "email.template"

    _columns = {
        'send_product_attachments': fields.boolean('Send Attachments?', help='On the sale order email composition wizard, attach also all attachments related to each products of the sale order'),      
    }
    def get_product_attachments(self, cr, uid, template_id, res_id, context=None):
        attachment_ids = self.pool['ir.attachment'].search(cr, uid, [('res_model','=','crm.lead'),('res_id','in',[res_id]),('send_doc','=',True)], context=context)
        return attachment_ids

    def generate_email(self, cr, uid, template_id, res_id, context=None):
        values = super(email_template, self).generate_email(cr, uid, template_id, res_id, context=context)
        template = self.get_email_template(cr, uid, template_id, res_id, context)
        if template.send_product_attachments:
            product_attachment_ids = self.get_product_attachments(cr, uid, template_id, res_id, context=context)
            print"product_attachment_ids",product_attachment_ids
            values['attachment_ids'].extend(product_attachment_ids)
        return values

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
