import urllib2
import string
import random
import binascii

import subprocess
import netsvc
import base64
from osv import fields,osv
import datetime
from datetime import timedelta
from datetime import date
import time
from base_status.base_stage import base_stage
import tools
from tools.translate import _
from tools import html2plaintext

from xml.dom.minidom import parse, parseString
import imp

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import string
ADDONS_PATH = tools.config['addons_path'].split(",")[-1]
import os
import stat
from xml.dom import minidom
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import dateutil.relativedelta
#from geolocate import GeoLocation
#gl = GeoLocation()

#from elementtree.ElementTree import XML, SubElement, Element, tostring
#import xml.etree.ElementTree as ET
#import sys

class crm_lead(osv.osv):
    _name = "crm.lead"
    _inherit = ['mail.thread', 'ir.needaction_mixin','crm.lead']
    _columns={
#        'priority': fields.selection(crm.AVAILABLE_PRIORITIES, 'Priority', select=True, track_visibility='onchange'),
        'email_from': fields.char('Email(Personal)', size=128, help="Email address of the contact", select=1),
        'email_work': fields.char('Email(work)', size=128, help="Email address of the contact"),        
        'mobile': fields.char('Cell', size=64),
        'work_phone': fields.char('Work', size=24),
        'phone': fields.char("Home", size=64),
        'preferred_number':fields.selection([('cell','Cell'),('home','Home'),('work','Work')],'Preferred Number',track_visibility='onchange'),
        'isUpdatedToUA':fields.boolean('IsupdatedToUA'),
        'application_no':fields.char('Application No',size=20, readonly=True),
        'web_response':fields.char('more web response',size=24),
#        'section_id': fields.many2one('crm.case.section', 'Sales Team', \
#                        select=True, help='When sending mails, the default email address is taken from the sales team.', invisible=True,),
        'lead_source': fields.selection([('corporate', 'Corporate'), ('referral', 'Referral'),
                                   ('prospecting', 'Prospecting'),('renewal', 'Renewal'),('website', 'Website'),('personal_market', 'Personal Market')], 'Lead Source', track_visibility='onchange'),
        'referral_source' : fields.many2one('res.partner','Referral Source', track_visibility='onchange'),
        'realtor' : fields.many2one('hr.applicant','Realtor', track_visibility='onchange'),
        'trainee' : fields.many2one('res.users','Training Associate Referral', track_visibility='onchange'),
#        'sales_asso' : fields.many2one('res.users','Sales Associate'),
#        'opp_info': fields.selection([('loan_amnt', 'Loan Ammount'), ('rate', 'Interest Rate'),
#                                   ('amortization', 'Amortization'),('sdate', 'Start Date'),('renewd', 'Renewal Date'),('type', 'type')], 'Opportunity Information'),   
        'opp_info_type':fields.selection([('Pre-Approval','Pre-Approval'),('Purchase','Purchase'),('Renewal','Renewal')],'Lead Type', track_visibility='onchange'),
        'opp_info_rate':fields.integer('Interest Rate',track_visibility='always'),
        'opp_info_loan_amnt':fields.integer('Current Mortgage Amount',track_visibility='always'),
        'existing_lender':fields.char('Existing Lender', size=240, track_visibility='always'),
        'opp_info_renewal_date':fields.date('Renewal Date', track_visibility='always'),
        'estimated_valueof_home':fields.char('Estimated Value of Home',size=120, track_visibility='always'),
        'desired_mortgage_amount':fields.char('Desired Mortgage Amount',size=120, track_visibility='always'),

        'Amortization':fields.char('Amortization',size=128),
        'opp_info_start_date':fields.date('Start Date'),        
        'term_rate':fields.selection([('term', 'Term'),],'Term Rate'),   
        'op_info_type':fields.selection([('p_approve', 'Pre_Approval'),('mortagage', 'Mortagage Roval'),],'Op Info Type'),   
        'credit_story': fields.text('Credit Story',track_visibility='onchange'),
#        'pen_app':fields.selection([('broker', 'Broker Reset Button'),('instruction', ' New Instruction'),],''),        
        'trigger': fields.selection([('save', 'Save to application stage'), ('create', 'create application'),
                                       ('send', 'send thank you email w/ application self server link'),('create_con', 'create contact')], 'Trigger'),   
        'existing_mortgage': fields.char('Existing Mortgage',size=124, track_visibility='always'),
        'future_mortgage': fields.char('Future Mortgage',size=124, track_visibility='always'),
        'marketing_auto': fields.char('Marketing Automation',size=124,track_visibility='always'),
        'approached_check':fields.boolean('approached'),
        'qualified_check':fields.boolean('qualified'),
        'process_presntedutio_check':fields.boolean('process_presnted'),
        'concerns_addressed_check':fields.boolean('concerns_addressed'),
        'pending_application_check':fields.boolean('pending_application'),
        'spouse': fields.char('Spouse', size=128),
#        'reporting_manager':fields.many2one('res.users','Reporting Manager'),
        'all_email_ids':fields.char('Webform User Name',size=128),
        'webform_uname':fields.char('Webform User Name',size=128),
        'webform_pwd':fields.char('Webform Password',size=128),
	'from_web_form':fields.char('From Web Form', size=240, track_visibility='always'),
        'lawyer':fields.many2one('res.partner','Lawyer'),
        #'broker_team':fields.many2one('hr.department','Team'),
        'referral_fee':fields.float('Referral Fee', digits=(16,2 )),
        "hr_department_id": fields.many2one("hr.department", 'Team'),
        'prod_count':fields.integer('Product Count'),
        'template_date':fields.datetime('Date'),
        'deadline':fields.datetime('Paperwork Deadline'),
        'dup_task_created':fields.boolean('Dupl Task Created'),
        'new_opp_users':fields.char('New Opportunity Users',size=128),
        'congrats_date':fields.datetime('Client Greeting Date'),
        'greeting_send':fields.boolean('Greeting Send'),
        'client_survey':fields.datetime('Client Survey Reminder'), #date to track to send client servey mail after 72 hours from congrats mail has been send
        'client_remd':fields.boolean('Client Reminder'), # boolean field to track that client has done the survey.
        'client_email_rem':fields.boolean('Client Email Reminder'), ##boolean field that client had not done the survey and mail has been send to them.
        'renewal_mail_date':fields.date('Renewal Mail Date',),
        'date_renewed':fields.boolean('Date Renewed'),
        
    }
    _defaults = {
        'preferred_number': 'cell',
    }
    _order = "create_date desc"

    def _reporting_manager(self, cr, uid, *args):
        
        user_obj = self.pool.get('res.users')
        hr_employee_obj = self.pool.get('hr.employee')
        
        employee_ids = hr_employee_obj.search(cr, uid, [('user_id','=',uid)])
        print "employee_ids======",employee_ids
        if employee_ids:
            emp_obj = hr_employee_obj.browse(cr, uid, employee_ids[0])
            report_mng_user_id = emp_obj.parent_id and emp_obj.parent_id.user_id.id or False
            print "report managers",report_mng_user_id 
            if report_mng_user_id:
                return report_mng_user_id
            else:
                return 1
        else:
            return 1
    
    def _renewal_date(self, cr, uid, *args):
#        date = datetime.date.today()+ timedelta(days=20)
        date = datetime.date.today()
        return date.strftime('%Y-%m-%d')
    
    _defaults = {
                'user_id': lambda obj, cr, uid, context: uid,
                'opp_info_start_date': datetime.date.today().strftime('%Y-%m-%d'),
                'opp_info_renewal_date':_renewal_date,
                'preferred_number':'cell'
#                'reporting_manager': _reporting_manager,
        }

    def on_change_partner(self, cr, uid, ids, partner_id, context=None):
        result = {}
        values = {}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)            
            values = {
                'email_from' : partner.email,
                'email_work' : partner.email_personal,
                'phone' : partner.phone,
                'mobile' : partner.mobile,
                'work_phone':partner.work_phone,
                'fax' : partner.fax, 
                'spouse':partner.spouse,
                'preferred_number' : partner.preferred_phone
            }
        return {'value' : values}


    def create(self, cr, uid, values, context=None):
        opp_info_renewal,stage_name,stage_id,delayed_app_date='','','',''
        ids_hr_employee = self.pool.get('hr.employee').search(cr,uid, [('user_id', '=', uid)])
        dep_id=self.pool.get('hr.employee').browse(cr,uid,ids_hr_employee[0]).department_id.id
        cur_date_time=datetime.datetime.now()
        delayed_app_date=cur_date_time+datetime.timedelta(days=1)

	cr.execute("select count(id) from product_product")
        prod_count = cr.fetchone()[0]
        print "prod_count----------------",prod_count
        values['date_renewed']=int(prod_count)

#        datetime.date.today() + datetime.timedelta(6*365/12)).isoformat()
        if values.get('opp_info_renewal_date',False):
#            renewal_mail_date = values.get('opp_info_renewal_date') - datetime.timedelta(month=8)
            opp_info_renewal=datetime.datetime.strptime(values.get('opp_info_renewal_date',False), "%Y-%m-%d")
            renewal_mail_date = opp_info_renewal - dateutil.relativedelta.relativedelta(months=8)
            
            values['renewal_mail_date']=renewal_mail_date
            values['date_renewed']=False

        
        stage_id=values.get('stage_id',False)
        if stage_id:
            stage_name=self.pool.get('crm.case.stage').browse(cr,uid,stage_id).name
        if values.get('stage_id') and stage_name=='Partial App':
            values['delayed_app_date']=delayed_app_date
            values['lead_followup_date']=delayed_app_date

        
        all_email_ids=""
        if values.get('app_rec_ids'):
