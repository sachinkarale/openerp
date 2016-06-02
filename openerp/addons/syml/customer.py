from validate_email import validate_email
from osv import fields,osv
from tools.translate import _


class res_partner(osv.osv):
    _inherit = 'res.partner'
    def desg_login_other(self, cr, uid, ids, field_name, arg, context=None):

        res={}
        login_id=context.get('uid')
        check_string=self.pool.get('res.users').browse(cr,uid,login_id).designation

        if check_string=='other':
            for o in self.browse(cr,uid,ids):
                res[o.id]=True
        else:
            for o in self.browse(cr,uid,ids):
                res[o.id]=False
        return res
    _columns={

        'res_company':fields.many2one('res.company','Employer'),
        'referredby':fields.many2one('res.partner',"Referred By:"),
        'newclientlead':fields.boolean('New Client Lead'),
        'newhrlead':fields.boolean('New HR Lead'),
        'newduallead':fields.boolean('New Dual Lead'),
        'isupdatedtoua':fields.boolean('isUpdatedToUA'),
        'birthdate':fields.date('DOB'),
        'atmail_contact':fields.boolean('Atmail Contact', readonly=True, help='read only field', invisible=True),
        'name': fields.char('First Name', size=128, required=True, select=True, track_visibility='onchange'),
        'last_name': fields.char('Last Name', size=128, select=True),
        'middle_name': fields.char('Middle Name', size=128, select=True),
        'spouse': fields.char('Spouse', size=128),
        'addr_type': fields.selection([('personal', 'Personal'), ('business', 'Business'),
                                   ('referral', 'Referral')], 'Category'),
        'email': fields.char('Email(personal)', size=240, required=True),
        'email_personal': fields.char('Email(work)', size=240),
        'po_box': fields.char('P/O Box', size=140),
        'sin':fields.char('Social Insurance Number',size=140),
        'province': fields.selection([('ON','Ontario'),('QC','Quebec'),('NS','Nova Scotia'),('NB','New Brunswick'),('MB','Manitoba'),('BC','British Columbia'),('PE','Prince Edward Island'),('SK','Saskatchewan'),('AB','Alberta'),('NL','Newfoundland and Labrador')], 'Province'),
	#'province': fields.selection([('Alabama','Alabama'),('Alaska','Alaska'),('Arizona','Arizona'),('Arkansas','Arkansas'),('California','California'),('Colorado','Colorado'),('Connecticut','Connecticut'),('Florida','Florida'),('Georgia','Georgia'),('Hawaii','Hawaii'),('Idaho','Idaho'),('Illinois','Illinois')], 'Province'),

	#'province': fields.selection([('Nunavut','Nunavut'),('Quebec','Quebec'),('Northwest Territories','NorthwestTerritories'),('Ontario','Ontario'),('British Columbia','BritishColumbia'),('Alberta','Alberta'),('Saskatchewan','Saskatchewan'),('Manitoba','Manitoba'),('Yukon','Yukon'),('New Brunswick','NewBrunswick'),('Nova Scotia','NovaScotia'),('Prince Edward Island','PrinceEdwardIsland'),('Newfoundland and Labrador','NewfoundlandandLabrador')], 'Province'),
#        'hr_candidate': fields.integer('Hr Candidate'),
        'phone': fields.char('Home', size=24),
        'mobile': fields.char('Cell', size=24),
        'work_phone': fields.char('Work', size=24),
#        'phone_validation':fields.char('',size=124, readonly=True),
#        'phone_check':fields.boolean('phone check', invisible=True),
        'preferred_phone':fields.selection([('cell','Mobile'),('Home','Home'),('Work','Work')],'Preferred Phone'),
        'name_title': fields.many2one('res.partner.title', 'Title'),
        'underwriting_office_street': fields.char('Street', size=128),
        'underwriting_office_street2': fields.char('Street2', size=128),
        'underwriting_office_city': fields.char('City', size=128),
        'underwriting_office_state_id': fields.many2one("res.country.state", 'State'),
        'underwriting_office_zip': fields.char('Zip', change_default=True, size=24),
        'underwriting_office_country_id': fields.many2one('res.country', 'Country'),
        'underwriting_office_website': fields.char('Website', size=64, help="Website of Partner or Company"),
        'underwriting_office_fax': fields.char('Fax', size=64),
        'underwriting_office_email': fields.char('Email(work)', size=240),
        'underwriting_office_work_phone': fields.integer('Work', ),
        'underwriting_office_phone': fields.integer('Home', ),
        'underwriting_office_mobile': fields.integer('Cell', ),
        'underwriting_office_work_phone': fields.integer('Work', ),
        'lender_business_development_manager':fields.many2one('res.partner','Lender Business Development Manager'),
        'underwriter':fields.many2one('res.partner','Underwriter'),
        'lender_credit_admin':fields.many2one('res.partner','Lender Credit Admin'),

        'lender_id':fields.many2one('product.product','Product Reference'),
#        lender
	'bonus_comp_period':fields.selection([('year_to_date','Year To Date'),('monthly','Monthly'),('rolling_12_month','Rolling 12 Month'),('quarterly','Quarterly')],'Bonus Comp Period'),
        'ytd_volume':fields.float('Ytd Volume'),
        'rolling_12Mo_volume':fields.float('Rolling 12Mo Volume'),
        'q1_volume':fields.float('Q1 Volume'),
        'q2_volume':fields.float('Q2 Volume'),
        'q3_volume':fields.float('Q3 Volume'),
        'q4_volume':fields.float('Q4 Volume'),
        'jan_volume':fields.float('January Volume'),
        'feb_volume':fields.float('February Volume'),
        'mar_volume':fields.float('March Volume'),
        'apr_volume':fields.float('April Volume'),
        'may_volume':fields.float('May Volume'),
        'june_volume':fields.float('June Volume'),
        'july_volume':fields.float('July Volume'),
        'aug_volume':fields.float('August Volume'),
        'sept_volume':fields.float('September Volume'),
        'oct_volume':fields.float('October Volume'),
        'nov_volume':fields.float('November Volume'),
        'dec_volume':fields.float('December Volume'),
        'bdo_check':fields.many2one('res.users','BDO Check'),
        'move_date':fields.date('Move Date'),
        'login_other_flag':fields.function(desg_login_other, string='other', type='boolean'),
        'document_portal': fields.char('Document Portal', size=240),
        'documentation_method':fields.selection([ ('email','Email'), ('fax','Fax'), ('portal','Portal')],'Documentation Method'),
        }

    def create(self, cr, uid, vals, context=None):

        if uid:
            vals.update({'bdo_check':uid})
        usr_id =super(res_partner, self).create(cr, uid, vals, context=context)

        return usr_id
    def onchange_phone_validation_phone(self,cr,uid,ids,number):
        if number:
            if len(number)>= 10:
                if '-' in number:
                    num1 = number.replace('-', '')
                    return {'value':{'phone':_('%s-%s-%s')%(num1[0:3],num1[3:6],num1[6:len(num1)])}}
                else:
                    return {'value':{'phone':_('%s-%s-%s')%(number[0:3],number[3:6],number[6:len(number)])}}
            else:            
                return {'value':{'phone':number}}
        else:
            return 1
                    
    def onchange_phone_validation_mobile(self,cr,uid,ids,number):
        if number:
            if len(number)>= 10:            
                if '-' in number:
                    num1 = number.replace('-', '')
                    return {'value':{'mobile':_('%s-%s-%s')%(num1[0:3],num1[3:6],num1[6:len(num1)])}}
                else:
                    return {'value':{'mobile':_('%s-%s-%s')%(number[0:3],number[3:6],number[6:len(number)])}}
            else:            
                return {'value':{'mobile':number}}
        else:
            return 1
                    
    def onchange_phone_validation_work_phone(self,cr,uid,ids,number):        
        if number:
            if len(number)>= 10:            
                if '-' in number:
                    num1 = number.replace('-', '')
                    return {'value':{'work_phone':_('%s-%s-%s')%(num1[0:3],num1[3:6],num1[6:len(num1)])}}
                else:
                    return {'value':{'work_phone':_('%s-%s-%s')%(number[0:3],number[3:6],number[6:len(number)])}}
            else:            
                return {'value':{'work_phone':number}}
        else:
            return 1
                    
    def onchange_email_validation(self, cr, uid, ids, mail): 
        if mail:
            is_valid = validate_email(mail)
            print "is_valid:",is_valid
            if is_valid:
                return 1
            else:
                raise osv.except_osv(_('Warning!'), _('Your email is Incorrect.')) 
        else:
            return 1
    
    _defaults = {
        'preferred_phone': 'cell',
        }       


    def mailto_customer(self, cr, uid, ids, context=None):
        print "inside mailto_customer +++++++++++++++++++++++++++++ function"
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        mod_obj = self.pool.get('ir.model.data')
        template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_edi_customer')
        template_id = template and template[1] or False
        res = mod_obj.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')
        res_id = res and res[1] or False
        ctx = dict(context)
        print "template_id=========",template_id
        ctx.update({
            'default_model': 'res.partner',
            'default_res_id': ids[0],
            'default_use_template': True,
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True
        })
        print"ctx==============",ctx
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(res_id, 'form')],
            'view_id': res_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
            'nodestroy': True,
        }
    

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        name = self.read(cr, uid, [id], ['name'], context)[0]['name']
        default.update({'email': '', 'phone':'', 'mobile':'', 'work_phone': '','name': _('%s (copy)') % name})
        return super(res_partner, self).copy(cr, uid, id, default, context)
        
    def onchange_check_selection1(self, cr, uid, ids, action):
        print "inside onchange_check_selection1"
        print "action",action
        if action:            
            return {'value':{'newhrlead':False, 'newduallead':False}}
        return True    
    def onchange_check_selection2(self, cr, uid, ids, action):
        print "inside onchange_check_selection2"
        print "action",action
        if action:            
            return {'value':{'newclientlead':False, 'newduallead':False}}        
        return True    
    def onchange_check_selection3(self, cr, uid, ids, action):
        print "inside onchange_check_selection13"
        print "action",action
        if action:            
            return {'value':{'newclientlead':False, 'newhrlead':False}}    
        return True

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            last_name=record.last_name
            if last_name:
                name = "%s %s" % (name,last_name)
            if record.parent_id:
                name =  "%s (%s)" % (name,record.parent_id.name)

            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
                name = name.replace('\n\n','\n')
                name = name.replace('\n\n','\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res

res_partner()
