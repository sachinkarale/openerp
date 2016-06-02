# -*- coding: utf-8 -*-
import base64
import logging

from openerp import netsvc
from openerp.osv import osv, fields
from openerp.osv import fields
from openerp import tools
from openerp.tools.translate import _
from urllib import urlencode, quote as quote
from datetime import datetime
import datetime
import time

_logger = logging.getLogger(__name__)
class email_template(osv.osv):
    _inherit='email.template'

    def send_mail_custom(self, cr, uid, template_id, res_id, force_send=False, obj=False, context=None):
        """ Custom Function to  Generates a new mail message for the given template and record,
           and schedules it for delivery through the ``mail`` module's scheduler.

           :param int template_id: id of the template to render
           :param int res_id: id of the record to render the template with
                              (model is taken from the template)
           :param bool force_send: if True, the generated mail.message is
                immediately sent after being created, as if the scheduler
                was executed for this message only.
           :returns: id of the mail.message that was created
        """
        if context is None:
            context = {}
        mail_mail = self.pool.get('mail.mail')
        ir_attachment = self.pool.get('ir.attachment')

        # create a mail_mail based on values, without attachments
        values = self.generate_email(cr, uid, template_id, res_id, context=context)
        if not values.get('email_from'):
            raise osv.except_osv(_('Warning!'),_("Sender email is missing or empty after template rendering. Specify one to deliver your message"))
        # process email_recipients field that is a comma separated list of partner_ids -> recipient_ids
        # NOTE: only usable if force_send is True, because otherwise the value is
        # not stored on the mail_mail, and therefore lost -> fixed in v8
        recipient_ids = []
        email_recipients = values.pop('email_recipients', '')
        if email_recipients:
            for partner_id in email_recipients.split(','):
                if partner_id:  # placeholders could generate '', 3, 2 due to some empty field values
                    recipient_ids.append(int(partner_id))

        attachment_ids = []
#        attachments = values.pop('attachments', [])
        msg_id = mail_mail.create(cr, uid, values, context=context)
        mail = mail_mail.browse(cr, uid, msg_id, context=context)


#        # manage attachments
#        for attachment in attachments:
#            attachment_data = {
#                'name': attachment[0],
#                'datas_fname': attachment[0],
#                'datas': attachment[1],
#                'res_model': 'mail.message',
#                'res_id': mail.mail_message_id.id,
#            }
#            context.pop('default_type', None)
#            attachment_ids.append(ir_attachment.create(cr, uid, attachment_data, context=context))
        if obj:
           for attachment in obj.send_attachment_ids:
                attachment_data = {
                    'name': attachment.name,
                    'datas_fname': attachment.name,
                    'datas': attachment.datas,
                    'res_model': 'mail.message',
                    'res_id': mail.mail_message_id.id,
                }
                attachment_ids.append(ir_attachment.create(cr, uid, attachment_data, context=context))
        print "attachment_ids.......",attachment_ids
        if attachment_ids:
            values['attachment_ids'] = [(6, 0, attachment_ids)]
            mail_mail.write(cr, uid, [msg_id], {'attachment_ids': [(6, 0, attachment_ids)]}, context=context)
