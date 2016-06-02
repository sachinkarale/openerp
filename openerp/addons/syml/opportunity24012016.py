import json
import urllib2
from osv import fields,osv
import datetime
from datetime import timedelta
from datetime import date
from base_status.base_stage import base_stage
import tools
from tools.translate import _
from tools import html2plaintext
import cgi
import time
import sys
#from pyPdf import PdfFileWriter, PdfFileReader
import tempfile
import os


class crm_lead(osv.osv):
    _name = "crm.lead"
    _inherit = ['mail.thread', 'ir.needaction_mixin','crm.lead']


    def desg_login_admin(self, cr, uid, ids, field_name, arg, context=None):

        res={}
        login_id=context.get('uid')
        check_string=self.pool.get('res.users').browse(cr,uid,login_id).designation
        
        if check_string=='admin':
            for o in self.browse(cr,uid,ids):
                res[o.id]=True
        else:
            for o in self.browse(cr,uid,ids):
                res[o.id]=False
        return res
    
    

    def desg_login_underwriter(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        login_id=context.get('uid')
        check_string=self.pool.get('res.users').browse(cr,uid,login_id).designation
#        erooooooooooo
        if check_string=='underwriter':
            for o in self.browse(cr,uid,ids):
                res[o.id]=True
        else:
            for o in self.browse(cr,uid,ids):
                res[o.id]=False

    #           user_id=o.user_id.id
#                if login_id==user_id:

#                else:
#                    res[o.id]=False
        return res





    _columns={
	'app_rec_ids': fields.many2many('applicant.record','opportunity_applicant_rel','opp_id','app_id','Applicants'),
        'opportunity_id':fields.many2one('applicant.record','Opportunity Reference'),        
        ###General###
        'application_date':fields.datetime('Application Date'),
        'condition_of_financing_date':fields.datetime('Condition of Financing Date'),
        'propsal_date':fields.datetime('Proposal Date'),
        'expected_closing_date':fields.datetime('Expected Closing Date'),
        'current_lender':fields.char('Current Lender',size=120),
        'sales_associate':fields.many2one('res.users','Sales Associate'),
        'assistant':fields.many2one('res.users','Assistant'),
        'underwriter':fields.many2one('res.users','Underwriter'),
	'current_mortgage_product':fields.many2one('product.product','Current Mortgage Product'),
        'referred_source':fields.many2one('hr.applicant','Referral Source'),
        'training_associate_referral':fields.many2one('res.users','Training Associate Referral'),
        'lead_source':fields.many2one('res.partner','Lead Source'),
        
        'applicant_record_line': fields.one2many('applicant.record', 'applicant_id', 'Applicant Lines'),
        'what_is_your_lending_goal':fields.selection([('1','Pre-Approved'),('2','Approved'),('3','Refinance')],'Lending Goal'),
        'looking_fora':fields.selection([('1','Condo/Mobile Home'),('2','House/Townhouse/Duplex/Acreage'),('5','Second Home/Vacation Property'),('7','Cottage Property'),('3','Rental Property'),('4','Raw Land/Leased Land'),('6',"Not Sure")],"I'm Looking for a"),
        'applicant_last_name':fields.char('Last Name', size=240),
        'ltv': fields.float('LTV (Loan to Value: %)',), 
        'GDS': fields.float('GDS'),
        'TDS': fields.float('TDS'),
        'completed_ref':fields.boolean('Completed Ref'),
        'charges_behind_amount':fields.float('Charges Behind  Amount'),
        'maximum_amount':fields.boolean('Additional Amount'),
        'date_created_co_applicant': fields.date('Date Created'),
        'delayed_app_date': fields.datetime('Delayed App Date'),
        'lead_followup_date': fields.datetime('Lead Folowup Date'),
        'delayed_app_task':fields.boolean('Task Created'),
        'lead_followed':fields.boolean('Lead Followed'),
        ####################### Address Summary
        'lender':fields.many2one('res.partner','Lender'),
        'prject_task_ids':fields.one2many('project.task','related_to','Projects'),
        
     
       
       
##################   loan details
        'down_payment_amount':fields.float('Down Payment Amount'),

        'draws_required':fields.integer('Draws Required'),
        

        'looking_to':fields.selection([('1','Refinance my Property to purchase an additional property'),('2','Reduce Interest Rate on my Mortgage'),('3','Renew Mortgage'),('4','Increase Mortgage Amount.'),('5','Buy an existing finished property'),('6','Get additional funds to purchase and renovate'),('7','Build a Property'),('8','Keep existing mortgage and port'),('9','Get Additional Money')],"Looking To"),
	
	'building_funds':fields.selection([('1','Funding When Complete'),('2','Builder Progress Funding'),('3','Self-Build Progress Funding')],"Building Funds"),
        'property_value':fields.float('Property Value'),
        'renovation_value':fields.float('Renovation Value'),
        'desired_amortization':fields.integer('Desired Amortization'),       
#	'desired_amortization':fields.selection([('1','10 Years'),('2','15 Years'),('3','20 Year'),('4','25 Year'),('5','30 Year'),('6','Desired Length')],'Desired Term'),
#        'desired_term':fields.selection([('1','My Best Option'),('2','Month6'),('3','Year1'),('4','Year2'),('5','Year3'),('6','Year4'),('7','Year5'),('17','Year6'),('8','Year7'),('19','Year8'),('20','Year9'),('9','Year10')],'Desired Term'),
        #'desired_term':fields.selection([('12','My Best Option'),('1','Month6'),('2','Year1'),('3','Year2'),('4','Year3'),('5','Year4'),('6','Year5'),('7','Year6'),('8','Year7'),('9','Year8'),('10','Year9'),('11','Year10'),('0','Other')],'Desired Term'),
	#'desired_term':fields.selection([('1','My Best Option'),('2','Month6'),('3','Year1'),('4','Year2'),('5','Year3'),('6','Year4'),('7','Year5'),('8','Year7'),('9','Year10')],'Desired Term'),
	'desired_term':fields.selection([('1','My Best Option'),('2','6 Months'),('3','1 Year'),('4','2 Years'),('5','3 Years'),('6','4 Years'),('7','5 Years'),('8','7 Years'),('9','10 Years')],'Desired Term'),
        'desired_mortgage_amount':fields.float('Desired Mortgage Amount'),
#         'desired_mortgage_type':fields.selection([('0','LOC'),('2','Variable'),('3','Cashback'),('1','Fixed'),('4','Recommend')],"Desired Mortgage Type"),
#        'desired_mortgage_type':fields.selection([('1','LOC'),('2','Variable'),('3','Fixed'),('4','Cashback'),('5','Combined'),('6','Recommend')],"Desired Mortgage Type"),
        'desired_mortgage_type':fields.selection([('0','LOC'),('2','Variable'),('1','Fixed'),('3','Cashback'),('5','Combined'),('4','Recommend')],"Desired Mortgage Type"),
        'desired_product_type':fields.selection([('1','LOC'),('2','Variable'),('3','Cashback'),('4','Fixed'),('3','Recommend')],"Desired Product Type"),

        

        'personal_cash_amount':fields.float('Personal Cash Amount'),
        'rrsp_amount':fields.float('RRSP Amount'),
        'gifted_amount':fields.float('Gifted Amount'),
        'borrowed_amount':fields.float('Borrowed Amount'),
        'sale_of_existing_amount':fields.float('Sale of Existing Amount'),
        'existing_equity_amount':fields.float('Existing Equity Amount'),
        'sweat_equity_amount':fields.float('Sweat Equity Amount'),
        'secondary_financing_amount':fields.float('Secondary Financing Amount'),
        'other_amount':fields.float('Other Amount / Vendor Takeback'),
        'down_payment_coming_from':fields.selection([('1','Bank Account Chequing/Savings'),('2','RRSPs or Investments'),('3','Borrowed(e.g LOC)'),('4','Sale of Asset/Sale of Existing Property'),('5','Gift'),('6','Other')],"Down Payment Coming From"),
        'bank_account':fields.float('Bank Account Chequing/Savings'),


        'job_5_years':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose not to Answer')],"Job - 5 years"),
        'income_decreased_worried':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose not to Answer')],"Income Decreased; Worried"),
        'future_family':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose not to Answer')],"Future Family"),
        'buy_new_vehicle':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose not to Answer')],"Buy New Vehicle"),

        'lifestyle_change':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose not to Answer')],"Lifestyle Change"),
        'financial_risk_taker':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose not to Answer')],"Financial Risk Taker"),
        'property_less_then_5_years':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose not to Answer')],"Property < 5 years"),

        'recommendations_ids':fields.one2many('opp.recommendations','opp_id','recommendations'),
        'deal_ids':fields.one2many('deal','opportunity_id','Deal'),
        'internal_note':fields.text('Internal Notes'),



        'property_style':fields.selection([('1','Bungalow/One Story'),('2','BiLevel'),('3','Two Story'),('4','Split Level'),('5','Story and A Half'),('6','Three Story'),('7','Other')],"Property Style"),
        'property_type':fields.selection([('1','House'),('2','Duplex'),('3','Four Plex'),('4','Apartment Style Condo'),('5','Town house/Raw house'),('6','Mobile Home/Modular Home'),('7','Other')],'Property Type'),
        'apartment_style':fields.selection([('1','LowRise'),('2','HighRise')],"Apartment Style"),
        'plan':fields.char('Plan', size=240),
        'block':fields.char('Block', size=240),
        'lot':fields.char('Lot', size=240),
        'mls':fields.char('MLS', size=240),
#        'new_home_warranty':fields.char('New Home Warranty', size=240),
        'new_home_warranty':fields.selection([('1','Yes'),('2','No'),('3','Unsure')],'New Home Warranty'),

        


        'address':fields.char('Address', size=240),
        'city':fields.char('City', size=240),
        'age':fields.integer('Age'),
        'square_footage':fields.integer('Square Footage'),
        'lot_size':fields.char('Lot Size', size=240),
        'acres':fields.float("# of Acres"),
        'property_taxes':fields.float('Property Taxes'),
        'min_heat_fee':fields.float('Minimum Heat Fee', size=240),

        'province':fields.char('Province', size=240),
        'Township_PID':fields.char('Township/PID', size=240),
        'postal_code':fields.char('Postal Code', size=240),
        'heating':fields.selection([('1','Furnace/ Forced Air'),('2','Electric Base board'),('3','Hot Water Baseboard In Floor Heating'),('4','Other')],"Heating"),
        'water':fields.selection([('1','Municipality'),('2','Well'),('3','Other')],"Water"),
        'sewage':fields.selection([('1','Municipality'),('2','Septic System'),('3','Holding Tank'),('4','Other')],"Sewage"),
        'condo_fees':fields.float('Condo Fees'),


        'garage_type':fields.selection([('1','Attached'),('2','Detached'),('3','None')],"Garage Type"),
        'garage_size':fields.selection([('1','Single'),('2','Double'),('3','Triple'),('4','Quadruple')],"Garage Size"),
        'outbuildings_value':fields.float('Outbuildings Value'),


        'living_in_property':fields.selection([('1','Owner (Self)'),('2','Renter'),('3','Owner and Renter'),('4','Second Home/Vacation property')],"Living In Property"),
        'renter_pay_heating':fields.selection([('1','HeatIncluded'),('2','HeatSeparate')],"Renter pay heating?"),
        'monthly_rental_income':fields.float('Monthly Rental Income'),


        'is_country_residential':fields.boolean('Is Country Residential'),
        'is_condo':fields.boolean('Is Condo'),
        'is_agricultural_less_10_acres':fields.boolean('Is Agricultural < 10 Acres'),
        'is_agricultural':fields.boolean('Is Agricultural'),
        'is_commercial':fields.boolean('Is Commercial'),
        'is_fractional_interests':fields.boolean('Is Fractional Interests'),
        'is_co_operative_housing':fields.boolean('Is Co-operative Housing'),
        'is_grow_ops':fields.boolean('Is Grow Ops'),
        'is_rental_pools':fields.boolean('Is Rental Pools'),
        'is_age_restricted':fields.boolean('Is Age Restricted'),
        'is_duplex':fields.boolean('Is Duplex'),
        'is_four_plex':fields.boolean('Is Four - Plex'),
        'is_six_plex':fields.boolean('Is Six - Plex'),
        'is_eight_plex':fields.boolean('Is Eight - Plex'),
        'distance_to_major_center':fields.float('Distance to Major Center', size=240),
        'lender_requires_insurance':fields.boolean('Lender Requires Insurance'),
        'needs_power_attorney':fields.boolean('Needs Power of Attorney'),
        'min_heat_fee':fields.float('Minimum Heat Fee', size=240),
        'selected_product':fields.many2one('product.product','Selected Product'),
        'is_construction_mortgage':fields.boolean('Is Construction Mortgage'),
        'is_life_leased_property':fields.boolean('Is Life Leased Property'),
        'is_leased_land':fields.boolean('Is Leased Land'),
        'is_raw_land':fields.boolean('Is Raw Land'),
        'is_mobile_homes':fields.boolean('Is Mobile Homes'),
        'is_modular_homes':fields.boolean('Is Modular Homes'),
        'is_floating_homes':fields.boolean('Is Floating Homes'),
        'is_boarding_houses':fields.boolean('Is Boarding Houses'),
        'is_rooming_houses':fields.boolean('Is Rooming Houses'),
        'is_non_conv_construction':fields.boolean('Is Non-Conv Construction'),
        'is_cottage_rec_property':fields.boolean('Is Cottage / Rec Property'),
        'is_rental_property':fields.boolean('Is Rental Property'),
        'is_high_ratio_2nd_home':fields.boolean('Is High Ratio 2nd Home'),
        'is_uninsured_conv_2nd_home':fields.boolean('Is Uninsured Conv 2nd Home'),
        'is_a_small_centre':fields.boolean('Is A Small Centre'),
        'internal_note_property':fields.text('Internal Notes'),
        'has_charges_behind':fields.boolean('Has Charges Behind'),
        'charge_on_title':fields.selection([('1','First'),('2','Second'),('3','Third'),('4','Fourth'),('5','Bridge')],'Charge On Title'),  
        'mortgage_insured':fields.boolean('Mortgage Insured'),




        
#        verification
        'task':fields.one2many('opp.task','opp_id','Task'),
        'broker_task':fields.one2many('broker.task','opp_id','Task'),   
        'internal_notes':fields.text('Internal Notes'),
        'internal_notes_final':fields.text('Internal Notes'),

#        final solution
        'final_lender':fields.many2one('res.partner','Lender'),
        'lender_name':fields.char('Lender Name',size=120),
        'lender_response':fields.datetime('Lender Response'),
        'lender_ref':fields.char('Lender Ref#'),
        'morweb_filogix':fields.char('Morweb/Filogix Ref#'),
        'insurer':fields.selection([('cmhc','CMHC'),('ge','GE'),('aig','AIG')],'Insurer'),
        'insurerref':fields.char('Insurer Ref#'),
        'insurerfee':fields.float('Insurer Fee'),
        'purchase_price':fields.float('Purchase Price'),
        'downpayment_amount':fields.float('DownPayment'),
        'closing_date':fields.date('Closing Date'),
        'renewaldate':fields.date('Renewal Date'),
        'total_mortgage_amount':fields.float('Total Mortgage Amount'),
        'rate':fields.float('Rate %'),
        #'term':fields.selection([('6month','6 Month'),('1year','1 Year'),('2year','2 Year'),('3year','3 Year'),('4year','4 Year'),('5year','5 Year'),('6year','6 Year'),('7year','7 Year'),('8year','8 Year'),('9year','9 Year'),('10year','10 Year'),('open','Open')],'Term'),
	'term':fields.selection([('1','6 Month'),('2','1 Year'),('3','2 Year'),('4','3 Year'),('5','4 Year'),('6','5 Year'),('7','6 Year'),('8','7 Year'),('9','8 Year'),('10','9 Year'),('11','10 Year'),('open','Open')],'Term'),
        'amortization':fields.float('Amortization'),
        'monthly_payment':fields.float('Payment'),
        'mortgage_type':fields.selection([('1','LOC'),('2','Variable'),('3','Fixed'),('4','Cashback'),('5','Combined')],'Mortgage Type'),
        'open_closed':fields.selection([('open','Open'),('closed','Closed')],'Open Closed'),
        'product_type':fields.selection([('fixed','Fixed'),('variable','Variable'),('loc','LOC')],'Product Type'),
        'cash_back':fields.integer('Cash Back'),
        'base_commission':fields.float('Base Commissions'),
        'volume_commission':fields.float('Volume Commissions'),
        'commitment_fee':fields.float('Commitment Fee'),
        'lender_fee':fields.float('Lender Fee'),
        'broker_fee':fields.float('Broker Fee'),
        'total_one_time_fees':fields.float('Total One Time Fees'),
	'posted_rate':fields.float('Posted Rate'),
        'verify_product':fields.boolean('Verify Product'),
        'frequency':fields.selection([('1','Monthly'),('2','Semi-Monthly'),('3','Bi-Weekly'),('4','Weekly'),('5','Quarterly'),('6','Annual')],"Frequency"),

        'considered_cites':fields.char('Considered Cities'),
        'current_balance':fields.float('Current Balance'),
        'current_mortgage_amount':fields.float('Current Mortgage Amount'),
        'current_monthly_payment':fields.float('Current Monthly Payment'),
        'non_income_qualifer':fields.boolean('Non Income Qualifer'),
        'source_of_borrowing':fields.selection([('1','Secured LOC'),('2','Other')],'Source of Borrowing'),
        'is_military':fields.boolean('Is Military'),
	'existing_payout_penalty':fields.float('Existing Payout Penalty'),

	'percent_variable':fields.float('Percent Variable'),

        'base_comp_amount':fields.float('Base Comp Amount'),
        'volume_bonus_amount':fields.float('Volume Bonus Amount'),
        'total_comp_amount':fields.float('Total Comp Amount'),
        'marketing_comp_amount':fields.float('Marketing Comp Amount'),
        'trailer_comp_amount':fields.float('Trailer Comp Amount'),

        'current_interest_rate':fields.float('Current Interest Rate'),
        'current_renewal_date':fields.date('Current Renewal Date'),
        'current_mortgage_type':fields.selection([('loc','LOC'),('variable','Variable'),('cashback','Cashback'),('fixed','Fixed')],'Current Mortgage Type'),
        'login_admin_flag':fields.function(desg_login_admin, string='admin', type='boolean'),
        'login_underwriter_flag':fields.function(desg_login_underwriter, string='underwriter', type='boolean'),
        'plus_minus_prime':fields.float('Plus-Minus Prime'),
        'welcum_email_date':fields.datetime('Welcome Email Date'),
        'renewal_reminder':fields.datetime('Renewal Reminder Date'),
        'renewal_email_send':fields.boolean('Renewal Email send'),
        ################3
        'base_commission':fields.float('Base Commission',digits=(16,2)),
        'volume_commission':fields.float('Volume Commission',digits=(16,2)),
        'commitment_fee':fields.float('Commitment Fee',digits=(16,2)),
        'lender_fee':fields.float('Lender Fee',digits=(16,2)),
        'private_fee':fields.float('Private Fee',digits=(16,2)),
        ##########################
        ####Document Fields###########
        'document_ids':fields.one2many('app.documents','opportunity_id','Opportunity'),
        'document_fields':fields.binary('Documents'),
        'from_pages':fields.integer('From Pages'),
        'to_pages':fields.integer('To Pages'),
        'final_documents':fields.binary('Final Documents'),
        ###############
        'attachment_ids': fields.many2many('ir.attachment',
            'opportunity_ir_attachments_rel',
            'opportunity_id', 'attachment_id', 'Attachments'),

	'fax1':fields.char('Fax',size=240),
	'mail_message_ids':fields.one2many('mail.message','opportunity_id','Mail Message'),        
    }
    _track = {
        'state': {
            'crm.mt_lead_create': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'new',
            'crm.mt_lead_won': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'done',
            'crm.mt_lead_lost': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'cancel',
#            'crm.mt_lead_task': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'task',
#            'crm.mt_lead_all_prod': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'all_product',
#            'crm.mt_lead_post_sel': lambda self, cr, uid, obj, ctx=None: obj['state'] == 'post_selection',
        },
        }
    
    _defaults = {
        #'issuing_province_canada': 39,
        'charge_on_title':'1',
        'frequency':'1',
        }
        
    '''def split(self,cr,uid,ids,context=None):
        crm_browse = self.browse(cr,uid,ids[0])
        source_documents=crm_browse.document_fields
        
        f = tempfile.NamedTemporaryFile(prefix='report_', suffix='.pdf',mode='w+b', delete=False)
        data=source_documents.decode('base64')
        f.write(data)
        f.close()
#        os.chmod(f,0o777)
        from_pages=crm_browse.from_pages
        to_pages=crm_browse.to_pages
        inputpdf = PdfFileReader(file(f.name, "rb"))
        for i in range(from_pages,to_pages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(i))
            outputStream = file("abc_page%s.pdf" % i, "wb")
            output.write(outputStream)
            outputStream.close()
        print"outputStream.name",outputStream.name
        f1=PdfFileReader(file(outputStream.name, "rb"))
#        os.chmod(f1,0o777)
        return f1'''

    def print_opportunity_report(self, cr, uid, ids, context=None):
       '''
       print the report
       '''
       datas = {
                'model': 'crm.lead',
                'ids': ids,
                'form': self.read(cr, uid, ids[0], context=context),
       }
       return {'type': 'ir.actions.report.xml', 'report_name': 'crm.lead', 'datas': datas, 'nodestroy': True}	

    


    def final_verify(self, cr, uid, ids, context=None):
        print "inside final_verify_product"
#        Product ID: "Selected Product" at the bottom of the "Property Tab" of the Opportunity Record
        cr.execute("select selected_product from crm_lead where id = %s",(ids[0],))
        product_id = cr.fetchall()
        if not product_id[0][0]:
            raise osv.except_osv(('UW App'),("product not selected..."))

        if product_id[0][0]:
            opp_obj = self.pool.get('crm.lead')
            crm_browse = self.browse(cr,uid,ids[0])
            uw_finalVerify = crm_browse.company_id.uw_finalVerify  or ''
            req = urllib2.Request('%s%s/%s'%(uw_finalVerify,ids[0],product_id[0][0]))	  	
            data = urllib2.urlopen(req)
            notes = json.loads(data.read())
            print "notessss:",notes
    #        Assistant Notes
            if 'assistantNotes' in notes.keys():
                print "assistantNotes>>>>>>>>>>>",notes['assistantNotes']
                assistant_obj = self.pool.get('opp.task')
                for assis_note in notes['assistantNotes']:
                    print "assis_noteeee:",assis_note
                    ass_id = assistant_obj.create(cr, uid, {
                                                            'note_type':assis_note['noteType'],
                                                            'urgency':assis_note['urgency'],
                                                            'description':assis_note['description'],
                                                            'marketing_field':assis_note['marketingField'],
                                                            'opp_id':ids[0]
                                                            })
                    print "ass_id",ass_id

    #        Broker Notes
            if 'brokerNotes' in notes.keys():
                print "brokerNotes>>>>>>>>>>>",notes['brokerNotes']
                broker_obj = self.pool.get('broker.task')
                for broker_note in notes['brokerNotes']:
                    print "brokerNotessss:",broker_note
                    broker_id = broker_obj.create(cr, uid, {
                                                            'note_type':broker_note['noteType'],
                                                            'urgency':broker_note['urgency'],
                                                            'description':broker_note['description'],
                                                            'marketing_field':broker_note['marketingField'],
                                                            'opp_id':ids[0]
                                                            })
                    print "ass_id",broker_id
    #        Deal Notes
            if 'dealNotes' in notes.keys():
                print "dealNotesssss>>>>>>>>>>>",notes['dealNotes']
                deal_obj = self.pool.get('deal')
                for deal_note in notes['dealNotes']:
                    print "deal_notessss:",deal_note
                    deal_id = deal_obj.create(cr, uid, {
                                                        'note_type':deal_note['noteType'],
                                                        'urgency':deal_note['urgency'],
                                                        'name':deal_note['description'],
                                                        'marketing_field':deal_note['marketingField'],
                                                        'opportunity_id':ids[0]
                                                        })
                    print "deal_id",deal_id
#           finalSolution
            open_closed = {}
            opp_obj.write(cr, uid, ids[0], {
                                            'amortization':notes['amortization'],
                                            'cash_back':notes['downpayment'],
                                            'insurerfee':notes['insurerfee'],
                                            'lender_name':notes['lenderName'],
                                            'monthly_payment':notes['monthlyPayment'],
#                                            'mortgage_type':notes['mortgageType'],
#                                            'open_closed':notes['openClosed'],
                                            'rate':notes['rate'],
#                                            'term':notes['term'],
                                            'total_mortgage_amount':notes['totalMortgageAmount'],
                                            'trailer_comp_amount':notes['trailerCompAmount'],
                                            'volume_bonus_amount':notes['volumeBonusAmount'],
                                            'base_comp_amount':notes['baseCompAmount'],
                                            'marketing_comp_amount':notes['marketingCompAmount'],
                                            'lender_fee':notes['lenderFee'],
                                            'broker_fee':notes['brokerFee'],
                                            'total_one_time_fees':notes['totalOneTimeFees'],
                                            'total_comp_amount':notes['totalCompAmount']
                                })
            
        return True
    def onchange_selected_product(self, cr, uid, ids, selected_product,context=None):
        if context==None:
            context={}
        if ids:
            vals={}
            print "selected_product=====",selected_product
            if selected_product:
                prod_obj=self.pool.get('product.product').browse(cr,uid,selected_product)
                lender=prod_obj.lender
                if lender:
                    fax=lender.fax
                    if fax:
                        vals.update({'fax1':fax})


        return {'value':vals}

#    def onchange_selected_product(self, cr, uid, ids, selected_product,context=None):
#        if context==None:
#            context={}
#        if ids:
#            crm_browse = self.browse(cr,uid,ids[0])
#            context.update({'crm_id':crm_browse})
#        vals={}
#        print"selected_product",selected_product
#        vals.update({'selected_product':selected_product})
#        context.update({'lead_id':ids[0],'user_id':uid})
#        self.write(cr,uid,ids,vals,context)
#        mod_obj = self.pool.get('ir.model.data')
#        template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_product_confirm')
#        template_id = template and template[1] or False
#        if template_id:
#
#            self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
#
#        template2 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_ref_product_notify')
#        template_id2 = template2 and template2[1] or False
#        if template_id2:
#
#            self.pool.get('email.template').send_mail(cr,uid,template_id2,ids[0],'True',context)
#        return True

    def post_selection(self, cr, uid, ids, context=None):
        mod_obj = self.pool.get('ir.model.data')
        project_task = self.pool.get('project.task')
        res_users_obj=self.pool.get('res.users')
        assig_to_ast,assig_to=uid,uid
        crm_browse = self.browse(cr,uid,ids[0])
        context.update({'crm_id':crm_browse})
        
        #        Product ID: "Selected Product" at the bottom of the "Property Tab" of the Opportunity Record
        cr.execute("select selected_product from crm_lead where id = %s",(ids[0],))
        product_id = cr.fetchall()
        if not product_id[0][0]:
            raise osv.except_osv(('UW App'),("product not selected..."))
        
        if product_id[0][0]:          
            try:
                
                uw_postSelection = crm_browse.company_id.uw_postSelection or ''
                req = urllib2.Request('%s%s/%s'%(uw_postSelection,ids[0],product_id[0][0]))
#                req = urllib2.Request('http://107.23.89.76:8080/UnderWritingApp/services/postSelection/3433/461')
                data = urllib2.urlopen(req)
                notes = json.loads(data.read())
                cr.commit()
            except:
                raise osv.except_osv(('UW App'),("Oops! We're having trouble connecting to UW web service. Please try again."))
            
        if 'dealNotes' in notes.keys():
            deal_obj = self.pool.get('deal')
            if not (notes['dealNotes']== None):
                deal_ids = deal_obj.search(cr, uid, [('opportunity_id','=',ids[0]),('uw_app','=','postselection')])
                deal_obj.unlink(cr, uid, deal_ids)
            for deal_note in notes['dealNotes']:
                deal_id = deal_obj.create(cr, uid, {
                                                    'note_type':deal_note['noteType'],
                                                    'urgency':deal_note['urgency'],
                                                    'name':deal_note['description'],
                                                    'marketing_field':deal_note['marketingField'],
                                                    'opportunity_id':ids[0],
                                                    'uw_app':'postselection',
                                                    })
               
#           Assistant Notes
        if 'assistantTasks' in notes.keys():
            print"notes['assistantTasks']",notes['assistantTasks']
	    
            if not (notes['assistantTasks'] == None):
                assistant_ids = project_task.search(cr, uid, [('related_to','=',ids[0]),('uw_app','=','postselection'),('user_id.designation','=','assistant')])
                if assistant_ids:
                    project_task.unlink(cr, uid, assistant_ids)
#            for assis_note in notes['assistantNotes']:
#                print "assis_noteeee:",assis_note
#                ass_id = assistant_obj.create(cr, uid, {
#                                                        'note_type':assis_note['noteType'],
#                                                        'urgency':assis_note['urgency'],
#                                                        'description':assis_note['description'],
#                                                        'marketing_field':assis_note['marketingField'],
#                                                        'opp_id':ids[0]
#                                                        })
#                print "ass_id",ass_id
            
            assig_to_ids_ast=res_users_obj.search(cr,uid,[('designation','=','assistant'),('hr_department_id','=',crm_browse.hr_department_id.id)])
            if assig_to_ids_ast:
                    assig_to_ast=assig_to_ids_ast[0]
            for assis_note in notes['assistantTasks']:
                deadline=datetime.datetime.strptime(assis_note['deadline'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                start=datetime.datetime.strptime(assis_note['date_start'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                end=datetime.datetime.strptime(assis_note['date_end'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                project_task.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': assis_note['name']  ,
                    'description':assis_note['description'],
                    'date_deadline': str(deadline),
                    'hr_department_id':crm_browse.hr_department_id.id,
                    'related_to':ids[0]  or False,
                    'user_id':assig_to_ast,
                    'create_date':datetime.datetime.now(),
                    'planned_hours':assis_note['planned_hours'],
                    'date_start':str(start),
                    'date_end':str(end),
                    'uw_app':'postselection',
                    'state':'open',


                    },context=context)

#        Broker Notes
        if 'brokerTasks' in notes.keys():
            broker_obj = self.pool.get('broker.task')
            if not (notes['brokerTasks'] == None):
                broker_ids = project_task.search(cr, uid, [('related_to','=',ids[0]),('uw_app','=','postselection'),('user_id.designation','=','broker')])
                if broker_ids:
                    project_task.unlink(cr, uid, broker_ids)
#            for broker_note in notes['brokerTasks']:
#                print "brokerNotessss:",broker_note
#                broker_id = broker_obj.create(cr, uid, {
#                                                        'note_type':broker_note['noteType'],
#                                                        'urgency':broker_note['urgency'],
#                                                        'description':broker_note['description'],
#                                                        'marketing_field':broker_note['marketingField'],
#                                                        'opp_id':ids[0]
#                                                        })
#                print "ass_id",broker_id

            assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','broker'),('hr_department_id','=',crm_browse.hr_department_id.id)])
            if assig_to_ids:
                assig_to=assig_to_ids[0]
            for broker_note in notes['brokerTasks']:
                deadline_b=datetime.datetime.strptime(broker_note['deadline'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                start_b=datetime.datetime.strptime(broker_note['date_start'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                end_b=datetime.datetime.strptime(broker_note['date_end'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                project_task.create(cr, uid, {

                    'name': broker_note['name']  ,
                    'description':broker_note['description'],
                    'date_deadline': str(deadline_b),
                    'hr_department_id':crm_browse.hr_department_id.id,
                    'related_to':ids[0]  or False,
                    'user_id':assig_to,
                    'create_date':datetime.datetime.now(),
                    'planned_hours':broker_note['planned_hours'],
                    'date_start':str(start_b),
                    'date_end':str(end_b),
                    'uw_app':'postselection',
                    'state':'open',

                    },context=context)

        if 'lender_name' in notes.keys():
            self.write(cr,uid,ids[0],{'lender_name':notes['lender_name']})
        if 'rate' in notes.keys():
            self.write(cr,uid,ids[0],{'rate':notes['rate']})
        if 'term' in notes.keys():
            self.write(cr,uid,ids[0],{'term':notes['term']})
        if 'payment' in notes.keys():
            self.write(cr,uid,ids[0],{'monthly_payment':notes['payment']})
        if 'mortgage_type' in notes.keys():
            self.write(cr,uid,ids[0],{'mortgage_type':notes['mortgage_type']})
        if 'cashback' in notes.keys():
            self.write(cr,uid,ids[0],{'cash_back':notes['cashback']})
        if 'base_comp_amount' in notes.keys():
            self.write(cr,uid,ids[0],{'base_comp_amount':notes['base_comp_amount']})
        if 'trailer_comp_amount' in notes.keys():
            self.write(cr,uid,ids[0],{'trailer_comp_amount':notes['trailer_comp_amount']})
        if 'volume_bonus_amount' in notes.keys():
            self.write(cr,uid,ids[0],{'volume_bonus_amount':notes['volume_bonus_amount']})
        if 'marketing_comp_amount' in notes.keys():
            self.write(cr,uid,ids[0],{'marketing_comp_amount':notes['marketing_comp_amount']})
        if 'total_comp_amount' in notes.keys():
            self.write(cr,uid,ids[0],{'total_comp_amount':notes['total_comp_amount']})
        if 'referral_fee' in notes.keys():
            self.write(cr,uid,ids[0],{'referral_fee':notes['referral_fee']})
        if 'gds' in notes.keys():
            self.write(cr,uid,ids[0],{'GDS':notes['gds']})
        if 'ltv' in notes.keys():
            self.write(cr,uid,ids[0],{'ltv':notes['ltv']})


        if 'tds' in notes.keys():
            self.write(cr,uid,ids[0],{'TDS':notes['tds']})



	if 'purchase_price' in notes.keys():
            self.write(cr,uid,ids[0],{'purchase_price':notes['purchase_price']})

        if 'downpayment_amount' in notes.keys():
            self.write(cr,uid,ids[0],{'downpayment_amount':notes['downpayment_amount']})

        if 'total_mortgage_amount' in notes.keys():
            self.write(cr,uid,ids[0],{'total_mortgage_amount':notes['total_mortgage_amount']})

        if 'insurer_fee' in notes.keys():
            self.write(cr,uid,ids[0],{'insurerfee':notes['insurer_fee']})

        if 'amortization' in notes.keys():
            self.write(cr,uid,ids[0],{'amortization':notes['amortization']})

        if 'lender' in notes.keys():
            self.write(cr,uid,ids[0],{'final_lender':notes['lender']})

        if 'open_closed' in notes.keys():
            self.write(cr,uid,ids[0],{'open_closed':notes['open_closed']})

        if 'term' in notes.keys():
            self.write(cr,uid,ids[0],{'term':notes['term']})

        if 'plus_minus_prime' in notes.keys():
            self.write(cr,uid,ids[0],{'plus_minus_prime':notes['plus_minus_prime']})

        if 'posted_rate' in notes.keys():
            self.write(cr,uid,ids[0],{'posted_rate':notes['posted_rate']})

        if 'closingDate' in notes.keys():
	    print "recived_close_date-----------------------",notes['closingDate']
            #closedate=datetime.datetime.strptime(notes['closingDate'], '%m/%d/%Y').strftime('%Y-%m-%d %H:%M:%S')
	    closedate=datetime.datetime.strptime(notes['closingDate'], '%m/%d/%Y').strftime('%Y-%m-%d')
            print "closedate-------------------",closedate
	    
            self.write(cr,uid,ids[0],{'closing_date':closedate})

        if 'renewalDate' in notes.keys():
            renewdate=datetime.datetime.strptime(notes['renewalDate'], '%m/%d/%Y').strftime('%Y-%m-%d')
            self.write(cr,uid,ids[0],{'renewaldate':renewdate})

        
        context.update({'lead_id':ids[0],'user_id':uid})
        template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_req_lawyer_email')
        template_id = template and template[1] or False
        if template_id:
            self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
        assig_to=uid
        create_date=datetime.datetime.now()
        deadline1=(create_date + datetime.timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','assistant'),('hr_department_id','=',crm_browse.hr_department_id.id)])
        if assig_to_ids:
            assig_to=assig_to_ids[0]
        project_task.create(cr, uid, {
                #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                'name': 'Ensure client has replied to the email requesting the Lawyer info who is going to be closing their mortgage.' ,
                'date_deadline': deadline1 ,
                'description':'In the event the Lawyer\'s contact information from the client is partial, please lookup the lawyer\'s contact information on the internet and edit the contact record of the Lawyer.  Ensure the Lawyer\'s contact record is saved into the "Lawyer" field in the final solution Tab of the Opportunity.',
                'hr_department_id':crm_browse.hr_department_id.id,
                'related_to':ids[0]  or False,
                'user_id':assig_to,
                'create_date':datetime.datetime.now(),
                'state':'open',

                },context=context)
        opp_into_name=''
        if crm_browse.selected_product and crm_browse.selected_product.application_method:
            if crm_browse.selected_product.application_method == '1':

                opp_into_name='Morweb'
            else:
                opp_into_name='Filelogix'
            deadline2=(create_date + datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            project_task.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': 'Enter Opportunity into' + " " + opp_into_name ,
                    'date_deadline': deadline2 ,
                    'hr_department_id':crm_browse.hr_department_id.id,
                    'related_to':ids[0]  or False,
                    'user_id':assig_to,
                    'create_date':datetime.datetime.now(),
                    'state':'open',

                    },context=context)
            app_name=''
            if crm_browse.app_rec_ids:
                app_name=crm_browse.app_rec_ids[0].applicant_name
            if len(crm_browse.app_rec_ids) >= 2:
                app_name=app_name + " " + "and" + " " + crm_browse.app_rec_ids[1].applicant_name
            
            project_task.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': 'Pull credit in' + " " + opp_into_name +" " + 'for' + " " + app_name + " ",
                    'date_deadline': deadline2 ,
                    'hr_department_id':crm_browse.hr_department_id.id,
                    'related_to':ids[0]  or False,
                    'user_id':assig_to,
                    'create_date':datetime.datetime.now(),
                    'state':'open',

                    },context=context)
            if opp_into_name=='Morweb':

                description='Step1- select lender' '\n' 'Step2- search product' '\n' 'Step3- select product'
            else:
                description='Step1- enter interest rate type' '\n' 'Step2- select rate type' '\n'  'Step3- select term type' '\n' 'Step4- select frequency' '\n'\
                            'Step5- select compounded period *must be semi-annually' '\n' 'Step5- select amortization''\n' 'Step6- select term'
            project_task.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': 'Select the correct product in' + " " + opp_into_name +" " +'for' + ' ' + app_name + " ",
                    'description':description,
                    'date_deadline': deadline2 ,
                    'hr_department_id':crm_browse.hr_department_id.id,
                    'related_to':ids[0]  or False,
                    'user_id':assig_to,
                    'create_date':datetime.datetime.now(),
                    'state':'open',

                    },context=context)
        deadline3=(create_date + datetime.timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        project_task.create(cr, uid, {
                #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                'name': 'Confirm Lender Acceptance of the Mortgage for' + " " + crm_browse.name ,
                'description':'When we get the final acceptance from the lender, please change the stage of the Opportunity from "Lender Submission" to "Commitment".  This stage change will send congratulatory messages to client and referral source, so please ensure we have first received the approval and commitment package.',
                'date_deadline': deadline3 ,
                'hr_department_id':crm_browse.hr_department_id.id,
                'related_to':ids[0]  or False,
                'user_id':assig_to,
                'create_date':datetime.datetime.now(),
                'state':'open',

                },context=context)
        deadline4=(create_date + datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        project_task.create(cr, uid, {
                #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                'name': 'Select the documents which the lender will require from the list of documents in the Opportunity Record. These documents will be sent automatically to the Lender when stage changes to lender Submission.',
                'description':'',
                'date_deadline': deadline4 ,
                'hr_department_id':crm_browse.hr_department_id.id,
                'related_to':ids[0]  or False,
                'user_id':assig_to,
                'create_date':datetime.datetime.now(),
                'state':'open',

                },context=context)
        
        return True
    def verify_product(self, cr, uid, ids, context=None):
        res_users_obj=self.pool.get('res.users')
        project_task=self.pool.get('project.task')
        crm_browse = self.browse(cr,uid,ids[0])
        desiredproduct  = crm_browse.company_id.uw_desiredProduct or ''
        assig_to_ast,assig_to=uid,uid
        
        try:
            req = urllib2.Request('%s%s'%(desiredproduct,ids[0]))

#            req=urllib2.Request('http://107.23.89.76:8080/UnderWritingApp/services/desiredProduct/3433')
#            req=urllib2.Request('http://107.23.89.76:8080/UnderWritingApp/services/desiredProduct/3502')
            data = urllib2.urlopen(req)
            print "opportunity id:",ids[0]
            notes = json.loads(data.read())
            print"notes",notes
            cr.commit()
        except:
            raise osv.except_osv(('UW App'),("Oops! We're having trouble connecting to UW web service. Please try again."))

   
#        Assistant Notes        
        if 'assistantNotes' in notes.keys():
#            unlink created assistant notes
            if not (notes['assistantNotes'] == None):
                assistant_ids = project_task.search(cr, uid, [('related_to','=',ids[0]),('uw_app','=','desiredProduct'),('user_id.designation','=','assistant')])
                print"assistant_ids",assistant_ids
                
                if assistant_ids:
                    project_task.unlink(cr, uid, assistant_ids)

#                create assistant notes
#	    oppor_id = ids[0]
#            for assis_note in notes['assistantNotes']:
#                print "assis_noteeee:",assis_note
#		if not (assis_note == None):
#	           ass_id = assistant_obj.create(cr, uid, {
#                                                        'note_type':assis_note['noteType'],
#                                                        'urgency':assis_note['urgency'],
#                                                        'description':assis_note['description'],
#                                                        'marketing_field':assis_note['marketingField'],
#							'uw_app':'desiredProduct',
#                                                        'opp_id':oppor_id
#                                                        })
#                   print "ass_id",ass_id
            
            assig_to_ids_ast=res_users_obj.search(cr,uid,[('designation','=','assistant'),('hr_department_id','=',crm_browse.hr_department_id.id)])
            if assig_to_ids_ast:
                assig_to_ast=assig_to_ids_ast[0]
            for assis_note in notes['assistantNotes']:
                deadline=datetime.datetime.strptime(assis_note['deadline'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                start=datetime.datetime.strptime(assis_note['date_start'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                end=datetime.datetime.strptime(assis_note['date_end'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                project_task.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': assis_note['name']  ,
                    'description':assis_note['description'],
                    'date_deadline': str(deadline),
                    'hr_department_id':crm_browse.hr_department_id.id,
                    'related_to':ids[0]  or False,
                    'user_id':assig_to_ast,
                    'create_date':datetime.datetime.now(),
                    'planned_hours':assis_note['planned_hours'],
                    'date_start':str(start),
                    'date_end':str(end),
                    'uw_app':'desiredProduct',
                    'state':'open',


                    },context=context)
 
#        Broker Notes        
        if 'brokerNotes' in notes.keys():
#            unlink created broker notes
            if not (notes['brokerNotes'] == None):
                broker_ids = project_task.search(cr, uid, [('related_to','=',ids[0]),('uw_app','=','desiredProduct'),('user_id.designation','=','broker')])
                if broker_ids:
                    project_task.unlink(cr, uid, broker_ids)
            
#            create broker notes
#            for broker_note in notes['brokerNotes']:
#                print "brokerNotessss:",broker_note
#		if not (broker_note == None):
#	           broker_id = broker_obj.create(cr, uid, {
#                                                        'note_type':broker_note['noteType'],
#                                                        'urgency':broker_note['urgency'],
#                                                        'description':broker_note['description'],
#                                                        'marketing_field':broker_note['marketingField'],
#							'uw_app':'desiredProduct',
#                                                        'opp_id':ids[0]
#                                                        })
#                   print "ass_id",broker_id
            assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','broker'),('hr_department_id','=',crm_browse.hr_department_id.id)])
            if assig_to_ids:
                assig_to=assig_to_ids[0]
            for broker_note in notes['brokerNotes']:
                deadline_b=datetime.datetime.strptime(broker_note['deadline'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                start_b=datetime.datetime.strptime(broker_note['date_start'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                end_b=datetime.datetime.strptime(broker_note['date_end'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                project_task.create(cr, uid, {

                    'name': broker_note['name']  ,
                    'description':broker_note['description'],
                    'date_deadline': str(deadline_b),
                    'hr_department_id':crm_browse.hr_department_id.id,
                    'related_to':ids[0]  or False,
                    'user_id':assig_to,
                    'create_date':datetime.datetime.now(),
                    'planned_hours':broker_note['planned_hours'],
                    'date_start':str(start_b),
                    'date_end':str(end_b),
                    'uw_app':'desiredProduct',
                    'state':'open',

                    },context=context)
        if 'dealNotes' in notes.keys():
            deal_obj = self.pool.get('deal')

#            unlink created deal
            if not (notes['dealNotes']== None):
                deal_ids = deal_obj.search(cr, uid, [('opportunity_id','=',ids[0]),('uw_app','=','desiredProduct')])
                deal_obj.unlink(cr, uid, deal_ids)


            for deal_note in notes['dealNotes']:
                if not (deal_note == None):
                   deal_id = deal_obj.create(cr, uid, {
                                                        'note_type':deal_note['noteType'],
                                                        'urgency':deal_note['urgency'],
                                                        'name':deal_note['description'],
                                                        'marketing_field':deal_note['marketingField'],
							'uw_app':'desiredProduct',
                                                        'opportunity_id':ids[0]
                                                        })
                   print "deal_id",deal_id

        return True

    def all_products(self, cr, uid, ids, context=None):
        res_users_obj=self.pool.get('res.users')
        project_task=self.pool.get('project.task')
        crm_browse = self.browse(cr,uid,ids[0])
        assig_to_ast,assig_to=uid,uid
        uw_allProduct  = crm_browse.company_id.uw_allProduct or ''
#        link='%s%s'%(uw_allProduct,ids[0])
        
	
        try:            
            req = urllib2.Request('%s%s'%(uw_allProduct,ids[0]))
#            print"req",req
#            fhdjfhjf
#            req = urllib2.Request('http://107.23.89.76:8080/UnderWritingApp/services/allProduct/3503')
            data = urllib2.urlopen(req)
            
            notes = json.loads(data.read())
            print "NOTES",notes
            cr.commit()
        except:
            raise osv.except_osv(('UW App'),("Oops! We're having trouble connecting to UW web service. Please try again."))             

#        Assistant Notes
#        notes={"assistantNotes":[{"noteType":"AssistantAction","urgency":"High","description":"assistant","marketingField":'null'},{"noteType":"AssistantAction","urgency":"Low","description":"assistant1","marketingField":'null'}],"brokerNotes":[{"noteType":"BrokerAction","urgency":"Med","description":"brokerNotes","marketingField":'null'},{"noteType":"BrokerAction","urgency":"High","description":"brokerNotes1","marketingField":'null'}],"lenderName":"xxx","cashBack":0,"downpayment":0.0,"insurerfee":0.0,"monthlyPayment":0.0,"totalMortgageAmount":0.0,"trailerCompAmount":0.0,"volumeBonusAmount":0.0,"baseCompAmount":0.0,"marketingCompAmount":0.0,"lenderFee":0.0,"brokerFee":0.0,"totalOneTimeFees":0.0,"totalCompAmount":0.0,"rate":0.0,"amortization":0.0}
#        notes={"assistantTasks":[{"sequence":0,"assigned_to":"Assistant","related_to":"Opportunity.ID","team":"Opportunity.Team","deadline":False,"tags":"","planned_hours":0.1,"date_start":False,"date_end":False,"progress":0.0,"description":"","name":"PATRICIA has no beacon 5 score.  Please confirm they have no credit history.  If they do, please revise opportunity and and re-run all Products."}]}
        if 'assistantTasks' in notes.keys():
#            assistant_obj = self.pool.get('opp.task')

#            unlink created assistant note(s)
            if not (notes['assistantTasks'] == None):
                assisnt_ids = project_task.search(cr, uid, [('related_to','=',ids[0]),('uw_app','=','allProduct'),('user_id.designation','=','assistant')])
                print"assisnt_ids",assisnt_ids
                if assisnt_ids:
                    project_task.unlink(cr, uid, assisnt_ids)


#            create assistant note(s)
            for assis_note in notes['assistantTasks']:
                if not (assis_note == None):
#                   ass_id = assistant_obj.create(cr, uid, {
#                                                        'note_type':assis_note['noteType'],
#                                                        'urgency':assis_note['urgency'],
#                                                        'description':assis_note['description'],
#                                                        'marketing_field':assis_note['marketingField'],
#							'uw_app':'allProduct',
#                                                        'opp_id':ids[0]
#                                                        })
#                   print "ass_id",ass_id
                   assig_to_ids_ast=res_users_obj.search(cr,uid,[('designation','=','assistant'),('hr_department_id','=',crm_browse.hr_department_id.id)])
                   if assig_to_ids_ast:
                        assig_to_ast=assig_to_ids_ast[0]
                   deadline=datetime.datetime.strptime(assis_note['deadline'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                   start=datetime.datetime.strptime(assis_note['date_start'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                   end=datetime.datetime.strptime(assis_note['date_end'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                   project_task.create(cr, uid, {
                        #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                        'name': assis_note['name']  ,
                        'description':assis_note['description'],
                        'date_deadline': str(deadline),
                        'hr_department_id':crm_browse.hr_department_id.id,
                        'related_to':ids[0]  or False,
                        'user_id':assig_to_ast,
                        'create_date':datetime.datetime.now(),
                        'planned_hours':assis_note['planned_hours'],
                        'date_start':str(start),
                        'date_end':str(end),
                        'uw_app':'allProduct',
                        'state':'open',
                        
                   
                        },context=context)

#        Broker Notes
        if 'brokerTasks' in notes.keys():
            project_task=self.pool.get('project.task')
#            unlink created broker notes
            if not (notes['brokerTasks'] == None):
                broker_ids = project_task.search(cr, uid, [('related_to','=',ids[0]),('uw_app','=','allProduct'),('user_id.designation','=','broker')])
                project_task.unlink(cr, uid, broker_ids)

#            unlink created broker 
#            if not (notes['brokerNotes']== None):
#                broker_ids = broker_obj.search(cr, uid, [('opp_id','=',ids[0]),('uw_app','=','allProduct')])
#                broker_obj.unlink(cr, uid, broker_ids)
            
#            create broker
            for broker_note in notes['brokerTasks']:
                
                if not (broker_note == None):	
#                   broker_id = broker_obj.create(cr, uid, {
#                                                        'note_type':broker_note['noteType'],
#                                                        'urgency':broker_note['urgency'],
#                                                        'description':broker_note['description'],
#                                                        'marketing_field':broker_note['marketingField'],
#							'uw_app':'allProduct',
#                                                        'opp_id':ids[0]
#                                                        })
                   assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','broker'),('hr_department_id','=',crm_browse.hr_department_id.id)])
                   if assig_to_ids:
                        assig_to=assig_to_ids[0]
                   deadline_b=datetime.datetime.strptime(broker_note['deadline'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                   start_b=datetime.datetime.strptime(broker_note['date_start'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                   end_b=datetime.datetime.strptime(broker_note['date_end'],'%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
                   project_task.create(cr, uid, {
                        
                        'name': broker_note['name']  ,
                        'description':broker_note['description'],
                        'date_deadline': str(deadline_b),
                        'hr_department_id':crm_browse.hr_department_id.id,
                        'related_to':ids[0]  or False,
                        'user_id':assig_to, 
                        'create_date':datetime.datetime.now(),
                        'planned_hours':broker_note['planned_hours'],
                        'date_start':str(start_b),
                        'date_end':str(end_b),
                        'uw_app':'allProduct',
                        'state':'open',

                        },context=context)
                   


#       marketing template
        if 'marketingTemplateNotes' in notes.keys():
            deal_obj = self.pool.get('deal')

#            unlink created marketing template
            if not (notes['marketingTemplateNotes']== None):
                deal_ids = deal_obj.search(cr, uid, [('opportunity_id','=',ids[0]),('uw_app','=','allProductmarketingtemplate')])
                deal_obj.unlink(cr, uid, deal_ids)


            for marketing_template in notes['marketingTemplateNotes']:
                print "marketing_template:",marketing_template
                if not (marketing_template == None):
                   marketing_template_id = deal_obj.create(cr, uid, {
                                                        'note_type':marketing_template['noteType'],
                                                        'urgency':marketing_template['urgency'],
                                                        'name':marketing_template['description'],
                                                        'marketing_field':marketing_template['marketingField'],
							'uw_app':'allProductmarketingtemplate',
                                                        'opportunity_id':ids[0]
                                                        })
                   


#        Deal Notes
        if 'dealNotes' in notes.keys():
            deal_obj = self.pool.get('deal')

#            unlink created deal
            if not (notes['dealNotes']== None):
                deal_ids = deal_obj.search(cr, uid, [('opportunity_id','=',ids[0]),('uw_app','=','allProduct')])
                deal_obj.unlink(cr, uid, deal_ids)


            for deal_note in notes['dealNotes']:
                if not (deal_note == None):
                   deal_id = deal_obj.create(cr, uid, {
                                                        'note_type':deal_note['noteType'],
                                                        'urgency':deal_note['urgency'],
                                                        'name':deal_note['description'],
                                                        'marketing_field':deal_note['marketingField'],
							'uw_app':'allProduct',
                                                        'opportunity_id':ids[0]
                                                        })
                   print "deal_id",deal_id

#        Recommendations
	if 'recommendations' in notes.keys():
           
            if notes['recommendations']:                
                recommendations_obj = self.pool.get('opp.recommendations')
#                unlink created recommendations
                recommendation_ids  = recommendations_obj.search(cr, uid, [('opp_id','=',ids[0]),('uw_app','=','allProduct')])
                if recommendation_ids:
                    recommendations_obj.unlink(cr, uid, recommendation_ids)

#                create recommendation
                if notes['recommendations']:
                    for recommend_note in notes['recommendations']:
                        if not (recommend_note == None):
        #                    product id
                            product_ids = self.pool.get('product.product').search(cr, uid, [('name_template','ilike',recommend_note['productName'])], limit=1) or ''
                            pr_id = ''
                            if product_ids:
                                pr_id = product_ids[0]
        #                    lender id
                            lender_id = self.pool.get('res.partner').search(cr, uid, [('name','ilike',recommend_note['lenderName'])], limit=1)
                            lender = ''
                            if lender_id:
                                lender = lender_id[0]
        #                    mortgage dictionary
                            mortgage_dict = {'1':'LOC','2':'Variable','3':'Fixed','4':'Cashback','5':'Combined'}                           
                            if recommend_note['mortgageType'] in mortgage_dict.keys():
                                mortgage_type = recommend_note['mortgageType']
                            else:
                                mortgage_type = '6'
        #                 term dictionary
                            term_dict = {'1':'6 Months','2':'1 Year','3':'2 Year','4':'3 Year','5':'4 Year','6':'5 Year','7':'6 Year','8':'7 Year','9':'8 Year','10':'9 Year','11':'10 Year'}
                            if recommend_note['term'] in term_dict.keys():
                                term = recommend_note['term']
                            else:
                                term = '12'
                            recommend_id = recommendations_obj.create(cr, uid, {
                                                                    'name' : recommend_note['rate'],
                                                                    'lender':lender,
                                                                    'product':pr_id,
                                                                    'mortgage_type':mortgage_type,
                                                                    'term':term,
                                                                    'maximum_amortization':recommend_note['amortization'],
                                                                    'interest_rate':recommend_note['rate'],
                                                                    'mortgage_amount':recommend_note['mortaggeAmout'],
                                                                    'mortgage_payment':recommend_note['payment'],
                                                                    'cashback':recommend_note['cashback'],
                                                                    'position':recommend_note['position'],
                                                                    'uw_app':'allProduct',
                                                                    'opp_id':ids[0]
                                                                    })
                            print "recommend_id$$$$$$$$$$$$$$$$$$$$$$",recommend_id
                    
        return True



    def onchange_partner_id(self, cr, uid, ids, part, email=False):
        data = super(crm_lead,self).onchange_partner_id(cr, uid, ids, part, email=False)
        if data:
            res = data['value']
            #get values to append
            obj_res_partner = self.pool.get('res.partner').browse(cr,uid,part)
            m_name = obj_res_partner.middle_name or ''
            l_name = obj_res_partner.last_name or ''
            Spouse = obj_res_partner.spouse or ''            
            mobile = obj_res_partner.mobile or ''
            applicant_work = obj_res_partner.work_phone or ''
            res['applicant_middle_name'] = m_name
            res['applicant_last_name'] = l_name
            res['Spouse'] = Spouse
            res['applicant_cell'] = mobile
            res['applicant_work']= applicant_work
            return {'value': res} 
        else:
            return {'value': data}

    def onchange_co_applicant_name(self, cr, uid, ids, co_applicant_name=False, email=False):
        if co_applicant_name :
            m_name = self.pool.get('res.partner').browse(cr, uid, co_applicant_name).middle_name or ''
            l_name = self.pool.get('res.partner').browse(cr, uid, co_applicant_name).last_name or ''
            email_work = self.pool.get('res.partner').browse(cr, uid, co_applicant_name).email or ''
            co_applicant_phone = self.pool.get('res.partner').browse(cr, uid, co_applicant_name).phone or ''
            co_applicant_cell = self.pool.get('res.partner').browse(cr, uid, co_applicant_name).mobile or ''
            co_applicant_work = self.pool.get('res.partner').browse(cr, uid, co_applicant_name).work_phone or ''
                        
            return {'value':{'co_applicant_middle_name': m_name, 'co_applicant_last_name':l_name, 'co_applicant_mail': email_work, 'co_applicant_phone': co_applicant_phone, 'co_applicant_cell':co_applicant_cell, 'co_applicant_work':co_applicant_work}}
        else:    
            return {'value':{'co_applicant_middle_name': False, 'co_applicant_last_name':False }}
    
        
    def onchange_date_difference(self, cr, uid, ids, Date_Moved_out=False, Date_Moved_In=False, context=None):  
        print Date_Moved_out,Date_Moved_In
        if Date_Moved_out and Date_Moved_In:
           print Date_Moved_out,Date_Moved_In
           d1 = datetime.strptime(Date_Moved_out,"%Y-%m-%d")
           d2 = datetime.strptime(Date_Moved_In,"%Y-%m-%d")
           diff = (d1-d2).days
           print "diff",diff
           if diff < 0 :
               return {'value':{'total_time_address_calculation': 0}}
           return {'value':{'total_time_address_calculation': diff}}
        else:
            return {'value':{'total_time_address_calculation': 0}}  

    def total_value(self, cr, uid, ids, context=None):        
        crm_lead_browse = self.pool.get('crm.lead').browse(cr,uid,ids[0])
        sum  = 0
        for each_crm_asset_object in crm_lead_browse.asset_ids:
            sum = sum + each_crm_asset_object.value                
        self.write(cr, uid, ids, {'total_asset' : sum}, context=context)

        
	    
    def action_opportunity_send(self, cr, uid, ids, context=None):
        
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        mod_obj = self.pool.get('ir.model.data')        
        template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_edi_opprtunity')
        template_id = template and template[1] or False
        res = mod_obj.get_object_reference(cr, uid, 'mail', 'email_compose_message_wizard_form')
        res_id = res and res[1] or False        
        ctx = dict(context)
        print "template_id=========",template_id
        ctx.update({
            'default_model': 'crm.lead',
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

crm_lead()


class number_suffix(osv.osv):
     _name = 'number.suffix'
     _columns = {
            'name':fields.char('Number Suffix', size=128),
        }
   
number_suffix() 


class street_type(osv.osv):
     _name = 'street.type'
     _columns = {
            'name':fields.char('Street Type', size=128),
        }  
street_type() 

class street_direction(osv.osv):
     _name = 'street.direction'   
     _columns = {
            'name':fields.char('Direction', size=128),
            }
street_direction()

class crm_asset(osv.osv):
    _name = 'crm.asset'
    _columns = {            
            'opportunity_id':fields.many2one('applicant.record','Opportunity Reference', invisible = True),            
            'asset_type':fields.selection([('Vehicle','Vehicle'),('RRSPs','RRSPs'),('Non-RRSPs','Non-RRSPs'),('other','Other')],'Type'),   
            'name': fields.text('Description',),
            'value': fields.float('Value'),
            }
crm_asset()


class crm_liability(osv.osv): 
    _name = 'crm.liability'
    _columns = {
            'liability_id':fields.many2one('crm.lead','Opportunity Reference', invisible = True),
#            'liability_types':fields.many2one('liability.type','Liability Type'),
            'Liability_Type':fields.selection([('Personal_Loan','Personal Loan'),('Secured_Loan','Secured Loan'),('Car_Loan','Car Loan'),('Lease_Agreement','Lease Agreement'),('Credit_Card','Credit Card'),('Line_of_Credit','Line of Credit'),('Child_Support','Child Support'),('Other','Other')],'Liability Type'),
#            'Liability_Type_Credit_Card':fields.selection([('Visa','Visa'),('Mastercard','Mastercard'),('American_Express','American Express'),('Store_Card','Store Card'),('other','Other')],'Credit Card', nolabel=True),
            'Lender':fields.many2one('res.partner','Lender'),
            'name':fields.text('Description'),
            'Credit Limit':fields.float('Credit Limit'),
            'Credit Balance':fields.float('Credit Balance'),
            'Monthly Payment':fields.float('Monthly Payment'),
            'Maturity Date':fields.date('Maturity Date'),
            'pay_off':fields.integer('Pay Off'),
        }
crm_liability()

class liability_type(osv.osv):
    _name = 'liability.type'
    _columns = {
        'name':fields.char('Liability Name',size=128),
    }
liability_type()

#class mail_compose_message(osv.osv):
#    _inherit = 'mail.compose.message'
#    def send_mail(self, cr, uid, ids, context=None):
#        context = context or {}
#        if context.get('mark_so_as_sent', False) and context.get('default_res_id', False):
#            wf_service = netsvc.LocalService("workflow")
#            wf_service.trg_validate(uid, 'sale.order', context.get('default_res_id', False), 'quotation_sent', cr)
#        return super(mail_compose_message, self).send_mail(cr, uid, ids, context=context)
#
#mail_compose_message()


class deal(osv.osv):
    _name = 'deal'
    _columns = {
        'name':fields.text('Description',size=128),
        'note_type':fields.selection([('Change','Change'),('Info','Info'),('AssistantAction','Assistant Action'),('BrokerAction',' Broker Action'),('ProposalInfo','Proposal Info'),('LenderInfo','Lender Info')],'Note Type'),
        'urgency':fields.selection([('Low','Low'),('Med','Medium'),('High','High'),('Highest','Highest')],'Urgency'),    
        'opportunity_id':fields.many2one('crm.lead','Opportunity Reference'),       
        'marketing_field':fields.char('Marketing Field'),
	'uw_app':fields.char('uw App',size=120)
    }
deal()

class opp_task(osv.osv):
    _name = 'opp.task'
    _rec_name = 'note_type'	
    _columns = {
                'note_type':fields.selection([('Change','Change'),('Info','Info'),('AssistantAction','Assistant Action'),('BrokerAction',' Broker Action'),('ProposalInfo','Proposal Info'),('LenderInfo','Lender Info')],'Note Type'),
                'done':fields.boolean('Done'),
                'urgency':fields.selection([('Low','Low'),('Med','Medium'),('High','High'),('Highest','Highest')],'Urgency'),
                'description':fields.text('Description'),
                'opp_id':fields.many2one('crm.lead','Opportunity'),
                'marketing_field':fields.char('Marketing Field'),
		'uw_app':fields.char('uw App',size=120)	
    }
opp_task()

class broker_task(osv.osv):
    _name = 'broker.task'
    _rec_name = 'note_type'
    _columns = {
                'note_type':fields.selection([('Change','Change'),('Info','Info'),('AssistantAction','Assistant Action'),('BrokerAction',' Broker Action'),('ProposalInfo','Proposal Info'),('LenderInfo','Lender Info')],'Note Type'),
                'done':fields.boolean('Done'),
                'urgency':fields.selection([('Low','Low'),('Med','Medium'),('High','High'),('Highest','Highest')],'Urgency'),
                'description':fields.text('Description'),
                'opp_id':fields.many2one('crm.lead','Opportunity'),
                'marketing_field':fields.char('Marketing Field'),
		'uw_app':fields.char('uw App',size=120)	
    }
broker_task()

#       Recommendations
class opp_recommendations(osv.osv):
    _name = 'opp.recommendations'
    _columns = {
            'mortgage_type': fields.selection([('1','LOC'),('2','Variable'),('3','Fixed'),('4','Cashback'),('5','Combined'),('6','Other')],'Mortgage Type'),            
            'lender':fields.many2one('res.partner','Lender'),
            'product':fields.many2one('product.product','Product'),
	    'name': fields.float('Interest Rate',),

           
            'qualifying_rate': fields.float('Qualifying Rate',),
            'posted_rate':fields.float('Posted Rate'),
            'term':fields.selection([('1','6 Months'),('2','1 Year'),('3','2 Year'),('4','3 Year'),('5','4 Year'),('6','5 Year'),('7','6 Year'),('8','7 Year'),('9','8 Year'),('10','9 Year'),('11','10 Year'),('12','Other')],'Term'),
            'cashback':fields.float('Cashback Percent'),
            'mortgage_amount':fields.float('Mortgage Amount'),
            'mortgage_payment':fields.float('Payment'),
            'cashback_percent':fields.float('Cashback Percent'),
            'position':fields.char('Position',size=40),
            'maximum_amortization': fields.float('Maximum Amortization'),
            'opp_id':fields.many2one('crm.lead','opportunity'),
	    'uw_app':fields.char('UW Algo',size=120)
        }

opp_recommendations()

class app_documents(osv.osv):
    _name='app.documents'
    _columns={
        'document_data':fields.binary('Document',size=256),
        'document_date':fields.datetime('Date'),
        'created_by':fields.many2one('res.users','Created By'),
        'doc_send':fields.boolean('Send'),
        'opportunity_id':fields.many2one('crm.lead','Opporutnity'),
        'applicant_id':fields.many2one('applicant.record','Applicant'),
        'document_name':fields.char('Document Name'),
	'ir_attachment_id':fields.many2one('ir.attachment','Attachment ID'),
    }
    _defaults={
        'document_date':lambda *a: time.strftime("%Y-%m-%d"),
        #'created_by':lambda obj, cr, uid, context: uid,
    }




    '''def onchange_doc_send(self,cr,uid,ids,doc_send,document_name,document_data,opportunity_id,context=None):
        print"doc_send",doc_send
        vals={}
        ir_attachment = self.pool.get('ir.attachment')
        attachment_ids=[]
        if doc_send==True:
            attachment_data = {
                    'name': document_name,
                    'datas_fname': document_name,
                    'datas': document_data,
                    'res_model': 'crm.lead',
                    'res_id': opportunity_id,
                    'send_doc':True,
                    
                }
            attachment_ids.append(ir_attachment.create(cr, uid, attachment_data, context=context))
        
        
        return {'value':vals}'''
    def create(self,cr,uid,vals,context=None):
	#print "uid-------------------------------",uid
	#vals.update({'created_by':uid})

        res = super(app_documents, self).create(cr, uid, vals)
        print"res",res
        opportunity_obj=self.pool.get('crm.lead')
        opportunity_id=opportunity_obj.search(cr,uid,[('document_ids','in',res)])
        if opportunity_id:
            opportunity_id=opportunity_id[0]
        app_doc_browse=self.browse(cr,uid,res)
        ir_attachment = self.pool.get('ir.attachment')
        if vals.get('doc_send',False):
            if vals.get('doc_send')==True:
                attachment_data = {
                        'name': app_doc_browse.document_name,
                        'datas_fname': app_doc_browse.document_name,
                        'datas': app_doc_browse.document_data,
                        'res_model': 'crm.lead',
                        'res_id': opportunity_id,
                        'send_doc':True,

                    }
                attachment_id=ir_attachment.create(cr, uid, attachment_data, context=context)
                self.write(cr,uid,[res],{'ir_attachment_id':int(attachment_id)},context)
            else:
                attachment_id=app_doc_browse.ir_attachment_id.id
                if attachment_id:
                    ir_attachment.write(cr,uid,[attachment_id],{'send_doc':False},context)
        return res

    def write(self,cr,uid,ids,vals,context):
        res = super(app_documents, self).write(cr, uid, ids, vals)
        opportunity_obj=self.pool.get('crm.lead')
        opportunity_id=opportunity_obj.search(cr,uid,[('document_ids','in',ids)])
        if opportunity_id:
            opportunity_id=opportunity_id[0]
        app_doc_browse=self.browse(cr,uid,ids[0])
        print"app_doc_browse",app_doc_browse
        ir_attachment = self.pool.get('ir.attachment')
        if vals.has_key('doc_send'):
            if vals.get('doc_send')==True:
                attachment_data = {
                        'name': app_doc_browse.document_name,
                        'datas_fname': app_doc_browse.document_name,
                        'datas': app_doc_browse.document_data,
                        'res_model': 'crm.lead',
                        'res_id': opportunity_id, 
                        'send_doc':True,

                    }
                attachment_id=ir_attachment.create(cr, uid, attachment_data, context=context)
                self.write(cr,uid,ids,{'ir_attachment_id':attachment_id},context)
            else:
                attachment_id=app_doc_browse.ir_attachment_id.id
                print"attachment_id",attachment_id
                if attachment_id:
                    ir_attachment.write(cr,uid,[attachment_id],{'send_doc':False},context)
                    

        return res
    
app_documents()
