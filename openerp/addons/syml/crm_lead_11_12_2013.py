
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

#from elementtree.ElementTree import XML, SubElement, Element, tostring
#import xml.etree.ElementTree as ET
#import sys

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
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
        'realtor' : fields.many2one('res.partner','Realtor', track_visibility='onchange'),
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
        'term_rate':fields.selection([('term', 'Term'),],''),   
        'op_info_type':fields.selection([('p_approve', 'Pre_Approval'),('mortagage', 'Mortagage Roval'),],''),   
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

    }
    _defaults = {
        'preferred_number': 'cell',
    }

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
    
    def sendmail(self,cr,uid,ids,template_title,res_id):
        email_template_obj = self.pool.get('email.template')        
        cr.execute('SELECT id FROM email_template WHERE "name" ilike %s',('%'+template_title+'%',) )
        cr.commit()
        template_details = cr.dictfetchall()
        if not template_details:
            raise osv.except_osv(('Template Not Found'),('The selected template "'+template_title+'" is not configured')) 
        template_id = template_details[0]['id'] 
        print "template_details======",template_details
#        print "email_from===============",template_id.id.email_from
#        print "email_to====",template_id.email_to
        message_id = email_template_obj.send_mail(cr, uid, template_id, res_id, force_send=True, context=None)         
        print "=======================message sent successfully=========================="
        return True
#        cr.execute('SELECT state FROM mail_message WHERE id = %s',(message_id,) )
#        cr.commit()
#        message_details = cr.dictfetchall()
#        message_state = message_details[0]['state']
#        if message_state == "exception": 
#            raise osv.except_osv(('Missing SMTP Server'),('Please define at least one SMTP server, or provide the SMTP parameters explicitly')) 
#        else:
#            return True 
    
    
    def write(self, cr, uid, ids, vals, context=None):         
        if vals.has_key('stage_id'):
            if vals['stage_id'] != False:
                print "inside stage id if statementtttttttt#######################"
                cr.execute('select id from crm_case_stage where id = %s and "name" ilike %s',(vals['stage_id'],'pending application',))
                stage_id = cr.fetchone()
                print "stage_id=========",stage_id
                if stage_id:                
                    self.sendmail(cr,uid,ids,'pending_lead',ids[0])
        res = super(crm_lead, self).write(cr, uid, ids, vals)
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


    def xml_parse(self,cr,uid,xml,context):
        applicant_obj = self.pool.get('applicant.record')
        applicant_address_obj = self.pool.get('applicant.address')
        responseDOM = parseString(xml)        
        tag_list = context.get('tag_name')
        applicant_id = context.get('applicant_id')
        print "applicant_id>>>",applicant_id
        print "tag_list>>>",tag_list
        address_ids = applicant_address_obj.search(cr, uid, [('applicant_id','=',applicant_id)])
        print "address_ids >>>>",address_ids

        for i in range(0,len(tag_list)):
            if tag_list[i] == 'CustomerBorrower':
                browse_record = applicant_obj.browse(cr,uid,applicant_id)                
                name = browse_record.applicant_name or ''
                last_name = browse_record.applicant_last_name or ''
                email = browse_record.email_personal or ''
                relationship_status = browse_record.relationship_status or ''
                sin = browse_record.sin or ''
                print "details###########",name,last_name,email,relationship_status,sin

                if relationship_status == 'Single':
                    status = '1'
                elif relationship_status == 'Married':
                    status = '2'
                elif relationship_status == 'Common-Law':
                    status = '3'
                elif relationship_status == 'Divorced':
                    status = '4'
                elif relationship_status == 'Separated':
                    status = '5'
                CustomerBorrower = responseDOM.getElementsByTagName(tag_list[i])
                CustomerBorrower[0].setAttribute('firstName', name)
                CustomerBorrower[0].setAttribute('lastName', last_name)
                CustomerBorrower[0].setAttribute('emailAddress1', email)
                CustomerBorrower[0].setAttribute('maritalStatus', '1')