#        mail_mail.write(cr, uid, [msg_id], {'custom_type': 'fax'}, context=context)
        if force_send:
            mail_mail.send(cr, uid, [msg_id], recipient_ids=recipient_ids, context=context)
        return msg_id
    


    def send_mail(self, cr, uid, template_id, res_id, force_send=False, context=None):
        """Generates a new mail message for the given template and record,
           and schedules it for delivery through the ``mail`` module's scheduler.

           :param int template_id: id of the template to render
           :param int res_id: id of the record to render the template with
                              (model is taken from the template)
           :param bool force_send: if True, the generated mail.message is
                immediately sent after being created, as if the scheduler
                was executed for this message only.
           :returns: id of the mail.message that was created
        """
        if context is None:
            context = {}
        mail_mail = self.pool.get('mail.mail')
        ir_attachment = self.pool.get('ir.attachment')

        # create a mail_mail based on values, without attachments
        values = self.generate_email(cr, uid, template_id, res_id, context=context)
	if values.get('email_from',False):
        	assert values.get('email_from',False), 'email_from is missing or empty after template rendering, send_mail() cannot proceed'
        del values['email_recipients']  # TODO Properly use them.
        mail_server_id=''
        msg_id = mail_mail.create(cr, uid, values, context=context)
        print"contexxxtttttttttttttt",context
        if context.get('crm_id',False) and context.get('crm_id',False).hr_department_id and context.get('crm_id',False).hr_department_id.mail_server:
	    if context.get('crm_id',False).hr_department_id.mail_server:
           	mail_server_id=context.get('crm_id',False).hr_department_id.mail_server.id
            	mail_mail.write(cr,uid,[msg_id],{'mail_server_id':mail_server_id})
	    else:
            	raise osv.except_osv(_('Warning!'),_("Please specify Outgoing mail server"))
        if context.get('hr_app_id',False) and context.get('hr_app_id',False).bdo_associate and context.get('hr_app_id',False).bdo_associate.hr_department_id and context.get('hr_app_id',False).bdo_associate.hr_department_id.mail_server:
	    if context.get('hr_app_id',False).bdo_associate.hr_department_id.mail_server:
            	mail_server_id=context.get('hr_app_id',False).bdo_associate.hr_department_id.mail_server.id 
            	mail_mail.write(cr,uid,[msg_id],{'mail_server_id':mail_server_id})
	    else:
            	raise osv.except_osv(_('Warning!'),_("Please specify Outgoing mail server"))
        attachment_ids = values.pop('attachment_ids', [])
        attachments = values.get('attachments', [])
        mail_to=values.get('email_to', '')
        print "mail-----to=========",mail_to
        mail_subject=values.get('subject', '')
        print 'leadisddddddddddddd',context.get('lead_id'),context.get('user_id'),context.get('crm_id',False)
        user_id=context.get('user_id')
        user_name=self.pool.get('res.users').browse(cr,uid,user_id).name
        if context.get('lead_id',False):
            cur_date=str(datetime.datetime.now())
            body=values.get('body', '')
            model=values.get('model')
            subject = ('''"%s" emailed "%s on "%s"''') % (user_name,mail_to,cur_date)
#            details = ('''Subject : "%s"''')% (mail_subject)
            details= ('''"%s"''')% (body)
            self.pool.get(model).message_post(cr, uid, [context.get('lead_id')], body=details, subject=subject, context=context)
        
#        erooooooooo
        
        # manage attachments
        for attachment in attachments:
            attachment_data = {
                    'name': attachment[0],
                    'datas_fname': attachment[0],
                    'datas': attachment[1],
                    'res_model': 'mail.message',
                    'res_id': msg_id,
            }
            context.pop('default_type', None)
            attachment_ids.append(ir_attachment.create(cr, uid, attachment_data, context=context))
        if attachment_ids:
            values['attachment_ids'] = [(6, 0, attachment_ids)]
            mail_mail.write(cr, uid, msg_id, {'attachment_ids': [(6, 0, attachment_ids)]}, context=context)

        if force_send:
            mail_mail.send(cr, uid, [msg_id], context=context)
        return msg_id
    
    def generate_email(self, cr, uid, template_id, res_id, context=None):
            """Generates an email from the template for given (model, res_id) pair.

               :param template_id: id of the template to render.
               :param res_id: id of the record to use for rendering the template (model
                              is taken from template definition)
               :returns: a dict containing all relevant fields for creating a new
                         mail.mail entry, with one extra key ``attachments``, in the
                         format expected by :py:meth:`mail_thread.message_post`.
            """
            if context is None:
                context = {}
            report_xml_pool = self.pool.get('ir.actions.report.xml')
            template = self.get_email_template(cr, uid, template_id, res_id, context)
            values = {}
            for field in ['subject', 'body_html', 'email_from',
                          'email_to', 'email_recipients', 'email_cc', 'reply_to']:
                values[field] = self.render_template(cr, uid, getattr(template, field),
                                                     template.model, res_id, context=context) \
                                                     or False
            if template.user_signature:
                signature = self.pool.get('res.users').browse(cr, uid, uid, context).signature
                values['body_html'] = tools.append_content_to_html(values['body_html'], signature)

            if values['body_html']:
                values['body'] = tools.html_sanitize(values['body_html'])
            values.update(mail_server_id=template.mail_server_id.id or False,
                          auto_delete=template.auto_delete,
                          model=template.model,
                          res_id=res_id or False)
            if context.get('pending_app',False):
                print"context.get('pending_app').email_from",context.get('pending_app').email_from
                
                values.update({'email_to':context.get('pending_app').email_from})
            if context.get('new_opp',False):


                values.update({'email_to':context.get('new_opp',False)})
            if context.get('app_completed',False):
                values.update({'email_cc':context.get('app_completed',False)})
            
            attachments = []
            # Add report in attachments
            if template.report_template:
                report_name = self.render_template(cr, uid, template.report_name, template.model, res_id, context=context)
                report_service = 'report.' + report_xml_pool.browse(cr, uid, template.report_template.id, context).report_name
                # Ensure report is rendered using template's language
                ctx = context.copy()
                if template.lang:
                    ctx['lang'] = self.render_template(cr, uid, template.lang, template.model, res_id, context)
                service = netsvc.LocalService(report_service)
                (result, format) = service.create(cr, uid, [res_id], {'model': template.model}, ctx)
                result = base64.b64encode(result)
                if not report_name:
                    report_name = report_service
                ext = "." + format
                if not report_name.endswith(ext):
                    report_name += ext
                attachments.append((report_name, result))

            attachment_ids = []
            # Add template attachments
            for attach in template.attachment_ids:
                attachment_ids.append(attach.id)

            values['attachments'] = attachments
            values['attachment_ids'] = attachment_ids
            return values
