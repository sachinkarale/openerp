from base_status.base_stage import base_stage
from osv import fields,osv
import datetime
import tools
from tools.translate import _
from tools import html2plaintext



class hr_applicant(base_stage, osv.osv):
    _inherit = 'hr.applicant'
    _columns={
            'partner_id':fields.many2one('res.partner',"Candidate Name"),
#            'candidate':fields.many2one('res.partner',"Applicant's Name"),
            'contact':fields.char('Contact',size=240),
            'trainee':fields.many2one('res.users','Trainee'),
            'hr_associate':fields.many2one('res.users','HR Associate'),
#            'referral_source': fields.selection([('referral', 'Referral'), ('candidate', 'Candidate'),
#                ('website', 'Website'),('prospecting', 'Prospecting'),('customer', 'Customer'),
#                ('personal_network', 'Personal Network'),('new_asso', 'New Associate')],
#                'Referral Source'),
            'no_bankruptcy': fields.boolean('No Bankruptcy'),
            'company':fields.char('Company',size=240),
            'driver_license': fields.boolean('Driver License'),
            'high_school': fields.boolean('High School Diploma'),
            'no_criminal': fields.boolean('No Criminal Record'),
            'no_judgement': fields.boolean('No Judgements'),
#            'motivator': fields.selection([('now', 'Now(Current Do)'), ('enjoy', 'Enjoy(What are the positive qualities of the job ?)'),
#                ('alter', 'What would you like better ?'),
#                ('decision', 'Decision Maker(Anyone else involved if you decided to make a change ?)')],
#                'Motivators'),
            'source_id': fields.many2one('hr.recruitment.source', 'Referral Source'),
            'what_do_they_do_now':fields.char('What do they do NOW ?',size=256),
            'what_they_enjoy_about_it':fields.char('What they ENJOY about it ?',size=256),
            'what_they_wish_to_alter':fields.char('What they wish to ALTER ?',size=256),
            'is_anyone_else_in_decision':fields.char('Is anyone else in the DECISION?',size=256),
            'why_we_are_here':fields.boolean('1.Why we are here'),
            'goals_hopes_dreams':fields.text('Top 3 Goals'),
            'employee':fields.boolean('3.Employee'),
            'self_employee':fields.boolean('4.Self Employed'),
            'business_ownership':fields.boolean('5.Business Ownership'),
            'helping_client':fields.boolean('6.Helping Clients'),
            'traditaionl_brokerage':fields.boolean('7.Traditional Brokerage'),
            'broker_problems':fields.boolean('8.Broker Problems'),
            'visdom_business_roles':fields.boolean('9.Visdom Business Roles'),
            'visdom_business_systems':fields.boolean('10.Visdom Business Systems'),
            'visdom_business_compensation':fields.boolean('11.Visdom Business Compensation'),
            'visdom_business_creation':fields.boolean('12.Visdom Business Creation'),
            'getting_sarted':fields.boolean('13.Getting Started'),
            'common_concerns':fields.boolean('14.Common Concerns'),
            'personal_vision':fields.boolean('15.Personal Vision'),
            'business_application':fields.boolean('16.Business Application'),
            'candidate_street': fields.char('Address1', size=128),
            'candidate_street2': fields.char('Street', size=128),
            'candidate_city': fields.char('City', size=128),
            'candidate_state_id': fields.many2one("res.country.state", 'State'),
            'candidate_zip': fields.char('Zip', change_default=True, size=24),
#            'candidate_country_id': fields.many2one('res.country', 'Country'),
            'year':fields.char('Deals/Year',size=128),
            'avg_house_price':fields.char('Avg. House Price',size=128),
            'rental_properties':fields.char('Rental Properties?',size=128),
            'current_broker':fields.char('Current Mtg Broker',size=128),
            'bdo_associate':fields.many2one('res.users','BDO Associate'),
            'referred_by':fields.many2one('res.partner','Referred By'),
            'signature':fields.char('Signature',size=128),
            'sign_ip':fields.char('Signature IP',size=128),
            'agreement_date':fields.datetime('Agreement Date'),
            'opp_hrapp_ids':fields.one2many('crm.lead','referred_source','Opportunities'), 
            'bdo_check':fields.many2one('res.users','BDO Check'),
            'year_in_industry':fields.selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5')],'Year in Industry'),
#            'opportunitiy_hrapp_ids':fields.one2many('crm.lead','opportunity_id','Opportunity'),
            'role':fields.selection([('realtor','Realtor'),('financial_planner','Financial Planner'),('lawyer_accountant','Lawyer/Accountant'),('client','Client'),('other','Other')],'Role'),
            'received_update':fields.boolean('Received Update'),

            


    }
    
    _defaults = {
        'hr_associate': lambda s, cr, uid, c: uid,
    }


    def create(self, cr, uid, vals, context=None):
