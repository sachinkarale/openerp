# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
import re
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _
import logging
# main mako-like expression pattern
EXPRESSION_PATTERN = re.compile('(\$\{.+?\})')


class mail_compose_message(osv.TransientModel):    
    _inherit = 'mail.compose.message'
    _description = 'Email composition wizard'
    _log_access = True
    _columns = {
            'email_to':fields.char('Email To',size=256),
            'email_ids':fields.char('All Recipients', size=240),
            'email_cc':fields.char('Email cc', size=240),
    }    
    
    def onchange_partner_ids(self, cr, uid, ids, partner_ids,email_ids , context=None):
        res_partner_obj = self.pool.get('res.partner')
        vals = {'email_ids':''}        
        email = ''
        if not email_ids:
            email_ids = ''
        if partner_ids:    
            for partner in partner_ids[0][2]:
                partner_id_browse=res_partner_obj.browse(cr, uid, partner)
                if partner_id_browse.email not in email_ids:
                    email += email_ids + partner_id_browse.email+';'
                    vals['email_ids'] = email
        return {'value':vals}
    
    
    #------------------------------------------------------
    # Wizard validation and send
    #------------------------------------------------------

    def send_mail(self, cr, uid, ids, context=None):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed. """
        if context is None:
            context = {}
        ir_attachment_obj = self.pool.get('ir.attachment')
        active_ids = context.get('active_ids')
        is_log = context.get('mail_compose_log', False)

        for wizard in self.browse(cr, uid, ids, context=context):
            mass_mail_mode = wizard.composition_mode == 'mass_mail'
            active_model_pool_name = wizard.model if wizard.model else 'mail.thread'
            active_model_pool = self.pool.get(active_model_pool_name)

            # wizard works in batch mode: [res_id] or active_ids
            res_ids = active_ids if mass_mail_mode and wizard.model and active_ids else [wizard.res_id]
            for res_id in res_ids:
                # mail.message values, according to the wizard options
                post_values = {
                    'subject': wizard.subject,
                    'body': wizard.body,
                    'parent_id': wizard.parent_id and wizard.parent_id.id,
                    'partner_ids': [partner.id for partner in wizard.partner_ids],
                    'attachment_ids': [attach.id for attach in wizard.attachment_ids],
                    'attachments': [],
                    'email_ids': wizard.email_ids,
                    'email_cc': wizard.email_cc,
                }
                # mass mailing: render and override default values
                if mass_mail_mode and wizard.model:
                    email_dict = self.render_message(cr, uid, wizard, res_id, context=context)
                    post_values['partner_ids'] += email_dict.pop('partner_ids', [])
                    for filename, attachment_data in email_dict.pop('attachments', []):
                        # decode as render message return in base64 while message_post expect binary
                        post_values['attachments'].append((filename, base64.b64decode(attachment_data)))
                    attachment_ids = []
                    for attach_id in post_values.pop('attachment_ids'):
                        new_attach_id = ir_attachment_obj.copy(cr, uid, attach_id, {'res_model': self._name, 'res_id': wizard.id}, context=context)
                        attachment_ids.append(new_attach_id)
                    post_values['attachment_ids'] = attachment_ids
                    post_values.update(email_dict)
                # post the message
                subtype = 'mail.mt_comment'
                if is_log:  # log a note: subtype is False
                    subtype = False
                elif mass_mail_mode:  # mass mail: is a log pushed to recipients, author not added
                    subtype = False
                    context = dict(context, mail_create_nosubscribe=True)  # add context key to avoid subscribing the author
                msg_id = active_model_pool.message_post(cr, uid, [res_id], type='comment', subtype=subtype, context=context, **post_values)
                # mass_mailing: notify specific partners, because subtype was False, and no-one was notified
                if mass_mail_mode and post_values['partner_ids']:
                    self.pool.get('mail.notification')._notify(cr, uid, msg_id, post_values['partner_ids'], post_values['email_ids'],post_values['email_cc'], context=context)

        return {'type': 'ir.actions.act_window_close'}
        
    #------------------------------------------------------
    # Wizard validation and send
    #------------------------------------------------------    
    def generate_email_for_composer(self, cr, uid, template_id, res_id, context=None):
        """ Call email_template.generate_email(), get fields relevant for
            mail.compose.message, transform email_cc and email_to into partner_ids """
        template_values = self.pool.get('email.template').generate_email(cr, uid, template_id, res_id, context=context)
        # filter template values
        fields = ['body_html', 'subject', 'email_to', 'email_recipients', 'email_cc', 'attachment_ids', 'attachments']
        values = dict((field, template_values[field]) for field in fields if template_values.get(field))
        values['body'] = values.pop('body_html', '')

        # transform email_to, email_cc into partner_ids
        partner_ids = set()
        mails = tools.email_split(values.pop('email_to', '')) + tools.email_split(values.pop('email_cc', ''))
        ctx = dict((k, v) for k, v in (context or {}).items() if not k.startswith('default_'))
        for mail in mails:
            partner_id = self.pool.get('res.partner').search(cr, uid, [('email','=',mail)])
            if partner_id:
                partner_ids.add(partner_id[0])
            else:
                values['email_ids'] = mail
        email_recipients = values.pop('email_recipients', '')        
        if email_recipients:
            for partner_id in email_recipients.split(','):
                if partner_id:  # placeholders could generate '', 3, 2 due to some empty field values
                    partner_ids.add(int(partner_id))
        # legacy template behavior: void values do not erase existing values and the
        # related key is removed from the values dict
        if partner_ids:
            values['partner_ids'] = list(partner_ids)
        return values
    
