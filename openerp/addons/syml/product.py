from osv import fields,osv
import datetime
from base_status.base_stage import base_stage
import tools
from tools.translate import _
from tools import html2plaintext
import urllib
import urllib2
from httplib2 import Http
from urllib import urlencode
import json
import requests

class product_product(osv.osv):
    _inherit = 'product.product'
    
    _columns = {

        # created on 2013-09-13 

        #'mortgage_type': fields.many2one('crm.case.categ','Mortgage Type'), #Discussion
        'mortgage_type': fields.selection([('1','LOC'),('2','Variable'),('3','Fixed'),('4','Cashback'),('5','Combined'),('','')],'Mortgage Type'),
        'lender':fields.many2one('res.partner','Lender'),
	'product_name':fields.char('Product',size=120),
        'interest_rate': fields.float('Interest Rate',),
        'qualifying_rate': fields.float('Qualifying Rate',),
	'posted_rate':fields.float('Posted Rate'),
#        'term':fields.many2one('product.term','Term'),
        'term':fields.selection([('1','6 Months'),('2','1 Year'),('3','2 Year'),('4','3 Year'),('5','4 Year'),('6','5 Year'),('7','6 Year'),('8','7 Year'),('9','8 Year'),('10','9 Year'),('11','10 Year')],'Term'),
	'quick_close_duration':fields.integer('Quick Close Duration'),
        'mortgage_amount':fields.integer('Mortgage Amount'),
        'mortgage_payment':fields.integer('Payment'),
        'cashback':fields.float('Cashback'),
	'position':fields.char('Position',size=40),
        'maximum_amortization': fields.integer('Maximum Amortization',),
        'loc_qualifying_rate': fields.selection([('1', 'Not LOC'), ('2', 'Qualifying Rate'),
            ('3', 'Product Rate')], 'LOC Qualifying Rate'), #Discussion
        ##'is_diff_length':fields.boolean('Is Differential Length'),
        'weekly_payments':fields.boolean('Weekly Payments'),
        'bi_weekly_payments':fields.boolean('Bi-Weekly Payments'),
        'semi_monthly_payments':fields.boolean('Semi Monthly Payments'),
        'monthly_payments':fields.boolean('Monthly Payments'),
        'increase_payments':fields.boolean('Increase Payment'),
        'double_up_payments':fields.boolean('Double Up Payments'),
        'extra_annual_paydown':fields.boolean('Extra Annual Paydown'),
        'extra_applied_any_time':fields.boolean('Extra Applied Any Time'),
        'skip_payment_possible':fields.boolean('Skip Payment Possible'),
        'prepay_to_reduce':fields.boolean('Prepay to reduce Penalty'),
        'reward_points':fields.boolean('Reward Points'),
        'outstanding_collection_payment':fields.boolean('Outstanding Collection Payment'),
#        'is_penalty_greater':fields.boolean('Penalty Is Greater of'),
        'months_interest_penalty': fields.integer('Months Interest Penalty',),
#        'avg_diff_used': fields.float('Avg Differential Used',),
#        'diff_length': fields.selection([('0-5', '0-5'), ('6-10', '6-10'), 
#            ('11-15', '11-15'),('16-20','16-20')], 'Differential Length'), #Discussion
        'waive_penalty_if_retain':fields.boolean('Waive Penalty if Retain'),
        'closing_period':fields.integer('Closed Period (Months)'),
        'avg_processing_speed': fields.float('Avg Processing Speed (Hours)',),
        'business_ease': fields.float('Business Ease 1-10',),
        'underwriter_pref': fields.float('Underwriter Pref 1-10'),
        'application_method': fields.selection([('1', 'Morweb'), ('2', 'Filelogix')], 'Application Method'),
        'base_commission': fields.float('Base Commission (Basis Pts)',),
        'marketing_commission': fields.float('Marketing Commission',),
        'trailer_commission': fields.float('Trailer Commission',),
        'vol_bonus_1': fields.float('Volume Bonus Level 1',),
        'vol_bonus_1_threshold': fields.float('Volume Bonus 1 Threshold',),
        'vol_bonus_2': fields.float('Volume Bonus Level 2',),
        'vol_bonus_2_threshold': fields.float('Volume Bonus 2 Threshold',),
        'vol_bonus_3': fields.float('Volume Bonus Level 3',),
        'vol_bonus_3_threshold': fields.float('Volume Bonus 3 Threshold',),
        'vol_bonus_4': fields.float('Volume Bonus Level 4',),
        'vol_bonus_4_threshold': fields.float('Volume Bonus 4 Threshold',),
        'vol_bonus_5': fields.float('Volume Bonus Level 5',),
        'vol_bonus_5_threshold': fields.float('Volume Bonus 5 Threshold',),

        'beacon_tds_split': fields.float('Beacon TDS Split',),
        'beacon_tds_cut_off': fields.float('Beacon TDS Cut Off',),
        'min_beacon': fields.float('Min Beacon',),
        'min_beacon_cut_off': fields.float('Min Beacon Cut Off',),
        'equifax_scoring_used':fields.selection([('1', 'Beacon5'), ('2', 'Beacon9'),('3','CRP3'),('4','ERS2')],'Equifax Scoring Used'),
        #'rules_method':fields.selection([('1', 'Rules Method'), ('2', 'Rules Method'),('3','Rules Method')],'Rules Method'),
        'whose_income_used': fields.selection([('1', 'Highest'), ('2', 'Lowest'),('3',' Averaged'),('4','IncomeWeightAvg')],'Whose Beacon Used'),
        'good_credit_beacon_split':fields.integer('Good Credit >= Beacon Split'),
        'good_credit_12_mo_lates':fields.integer('Good Credit <= 12 Mo Lates'),
        'maximum_applicants':fields.float('Maximum Applicants'),
        'poor_credit_beacon_split':fields.float('Poor Credit < Beacon Split'),
        'poor_credit_12_mo_lates':fields.float('Poor Credit > 12 Mo Lates'),
        'mths_from_discharge_allowable': fields.float('Mths From Discharge Allowable',),
        'active_credit_trades_required': fields.float('Active Credit Trades Required',),

        'great_tds_greater_equal_split': fields.float('Max TDS % >= Split',),
        'great_tds_less_split': fields.float('Max TDS % < Split',),
        'great_gds_greater_equal_split': fields.float('Max GDS %  >= Split',),
        'great_gds_less_split': fields.float('Max GDS %  < Split',),

        'med_tds_greater_equal_split': fields.float('Max TDS % >= Split',),
        'med_tds_less_split': fields.float('Max TDS % < Split',),
        'med_gds_greater_equal_split': fields.float('Max GDS %  >= Split',),
        'med_gds_less_split': fields.float('Max GDS %  < Split',),

        'poor_tds_greater_equal_split': fields.float('Max TDS % >= Split',),
        'poor_tds_less_split': fields.float('Max TDS % < Split',),
        'poor_gds_greater_equal_split': fields.float('Max GDS %  >= Split',),
        'poor_gds_less_split': fields.float('Max GDS %  < Split',),

        'letter_of_employment':fields.boolean('Letter of Employment'),
        'pay_stub_prorate':fields.boolean('Pay-Stub Prorate'),
        '2_yr_average_noa':fields.boolean('2 Yr Average NOA'),
        'last_yr_noa':fields.boolean('Last  Yr NOA'),

        '2_yr_avg_noa':fields.boolean('2 Yr Average NOA'),
        '2_yr_avg_noa_percent':fields.boolean('2 Yr Average NOA + 15%'),
        'se_grossup_percent':fields.float('S/E Gross Percentage'),
        'last_yr_noa':fields.boolean('Last Yr NOA'),
        't1_general_formula':fields.boolean('T1 General Formula'),

        'rental_income_percent':fields.float('Rental Income % Included'),
        'rental_income_treatment':fields.selection([('1','Add To Income'),('2','Subtract From Liabilites')],'Rental Income Treatment'),
        'small_center_insure_ltv':fields.float('Small Center Insure LTV'),
        'rental_2_yr_avg_noa':fields.boolean('2 Yr Average NOA'),
        'rental_last_yr_noa':fields.boolean('Last Yr NOA'),

        'revolving_debt_payments':fields.selection([('1','Three Percent Balance'),('2','Three Percent Limit'),('3','Stated Minimum')],'Revolving Debt Payments'),
        'remove_loan_mo_remaining':fields.float('Remove Loan Mo Remaining'),
        'remove_loans_done_pre_close':fields.boolean('Remove Loans done pre-close'),
        'child_support_treatment':fields.selection([('1','Add To Liabilities'),('2','Subtract From Income')],'Child Support Treatment'),
        'child_tax_credit':fields.float('Child Tax Credit % Allowed'),
        'living_allowance':fields.float('Living Allowance % Allowed'),
        'vehicle_allowance':fields.float('Vehicle Allowance % Allowed'),

        'allowed_on_1st':fields.boolean('Allowed on 1st'),
        'allowed_on_2nd':fields.boolean('Allowed on 2nd'),
        'charges_allowed_behind':fields.boolean('Charges Allowed Behind'),
        'allowed_on_3rd':fields.boolean('Allowed on 3rd'),
        'allowed_on_bridge':fields.boolean('Allowed on Bridge'),
        'specific_lenders_on_1st':fields.boolean('Specific Lenders on 1st'),


        'vtb_max_ltv':fields.float('VTB Max LTV'),
#        'min_allowed_charge':fields.selection([('0-5', '0-5'), ('6-10', '6-10'),
#            ('11-15', '11-15'),('16-20','16-20')], 'Min Allowed Charge'),
#        'max_loan_to_value':fields.float('Maximum Loan To Value'),


        'country_residential':fields.boolean('Country Residential'),
        'condo':fields.boolean('Condo'),
        'allow_agricultural_less_then_10_acres':fields.boolean('Agricultural < 10 Acres'),
        'agricultural':fields.boolean('Agricultural'),
        'commercial':fields.boolean('Commercial'),
        'fractional_interests':fields.boolean('Fractional Interests'),
        'co_operative_housing':fields.boolean('Co-operative Housing'),
        'grow_ops':fields.boolean('Grow Ops'),
        'rental_pools':fields.boolean('Rental Pools'),
        'age_restricted':fields.boolean('Age Restricted'),
        'allow_duplex':fields.boolean('Duplex'),
        'allow_four_plex':fields.boolean('Four - Plex'),
        'allow_six_plex':fields.boolean('Six - Plex'),
        'allow_eight_plex':fields.boolean('Eight - Plex'),
        'construction_product':fields.boolean('Construction Product'),
        'self_build_product':fields.boolean('Self-Build Product'),
        'min_sq_allow_condo':fields.integer('Min Sq Ft Allowed (Condo)'),
        'min_sq_cutoff_condo':fields.integer('Min Sq Ft CutOff (Condo)'),
        'min_sq_allow_house':fields.float('Min Sq Ft Allowed (House)'),
        'min_sq_cutoff_house':fields.integer('Min Sq Ft CutOff (House)'),
        'cottage_insure_ltv':fields.float('Cottage Insure LTV'),
        'cottage_max_ltv':fields.float('Cottage Maximum LTV'),
        'rental_maximum_ltv':fields.float('Rental Maximum LTV'),

        'life_leased_property':fields.boolean('Life Leased Property'),
        'leased_land':fields.boolean('Leased Land'),
        'mobile_homes':fields.boolean('Mobile Homes'),
        'modular_homes':fields.boolean('Modular Homes'),
        'floating_homes':fields.boolean('Floating Homes'),
        'boarding_houses':fields.boolean('Boarding Houses'),
        'rooming_houses':fields.boolean('Rooming Houses'),
        'non_conv_construction':fields.boolean('Non-Conv Construction'),
        'cottage_rec_property':fields.boolean('Cottage / Rec Property'),
        'rental_property':fields.boolean('Rental Property'),
        'allow_2nd_homes':fields.boolean('Allow 2nd Homes'),
        'high_ratio_2nd_home':fields.boolean('High Ratio 2nd Home'),
        'uninsured_conv_2nd_home':fields.boolean('Uninsured Conv 2nd Home'),
        'max_number_of_draws':fields.integer('Max # of Draws'),
        'outbuilding_included':fields.integer('% outbuilding included'),
        'age_restricted_ltv':fields.float('Age Restricted LTV'),
        'max_acreage_allowed':fields.float('Max Acreage Allowed'),
        'max_acreage_cutoff':fields.float('Max Acreage Cutoff'),
        'max_mortgage_allowed':fields.float('Max Mortgage Allowed'),
        'min_mortgage_allowed':fields.float('Min Mortgage Allowed'),
        'cottage_min_beacon':fields.float('Cottage Min Beacon'),

        'requir_distance_to_city':fields.float('Required Distance to City'),
        'allow_provinces':fields.text('Allowable Provinces'),
        'excl_or_incl_city':fields.selection([('1','Exclude'),('2','Include')],'Excluded or Included Cities'),
        'cities':fields.text('Cities'),

        'res_con_cutoff':fields.float('Residence Conventional CutOff'),
        'res_ltv_cutOff_grt':fields.float('Residence LTV % > CutOff'),
        'res_ltv_cutoff_les':fields.float('Residence LTV % <= CutOff'),
        'rental_con_cutOff':fields.float('Rental Conventional CutOff'),
        'rental_ltv_cutOff_grt':fields.float('Rental LTV % > CutOff'),
        'rental_ltv_cutOff_les':fields.float('Rental LTV % <= CutOff'),
        'is_product_insured':fields.boolean('Is Product Insured'),

        'sm_center_con_cutOff':fields.float('Sm Center Conventional CutOff'),
        'sm_center_ltv_cutOff_grt':fields.float('Sm Center LTV % > CutOff'),
        'sm_center_ltv_cutOff_les':fields.float('Sm Center LTV % <= CutOf'),
        'lender_fees_percent':fields.float('Lender Fees % '),
        'lender_fees_flat':fields.float('Lender Fees Flat'),
        'broker_fees_percent':fields.float('Broker Fees %'),
        'broker_fees_flat':fields.float('Broker Fees Flat'),

        'allow_self_emp_income':fields.boolean('Allow Self Employed Income'),
        'stated_income_max_ltv':fields.float('Stated Income Max LTV '),
        'stated_income_min_beacon':fields.float('Stated Income Min Beacon'),
        'short_avg_fund_day':fields.float('Shortest Avg Funding Days'),
        'canadian_military_allow':fields.boolean('Canadian Military Allowed'),
        'branch_signing':fields.boolean('Branch Signing'),
        'non_resident_allow':fields.boolean('Non-Resident Allowed'),
        'line_of_credit':fields.boolean('Line of Credit'),
        'capped_variable':fields.boolean('Capped Variable Allowed'),
        'max_gift_allow':fields.float('Max % Gift Allowed'),
        #'min_gift_allow':fields.float('% Min Gift Allowed'),
        'max_borrow_allow':fields.float('Max % Borrowed Allowed'),
        #'min_borrow_allow':fields.float('% Min Borrowed Allowed'),


        'allow_power_of_attorney':fields.boolean('Allow Power of Attorney'),
        'max_allow_property':fields.float('Max Allowed Properties'),
        'allow_title_ins':fields.boolean('Allowed Title Ins'),
        'immigrant_min_emp_mo':fields.float('Immigrant Min Employ Mo'),
        'immigrant_max_mo':fields.float('Immigrant Max Mo in Can'),
        'immigrant_max_ltv':fields.float('Immigrant Max LTV'),
        'min_heat_cost':fields.float('Minimum Heating Cost'),
        'max_property_age':fields.integer('Max Property Age (not verified)'),
        #'min_heat_cost':fields.float('Minimum Heating Cost'),

        'allowed_on_1st':fields.boolean('Allowed on 1st'),
        'allowed_on_2nd':fields.boolean('Allowed on 2nd'),
        'charges_allowed_behind':fields.boolean('Charges Allowed Behind'),
        'specific_lenders_on_1st':fields.boolean('Specific Lenders on 1st'),
        'allowed_on_3rd':fields.boolean('Allowed on 3rd'),
        'allowed_on_bridge':fields.boolean('Allowed on Bridge'),
        
        'allowed_grey_flags_good':fields.float('Allowed Grey Flags (Good Credit)'),
        'allowed_grey_flags_med':fields.float('Allowed Grey Flags (Med Credit)'),
        'allowed_grey_flags_poor':fields.float('Allowed Grey Flags (Poor Credit)'),
        'allowed_red_flags_good':fields.float('Allowed Red Flags (Good Credit)'),
        'allowed_red_flags_med':fields.float('Allowed Red Flags (Med Credit)'),
        'allowed_red_flags_poor':fields.float('Allowed Red Flags (Poor Credit)'),

        'lender_line': fields.one2many('res.partner', 'lender_id', 'Lender Lines'),

        'opportunity_id':fields.many2one('crm.lead','Opportunity Reference'),
        'raw_land':fields.boolean('Raw Land'),    
        'open_closed':fields.selection([('open','Open'),('closed','Closed')],'Open Closed'),
	'uninsurable':fields.boolean('Uninsurable'),
	'combined_product':fields.many2one('product.product','Combined Product'),

    }

    _defaults = {
            'outstanding_collection_payment':True,
    }

    '''def create(self,cr,uid,vals,context=None):
        res = super(product_product, self).create(cr, uid, vals)
        print"res",res
#        crm_browse = self.browse(cr,uid,ids[0])
#        uw_product = crm_browse.company_id.uw_product  or ''
#        req = urllib2.Request('%s/%s'%(uw_product,res[0]))
        #link='http://107.23.89.76:8080/UnderWritingApp/services/product'
        #req = urllib2.Request('%s/%s'%(link,res)) 
#        print"req",req
#        data = urllib2.urlopen(req)
#        print"data",data
#        notes = json.loads(data.read())
#        print"notessssssssssssss",notes
#        
        return res'''
    
    '''def create(self,cr,uid,vals,context=None):
        res = super(product_product, self).create(cr, uid, vals)
        print"res",res
#        crm_browse = self.browse(cr,uid,ids[0])
#        uw_product = crm_browse.company_id.uw_product  or ''
#        req = urllib2.Request('%s/%s'%(uw_product,res[0]))
        #link='http://107.23.89.76:8080/UnderWritingApp/services/product'
        #req = urllib2.Request('%s/%s'%(link,res))
        #encoded_vals = urllib.urlencode(vals)
        #print"encoded_valsencoded_vals",encoded_vals
        #urllib2.Request.add_data(req,encoded_vals)
        #response=urllib2.urlopen(req, encoded_vals).read()
        #print "response------------",response
#        print"req",req
#        data = urllib2.urlopen(req)
#        print"data",data
#        notes = json.loads(data.read())
#        print"notessssssssssssss",notes
#        
        return res'''

    def send_product_info(self,cr,uid,ids,context):
        sub,email_body,mail_from,mail_to='','','',''
        ir_mail_server = self.pool.get('ir.mail_server')
        mail=self.pool.get('mail.mail')
        if context.get('not_created')==True:
            sub='Product ID :'+str(ids[0])+'  not created in UW App database.'
            email_body='Product ID :'+str(ids[0])+'  has not been created in the UW App database.'

        if context.get('not_updated')==True:
            sub='Product ID :'+str(ids[0])+'  not updated in UW App database.'
            email_body='Product ID :'+str(ids[0])+' has not been updated in the UW App database.'
	
	if context.get('not_deleted')==True:
            sub='Product ID :'+str(ids[0])+'  not deleted in UW App database.'
            email_body='Product ID :'+str(ids[0])+'  has not been deleted in the UW App database.'
	
        user_brow=self.pool.get('res.users').browse(cr,uid,uid)
        mail_to=user_brow.email
        print "email_to----------------",mail_to

        mail_from=user_brow.hr_department_id.mail_server.smtp_user
        mail_servr_id=user_brow.hr_department_id.mail_server.id
        print "from--------------------",mail_from
        msg = ir_mail_server.build_email(
           email_from = mail_from,
           email_to = [mail_to],
           subject = sub,
           body = email_body)
        res = ir_mail_server.send_email(cr, uid, msg,
           mail_server_id=mail_servr_id, context=context)
        
        return True



    def create(self, cr, uid, vals, context=None):
	context.update({'do_not_update':True})
        usr_id =super(product_product, self).create(cr, uid, vals, context=context)