#            elif tag_list[i] == 'ApplicationAddressCanada':
#                if address_ids:
#                    applcntaddress = responseDOM.getElementsByTagName(tag_list[i])
#                    print "applcntaddress>>>>>>>>>>>>>",applcntaddress[0].toprettyxml()
#                    applcntaddress[0].setAttribute('cityTown', name)
#                    applcntaddress[0].setAttribute('countryCode', name)
#                    applcntaddress[0].setAttribute('postalCode', name)
#                    applcntaddress[0].setAttribute('provinceCode', name)
#                    applcntaddress[0].setAttribute('POBoxRRNumber', name)
#                    applcntaddress[0].setAttribute('streetDirection', "1")
#                    applcntaddress[0].setAttribute('streetName', name)
#                    applcntaddress[0].setAttribute('streetNumber', "0")
#                    applcntaddress[0].setAttribute('streetType', "-1")
#                    applcntaddress[0].setAttribute('unitNumber', "0")
#
#                    print "applcntaddress>>>>>>>>>>>>>",applcntaddress[1].toprettyxml()
#                    applcntaddress[1].setAttribute('cityTown', name)
#                    applcntaddress[1].setAttribute('countryCode', name)
#                    applcntaddress[1].setAttribute('postalCode', name)
#                    applcntaddress[1].setAttribute('provinceCode', name)
#                    applcntaddress[1].setAttribute('POBoxRRNumber', name)
#                    applcntaddress[1].setAttribute('streetDirection', "1")
#                    applcntaddress[1].setAttribute('streetName', name)
#                    applcntaddress[1].setAttribute('streetNumber', "0")
#                    applcntaddress[1].setAttribute('streetType', "-1")
#                    applcntaddress[1].setAttribute('unitNumber', "0")
#
#                    print "applcntaddress>>>>>>>>>>>>>",applcntaddress[2].toprettyxml()
#                    applcntaddress[2].setAttribute('cityTown', name)
#                    applcntaddress[2].setAttribute('countryCode', name)
#                    applcntaddress[2].setAttribute('postalCode', name)
#                    applcntaddress[2].setAttribute('provinceCode', name)
#                    applcntaddress[2].setAttribute('POBoxRRNumber', name)
#                    applcntaddress[2].setAttribute('streetDirection', "1")
#                    applcntaddress[2].setAttribute('streetName', name)
#                    applcntaddress[2].setAttribute('streetNumber', "0")
#                    applcntaddress[2].setAttribute('streetType', "-1")
#                    applcntaddress[2].setAttribute('unitNumber', "0")
#
        return responseDOM.toprettyxml()

        
    def send_morweb_request(self,cr,uid,ids,context=None):        
        morweb_request = self.browse(cr,uid,ids[0]).company_id.morweb_request
        
        applicant_obj = self.pool.get('applicant.record')
        applicant_list = self.browse(cr,uid,ids[0]).applicant_record_line
        if morweb_request:
            for applicant_rec in applicant_list:
                indexEOD_start = morweb_request.find('<<<EOD')
                indexEOD_end = morweb_request.find('EOD;')
                #print "data////////: ",morweb_request[indexEOD_start:indexEOD_end]
                xml = str(morweb_request[indexEOD_start+6:indexEOD_end])
                customer_borrower = self.xml_parse(cr,uid,xml,{'applicant_id':applicant_rec.id,'tag_name':['CustomerBorrower','ApplicationAddressCanada','PostalAddressStreetAddress']})
#                print "customer_borrower#########",customer_borrower
                
                xml_srtindx = customer_borrower.find('<?xml')
                xml_endindx = customer_borrower.find('?>')
                print "start index: ",xml_srtindx
                print "end index: ",xml_endindx
                cus_borro = customer_borrower.replace(customer_borrower[xml_srtindx:xml_endindx+2],'<<<EOD')

                php_code = morweb_request.replace(morweb_request[indexEOD_start:indexEOD_end], str(cus_borro))          
                
                php_file_path =  ADDONS_PATH + "/syml/phptest.php"
                fp = open(php_file_path, 'w+b')
                fp.truncate()
                fp.write(php_code)
                fp.close()
                proc = subprocess.Popen("php " + php_file_path, shell=True, stdout=subprocess.PIPE) #stdout=subprocess.PIPE >>>> to get the value in proc otherwise it stores blank value.                
                script_response = proc.stdout.read()
                print "script_response==",script_response
                
                indexno = script_response.find('applicationNumber')
                print "indexno&&&&&&&&&&&&&&&",indexno
                startindx =  indexno + 24
                print "start index",startindx
                temp_application = script_response[startindx:len(script_response)]
                applicationnumber = ''
                for appNo in temp_application:
                    if appNo == '&':
                        break
                    else:
                        applicationnumber = applicationnumber + appNo
                        print applicationnumber
                if  applicationnumber:
                    print "application no:",applicationnumber
                    self.write(cr,uid,ids,{'application_no':applicationnumber,})
        else:
            raise osv.except_osv(('MorWEB Request Script not found !!'),(''))
        return True
    
crm_lead()