email_template()


class mail_compose_message(osv.TransientModel):
    _inherit = 'mail.compose.message'



    def onchange_template_id(self, cr, uid, ids, template_id, composition_mode, model, res_id, context=None):
        """ - mass_mailing: we cannot render, so return the template values
            - normal mode: return rendered values """
        if template_id and composition_mode == 'mass_mail':
            values = self.pool.get('email.template').read(cr, uid, template_id, ['subject', 'body_html', 'attachment_ids'], context)
            values.pop('id')
        elif template_id:
            values = self.generate_email_for_composer(cr, uid, template_id, res_id, context=context)
            print "valuessssssssssssssssssss=============222222222",values
            # transform attachments into attachment_ids; not attached to the document because this will
            # be done further in the posting process, allowing to clean database if email not send
            values['attachment_ids'] = values.pop('attachment_ids', [])
            ir_attach_obj = self.pool.get('ir.attachment')
            for attach_fname, attach_datas in values.pop('attachments', []):
                data_attach = {
                    'name': attach_fname,
                    'datas': attach_datas,
                    'datas_fname': attach_fname,
                    'res_model': 'mail.compose.message',
                    'res_id': 0,
                    'type': 'binary',  # override default_type from context, possibly meant for another model!
                }
                values['attachment_ids'].append(ir_attach_obj.create(cr, uid, data_attach, context=context))
        else:
            values = self.default_get(cr, uid, ['body', 'subject', 'partner_ids', 'attachment_ids'], context=context)
        print "valuessssssssssssssssssssssssssss----------------------abc",values
#        erooooooooooooooooo
        if template_id:
            email_temp_obj=self.pool.get('email.template')
            email_to=email_temp_obj.browse(cr,uid,template_id).email_to
            email_cc=email_temp_obj.browse(cr,uid,template_id).email_cc
	    if email_to:
                model_id=email_temp_obj.browse(cr,uid,template_id).model_id.model
                mail_to=email_temp_obj.render_template(cr, uid, email_to, model_id, res_id, context=None)
                values['email_to'] = mail_to
            if email_cc:
                model_id=email_temp_obj.browse(cr,uid,template_id).model_id.model
                mail_cc=email_temp_obj.render_template(cr, uid, email_cc, model_id, res_id, context=None)
                values['email_cc'] = mail_cc
                partner_ids=values.get('partner_ids')
                print "partnerids=======================",partner_ids
                if partner_ids:
                    partner_new_ids=[]
                    partner_obj=self.pool.get('res.partner')
                    for each in partner_ids:
                        email=partner_obj.browse(cr,uid,each).email
                        if email not in mail_cc:
                            partner_new_ids.append(each)
                    print "newpartner_ids==============",partner_new_ids
                    values['partner_ids'] = partner_new_ids





#                eroooooooo
        if values.get('body_html'):
            values['body'] = values.pop('body_html')
        return {'value': values}



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
        mails = tools.email_split(values.pop('email_to', '') + ' ' + values.pop('email_cc', ''))
        for mail in mails:
            partner_id = self.pool.get('res.partner').find_or_create(cr, uid, mail, context=context)
            partner_ids.add(partner_id)
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

mail_compose_message()