#        url = "http://107.23.89.76:8080/UnderWritingApp/services/product/"
	#url = "http://uwserv.visdom.ca:8080/UnderWritingApp/services/product/"
	#final_url=url+str(usr_id)
        #print"final_url",final_url
        #headers = {'Content-type': 'application/json' }
        #r = requests.post(final_url)
        #print "r=-------------------------",r.text
	
	#if r.text=='false':
            #self.send_product_info(cr,uid,ids,{'not_created':True})
         

        return usr_id

   


    def uw_app_check(self,cr,uid,ids,vals):
        print "ids[0]------------",ids[0]
        print "valsss--------------",vals
        encoded_vals = urllib.urlencode(vals)
        print "encoded_valsencoded_vals------------------",encoded_vals
#        crm_browse = self.browse(cr,uid,ids[0])
#        uw_allProduct  = crm_browse.company_id.uw_allProduct or ''
        company_brw=self.pool.get('res.company').browse(cr,uid,1)
        uw_allProduct  = company_brw.uw_product or ''
        print "uw_allProduct------------------",uw_allProduct
#        request.add_data(urllib.urlencode(query_args))
        
#        req = urllib2.Request('%s%s'%(uw_allProduct,ids[0]))
        req = urllib2.Request('%s%s'%(uw_allProduct,9))
        urllib2.Request.add_data(req, urlencode(vals))
        response=urllib2.urlopen(req, encoded_vals).read()
        print "response------------",response
