
import logging
from openerp import tools

from email.header import decode_header
from openerp import SUPERUSER_ID
from openerp.osv import osv, orm, fields
from openerp.tools import html_email_clean
from openerp.tools.translate import _
from datetime import datetime
import datetime


class mail_message(osv.Model):
    _inherit = 'mail.message'
    _columns={
        'opportunity_id':fields.many2one('crm.lead','Opportunity'),
        
    }
    
    def create(self, cr, uid, values, context=None):
        print "values inside mail_message class==========",values

	if values.has_key('model'):
            model=values.get('model')
            print "model---------------",model
            if model=='crm.lead':
                if values.has_key('res_id'):
                    res_id=values.get('res_id')
                    print "res_id-----------------",res_id
                    if res_id:
                        values.update({'opportunity_id':res_id})
        
        if values.has_key('email_from'):
            res_partner_email = values['email_from']
            if res_partner_email:
                print "res_partner_email>>>>>",res_partner_email
               # email = res_partner_email.split('<')[1]
               # final_email  = email.split('>')[0]

                final_email = ''
                if res_partner_email in '<':
                    email = res_partner_email.split('<')[1]
                    final_email  = email.split('>')[0]
                else:
                    final_email  = res_partner_email

                print "final_email+++++++++++++++",final_email
                res_partner_obj = self.pool.get('res.partner')
                res_id = res_partner_obj.search(cr,uid,[('email','=',final_email)])
                print "res_id-----------",res_id
                if res_id:            
                    ir_attachment =  values['attachment_ids']
                    print "ir_attachment>>>",ir_attachment
                    if ir_attachment:
                        ir_attachment_data = ir_attachment[0][2]
                        ir_attachment_data.update({'res_id':res_id[0],'res_model':'res.partner'})
                        print "ir_attachment_data000000000000000000000",ir_attachment_data		
                    #ir_attachment_data = ir_attachment[0][2]            
                    #ir_attachment_data.update({'res_id':res_id[0],'res_model':'res.partner'})
                   # print "ir_attachment_data000000000000000000000",ir_attachment_data            
        if context is None:
            context = {}
        default_starred = context.pop('default_starred', False)
        if not values.get('message_id') and values.get('res_id') and values.get('model'):
            values['message_id'] = tools.generate_tracking_message_id('%(res_id)s-%(model)s' % values)
        elif not values.get('message_id'):
            values['message_id'] = tools.generate_tracking_message_id('private')
        newid = super(mail_message, self).create(cr, uid, values, context)

	x=self.attach_to_opportunity(cr,uid,[newid],context)
        print "x------------",x

#        self._notify(cr, uid, newid, context=context)
        print"values",values
        partner_ids=values.get('partner_ids')
        if partner_ids:
            for each in partner_ids:
                partner_id=each[1]
                if partner_id:
                    cur_date=str(datetime.datetime.now())
                    user_name=self.pool.get('res.users').browse(cr,uid,uid).name
                    mail_to=self.pool.get('res.partner').browse(cr,uid,partner_id).email
                    subject = ('''"%s" emailed "%s on "%s"''') % (user_name,mail_to,cur_date)
                    details = ('''"%s"''')% (values.get('body',False))
        #           self.pool.get('res.partner').message_post(cr, uid, [partner_id], type='comment', subtype=subtype, context=context, **post_values)
                    self.pool.get('res.partner').message_post(cr, uid, [partner_id], body=details, subject=subject, context=context)

        # TDE FIXME: handle default_starred. Why not setting an inv on starred ?
        # Because starred will call set_message_starred, that looks for notifications.
        # When creating a new mail_message, it will create a notification to a message
        # that does not exist, leading to an error (key not existing). Also this
        # this means unread notifications will be created, yet we can not assure
        # this is what we want.
        if default_starred:
            self.set_message_starred(cr, uid, [newid], True, context=context)
        return newid

    def write(self , cr ,uid ,ids ,vals , context=None):
        print "write for mail.message......."
        res = []
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res =  super(mail_message , self ).write( cr ,uid ,ids ,vals , context=None)

#        for cur in self.browse( cr ,uid , ids ):
#            if cur.opportunity_id:
#                for attach in cur.attachment_ids:
#                    #print "attach.attach........",attach.attach
#                    if attach.attach:
#                        print"attachhhhhhhhhhhhhhh",attach.attach
##                        self.pool.get('crm.lead').write(cr,uid,cur.opportunity_id.id,{'document_name':attach.datas},context)
##                        print"attachment"
##                        self.pool.get('mail.message').create(cr ,uid ,attach.id ,{'res_model':'crm.lead', 'res_id':cur.opportunity_id.id,'res_name':cur.opportunity_id.name})
#                        cr.execute("Insert into opportunity_ir_attachments_rel (opportunity_id,attachment_id) values (%s,%s)"%(cur.opportunity_id.id,attach.id))
        return res

    def attach_to_opportunity(self,cr,uid,ids,context=None):
	user=''
	user=self.pool.get('res.users').browse(cr,uid,uid).login
	print "users===============================",user
        for cur in self.browse( cr ,uid , ids ):
            if cur.opportunity_id:
                for attach in cur.attachment_ids:
                    #print "attach.attach........",attach.attach
                    #if attach.attach:
#                        self.pool.get('crm.lead').write(cr,uid,cur.opportunity_id.id,{'document_name':attach.datas},context)
#                        print"attachment"
#                        self.pool.get('mail.message').create(cr ,uid ,attach.id ,{'res_model':'crm.lead', 'res_id':cur.opportunity_id.id,'res_name':cur.opportunity_id.name})
                        #cr.execute("Insert into opportunity_ir_attachments_rel (opportunity_id,attachment_id) values (%s,%s)"%(cur.opportunity_id.id,attach.id))

		    link='https://visdom.ca/document-handling.php?crm_lead='+str(cur.opportunity_id.id)+'&attachment_id='+str(attach.id)+"&user="+user
                    print "link-------------------",link
                    self.pool.get('ir.attachment').write(cr,uid,[attach.id],{'document_link':link})

        return True
mail_message()