#            print "vals.get('app_rec_ids')===========",vals.get('app_rec_ids')
            new_rec_ids=values.get('app_rec_ids')[0][2]
            if new_rec_ids:
                applicant_obj=self.pool.get('applicant.record')

                for each in new_rec_ids:
                    mail_id=""
                    mail_id=applicant_obj.browse(cr,uid,each).email_personal+","
                    if mail_id not in all_email_ids:
                        all_email_ids+=mail_id
                
                all_email_ids=all_email_ids[:-1]
            values['all_email_ids']=all_email_ids

        
        app_lst=[]
        if values.get('app_rec_ids'):
            app_lst=values.get('app_rec_ids')[0][2]
        if values.get('what_is_your_lending_goal') and app_lst:

            

            app_objs=self.pool.get('applicant.record').browse(cr,uid,app_lst[0])
            if values.get('what_is_your_lending_goal') == '1':

                sub_name=app_objs.applicant_name + " " + app_objs.applicant_last_name+ " - " +(values.get('considered_cites') or "NA" )+ ", " +(values.get('application_date') or 'NA')
                values['name']=sub_name
            elif values.get('what_is_your_lending_goal') == "2" or values.get('what_is_your_lending_goal') == "3":
                sub_name=app_objs.applicant_name + " " + app_objs.applicant_last_name+" - "+(values.get('address') or "NA")+ ", " +(values.get('city') or "NA")+ ", " +(values.get('charge_on_title') or "NA")+ ", " +(values.get('application_date') or "NA")
                values['name']=sub_name


        deadline=( datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
        if values.get('closing_date',False):
            congrats_date=( values.get('closing_date',False) + datetime.timedelta(hours=72)).strftime('%Y-%m-%d %H:%M:%S')
            values.update({'congrats_date':congrats_date})
        if dep_id:
#            values.update({'hr_department_id':dep_id[0]})
            values.update({'hr_department_id':dep_id})
        values.update({'deadline':deadline})

        
        usr_id =super(crm_lead, self).create(cr, uid, values, context=context)

        return usr_id

    def onchange_contact(self, cr, uid, ids, partner_id): 
        if partner_id:
            obj_res_partner = self.pool.get('res.partner').browse(cr,uid,partner_id)
            val = {'Spouse': obj_res_partner.Spouse or '',
                    'email_from':obj_res_partner.email or '',
                    'email_work':obj_res_partner.email_personal or '',
                    'mobile':obj_res_partner.mobile or '',
                    'work_phone':obj_res_partner.work_phone or '',
                    'phone':obj_res_partner.phone or '',
                    'preferred_number':obj_res_partner.preferred_phone or '',
                    'fax':obj_res_partner.fax or ''
                }
            return {'value': val}
        else:
            return 1
    
    def sendmail(self,cr,uid,ids,template_title,res_id,context=None):
        if context==None:
            context={}
        email_template_obj = self.pool.get('email.template')        

        crm_browse = self.browse(cr,uid,ids[0])
        context.update({'crm_id':crm_browse})
        print "ids===",ids
        print"context",context
        # Random create pwd
        uname = pwd = ''
        if crm_browse.webform_uname and crm_browse.webform_pwd:
            uname = crm_browse.webform_uname
            pwd = crm_browse.webform_pwd
        else:
            name = crm_browse.partner_id.name 
            #uname = name.replace(" ", "")
            uname = ''.join(e for e in name if e.isalnum())
            #pwd = ''.join(random.choice(string.ascii_lowercase) for x in range(6))
            pwd = binascii.b2a_hex(os.urandom(3))

        print "uname===",uname
        print "pwd===",pwd

        # Create Joomla Record

        #req = urllib2.Request('http://107.23.130.227/visdom/Visdomlive/tmp/generaterecord.php?view=mortgageapplication&id=%s&username=%s&password=%s'%(ids[0],uname,pwd))
       # req = urllib2.Request('https://198.72.106.11/visdom/tmp/generaterecord.php?view=mortgageapplication&id=%s&username=%s&password=%s'%(ids[0],uname,pwd))
	req = urllib2.Request('https://webserv.visdom.ca/tmp/generaterecord.php?view=mortgageapplication&id=%s&username=%s&password=%s'%(ids[0],uname,pwd))
#        req = urllib2.Request('http://192.168.1.89/visdom/tmp/generaterecord.php?view=mortgageapplication&id=%s&username=%s&password=%s'%(ids[0],uname,pwd))
	print "*****************req**********************",req
        urllib2.urlopen(req)

        self.write(cr,uid,ids,{'webform_uname':uname,'webform_pwd':pwd})

#        cr.execute('SELECT id FROM email_template WHERE "name" ilike %s',('%'+template_title+'%',) )
#        cr.commit()
#        template_details = cr.dictfetchall()
#        if not template_details:
#            raise osv.except_osv(('Template Not Found'),('The selected template "'+template_title+'" is not configured'))
#        template_id = template_details[0]['id']
#        print "email_from===============",template_id.id.email_from
#        print "email_to====",template_id.email_to
        context.update({'lead_id':ids[0],'user_id':uid})
#        message_id = email_template_obj.send_mail(cr, uid, template_title, res_id, force_send=True, context=context)
#        print "=======================message sent successfully=========================="
        return True
#        cr.execute('SELECT state FROM mail_message WHERE id = %s',(message_id,) )
#        cr.commit()
#        message_details = cr.dictfetchall()
#        message_state = message_details[0]['state']
#        if message_state == "exception": 
#            raise osv.except_osv(('Missing SMTP Server'),('Please define at least one SMTP server, or provide the SMTP parameters explicitly')) 
#        else:
#            return True

    def send_email_awaiting(self,cr,uid,ids,context=None):
        ir_model_data = self.pool.get('ir.model.data')
#        template_id = ir_model_data.get_object_reference(cr, uid, 'syml', 'email_template_related_docs')[1]
        compose_form_id = ir_model_data.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')[1]
        print"compose_form_id",compose_form_id
        ctx = dict(context)
        print"ctx",ctx
        ctx.update({
            'default_model': 'crm.lead',
            'default_res_id': ids[0],
            'default_type': '',
            
            'default_composition_mode': 'comment',
            'crm_id':''


            #'mark_so_as_sent': True
        })
	print"ctx",ctx
        return {
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'mail.compose.message',
        'views': [(compose_form_id, 'form')],
        'view_id': compose_form_id,
        'target': 'new',
        'context': ctx,
         'nodestroy': True,
        }

    
    def write(self, cr, uid, ids, vals, context=None):
        if context==None:
            context={}
        if not isinstance(ids,list):
           ids = [ids]
        stage_name,opp_info_renewal,stage_id,assig_to,user,user_id,delayed_app_date='','','',uid,'',uid,''
        project_task = self.pool.get('project.task')
        mod_obj = self.pool.get('ir.model.data')
        res_users_obj=self.pool.get('res.users')
        
        crm_browse = self.browse(cr,uid,ids[0])
        
        context.update({'crm_id':crm_browse})
        stage_id=vals.get('stage_id',False)

	cr.execute("select count(id) from product_product")
        prod_count = cr.fetchone()[0]
        print "prod_count--------write--------",prod_count
        vals['prod_count']=prod_count

        if stage_id:
            stage_name=self.pool.get('crm.case.stage').browse(cr,uid,stage_id).name
        delayed_app_date=crm_browse.delayed_app_date
        lead_followup_date=crm_browse.lead_followup_date

        if vals.get('opp_info_renewal_date',False):
            opp_info_renewal=datetime.datetime.strptime(values.get('opp_info_renewal_date',False), "%Y-%m-%d")
            renewal_mail_date = opp_info_renewal - dateutil.relativedelta.relativedelta(months=8)
            vals['renewal_mail_date']=renewal_mail_date
            vals['date_renewed']=False
        cur_date_time=datetime.datetime.now()
        delayed_app_date=cur_date_time+datetime.timedelta(days=1)

        if vals.get('stage_id',False) and stage_name=='Partial App':
            if delayed_app_date==False:
                vals['delayed_app_date']=delayed_app_date
            if lead_followup_date==False:
                vals['lead_followup_date']=delayed_app_date
        app_brow_ids=self.browse(cr,uid,ids[0]).app_rec_ids

#        what_is_your_lending_goal,considered_cites=''
        what_is_your_lending_goal=crm_browse.what_is_your_lending_goal
        if what_is_your_lending_goal and app_brow_ids:
            considered_cites,application_date,charge_on_title,address,city='','','','',''
            if app_brow_ids:
                app_objs=app_brow_ids[0]
#            if vals.has_key('what_is_your_lending_goal'):
            
    #        else:
    #            what_is_your_lending_goal=self.browse(cr,uid,ids[0]).what_is_your_lending_goal

            if vals.has_key('considered_cites'):
                considered_cites=vals.get('considered_cites')
            else:
                considered_cites=self.browse(cr,uid,ids[0]).considered_cites

            if vals.has_key('application_date'):
                application_date=vals.get('application_date')
            else:
                application_date=self.browse(cr,uid,ids[0]).application_date

            if vals.has_key('address'):
                address=vals.get('address')
            else:
                address=self.browse(cr,uid,ids[0]).address

            if vals.has_key('city'):
                city=vals.get('city')
            else:
                city=self.browse(cr,uid,ids[0]).city

            if vals.has_key('charge_on_title'):
                charge_on_title=vals.get('charge_on_title')
	
            else:
                charge_on_title=self.browse(cr,uid,ids[0]).charge_on_title
	    print"charge on titleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",charge_on_title
	    if charge_on_title:
                if charge_on_title=='1':
                    charge_on_title='First'
                elif charge_on_title=='2':
                    charge_on_title='Second'
                elif charge_on_title=='3':
                    charge_on_title='Third'
                elif charge_on_title=='4':
                    charge_on_title='Fourth'
                elif charge_on_title=='5':
                    charge_on_title='Bridge'
                else:

                    charge_on_title=''
	        print"charge_on_titlecharge_on_title",charge_on_title	
            if what_is_your_lending_goal and app_brow_ids:
                if what_is_your_lending_goal == '1':
                    sub_name=app_objs.applicant_name + " " + app_objs.applicant_last_name+ " - " +(considered_cites or "NA" )+ ", " +(application_date or 'NA')
                    vals['name']=sub_name
                elif what_is_your_lending_goal == "2" or what_is_your_lending_goal == "3":
                    sub_name=app_objs.applicant_name + " " + app_objs.applicant_last_name+" - "+(address or "NA")+ ", " +(city or "NA")+ ", " +(charge_on_title or "NA")+ ", " +(application_date or "NA")
                    vals['name']=sub_name
        
        all_email_ids=""
        if vals.get('app_rec_ids'):
            new_rec_ids=vals.get('app_rec_ids')[0][2]
            if new_rec_ids:
                applicant_obj=self.pool.get('applicant.record')

                for each in new_rec_ids:
                    mail_id=""
                    mail_id=applicant_obj.browse(cr,uid,each).email_personal+","
                    if mail_id not in all_email_ids:
                        all_email_ids+=mail_id
                all_email_ids=all_email_ids[:-1]
            vals['all_email_ids']=all_email_ids
        
        
        app_record_obj=self.pool.get('applicant.record')
        app_name=''
        emails_cc=''
        if crm_browse.app_rec_ids:
            for each_appl in crm_browse.app_rec_ids[1:]:
                emails_cc += each_appl.email_personal + ","

        if vals.has_key('stage_id') and vals['stage_id']:
            stage_brw=self.pool.get('crm.case.stage').browse(cr,uid,vals['stage_id'])
            print"stage_brw",stage_brw.name
#            if stage_brw.name=='Pending Application':
#                mod_obj = self.pool.get('ir.model.data')
#                template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_relator_referal_received')
#                template_id = template and template[1] or False
#                if template_id:
#                    self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
#            print"crm_browse.state",crm_browse.state
            if stage_brw.name=='Task':
                self.verify_product(cr,uid,ids,context)
            if stage_brw.name=='All Product':
                self.all_products(cr,uid,ids,context)
            if stage_brw.name=='Post Selection':
                self.post_selection(cr,uid,ids,context)
            if stage_brw.name=='Expired' or stage_brw.name=='Lost':
                mod_obj = self.pool.get('ir.model.data')
                template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_relator_expired_referal')
                template_id = template and template[1] or False
#                if template_id:
#                    self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
            if stage_brw.name=='Paid':
                datas=[]
                ir_attachment = self.pool.get('ir.attachment')
                mod_obj = self.pool.get('ir.model.data')
                template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_paid_refferal_message')
                template_id = template and template[1] or False
#                if template_id:
#                    self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)

#                template2 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_paid_refferal_relator')
#                template_id2 = template2 and template2[1] or False
#                if template_id2:
#                    self.pool.get('email.template').send_mail(cr,uid,template_id2,ids[0],'True',context)
               
#                datas = {
#                         'model': 'crm.lead',
#                         'ids': ids,
#                         'form': self.read(cr, uid, ids[0], context=context),
#                }
                attach_data= {'type': 'ir.actions.report.xml',
                'report_name': 'appl.snap3',
                'datas': datas, 'nodestroy': True}
                ir_attachment = self.pool.get('ir.attachment')
                service = netsvc.LocalService('report.appl.snap3')
                (result, format) = service.create(cr, uid,ids, attach_data, context)
                ir_attachment.create(cr, uid, {
                'name': 'Applicant Snapshot',
                'datas': base64.b64encode(result),
                'datas_fname': 'Applicant Snapshot',
                'res_model': 'crm.lead',
                'res_id': ids[0],
                'type':'binary'}, context)
                
                
            if stage_brw.name == 'Credit':
                app_ids=crm_browse.app_rec_ids
                if app_ids:
                    for each in app_ids:
                        app_record_obj.send_to_equifax(cr,uid,[each.id],context)
                    time.sleep(10)
                    for each in app_ids:
                        app_record_obj.fetch_equifax_response(cr,uid,[each.id],context)
            if stage_brw.name == 'Proposal':
                user=crm_browse.hr_department_id.id
                if user:
                    user_id=user
                assig_to_ids=''
                context.update({'lead_id':ids[0],'user_id':user_id})
                
                self.all_products(cr,uid,ids,context)
#                template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_referral_proposal_notify')
#                template_id = template and template[1] or False
#                if template_id:
#                    context.update({'proposal':ids[0],'user_id':uid})
#                    self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
                template2= mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_client_proposal_notify')
                template_id2 = template2 and template2[1] or False
#                if template_id2:
#                    context.update({'proposal':ids[0],'user_id':uid})
#                    self.pool.get('email.template').send_mail(cr,uid,template_id2,ids[0],'True',context)
                create_date=datetime.datetime.strptime(crm_browse.create_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
                create_date=(create_date + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
                app_name,name='',''
                if crm_browse.app_rec_ids:
                    app_name=crm_browse.app_rec_ids[0].applicant_name
                name='Contact' + "  " + app_name + "  " + \
                'with a phone call before' + " " +str(create_date) +" " +\
                'to review the proposal together and answer questions / have product selected.'
                assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','broker'),('hr_department_id','=',crm_browse.hr_department_id.id)])
                if assig_to_ids:
                    assig_to=assig_to_ids[0]
                project_task.create(cr, uid, {
                        #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                        'name': name  ,
                        'date_deadline': str(create_date) ,
                        'hr_department_id':crm_browse.hr_department_id.id,
                        'related_to':ids[0]  or False,
                        'user_id':assig_to,
                        'create_date':datetime.datetime.now(),
                        'state':'open',
                       
                        },context=context)
                user = self.pool.get('res.users').browse(cr ,uid ,uid)
                subject = ('''Task has been created''')
                details = ('''User "%s" has created the task''') % (user.name)

                self.message_post(cr, uid, ids, body=details, subject=subject, context=context)
            if stage_brw.name == 'Awaiting Docs':
                user=crm_browse.hr_department_id.id
                if user:
                    user_id=user
                assig_to_ids=''
                context.update({'lead_id':ids[0],'user_id':user_id})
                if crm_browse.referred_source.received_update==True and crm_browse.referred_source.role=='realtor':
                    template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_related_docs')
                    template_id = template and template[1] or False
                    print"templatee1",template_id
 #                   if template_id:
    #                    context.update({'proposal':ids[0],'user_id':uid})
#                        self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
                cr.execute("select count(id) from product_product")
                prod_count = cr.fetchone()[0]
                date=(datetime.datetime.now()+ datetime.timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
                self.write(cr,uid,ids,{'prod_count':int(prod_count),'template_date':date},context)
#                template2 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_document_requirement')
#                template_id2 = template2 and template2[1] or False
#                print"templatee2",template_id2
#                if template_id2:
#                    context.update({'app_completed':emails_cc})
##                    context.update({'proposal':ids[0],'user_id':uid})
#                    self.pool.get('email.template').send_mail(cr,uid,template_id2,ids[0],'True',context)
            if stage_brw.name == 'Completed App':
                context.update({'app_completed':''})

                #template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_acknowledge_app_receieved')
                #template_id = template and template[1] or False
                #if template_id:
#                    context.update({'app_completed':emails_cc,'crm_id':crm_browse})
                    #context.update({'crm_id':crm_browse})
                    #self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)

#                second mail
                #if crm_browse.referred_source.received_update==True:
                    #context.update({'app_completed':''})
                    #template2 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_app_complete')
                    #template_id2 = template2 and template2[1] or False
                    #if template_id2:

                        #self.pool.get('email.template').send_mail(cr,uid,template_id2,ids[0],'True',context)

                if crm_browse.condition_of_financing_date:
                    app_name,app_email,comp_app_name='','',''
                    if crm_browse.app_rec_ids:
                        app_name=crm_browse.app_rec_ids[0].applicant_name
                        app_email=crm_browse.app_rec_ids[0].email_personal
                    comp_app_name=' Send Condition of Financing Letter before' + "  " + (crm_browse.condition_of_financing_date or '') + "  " + \
                    'to' + " " +app_name +  " " + 'at' + " " + app_email + " " + "and" + " " + ( crm_browse.referred_source and crm_browse.referred_source.partner_id and crm_browse.referred_source.partner_id.name  or '')+  " " + 'at' + " " + (crm_browse.referred_source and crm_browse.referred_source.email_from or '')  + " "+ \
                    'using the Condition of Financing Letter template.'
                    assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','broker'),('hr_department_id','=',crm_browse.hr_department_id.id)])
                    if assig_to_ids:
                        assig_to=assig_to_ids[0]
                    project_task.create(cr, uid, {
                            #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                            'name': comp_app_name  ,
                            'date_deadline': crm_browse.condition_of_financing_date or False,
                            'hr_department_id':crm_browse.hr_department_id.id,
                            'related_to':ids[0]  or False,
                            'user_id': assig_to,
                            'create_date':datetime.datetime.now(),
                            'state':'open',

                            },context=context)
                new_opp_name=''
		
                new_opp_name='Review ' + crm_browse.name or  '' + 'as well as the list of applicants for completeness and change stage to Credit'
                create_date=datetime.datetime.now()
		
                deadline=(create_date + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
                assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','assistant'),('hr_department_id','=',crm_browse.hr_department_id.id)])
                print"assig_to_ids",assig_to_ids
                if assig_to_ids:
                    assig_to=assig_to_ids[0]
                
                project_task.create(cr, uid, {
                        #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                        'name': new_opp_name  ,
                        'date_deadline': deadline or False ,
                        'hr_department_id':crm_browse.hr_department_id.id,
                        'related_to':ids[0]  or False,
                        'user_id': assig_to,
                        'create_date':datetime.datetime.now(),
                        'state':'open',

                        },context=context)
                template,template_id=False,False
                template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_review_task')
                template_id = template and template[1] or False
                assig_to_email=res_users_obj.browse(cr,uid,assig_to).email
                dept_email=crm_browse.hr_department_id.mail_server.smtp_user
                if dept_email:
                    assig_to_email = assig_to_email + ',' +  dept_email
                print"assig_to_emailassig_to_emailassig_to_emailassig_to_emaillllllllllllllllllllll",assig_to_email
                
                context.update({'new_opp':assig_to_email})
#                if template_id:
#                    context.update({'proposal':ids[0],'user_id':uid})
#                    self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
            if stage_brw.name == 'Commitment':
                context.update({'new_opp':''})
                referred_source_name,app_name,lender_name='','',''
                assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','assistant'),('hr_department_id','=',crm_browse.hr_department_id.id)])
                
                if assig_to_ids:
                    assig_to=assig_to_ids[0]
                create_date=datetime.datetime.now()
                deadline=(create_date + datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
                if crm_browse.app_rec_ids:
                    app_name=crm_browse.app_rec_ids[0].applicant_name
                if len(crm_browse.app_rec_ids) >= 2:
                    app_name=app_name + ' '+ "and" + " " + crm_browse.app_rec_ids[1].applicant_name
                if crm_browse.referred_source:
                    referred_source_name= crm_browse.referred_source.partner_id.name
                if crm_browse.referred_source and crm_browse.referred_source.partner_id and crm_browse.referred_source.partner_id.last_name:
                    referred_source_name = referred_source_name + ' ' + crm_browse.referred_source.partner_id.last_name
                if crm_browse.selected_product and crm_browse.selected_product.lender:
                    lender_name=crm_browse.selected_product.lender.name
                project_task.create(cr, uid, {
                            #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                            'name': 'Build "outstanding items list" and send congratulations message to' + ' ' + app_name + ' ' +   'as well as the Referral Source, ' +  ' ' + referred_source_name ,
                            'description':'Please cross-reference the Commitment Package from' + ' ' +  lender_name + ' ' + 'to determine whether there are any requirements which have not already been fulfilled with existing documentation.  Create an "outstanding items" list and send the client and referral source a congratulations message which includes the outstanding items list using the "Client Approval Message" template.  (Please choose the correct template depending on whether the lender pays property taxes or whether client is responsible for property taxes.',
                            'date_deadline': deadline,
                            'hr_department_id':crm_browse.hr_department_id.id,
                            'related_to':ids[0]  or False,
                            'user_id': assig_to,
                            'create_date':datetime.datetime.now(),
                            'state':'open',

                            },context=context)
                user=crm_browse.hr_department_id.id
                if user:
                    user_id=user
                assig_to_ids=''
                context.update({'lead_id':ids[0],'user_id':user_id})
                template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_req_ref_approval_msg')
                template_id = template and template[1] or False
#                if template_id:
#                    self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)

#                app_name,deadline_broker,assig_to_broker='',False,uid
                if crm_browse.app_rec_ids:
                    app_name=crm_browse.app_rec_ids[0].applicant_name
                    app_name1=crm_browse.app_rec_ids[0].applicant_name
                if len(crm_browse.app_rec_ids) >= 2:
                    app_name1=app_name1 + ' '+ "and" + " " + crm_browse.app_rec_ids[1].applicant_name
                assig_to_ids_broker=res_users_obj.search(cr,uid,[('designation','=','broker'),('hr_department_id','=',crm_browse.hr_department_id.id)])
                
                if assig_to_ids_broker:
                    assig_to_broker=assig_to_ids_broker[0]
                deadline_broker=(create_date + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
                project_task.create(cr, uid, {
                            #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                            'name': 'Contact' + ' ' + app_name + ' ' + 'with a phone call before ' + ' ' + deadline + ' to review the Lender Commitment together and answer questions / have product selected.',
                            'description':'When you contact' + ' ' +  app_name1 + ' ' + 'please note there might be outstanding documentation or steps which are required by' + ' ' + lender_name + ' ' + 'Please review the Lender Commitment message which includes outstanding items in the Audit trail of the Opportunity record.  Additionally, please review the Commitment Package from the lender which is in the Opportunity Documents' ,
                            'date_deadline': deadline_broker,
                            'hr_department_id':crm_browse.hr_department_id.id,
                            'related_to':ids[0]  or False,
                            'user_id': assig_to_broker,
                            'create_date':datetime.datetime.now(),
                            'state':'open',

                            },context=context)
                if crm_browse.final_lender:
                    final_lender_name= crm_browse.final_lender.name
                    project_task.create(cr, uid, {
                                #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                                'name': 'Get File Complete from' + ' ' + final_lender_name + ' ' +   'using the "Request File Complete" email template after Commitment is returned to' +  ' ' + final_lender_name,
                                'description':'1) After the commitment and any outstanding documents have been sent to the lender, please request File Complete from' + ' ' +  final_lender_name + ' ' + 'using the "Request File Complete" email template.  2) Once the file complete please ensure the received email from the lender in the email history of the Opportunity.  3) Please change the stage of the Opportunity to "Compensation".' ,
                                'date_deadline': deadline,
                                'hr_department_id':crm_browse.hr_department_id.id,
                                'related_to':ids[0]  or False,
                                'user_id': assig_to,
                                'create_date':datetime.datetime.now(),
                                'state':'open',

                                },context=context)
#                    user=crm_browse.hr_department_id.id
#                    if user:
#                        user_id=user
#                    assig_to_ids=''
#                    context.update({'lead_id':ids[0],'user_id':user_id})
#                    template_file_comp = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_file_complete')
#                    template_id_file_comp = template_file_comp and template_file_comp[1] or False
#                    if template_id_file_comp:
#                        self.pool.get('email.template').send_mail(cr,uid,template_id_file_comp,ids[0],'True',context)
#                    template_file_comp_ref = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_file_complete_referral')
#                    template_id_file_comp_ref = template_file_comp_ref and template_file_comp_ref[1] or False
#                    if template_id_file_comp_ref:
#                        self.pool.get('email.template').send_mail(cr,uid,template_id_file_comp_ref,ids[0],'True',context)
                
                project_task.create(cr, uid, {
                            #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                            'name': 'Read through the Lender Commitment and ensure all fields in the Final Solution Tab of the Opportunity match the Lender Commitment. ' ,
                            'description':'Please edit the fields on the FInal Solution tab of the Opportunity record to reflect the information in the commitment letter.' ,
                            'date_deadline': deadline_broker,
                            'hr_department_id':crm_browse.hr_department_id.id,
                            'related_to':ids[0]  or False,
                            'user_id': assig_to,
                            'create_date':datetime.datetime.now(),
                            'state':'open',

                            },context=context)
            if stage_brw.name == 'Lender Submission':
		    print"lender submission"
                    context.update({'new_opp':''})
                    print"crm_browse.selected_product",crm_browse.selected_product.lender.documentation_method
                    if crm_browse.selected_product and crm_browse.selected_product.lender and crm_browse.selected_product.lender.documentation_method=='email':
                        
                        template_id_email_doc = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_email_lender_docs')
                        template_id_thr_email = template_id_email_doc and template_id_email_doc[1] or False

#                        if template_id_thr_email:
#                            self.pool.get('email.template').send_mail(cr,uid,template_id_thr_email,ids[0],'True',context)
#		    elif crm_browse.selected_product and crm_browse.selected_product.lender and crm_browse.selected_product.lender.documentation_method=='fax':
#                        template_id_fax_doc = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_fax_lender_docs')
#                        template_id_tmp_fax = template_id_fax_doc and template_id_fax_doc[1] or False

#                        if template_id_tmp_fax:
#                            self.pool.get('email.template').send_mail(cr,uid,template_id_tmp_fax,ids[0],'True',context)
            if vals.get('stage_id',False):
                context.update({'new_opp':''})
                cr.execute('select id from crm_case_stage where id = %s and "name" ilike %s',(vals.get('stage_id',False),'compensation',))
                stage_id = cr.fetchone()
                print "stage_id=========",stage_id
                if stage_id:
                    context.update({'lead_id':ids[0],'user_id':uid})
                    template_law_msg = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_lawyer_msg')
                    template_id_law_msg = template_law_msg and template_law_msg[1] or False

#                    if template_id_law_msg:
#                        self.pool.get('email.template').send_mail(cr,uid,template_id_law_msg,ids[0],'True',context)
                    if crm_browse.trailer_comp_amount > 0:
                        template_trailer = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_trailer')
                        template_id_trailer = template_trailer and template_trailer[1] or False

#                        if template_id_trailer:
#                            self.pool.get('email.template').send_mail(cr,uid,template_id_trailer,ids[0],'True',context)
                    else:
                        template_id_no_trailer = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_no_trailer')
                        template_id_no_trailer = template_id_no_trailer and template_id_no_trailer[1] or False

#                        if template_id_no_trailer:
#                            self.pool.get('email.template').send_mail(cr,uid,template_id_no_trailer,ids[0],'True',context)
                    user=crm_browse.hr_department_id.id
                    if user:
                        user_id=user
#                    assig_to_ids=''
                    context.update({'lead_id':ids[0],'user_id':user_id})
                    template_file_comp = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_file_complete')
                    template_id_file_comp = template_file_comp and template_file_comp[1] or False
#                    if template_id_file_comp:
#                        self.pool.get('email.template').send_mail(cr,uid,template_id_file_comp,ids[0],'True',context)
#                    template_file_comp_ref = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_file_complete_referral')
#                    template_id_file_comp_ref = template_file_comp_ref and template_file_comp_ref[1] or False
#                    if template_id_file_comp_ref:
#                        self.pool.get('email.template').send_mail(cr,uid,template_id_file_comp_ref,ids[0],'True',context)
            if vals.get('stage_id',False):
                context.update({'new_opp':''})
                cr.execute('select id from crm_case_stage where id = %s and "name" ilike %s',(vals.get('stage_id',False),'pending application',))
                stage_id = cr.fetchone()
                print "stage_id=========",stage_id
                #if stage_id:
                    
                   # template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_relator_referal_received')
                    #template_id = template and template[1] or False
                   # if template_id:
                        #self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
                   # cur_dt=time.strftime('%Y-%m-%d %H:%M:%S')
                    #cur_dt=datetime.datetime.strptime(cur_dt, tools.DEFAULT_SERVER_DATETIME_FORMAT)
                    #welcum_exp_date=(cur_dt + datetime.timedelta(days=14)).strftime('%Y-%m-%d %H:%M:%S')
                    #self.write(cr,uid,ids,{'welcum_email_date':welcum_exp_date})
                    #template2 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_mortgage_referral')
                    #template_id2 = template2 and template2[1] or False
                    #if template_id2:
#                        self.pool.get('email.template').send_mail(cr,uid,template_id2,ids[0],'True',context)
#                    if crm_browse.partner_id:
                        #context.update({'pending_app':crm_browse})
                        #self.sendmail(cr,uid,ids,template_id2,ids[0],context)
                    #else:
                        #raise osv.except_osv(('Error'),('Partner Not Found....'))


        if crm_browse.type == 'opportunity':
            context.update({'new_opp':''})
            pdate=(datetime.datetime.now()+ datetime.timedelta(hours=72)).strftime('%Y-%m-%d %H:%M:%S')
            vals.update({'propsal_date':pdate})
        
                
        
        res = super(crm_lead, self).write(cr, uid, ids, vals)
        if vals.get('selected_product',False):
            context.update({'new_opp':''})
            assig_to_ids=''
            if crm_browse.type=='opportunity':
                user=crm_browse.hr_department_id.id
                if user:
                    user_id=user
                assig_to_ids=''
                context.update({'lead_id':ids[0],'user_id':user_id})
                prdate=(datetime.datetime.now()+ datetime.timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
                vals.update({'propsal_date':prdate})
                assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','assistant'),('hr_department_id','=',crm_browse.hr_department_id.id)])
                print"assig_to_ids",assig_to_ids
                if assig_to_ids:
                    assig_to=assig_to_ids[0]
                create_date=datetime.datetime.now()
                deadline=(create_date + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
#                post_select_task = project_task.search(cr, uid, [('related_to','=',ids[0]),('uw_app','=','postselection')])
#                if post_select_task:
#                    project_task.unlink(cr, uid, post_select_task)
                project_task.create(cr, uid, {
                            #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                            'name': 'Run Post Selection workflow by clicking the "Post Selection" Stage. Afterwards, check tasks for new tasks and No Error Messages. ' ,
                            'date_deadline': deadline,
                            'hr_department_id':crm_browse.hr_department_id.id,
                            'related_to':ids[0]  or False,
                            'user_id': assig_to,
                            'create_date':datetime.datetime.now(),
                            'uw_app':'postselection',
                            'state':'open',

                            },context=context)
                user = self.pool.get('res.users').browse(cr ,uid ,uid)
                subject = ('''Task has been created to Verify Product Algo is run''')
                details = ('''User "%s" has created the task''') % (user.name)
                self.message_post(cr, uid, ids, body=details, subject=subject, context=context)
                template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_product_confirm')
                template_id = template and template[1] or False
#                if template_id:
#                    print"template_id",template_id
#                    self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
                if crm_browse.referred_source.received_update==True:
                    template2 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_ref_product_notify')
                    template_id2 = template2 and template2[1] or False
#                    if template_id2:

#                       self.pool.get('email.template').send_mail(cr,uid,template_id2,ids[0],'True',context)
#                template3 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_assistant_lender_entry_notice_template')
#                template_id3 = template3 and template3[1] or False
#                if template_id3:

#                    self.pool.get('email.template').send_mail(cr,uid,template_id3,ids[0],'True',context)
        if vals.get('closing_date',False):
            context.update({'new_opp':''})
            print"vals.get('closing_date',False)",vals.get('closing_date',False)
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            closing_date=datetime.datetime.strptime(datetime.datetime.strptime(vals.get('closing_date',False),"%Y-%m-%d").strftime('%Y-%m-%d %H:%M:%S'), DATETIME_FORMAT)
#            closing_date=(vals.get('closing_date',False)).strftime('%Y-%m-%d %H:%M:%S')
#            closing_date=datetime.datetime.strptime(vals.get('closing_date',False),"%Y-%m-%d %H:%M:%S")

            congrats_date=(closing_date + datetime.timedelta(hours=72)).strftime('%Y-%m-%d %H:%M:%S')
            vals.update({'congrats_date':congrats_date})
	    self.write(cr,uid,ids,{'congrats_date':congrats_date})
            close_date_name=''
            close_date_name='Close' + "  " + crm_browse.name + "  " + 'in Morweb / Filogix on' + " " + vals.get('closing_date',False)
            assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','assistant'),('hr_department_id','=',crm_browse.hr_department_id.id)])

            if assig_to_ids:
                assig_to=assig_to_ids[0]
            project_task.create(cr, uid, {
                        #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                        'name': close_date_name  ,
#                        'date_deadline': vals.get('closing_date',False) ,
                        'date_deadline': str(closing_date) ,
                        'hr_department_id':crm_browse.hr_department_id.id,
                        'related_to':ids[0]  or False,
                        'user_id': assig_to,
                        'create_date':datetime.datetime.now(),
                        'state':'open',

                        },context=context)

        if vals.get('renewaldate',False):
            context.update({'new_opp':''})
            renewal_remainder_mail_date=''
            opp_info_renewal=datetime.datetime.strptime(vals.get('renewaldate',False), "%Y-%m-%d")
            if crm_browse.term in ('6month','1year','2year'):
                renewal_remainder_mail_date = opp_info_renewal - dateutil.relativedelta.relativedelta(months=3)
            else:
                renewal_remainder_mail_date = opp_info_renewal - dateutil.relativedelta.relativedelta(months=8)
            vals.update({'renewal_reminder':renewal_remainder_mail_date})
	    self.write(cr,uid,ids,{'renewal_reminder':renewal_remainder_mail_date})
        return res
    
    def scheduler_for_lead(self, cr, uid, context={}):
        """
        Convert lead to opportunity. OR
        Cancel the Lead. i.e. Dead state
        """
        print "================web response scheduler called================"
        
        crm_lead = self.pool.get('crm.lead')
        lead2oppr = self.pool.get('crm.lead2opportunity.partner')
#        cr.execute('select id from crm_case_stage where "name" ilike %s',('pending application',))
#        pending_application_id = cr.fetchone()
#        if pending_application_id:
        cr.execute(""" select id,web_response from crm_lead where web_response in %s and stage_id = 
            (select id from crm_case_stage where "name" ilike %s)""",
                (('accept','reject'),'pending application'))
        lead_ids = cr.fetchall()
        print "lead_ids",lead_ids
        if lead_ids:
            print "lead responde by customer ======",lead_ids
            for lead in lead_ids:                    
                   if lead[1] == 'accept':
                        print "inside if condition. lead web response ======",lead[1]
                        print "lead id",lead[0]
                        context['active_id']=lead[0]
                        context['active_ids']=[lead[0]]
                        context['active_model']='crm.lead'
                        lead2oppr_id = lead2oppr.create(cr, uid, {},context=context)
                        lead2oppr.action_apply(cr, uid, [lead2oppr_id],context=context)
                   elif lead[1] == 'reject':
                        print "inside elif condition. lead web response =========",lead[1]
                        print "lead id",lead[0]
                        crm_lead.case_cancel(cr, uid, [lead[0]], context=context)
        
        return True


    def xml_set_attribute(self,cr,uid,xml_data,key,val):
        if val:
            print "key>>>",key
            print "val>>>",val
            xml_data.setAttribute(key, val)
        
        

    def xml_parse(self,cr,uid,ids,xml,context):
        print "type>>>",type(xml)
        
        applicant_obj = self.pool.get('applicant.record')
        applicant_address_obj = self.pool.get('applicant.address')
        crm_browse = self.browse(cr,uid,ids[0])
        responseDOM = parseString(xml)
        print "responseDOM>>",type(responseDOM)
        
        tag_list = context.get('tag_name')
        applicant_id = context.get('applicant_id')
        print "applicant_id>>>",applicant_id
        print "tag_list>>>",tag_list
        address_ids = applicant_address_obj.search(cr, uid, [('applicant_id','=',applicant_id)])
        print "address_ids >>>>",address_ids
        
        for i in range(0,len(tag_list)):
            if tag_list[i] == 'CustomerBorrower':
                applicant_browse = applicant_obj.browse(cr,uid,applicant_id)
                name = applicant_browse.applicant_name or ''
                last_name = applicant_browse.applicant_last_name or ''
                email = applicant_browse.email_personal or ''
                relationship_status = applicant_browse.relationship_status or ''
                date_birth = applicant_browse.dob or ''
                sin = applicant_browse.sin or ''
                customer_data = responseDOM.getElementsByTagName(tag_list[i])
                self.xml_set_attribute(cr,uid,customer_data[0],'firstName',name)
                self.xml_set_attribute(cr,uid,customer_data[0],'lastName',last_name)
                self.xml_set_attribute(cr,uid,customer_data[0],'emailAddress1',email)
                self.xml_set_attribute(cr,uid,customer_data[0],'SIN',sin)
                self.xml_set_attribute(cr,uid,customer_data[0],'dateBirth',date_birth)
                rel_status_dict = {'Single':'1','Married':'2','Widowed':'3','Separated':'4','Divorced':'5','Common-Law':'6','Other':'99'}
                if relationship_status in rel_status_dict.keys():
                    status = rel_status_dict[relationship_status]
                    self.xml_set_attribute(cr,uid,customer_data[0],'maritalStatus',status)

            elif tag_list[i] == 'ApplicationAddressCanada':
                applicant_address_search = applicant_address_obj.search(cr, uid, [('applicant_id','=',applicant_id)])
                if applicant_address_search:
                    print "applicant_address_search>>>>>>>>>",applicant_address_search
                    applicant_address_browse = applicant_address_obj.browse(cr,uid,applicant_address_search[0])
                    city = applicant_address_browse.city or ''
                    postal_code = applicant_address_browse.postal_code or ''
                    #po_box_number = applicant_address_obj.browse(cr,uid,address_ids[0]).postal_code or ''
                    street = applicant_address_browse.street or ''
                    customer_data = responseDOM.getElementsByTagName(tag_list[i])
                    self.xml_set_attribute(cr,uid,customer_data[0],'cityTown',city)
                    


            ##elif tag_list[i] == 'ApplicationAddressCanada':
                ##if address_ids[0]:
                    ##applicant_address_browse = applicant_address_obj.browse(cr,uid,address_ids[0])
                    ##city = applicant_address_browse.city or ''
                    #postal_code = applicant_address_obj.browse(cr,uid,address_ids[0]).postal_code or ''
                    #po_box_number = applicant_address_obj.browse(cr,uid,address_ids[0]).postal_code or ''
                    ##street = applicant_address_browse.street or ''
                    ##customer_data = responseDOM.getElementsByTagName(tag_list[i])
                    ##self.xml_set_attribute(cr,uid,customer_data[0],'cityTown',city)
                    #print "postal_code>",postal_code
                    
                    
                    #self.xml_set_attribute(cr,uid,customer_data[0],'postalCode',postal_code)
                    #self.xml_set_attribute(cr,uid,customer_data[0],'po_box_number',postal_code)
                    #self.xml_set_attribute(cr,uid,customer_data[0],'countryCode','1')
                    #self.xml_set_attribute(cr,uid,customer_data[0],'streetNumber','0')
                    #self.xml_set_attribute(cr,uid,customer_data[0],'streetType','-1')
                    #self.xml_set_attribute(cr,uid,customer_data[0],'unitNumber','0')
                    #self.xml_set_attribute(cr,uid,customer_data[0],'streetDirection',"-1")


#                    print "applcntaddress>>>>>>>>>>>>>",applcntaddress[1].toprettyxml()
#                    applcntaddress[1].setAttribute('cityTown', name)
#                    applcntaddress[1].setAttribute('countryCode', '1')
#                    applcntaddress[1].setAttribute('postalCode', 'V2A1A5')
#                    applcntaddress[1].setAttribute('provinceCode', '10')
#                    applcntaddress[1].setAttribute('POBoxRRNumber', "12")
#                    applcntaddress[1].setAttribute('streetDirection', "-1")
#                    applcntaddress[1].setAttribute('streetName', name)
#                    applcntaddress[1].setAttribute('streetNumber', "0")
#                    applcntaddress[1].setAttribute('streetType', "-1")
#                    applcntaddress[1].setAttribute('unitNumber', "0")                   #applicantaddress[0].setAttribute('countryCode', '1')

                    #applicantaddress[0].setAttribute('streetDirection', "-1")

#
#                    print "applcntaddress>>>>>>>>>>>>>",applcntaddress[2].toprettyxml()
#                    applcntaddress[2].setAttribute('cityTown', name)
#                    applcntaddress[2].setAttribute('countryCode', '1')
#                    applcntaddress[2].setAttribute('postalCode', 'V2A1A5')
#                    applcntaddress[2].setAttribute('provinceCode', '10')
#                    applcntaddress[2].setAttribute('POBoxRRNumber', "12")
#                    applcntaddress[2].setAttribute('streetDirection', "-1")
#                    applcntaddress[2].setAttribute('streetName', name)
#                    applcntaddress[2].setAttribute('streetNumber', "0")
#                    applcntaddress[2].setAttribute('streetType', "-1")
#                    applcntaddress[2].setAttribute('unitNumber', "0")


#            elif tag_list[i] == 'Employment':
#                applicant_employer_obj = self.pool.get('income.employer')
#                print "applicant_id>>>>",applicant_id
#                applicant_employer_search = applicant_employer_obj.search(cr, uid, [('applicant_id','=',applicant_id)])
#                if applicant_employer_search:
#                    applicant_employer_browse = applicant_employer_obj.browse(cr,uid,applicant_employer_search[0])
#                    companyName = applicant_employer_browse.business or ''
#                    jobTitle = applicant_employer_browse.position or ''
#                    earnedIncomeAmount = applicant_employer_browse.annual_income or ''
#                    customer_data = responseDOM.getElementsByTagName(tag_list[i])
#                    self.xml_set_attribute(cr,uid,customer_data[0],'companyName',companyName)
#                    self.xml_set_attribute(cr,uid,customer_data[0],'jobTitle',jobTitle)
                    
                
                

#            elif tag_list[i] == 'SubjectProperty':
#                customer_data = responseDOM.getElementsByTagName(tag_list[i])
#                propertyType = crm_browse.property_type or ''
#                heatingType = crm_browse.heating or ''
#                sewageType = crm_browse.sewage or ''
#                garageType = crm_browse.garage_type or ''
#                garageSize = crm_browse.garage_size or ''
#                MLSNumber = crm_browse.mls or ''
#
#                if MLSNumber:
#                    self.xml_set_attribute(cr,uid,customer_data[0],'MLSNumber',MLSNumber)
#
#                heat_dict = {'1':'2','2':'1','3':'3','4':'4'}
#                if heatingType in heat_dict.keys():
#                    heat_type = heat_dict[heatingType]
#                    self.xml_set_attribute(cr,uid,customer_data[0],'heatingType',heat_type)
#
#                sewage_dict = {'1':'10','2':'20','3':'30','4':'99'}
#                if sewageType in sewage_dict.keys():
#                    sewage_type = sewage_dict[sewageType]
#                    self.xml_set_attribute(cr,uid,customer_data[0],'waterWasteType',sewage_type)
#
#                property_type_dict = {'1':'7','2':'3','3':'5','4':'6','5':'7','6':'12'}
#                if propertyType in property_type_dict.keys():
#                        property_type = property_type_dict[propertyType]
#                    self.xml_set_attribute(cr,uid,customer_data[0],'propertyDescriptionType',property_type)
#
#                if garageSize:
#                    garage_size_dict = {}
#                    if garageType == "1":
#                        garage_size_dict = {'1':'1','2':'3','3':'5','4':'7'}
#                        if garageSize in garage_size_dict.keys():
#                            garage_size = garage_size_dict[garageSize]
#                            self.xml_set_attribute(cr,uid,customer_data[0],'parkingType',garage_size)
#
#                    elif garageType == "2":
#                        garage_size_dict = {'1':'2','2':'4','3':'6','4':'7'}
#                        if garageSize in garage_size_dict.keys():
#                            garage_size = garage_size_dict[garageSize]
#                            self.xml_set_attribute(cr,uid,customer_data[0],'parkingType',garage_size)
#
#                    elif garageType == "3":
#                        self.xml_set_attribute(cr,uid,customer_data[0],'parkingType',"7")

                
#            elif tag_list[i] == 'PropertyTax':
#                propertyTaxes = crm_browse.property_taxes or ''
#                if propertyTaxes:
#                    customer_data = responseDOM.getElementsByTagName(tag_list[i])
#                    annualTaxAmount = str(propertyTaxes)
#                    annualTaxAmount = annualTaxAmount.replace(",", "")
#                    self.xml_set_attribute(cr,uid,customer_data[0],'annualTaxAmount',annualTaxAmount)
 
            elif tag_list[i] == 'Loan':
                loanAmount = crm_browse.desired_mortgage_amount or '' 
                customer_data = responseDOM.getElementsByTagName(tag_list[i])
                self.xml_set_attribute(cr,uid,customer_data[0],'loanAmount',str(loanAmount))


            elif tag_list[i] == 'MortgageApplication':
                fundingDate = crm_browse.expected_closing_date or ''
                loanPurposeType = crm_browse.what_is_your_lending_goal or ''
                if loanPurposeType:
                    loanPurposeType_dict = {'2':'3','3':'1'}
                    customer_data = responseDOM.getElementsByTagName(tag_list[i])
                    if loanPurposeType in loanPurposeType_dict.keys():
                        self.xml_set_attribute(cr,uid,customer_data[0],'loanPurposeType',loanPurposeType_dict[loanPurposeType])
                    else:
                        self.xml_set_attribute(cr,uid,customer_data[0],'isPreapproval','true')

                if fundingDate:
                    fdt = fundingDate.split('/')
                    fundingDate = fdt[2] + "-" + fdt[1] + "-" + fdt[0]
                    customer_data = responseDOM.getElementsByTagName(tag_list[i])
                    self.xml_set_attribute(cr,uid,customer_data[0],'fundingDate',fundingDate)
                

#            elif tag_list[i] == 'LegalAddress':
#                planNumber = crm_browse.plan or ''
#                lotNumber = crm_browse.lot or ''
#                pin = crm_browse.block or ''
#                customer_data = responseDOM.getElementsByTagName(tag_list[i])
#                self.xml_set_attribute(cr,uid,customer_data[0],'planNumber',planNumber)
#                self.xml_set_attribute(cr,uid,customer_data[0],'lotNumber',lotNumber)
#                self.xml_set_attribute(cr,uid,customer_data[0],'PIN',pin)
#
#            elif tag_list[i] == 'Condo':
#                annualCondoFees = crm_browse.condo_fees or ''
#                if annualCondoFees:
#                    customer_data = responseDOM.getElementsByTagName(tag_list[i])
#                    self.xml_set_attribute(cr,uid,customer_data[0],'annualCondoFees',annualCondoFees)
                    
        return responseDOM.toprettyxml()

    
    def send_morweb_request(self,cr,uid,ids,context=None):
        applicant_obj = self.pool.get('applicant.record')
        crm_browse = self.browse(cr,uid,ids[0])
        morweb_request = crm_browse.company_id.morweb_request
        applicant_list = crm_browse.applicant_record_line
        
        
        if morweb_request:
            for applicant_rec in applicant_list:
                asset_tag = customer_asset_other = employment_tag = subject_property_tag = unearned_income_list = customer_address_previous_residence = application_address_canada_x = customer_borrower_n = asset_real_estate_a = ""
                i = 1
                #### for one2many fields (asset_ids)
                for asset_line in applicant_obj.browse(cr,uid,applicant_rec.id).asset_ids:
                    type = asset_line.asset_type
                    type_dict = {'Vehicle':'40','RRSPs':'30'}
                    if type:
                        if type in type_dict.keys():
                            asset_tag += '<AssetOther key="%s" value="%s" assetType="%s" description="%s"/>'%('AssetSavingkey%s'%(i),asset_line.value,type_dict[type],asset_line.name)
                            customer_asset_other += '<CustomerAssetOther refkeyAsset="%s"> <CustomerReference refkeyCustomer="MainCustomerKey1"/> </CustomerAssetOther>'%('AssetSavingkey%s'%(i))
                            i = i+1
                        else:
                            asset_tag += '<AssetOther key="%s" value="%s" assetType="%s" description="%s"/>'%('AssetSavingkey%s'%(i),asset_line.value,'99',asset_line.name)
                            customer_asset_other += '<CustomerAssetOther refkeyAsset="%s"> <CustomerReference refkeyCustomer="MainCustomerKey1"/> </CustomerAssetOther>'%('AssetSavingkey%s'%(i))
                            i = i+1
                

                #### for one2many fields (Applicant >>>>>> Employment/Income Tab)
                for income_line in applicant_obj.browse(cr,uid,applicant_rec.id).incomes:
                    type = income_line.name or ''
                    business = income_line.business or ''
                    position = income_line.position or ''
                    industry = income_line.industry or ''
                    annual_income = income_line.annual_income or ''
                    month = income_line.month or '' ## still need to be done 

                    type_dict = {'1':'8','2':'2','3':'4','5':'3','5':'11','6':'10','7':'9','8':'99'}
                    
                    if type in type_dict.keys():
                        type = type
                    else:
                        type = '99'

                    employment_tag += '''<Employment industryType="%s" employmentType="7" employmentStatus="10" dateStart="2008-03-30" jobTitle="developer" companyName="bistasolutions">
                                                <EarnedIncomeList>
                                                           <EarnedIncome earnedIncomeType="99" paymentFrequency="12" earnedIncomeAmount="1.12"/>
                                                </EarnedIncomeList>
                                        </Employment>'''%(type)


                ##Subject Property
                waterSupplyType = crm_browse.water or ''
                propertyTaxes = crm_browse.property_taxes or ''
                propertyType = crm_browse.property_type or ''
                heatingType = crm_browse.heating or ''
                sewageType = crm_browse.sewage or ''
                garageType = crm_browse.garage_type or ''
                garageSize = crm_browse.garage_size or ''
                MLSNumber = crm_browse.mls or '0000'
                square_footage = crm_browse.square_footage or '0000'
                #OccupancyCode = crm_browse.living_in_property or ''

                planNumber = crm_browse.plan or '0000'
                lotNumber = crm_browse.lot or '0000'
                pin = crm_browse.block or '0000'

                annualCondoFees = crm_browse.condo_fees or '0000'

                annualTaxAmount = crm_browse.property_taxes or '0000'
                occupancyStatus = crm_browse.living_in_property

                if occupancyStatus:
                    if occupancyStatus == '3':
                        customer_address_previous_residence += '''<CustomerAddressPreviousResidence fromDate="2008-03-30"  toDate="2008-10-30" refkeyAddress="X">
								<CustomerReference refkeyCustomer="N"/>
									<AddressOccupancyPartialOwnerOccupied refkeyAsset="A">
										<RentalDetails annualGrossRentalIncome="0"/>
									</AddressOccupancyPartialOwnerOccupied>
                                                            </CustomerAddressPreviousResidence> '''


                        application_address_canada_x += '''<ApplicationAddressCanada cityTown="- " countryCode="1" key="X" postalCode="V2A1A5" provinceCode="10">
							     <PostalAddressStreetAddress POBoxRRNumber="" streetDirection="-1" streetName="STREET" streetNumber="0" streetType="-1" unitNumber="0"/>
							</ApplicationAddressCanada>'''

                      

                        unearnedIncomeAmount = float(1000.11)
                        customer_borrower_n += '''<CustomerBorrower  dateBirth="1995-12-01" emailAddress1="ashish.raturi.erpincloud@gmail.com" firstName="Sunil" honorific="1" key="N" lastName="Sharma" maritalStatus="1" numberOfDependents="0">
						 	<EmploymentList>
								<Employment companyName="XYZ Pvt" dateStart="2008-03-30" employmentStatus="10" employmentType="7" industryType="99" jobTitle="Mrrr">
									<EarnedIncomeList>
										<EarnedIncome earnedIncomeAmount="1.12" earnedIncomeType="99" paymentFrequency="12"/>
									</EarnedIncomeList>
								</Employment>
							</EmploymentList>
							<UnearnedIncomeList>
								<UnearnedIncome paymentFrequency="12" unearnedIncomeAmount="%s" unearnedIncomeType="3"/>
							</UnearnedIncomeList>
						</CustomerBorrower>'''%(unearnedIncomeAmount)


                        asset_real_estate_a += '''<AssetRealEstate key="A" value="10.00"/>'''





                if propertyTaxes:
                    annualTaxAmount = str(propertyTaxes)
                    annualTaxAmount = annualTaxAmount.replace(",", "")
                    
                
                heat_dict = {'1':'2','2':'1','3':'3','4':'4'}
                sewage_dict = {'1':'10','2':'20','3':'30','4':'99'}
                property_type_dict = {'1':'7','2':'3','3':'5','4':'6','5':'7','6':'12'}
                water_supply_dict = {'1':'10','2':'20','3':'99'}

                water_supply = '99'
                if waterSupplyType in water_supply_dict.keys():
                    water_supply = water_supply_dict[waterSupplyType]

                heat_type = '4'
                if heatingType in heat_dict.keys():
                    heat_type = heat_dict[heatingType]
                

                sewage_type = '99'
                if sewageType in sewage_dict.keys():
                    sewage_type = sewage_dict[sewageType]
                

                property_type = '99'
                if propertyType in property_type_dict.keys():
                    property_type = property_type_dict[propertyType]
                

                garage_size = 7
                if garageSize:
                    garage_size_dict = {}
                    if garageType == "1":
                        garage_size_dict = {'1':'1','2':'3','3':'5','4':'7'}
                        if garageSize in garage_size_dict.keys():
                            garage_size = garage_size_dict[garageSize]
                

                    elif garageType == "2":
                        garage_size_dict = {'1':'2','2':'4','3':'6','4':'7'}
                        if garageSize in garage_size_dict.keys():
                            garage_size = garage_size_dict[garageSize]
                

                    elif garageType == "3":
                        garage_size = "7"

                subject_property_tag += ''' <SubjectProperty  parkingType="%s" yearBuilt="1999" propertyDescriptionType="%s"  heatingType="%s" waterSupplyType="%s" waterWasteType="%s" MLSNumber="%s" propertySize="%s">
						<SubjectPropertyOccupancyOwnerOccupied/>

						<LegalAddress details="None" levelNumber="0000" lotNumber="%s" PIN="%s" planNumber="%s" unitNumber="0000"/>

                                                <Condo annualCondoFees="%s"/>

                                                <PropertyTax annualTaxAmount="%s"/>
						<PropertyAppraisal/>
						<SubjectPropertyAddress refkeyAddress="MainCurrentAddKey2"/>
					    </SubjectProperty> '''%(garage_size,property_type,heat_type,water_supply,sewage_type,MLSNumber,square_footage,lotNumber,pin,planNumber,annualCondoFees,annualTaxAmount)
                    
                ####UnearnedIncomeList
                #unearnedIncomeAmount =  applicant_obj.browse(cr,uid,applicant_rec.id).monthlychildsupport or '0000'
                unearnedIncomeAmount = float('888')
                if unearnedIncomeAmount:
                    print "unearnedIncomeAmount>>>>>",unearnedIncomeAmount
                    
                    #print "unearnedIncomeAmount>>>>>",type(unearnedIncomeAmount)
                    
                    unearned_income_list += '''<UnearnedIncomeList>
						    <UnearnedIncome unearnedIncomeAmount="%s" unearnedIncomeType="3" paymentFrequency="12"/>
				           </UnearnedIncomeList>'''%(unearnedIncomeAmount)
                print "asset_real_estate_a###",asset_real_estate_a
                print "customer_borrower_n###",customer_borrower_n
                print "application_address_canada_x###",application_address_canada_x
                print "customer_address_previous_residence###",customer_address_previous_residence

                
                morweb_request = morweb_request % {'asset_tag':asset_tag,
                                                    'customer_asset_other':customer_asset_other,
                                                    'employment_tag':employment_tag,
                                                    'subject_property_tag':subject_property_tag,
                                                    'unearned_income_list':unearned_income_list,
                                                    'asset_real_estate_a':asset_real_estate_a,
                                                    'customer_borrower_n':customer_borrower_n,
                                                    'application_address_canada_x':application_address_canada_x,
                                                    'customer_address_previous_residence':customer_address_previous_residence,
                                                    }

                indexEOD_start = morweb_request.find('<<<EOD')
                indexEOD_end = morweb_request.find('EOD;')
                xml = str(morweb_request[indexEOD_start+6:indexEOD_end])
                customer_borrower = self.xml_parse(cr,uid,ids,xml,{'applicant_id':applicant_rec.id,'tag_name':['CustomerBorrower','ApplicationAddressCanada','Employment','SubjectProperty','PropertyTax','Loan','MortgageApplication','LegalAddress','Condo']})
                xml_srtindx = customer_borrower.find('<?xml')
                xml_endindx = customer_borrower.find('?>')
                cus_borro = customer_borrower.replace(customer_borrower[xml_srtindx:xml_endindx+2],'<<<EOD')
                print "morweb_request",morweb_request
                php_code = morweb_request.replace(morweb_request[indexEOD_start:indexEOD_end], str(cus_borro))
                print "**************************",php_code
                
                php_file_path =  ADDONS_PATH + "/syml/phptest.php"
                fp = open(php_file_path, 'w+b')
                #os.chmod('php_file_path', st.st_mode | stat.S_IEXEC)
                #os.chmod(php_file_path, 0777)
                #os.system('chmod 755' + ' ' + php_file_path)
                fp.truncate()
                fp.write(php_code)
                fp.close()

                # if you want output
                #proc = subprocess.Popen("php /opt/lampp/htdocs/syml/phptest.php", shell=True, stdout=subprocess.PIPE) #stdout=subprocess.PIPE >>>> to get the value in proc otherwise it stores blank value.
                proc = subprocess.Popen("php " + php_file_path, shell=True, stdout=subprocess.PIPE) #stdout=subprocess.PIPE >>>> to get the value in proc otherwise it stores blank value.                
                script_response = proc.stdout.read()
                
                script_response = str.replace(script_response, "&gt;", ">")
                script_response = str.replace(script_response, "&lt;", "<")
                #print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
                print "script_response==>>>>>>>",script_response

                
                script_reponse_start = script_response.find('<ProcessRequestResponse')
                script_reponse_end = script_response.find('</soap:Body>')
                
                script_response = script_response[script_reponse_start:script_reponse_end]
                script_response = str.replace(script_response, "&quot;", '"')
                print "script_response>>>>>>>>",script_response
        



    def send_morweb_request_test(self,cr,uid,ids,context=None):
        applicant_obj = self.pool.get('applicant.record')
        crm_asset_obj = self.pool.get('crm.asset')
        
        crm_browse = self.browse(cr,uid,ids[0])
        morweb_request = crm_browse.company_id.morweb_request
        #applicant_list = crm_browse.applicant_record_line
        applicant_list_arr = crm_browse.app_rec_ids
        applicant_list = crm_browse.app_rec_ids
            
        print "applicant_list>>>",applicant_list
        

        i = j = 0

        address = ''
        customer_address_primary_residence = customer_borrower = asset_other = customer_asset_other = subject_property_tag = ''
        rel_status_dict = {'Single':'1','Married':'2','Widowed':'3','Separated':'4','Divorced':'5','Common-Law':'6','Other':'99'}
        province_dict = {'ON':50,'QC':60,'NS':80,'NB':70,'MB':40,'BC':10,'PE':100,'SK':30,'AB':20,'NL':90,'Other':99999}
        type_dict = {'Bank Account':'10','Insurance Policy':'20','RRSPs':'30','Vehicle':'40','Investments':'60','Other':'99'}
        if morweb_request:
            ##Subject Property
            heat_dict = {'1':'2','2':'1','3':'3','4':'4'}
            sewage_dict = {'1':'10','2':'20','3':'30','4':'99'}
            property_type_dict = {'1':'7','2':'3','3':'5','4':'6','5':'7','6':'12'}
            water_supply_dict = {'1':'10','2':'20','3':'99'}

            waterSupplyType = crm_browse.water or ''
            propertyTaxes = crm_browse.property_taxes or ''
            propertyType = crm_browse.property_type or ''
            heatingType = crm_browse.heating or ''
            sewageType = crm_browse.sewage or ''
            garageType = crm_browse.garage_type or ''
            garageSize = crm_browse.garage_size or ''
            MLSNumber = crm_browse.mls or '0000'
            square_footage = crm_browse.square_footage or '0000'
            #OccupancyCode = crm_browse.living_in_property or ''

            planNumber = crm_browse.plan or '0000'
            lotNumber = crm_browse.lot or '0000'
            pin = crm_browse.block or '0000'

            annualCondoFees = crm_browse.condo_fees or '0000'

            annualTaxAmount = crm_browse.property_taxes or '0000'
            occupancyStatus = crm_browse.living_in_property


            water_supply = '99'
            if waterSupplyType in water_supply_dict.keys():
                water_supply = water_supply_dict[waterSupplyType]

            heat_type = '4'
            if heatingType in heat_dict.keys():
                heat_type = heat_dict[heatingType]


            sewage_type = '99'
            if sewageType in sewage_dict.keys():
                sewage_type = sewage_dict[sewageType]


            property_type = '99'
            if propertyType in property_type_dict.keys():
                property_type = property_type_dict[propertyType]


            garage_size = 7
            if garageSize:
                garage_size_dict = {}
                if garageType == "1":
                    garage_size_dict = {'1':'1','2':'3','3':'5','4':'7'}
                    if garageSize in garage_size_dict.keys():
                        garage_size = garage_size_dict[garageSize]


                elif garageType == "2":
                    garage_size_dict = {'1':'2','2':'4','3':'6','4':'7'}
                    if garageSize in garage_size_dict.keys():
                        garage_size = garage_size_dict[garageSize]


                elif garageType == "3":
                    garage_size = "7"



            
            subject_property_tag += ''' <SubjectProperty  parkingType="%s" yearBuilt="1999" propertyDescriptionType="%s"  heatingType="%s" waterSupplyType="%s" waterWasteType="%s" MLSNumber="%s">
                                            <SubjectPropertyOccupancyOwnerOccupied/>

                                            <LegalAddress details="None" levelNumber="0000" lotNumber="%s" PIN="%s" planNumber="%s" unitNumber="0000"/>

                                            <Condo annualCondoFees="%s"/>

                                            <PropertyTax annualTaxAmount="%s"/>
                                            <PropertyAppraisal/>
                                            <SubjectPropertyAddress refkeyAddress="MainCurrentAddKey2"/>
                                        </SubjectProperty> '''%(garage_size,property_type,heat_type,water_supply,sewage_type,MLSNumber, lotNumber,pin,planNumber,annualCondoFees,annualTaxAmount)



            
            #print "subject_property_tag>>>>>>>>>>>>>",subject_property_tag
            
            for applicant_rec in applicant_list:
                if applicant_rec:
                    print "applicant_rec>>>",applicant_rec
                    if applicant_rec.address_ids:
                        address_ids = applicant_rec.address_ids
                        applicant_id = applicant_rec.id
                        flag = 0
                        for address_ids in applicant_rec.address_ids:
                            i = i + 1

                            provinceCode = ''
                            if address_ids.province and province_dict.has_key(address_ids.province):
                                provinceCode = province_dict[address_ids.province]
                            else:
                                provinceCode = province_dict['Other']
                            if address_ids.postal_code:
                                postalCode = address_ids.postal_code
                            else:
                                raise osv.except_osv(('Error'),('Postal Code Not Found....'))
                            print "provinceCode>>>>>>>>>>",provinceCode
                            address += '''<ApplicationAddressCanada key="%s" cityTown="%s" provinceCode="%s" postalCode="%s" countryCode="1">
                                                <PostalAddressStreetAddress unitNumber="0" streetNumber="0" streetName="%s" streetType="-1" streetDirection="-1" POBoxRRNumber=""/>
                                          </ApplicationAddressCanada>'''%('MainCurrentAddKey%s'%(i),address_ids.name,provinceCode,postalCode,address_ids.name)





                            if i == 1:
                                customer_address_primary_residence = customer_address_primary_residence + '''<CustomerAddressPrimaryResidence fromDate="2008-03-30" refkeyAddress="%s">
                                                                       '''%('MainCurrentAddKey%s'%(i))






                            if flag == 0:
                                customer_address_primary_residence = customer_address_primary_residence + '''<CustomerReference refkeyCustomer="%s"/>'''%('MainCustomerKey%s'%(i))
                                applicant_browse = applicant_obj.browse(cr,uid,applicant_id)
                                name = applicant_browse.applicant_name or ''
                                last_name = applicant_browse.applicant_last_name or ''
                                email = applicant_browse.email_personal or ''
                                relationship_status = applicant_browse.relationship_status or ''
                                date_birth = applicant_browse.dob or ''
                                sin = applicant_browse.sin or ''

                                if relationship_status in rel_status_dict.keys():
                                    status = rel_status_dict[relationship_status]
                                else:
                                    status = rel_status_dict['Other']

                                customer_borrower = customer_borrower + '''<CustomerBorrower key="%s" dateBirth="%s" lastName="%s" firstName="%s" emailAddress1="%s" maritalStatus="%s" numberOfDependents="0">
                                                                                <EmploymentList>
                                                                                    <Employment employmentType="1" employmentStatus="10" dateStart="2008-03-30" jobTitle="Commercial Technician / Installer" companyName="Chubb Security">
                                                                                        <EarnedIncomeList>
                                                                                            <EarnedIncome earnedIncomeType="1" paymentFrequency="12" earnedIncomeAmount="4145.00"/>
                                                                                        </EarnedIncomeList>
                                                                                    </Employment>
                                                                                </EmploymentList>
                                                                         </CustomerBorrower>'''%('MainCustomerKey%s'%(i),date_birth,last_name,name,email,status)



                                ##<CustomerAssetOther> this tag will come inside the loop
                                asset_ids = crm_asset_obj.search(cr,uid,[('opportunity_id','=',applicant_id)])
                                if asset_ids:
                                    for asset in asset_ids:
                                        j = j + 1
                                        print "asset>>>>>>>>>",asset
                                        crm_data = crm_asset_obj.browse(cr,uid,asset)
                                        print "crm_data>>>>>>",crm_data.name
                                        if type_dict.has_key(crm_data.asset_type):
                                            asset_type = crm_data.asset_type
                                        else:
                                            asset_type = 'Other'
                                        value = crm_data.value or 0
                                        print "asset_type>>>>",type_dict['Other']
                                        customer_asset_other = customer_asset_other + '''<CustomerAssetOther refkeyAsset="%s">
                                                                                    <CustomerReference refkeyCustomer="%s"/>
                                                                                  </CustomerAssetOther>'''%('AssetSavingkey%s'%(j),'MainCustomerKey%s'%(i))
                                        asset_other = asset_other + '''<AssetOther key="%s" value="%s" assetType="%s" description="%s"/>'''%('AssetSavingkey%s'%(j),value,type_dict[asset_type],crm_data.name)

                                #else:
                                   # raise osv.except_osv(('Error'),('Applicant Assests not defined....!!!'))
                                #print "customer_borrower>>",customer_borrower



                            flag = flag + 1

                else:
                    raise  osv.except_osv(('Error'),('Applicant Address not defined....!!!'))
            
            print "customer_borrower:::::",customer_borrower
            print "customer_address_primary_residence:::",customer_address_primary_residence
            
            customer_address_primary_residence =   customer_address_primary_residence +  '''<AddressOccupancyOwnerOccupied refkeyAsset= "%s"/>
                                        </CustomerAddressPrimaryResidence>'''%('AssetPrimaryRealEstate1')
            #print "customer_address_primary_residence:::",customer_address_primary_residence
            
            indexEOD_start = morweb_request.find('<<<EOD')
            indexEOD_end = morweb_request.find('EOD;')
            xml = str(morweb_request[indexEOD_start:indexEOD_end])
            xml = xml % {'address':address,
                         'customer_borrower':customer_borrower,
                         'customer_address_primary_residence':customer_address_primary_residence,
                         'asset_other':asset_other,
                         'customer_asset_other':customer_asset_other,
                         'subject_property_tag':subject_property_tag
                         }
            print "xmmmmmmmmmmmmm>>>>",xml
        
            
#            xml = parseString(xml)
            #customer_borrower = self.xml_parse(cr,uid,ids,xml,{'applicant_id':applicant_rec.id,'tag_name':['CustomerBorrower','ApplicationAddressCanada','Employment','SubjectProperty','PropertyTax','Loan','MortgageApplication','LegalAddress','Condo']})
#            xml_srtindx = xml.find('<?xml')
#            xml_endindx = xml.find('?>')
#            print "xml_srtindx>>>",xml_srtindx
#            print "xml_endindx>>>",xml_endindx
#            cus_borro = xml.replace(xml[xml_srtindx:xml_endindx+2],'<<<EOD')
#            print "cus_borro>>>>",cus_borro
#            dfg
            #print "morweb_request",morweb_request
            php_code = morweb_request.replace(morweb_request[indexEOD_start:indexEOD_end], str(xml))
            print "ADDONS_PATH>>>>>>>>>",ADDONS_PATH
            php_file_path =  ADDONS_PATH + "/syml/phptest.php"
            #php_file_path = "/home/dikshitha/syml/openerp/addons/syml/phptest.php"
            print "php_file_path>>>>>>>>>",php_file_path
            fp = open(php_file_path, 'w+b')
            fp.truncate()
            fp.write(php_code)
            fp.close()
            proc = subprocess.Popen("php"+ " " + php_file_path, shell=True, stdout=subprocess.PIPE) #stdout=subprocess.PIPE >>>> to get the value in proc otherwise it stores blank value.
            script_response = proc.stdout.read()
            print "script_response1>>>>",script_response
            
            
            script_response = str.replace(script_response, "&gt;", ">")
            script_response = str.replace(script_response, "&lt;", "<")

            if script_response.find('<ProcessRequestResponse'):
                script_reponse_start = script_response.find('<ProcessRequestResponse')
                script_reponse_end = script_response.find('</ProcessRequestResponse>')
                print "script_response2>>>>",script_response
            
                script_response = script_response[script_reponse_start:script_reponse_end]
                print "script_response3>>>>>",script_response
                script_response = str.replace(script_response, "&quot;", '"')
                print "script_response4>>>>>>>>",script_response + " </ProcessRequestResponse>"
            
                script_response = script_response + " </ProcessRequestResponse>"
                responseDOM1 = parseString(script_response)
                if responseDOM1.getElementsByTagName('BDIResponse'):
                    bdiResponse = responseDOM1.getElementsByTagName('BDIResponse')
                    print "bdiResponse>>>>",bdiResponse
                    bdiStatus = bdiResponse[0].attributes['status'].value
                    mortgageApplication = responseDOM1.getElementsByTagName('MortgageApplication')
                    applicationnumber = mortgageApplication[0].attributes['applicationNumber'].value
                    print "appppppppppppp:",applicationnumber
                    if applicationnumber:
                        self.write(cr,uid,ids,{'application_no':applicationnumber,})
          

        return True





                 
    
crm_lead()