#        ero
        try:
#            req = urllib2.Request('%s%s'%(uw_allProduct,ids[0]))
#            print"req",req
#            fhdjfhjf
#            req = urllib2.Request('%s%s'%('http://107.23.89.76:8080/UnderWritingApp/services/product/',ids[0]))
            print "req---------------",req
#            post_response = requests.post(url= req, data=post_data)
            data = urllib2.urlopen(req)
#            print 'postesp-----------------------',post_response
            notes = json.loads(data.read())
#            print "NOTES---------------",notes
            cr.commit()
        except:
            raise osv.except_osv(('UW App'),("Oops! We're having trouble connecting to UW web service. Please try again."))

        return True

    def uw_product(self, cr, uid, ids, context=None):
        print "inside product methodddddddddddddddddd",ids[0]
#        product_bool  = self.browse(cr, uid, ids[0]).product_uw
#        print  "product_boolllllllllllll",product_bool
#
#        if product_bool:
        try:
            crm_browse = self.browse(cr,uid,ids[0])
            uw_product = crm_browse.company_id.uw_product  or ''
            req = urllib2.Request('%s/%s'%(uw_product,ids[0]))
#            req = urllib2.Request('http://107.23.89.76:8080/UnderWritingApp/services/product/771')
            print"req",req
            data = urllib2.urlopen(req)
            notes = json.loads(data.read())
            print"notessssssssssssss",notes
            cr.commit()
        except:
              raise osv.except_osv(('UW App'),("Oops! We're having trouble connecting to UW web service. Please try again."))

        if 'treatmentOfRental' in notes.keys():
            print "treatmentOfRental$$$$$$$$$$$$$$$$$$$$$$$$$",notes['treatmentOfRental']
        if 'cottageInsureLtv' in notes.keys():
            print "cottageInsureLtv$$$$$$$$$$$$$$$$$$$$$$$$$",notes['cottageInsureLtv']
                
          
        return True

    '''def uw_product(self, cr, uid, ids, context=None):
        print "inside product methodddddddddddddddddd",ids[0]
        product_bool  = self.browse(cr, uid, ids[0]).product_uw
        print  "product_boolllllllllllll",product_bool
        
        if product_bool:
            try:
                crm_browse = self.browse(cr,uid,ids[0])
                uw_product = crm_browse.company_id.uw_product  or ''
                req = urllib2.Request('%s/%s'%(uw_product,ids[0]))
                data = urllib2.urlopen(req)
                notes = json.loads(data.read())
                cr.commit()
            except:
                  raise osv.except_osv(('UW App'),("Oops! We're having trouble connecting to UW web service. Please try again."))

            if 'treatmentOfRental' in notes.keys():
                print "treatmentOfRental$$$$$$$$$$$$$$$$$$$$$$$$$",notes['treatmentOfRental']
                
          
        return True'''

    def write(self , cr ,uid ,ids ,vals , context=None):
        print "write for product.......",context