#        ids_hr_employee = self.pool.get('hr.employee').search(cr,uid, [('user_id', '=', uid)])
#        print "depids================",ids_hr_employee
#        dep_id=self.pool.get('hr.employee').browse(cr,uid,ids_hr_employee[0]).department_id.id
#        print "depidddddddddddddddddd",dep_id
	mod_obj = self.pool.get('ir.model.data')
	print "insitialvalssssssssssssssssssssssss",vals
	print "my-------------------context--------------------",context
	req=context.get('request')
	pat_id=context.get('partner_id')
	print "req---------------------",req
	print "pat_iddddddddddddddddddd",pat_id
	if  req=='web':
	    print "inside-----------------111111111"
            if pat_id==None:
		print "inside popppppppppppppp func",pat_id
		if vals.has_key('partner_id'):
		    print "popingggggggggggggggggggggggggg------------"
                    vals.pop('partner_id')
                email=vals.get('email_from')
                cr.execute('select id from res_partner where email = %s', (email,))
                contact_id = cr.fetchall()
                if contact_id:
                    vals.update({'partner_id':contact_id[0]})
        print "vals----------------123-----456----------------",vals




	if uid:
#            values.update({'hr_department_id':dep_id[0]})
            vals.update({'bdo_check':uid})
	    vals.update({'bdo_associate':uid})
        usr_id =super(hr_applicant, self).create(cr, uid, vals, context=context)

	#if vals.get('stage_id',False):
                #cr.execute('select id from hr_recruitment_stage where id = %s and "name" ilike %s',(vals.get('stage_id',False),'involved',))
                #stage_id = cr.fetchone()
#                print "stage_id=========",int(stage_id[0])

                #if stage_id:
                    #template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_referral_agreement')
                    #template_id = template and template[1] or False
                    #if template_id:
                        #self.pool.get('email.template').send_mail(cr,uid,template_id,usr_id,'True',context)
                    #template2 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_referral_to_visdom')
                    #template_id2 = template2 and template2[1] or False
                    #if template_id2:
                        #self.pool.get('email.template').send_mail(cr,uid,template_id2,usr_id,'True',context)

#        if uid:
#            values.update({'hr_department_id':dep_id[0]})
 #           vals.update({'bdo_check':uid})
  #      usr_id =super(hr_applicant, self).create(cr, uid, vals, context=context)

        return usr_id
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        data = {'partner_phone': False,
                'partner_mobile': False,
                'email_from': False,
                'contact': False}
        if partner_id:
            addr = self.pool.get('res.partner').browse(cr, uid, partner_id, context)
            name = addr.name or ''
            middle_name = addr.middle_name or ''
            last_name = addr.last_name or '' 
            contact = name +' '+middle_name+' ' +last_name
            data.update({'partner_phone': addr.phone,
                        'partner_mobile': addr.mobile,
                        'email_from': addr.email,
                        'contact':contact})
        return {'value': data}

    def write(self, cr, uid, ids, vals, context=None):
        if context==None:
            context={}
        if not isinstance(ids,list):
           ids = [ids]
        user_id,user=uid,''
        mod_obj = self.pool.get('ir.model.data')
        hr_app_browse = self.browse(cr,uid,ids[0])
        user=hr_app_browse.bdo_associate.id 
        if user:
            user_id=user
        context.update({'hr_app_id':hr_app_browse,'lead_id':ids[0],'user_id':user_id})
	res = super(hr_applicant, self).write(cr, uid, ids, vals)
        #if vals.get('stage_id',False):
                #cr.execute('select id from hr_recruitment_stage where id = %s and "name" ilike %s',(vals.get('stage_id',False),'involved',))
                #stage_id = cr.fetchone()
#                print "stage_id=========",int(stage_id[0])
                
                #if stage_id:
                   # template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_referral_agreement')
                   # template_id = template and template[1] or False
                    #if template_id:
                       # self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
                    #template2 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_referral_to_visdom')
                    #template_id2 = template2 and template2[1] or False
                    #if template_id2:
                        #self.pool.get('email.template').send_mail(cr,uid,template_id2,ids[0],'True',context)
        
        return res

hr_applicant()
