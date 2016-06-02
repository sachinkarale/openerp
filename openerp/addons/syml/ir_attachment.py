from openerp import tools
from openerp.osv import fields,osv

class ir_attachment(osv.osv):
    _inherit = 'ir.attachment'
    _columns={ 
            'email':fields.char('E-mail', size=64, select=True),
            'attach':fields.boolean('Attach'),
	    'send_doc':fields.boolean('Send Doc'),
	    'document_link':fields.char('Document Link', size=128),
        }

    def select_attach(self, cr, uid, ids, context=None):
        cur_obj = self.browse(cr ,uid ,ids[0] )
        attach=cur_obj.attach
        if attach==False:
            self.write(cr ,uid , ids , {'attach':True})
        else:
            self.write(cr ,uid , ids , {'attach':False})
        return True


    def redirect_url(self, cr, uid, ids, context=None):
        cur_obj = self.browse(cr ,uid ,ids[0] )
        
        link=cur_obj.document_link
        print "link------------------",link
        if link==False:
            raise osv.except_osv(('Warning!'),('proper address not found..'))
        return {
                  'res_model': 'ir.actions.act_url',
                  'type'     : 'ir.actions.act_url',
                  'target'   : 'new',
#                  'nodestroy': True,
                  'url'      : link
                  
               }

    
    def create(self, cr, uid, values, context=None):
        print"values",values
        res_id = values.get('res_id')
        res_model = values.get('res_model')        
        print "res_id=====",res_id
        print "res_model======",res_model
        if res_id and res_model == 'crm.lead':
            print "inside if statement//////////////////////////////////"
            crm_obj = self.pool.get('crm.lead')
            email = crm_obj.browse(cr,uid,res_id).email_from or ''
            if email:
                print "email_from =======",email
                values['email'] = email            
        elif res_id and res_model == 'res.partner':
            print "inside elif statement/////////////////////////////////////"
            res_obj = self.pool.get('res.partner')
            email = res_obj.browse(cr,uid,res_id).email or ''
            if email:
                print "email_from =======",email
                values['email'] = email
            
        return super(ir_attachment, self).create(cr, uid, values, context)
    
ir_attachment()