#        if vals:
#            self.uw_app_check(cr,uid,ids,vals)
#        vals={'application_method':'2'}
        res =  super(product_product , self ).write( cr ,uid ,ids ,vals , context=None)
	#cr.commit()
#        url = "http://107.23.89.76:8080/UnderWritingApp/services/product/"
	#url = "http://uwserv.visdom.ca:8080/UnderWritingApp/services/product/"
        #final_url=url+str(ids[0])
	#print "vals---------------------------",vals
        #print"final_url",final_url
        #headers = {'Content-type': 'application/json'}
	#payload = {'json_playload': json.dumps(vals)}
	#cr.commit()
#        r = requests.put(final_url, data=json.dumps(vals), headers=headers)
	#if not context.get('do_not_update',False):
	   
            #r = requests.put(final_url, data=payload,headers=headers)


            #print "r=-------------------------",r.text
	    #if r.text=='false':
                #self.send_product_info(cr,uid,ids,{'not_updated':True})
#        notes = json.loads(r.read())
#        print "notesssssssssssssss=============",notes
#        eroooo




        return res

    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
	result=super(product_product, self).unlink(cr, uid, ids, context=context)	
        payload={}
	#for each in ids:
            #headers = {'content-type': 'application/json'}
            #url = "http://107.23.89.76:8080/UnderWritingApp/services/product/" + str(each)
            #response = requests.delete(url, data=json.dumps(payload), headers=headers)
	    #print "responseeeee-----------------------------------",response.text

	    #if response.text=='false':
                #self.send_product_info(cr,uid,ids,{'not_deleted':True})

