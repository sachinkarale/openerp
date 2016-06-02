# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-Today OpenERP S.A. (<http://www.openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import re
from openerp.osv import osv, fields
import openerp.tools as tools
from openerp.tools.translate import _
from openerp.tools import html2plaintext
from openerp.tools import flatten
from tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
import datetime
import time

class sent_fax_response(osv.Model):
    ''' Keeps response of sent fax '''
    _description = 'Sent Fax Response'
    _name = 'sent.fax.response'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _columns = {
        'name': fields.char('Subject', size=300),
        'message_id': fields.char( 'Message Id', size=300),
        'email_from': fields.char('From', help='Message sender, taken from user preferences.'),
        'email_to': fields.text('To', help='Message recipients',),
        'email_cc': fields.char('Cc', help='Carbon copy message recipients'),
        'reply_to': fields.char('Reply-To', help='Preferred response address for the message'),
        'body': fields.text('Body', help="Rich-text/HTML message"),
        'fax': fields.char('Fax', size=64, select=1),
        'status': fields.char('status', size=64, select=1),
        'date': fields.datetime('Date'),
        'company_id': fields.many2one('res.company', 'Company', select=1,),
#        'fax_attachment_ids': fields.many2many('ir.attachment', 'sent_fax_attachment_rel',
#                                                'fax_id', 'attachment_id', 'Attachments'),
        }
    _defaults = {
        'company_id': lambda self, cr, uid, ctx: self.pool.get('res.company')._company_default_get(cr, uid, 'sent.fax.response', context=ctx),
        }

    def message_new(self, cr, uid, msg, custom_values=None, context=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        for key in msg.iterkeys():
            print "key.....",key
        if custom_values is None:
            custom_values = {}
        if context is None:
            context = {}
#        print "msg.get('body').......",msg.get('body','')
        desc = ''
        try:
            desc = html2plaintext(msg.get('body')) if msg.get('body',False) else ''
        except Exception ,e :
            pass
        defaults = {
            'name':  str(msg.get('subject'))[:299] or _("No Subject"),
            'email_to': msg.get('to'),
            'email_from': msg.get('from'),
            'email_cc': msg.get('cc'),
#            'author': msg.get('author_id', False),
            'message_id': str(msg.get('message_id', False))[:299],
            'body': desc or '',
        }
        if msg.get('date', False):
            defaults['date'] = str(msg.get('date', False))

        subject = str(msg.get('subject')) or _("No Subject")
        subject = 'Unsuccessful fax transmission to 18582253436. Re: 18582253436'
        subject = subject.upper()
        if subject.find('UNSUCCESSFUL') >= 0:
            defaults['status'] = 'unsuccessful'
        elif subject.find('SUCCESSFUL') >= 0:
            defaults['status'] = 'successful'
        else:
            defaults['status'] = 'unsuccessful'
        try:
            lst = [int(s) for s in subject.split() if s.isdigit()]
            #print "lst.........",lst
            lst = flatten(lst)
            lst = list(set(lst))
            if lst:
                defaults['fax'] = lst[0]
            else:
                defaults['fax'] = ''
#            defaults['fax'] = int(re.match(r'\d+', subject).group())
        except Exception ,e :
            defaults['fax'] = ''
            pass
#        int_str = re.sub(r'[^0-9]',r'', subject)
#        print "int_str....",int_str
#        fax = int_str.split(' ')[0]
#        print "fax.........",fax

        defaults.update(custom_values)
        res_id = super(sent_fax_response, self).message_new(cr, uid, msg, custom_values=defaults, context=context)
#        print "res_id........",res_id
        attachments = custom_values.get('attachments', [])
        # manage attachments
        for attachment in attachments:
            attachment_data = {
                'name': attachment[0],
                'datas_fname': attachment[0],
                'datas': attachment[1],
                'res_model': 'incoming.fax',
                'res_id': res_id,
            }
            context.pop('default_type', None)
            attachment_ids.append(ir_attachment.create(cr, uid, attachment_data, context=context))
        return res_id

class incoming_fax(osv.Model):
    '''Keeps Incoming Fax'''
    _name = 'incoming.fax'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Incoming Fax'

    def write(self , cr ,uid ,ids ,vals , context=None):
        #print "write for mail.message......."
        res = []
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res =  super(incoming_fax , self ).write( cr ,uid ,ids ,vals , context=None)

        for cur in self.browse( cr ,uid , ids ):
            if cur.event_id:
                for attach in cur.fax_attachment_ids:
                    #print "attach.attach........",attach.attach
                    if attach.attach:
                        self.pool.get('ir.attachment').write(cr ,uid ,attach.id ,{'res_model':'event', 'res_id':cur.event_id.id,'res_name':cur.event_id.name})
        return res

    _columns = {
        'name': fields.char('Subject', size=300),
        'message_id': fields.char( 'Message Id', size=300),
        'email_from': fields.char('From', help='Message sender, taken from user preferences.'),
        'email_to': fields.text('To', help='Message recipients',),
        'email_cc': fields.char('Cc', help='Carbon copy message recipients'),
        'reply_to': fields.char('Reply-To', help='Preferred response address for the message'),
        'body': fields.text('Body', help="Rich-text/HTML message"),
        'fax': fields.char('Fax', size=64, select=1),
        'caller_id': fields.char('Caller_id', size=64, select=1),
        'date': fields.datetime('Date'),
#        'event_id':fields.many2one('event','Event'),
        'company_id': fields.many2one('res.company', 'Company', select=1,),
        'fax_attachment_ids': fields.many2many('ir.attachment', 'fax_attachment_rel',
            'fax_id', 'attachment_id', 'Attachments'),
        }
    def message_new(self, cr, uid, msg, custom_values=None, context=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        print "custom_values.........",custom_values
#        for key in msg.iterkeys():
#            print "key.....",key
        if custom_values is None:
            custom_values = {}
        if context is None:
            context = {}
#        print "msg.get('body').......",msg.get('body','')
        desc = ''
        try:
            desc = html2plaintext(msg.get('body')) if msg.get('body',False) else ''
        except Exception ,e :
            pass
        defaults = {
            'name':  str(msg.get('subject'))[:299] or _("No Subject"),
            'email_to': msg.get('to'),
            'email_from': msg.get('from'),
            'email_cc': msg.get('cc'),
            'message_id': str(msg.get('message_id', False))[:299],
            'body': desc or '',
        }
        if msg.get('date', False):
            defaults['date'] = str(msg.get('date', False))

        subject = str(msg.get('subject')) or _("No Subject")
        subject = 'eFax message from "912266459412" - 1 page(s), Caller-ID: 1-613-701-0200'
        subject = subject.upper()
        lst = re.findall('"([^"]*)"', subject)
        if lst:
            if lst:
                defaults['fax'] = lst[0]
            else:
                defaults['fax'] = ''
        try:
            lst = ''
            lst = subject.split(': ')
            lst = flatten(lst)
            lst = list(set(lst))
            print "lst.......",lst,len(lst)
            if len(lst) > 1 :
                defaults['caller_id'] = lst[0]
            else:
                defaults['caller_id'] = ''
#            defaults['fax'] = int(re.match(r'\d+', subject).group())
        except Exception ,e :
            print "e,.args...",e.args
            defaults['caller_id'] = ''
            pass

        defaults.update(custom_values)
        attachments = custom_values.pop('attachments', [])
        print "attachments........",attachments
        res_id = super(incoming_fax, self).message_new(cr, uid, msg, custom_values=defaults, context=context)
#        print "res_id........",res_id
        attachment_ids = []
        # manage attachments
        for attachment in attachments:
            attachment_data = {
                'name': attachment[0],
                'datas_fname': attachment[0],
                'datas': attachment[1],
                'res_model': 'incoming.fax',
                'res_id': res_id,
            }
            context.pop('default_type', None)
            attachment_ids.append(ir_attachment.create(cr, uid, attachment_data, context=context))
        print "attachment_ids.....",attachment_ids
        self.pool.get('incoming.fax').write(cr , uid , [res_id], {'fax_attachment_ids': [(6, 0, attachment_ids)]})
        return res_id

class fax_attachments(osv.TransientModel):
    '''Used in fax Attachments '''
    _name = 'fax.attachments'
    _description = 'Fax Attachments'
    _columns = {
                'name': fields.char('Attachment name'),
                'datas': fields.binary('Attachment'),
                'send_fax_id': fields.many2one('send.fax','Send Fax'),
               }

class outgoing_fax(osv.Model):
    '''Fax Sent History '''
    _name = 'outgoing.fax'
    _description = 'Outgoing Fax'
    _columns = {
        'name': fields.char('Attachment name'),
        'partner_id': fields.many2one('res.partner',"Partner", required=True),
        'fax': fields.char('Fax', size=64),
        'date': fields.datetime('Date'),
        'company_id': fields.many2one('res.company', 'Company', select=1,),
#                'fax_attachment_ids': fields.many2many('ir.attachment', 'fax_attachment_rel',
#                    'fax_id', 'attachment_id', 'Attachments'),
               }
    _defaults = {
        'company_id': lambda self, cr, uid, ctx: self.pool.get('res.company')._company_default_get(cr, uid, 'outgoing.fax', context=ctx),
        }

class send_fax(osv.osv_memory):
    '''Form For Fax sending '''
    _name = 'send.fax'
    _description = 'Send Faxes'
    def _get_name(self, cr, uid, ids, name, arg, context=None):
        ''' Returns name for Fax '''
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.partner_id :
                result[obj.id] =  obj.partner_id.name
            else:
                result[obj.id] = ""
        #print "result..........",result
        return result

    def _get_fax(self, cr, uid, ids, name, arg, context=None):
        ''' Returns Fax  '''
        result = {}
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.partner_id :
                if obj.partner_id.fax1:
                    result[obj.id] =  re.sub(r'[^0-9]',r'',obj.partner_id.fax1)
                else:
                    result[obj.id] = ""
            else:
                result[obj.id] = ""
        print "result..........",result
        return result

    def _count_attachments(self, cr, uid, ids, name, arg, context=None):
        ''' Returns No of Attachments  '''
        result = {}
        count = 0
        for obj in self.browse(cr, uid, ids, context=context):
            if obj.send_attachment_ids :
                for attachment in obj.send_attachment_ids:
                    count += 1

        result[obj.id] = count
        #print "result..........",result
        return result
    
    _columns={
        'name': fields.function(_get_name, string='Is Empty', type="char", store=True),
        'partner_id': fields.many2one('crm.lead',"Opportunity", required=True),
#        'opp_id': fields.many2one('crm.lead',"Opportunity"),
        'opp_fax_ids': fields.many2many('app.documents','opportunity_fax_rel','opp_id','fax_id','Opportunity'),
        'body_fax': fields.html('Contents', help='Automatically sanitized HTML contents'),
        'send_attachment_ids': fields.one2many('fax.attachments','send_fax_id',"Attachments"),
        'state': fields.selection([('draft','Draft'),('done','Sent')],'State'),
        'fax': fields.function(_get_fax, string='Fax', type="char", store=True),
        'show_fax': fields.char('Fax', size=32),
        'count': fields.function(_count_attachments, string='No of Attachments',type="integer" ),
    }
    _defaults={
        'state':'draft',
    }

    def send_fax(self,cr,uid,ids,context=None):
        '''Function to send Fax '''
        ir_model_data = self.pool.get('ir.model.data')
        if context is None:
            context = {}
        ir_attachment = self.pool.get('ir.attachment')
        outgoing_obj = self.pool.get('outgoing.fax')
        for each in self.browse(cr, uid, ids):
            if each.count < 1:
                raise osv.except_osv(_("Warning"),_("No Attachment is selected to send via Fax"))
            if not each.partner_id:
                raise osv.except_osv(_("Warning"),_("No Partner is selected to send Fax"))
            if each.partner_id:
                fax = each.partner_id.fax1
                if not fax:
                    raise osv.except_osv(_("Warning"),_("No Fax is available for this Partner. Open form to enter Fax"))
                
            template_id = False
            try:
                template_id = ir_model_data.get_object_reference(cr, uid, 'syml', 'event_fax_sending_template')[1]
                #print"template_id",template_id
            except ValueError:
                template_id = False
            if template_id:
                msg_id = self.pool.get('email.template').send_mail_custom( cr, uid, template_id, each.id, True, each , context)
                print "msg_id .......",msg_id
                attachment_ids = []
                history_data = {
                    'partner_id': each.partner_id and each.partner_id.id or False,
                    'name': each.name or '',
                    'fax': each.fax or '',
                    'date': str(time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
                }
                history_id = outgoing_obj.create(cr ,uid , history_data)
                for attachment in each.send_attachment_ids:
                    attachment_data = {
                        'name': attachment.name,
                        'datas_fname': attachment.name,
                        'datas': attachment.datas,
                        'res_model': 'outgoing.fax',
                        'res_id': history_id or False,
                    }
                    attachment_ids.append(ir_attachment.create(cr, uid, attachment_data, context=context))
                outgoing_obj.write(cr, uid, [history_id], {'attachment_ids': [(6, 0, attachment_ids)]}, context=context)

                return msg_id
        return True

    def onchange_partner_id(self ,cr ,uid ,ids , partner_id, context=None):
        ''' Onchange Function to bring Fax from partner '''
        if partner_id:
            partner = self.pool.get('crm.lead').browse(cr ,uid , partner_id)
            print "partnerrrrrrrrrrrrrrrrrrr",partner
            print "docsssssssssssssssssssssssss",partner.document_ids
            doc_lst=[]
            doc_names=[]
            if partner.document_ids:
                for each in partner.document_ids:
                    doc_lst.append(each.document_data)
                    doc_names.append(each.document_name)

#                print "document_name===================",doc_lst
            doc_dict=[]
            i=0
            for each in doc_lst:
#                print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",each.name
                
                doc_dict.append((0,False,{'datas':each,'name':doc_names[i] or ''}))
                i+=1
#            print "doc_dictdoc_dictdoc_dict",doc_dict
            print "doc_dictdoc_dictdoc_dict",partner.fax1
#            eroooooooooooo
            val={
                'show_fax': partner.fax1,
#                'opp_id': partner.opp_id.id,
                'send_attachment_ids': doc_dict,


                }
        else:
            val={
                'show_fax': False,
#                'opp_id': False,
                'send_attachment_ids': [],
                }

        return {'value': val}
    