#
#        company_brw=self.pool.get('res.company').browse(cr,uid,1)
#        uw_allProduct  = company_brw.uw_product or ''
#        for each in ids:
#            req = urllib2.Request('%s%s'%(uw_allProduct,each))
##            opener = urllib2.build_opener(urllib2.HTTPHandler)
##            req = urllib2.Request(query_url, None)
#            req.get_method = lambda: 'DELETE'
#            url = urllib2.urlopen(req)

        return result

product_product()


class product_supplierinfo(osv.osv):
    _inherit = 'product.supplierinfo'
    
    _columns = {
        'name' : fields.many2one('res.partner', 'Lender', required=True,domain = [('supplier','=',True)], ondelete='cascade', help="Lender of this product"),
        'product_name': fields.char('Lender Product Name', size=128, help="This lender's product name will be used when printing a request for quotation. Keep empty to use the internal one."),
        'product_code': fields.char('Lender Product Code', size=64, help="This lender's product code will be used when printing a request for quotation. Keep empty to use the internal one."),
        'lender_code': fields.char('Lender Code', size=64,),
       }

product_supplierinfo()    

class product_term(osv.osv):
    _name='product.term'
    _columns={
            'name': fields.char('Name', size=64, required=True, select=True),
        }    
product_term()

class product_rate_type(osv.osv):
    _name='product.rate.type'
    _columns={
            'name': fields.char('Name', size=64, required=True, select=True),
        }
        
product_rate_type()

class product_compensation(osv.osv):
    _name ='product.compensation'
    _columns ={
            'name': fields.char('Name', size=64, required=True, select=True),
        }
product_compensation()


class pre_payment_option(osv.osv):
    _name ='pre.payment.option'
    _columns ={
            'name': fields.char('Name', size=64, required=True, select=True),
        }
pre_payment_option()

class product_descriptions(osv.osv):
    _name ='product.descriptions'
    _columns ={
            'name': fields.char('Name', size=64, required=True, select=True),
        }
product_descriptions()
