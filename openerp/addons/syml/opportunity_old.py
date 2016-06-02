from osv import fields,osv
from datetime import datetime   
from base_status.base_stage import base_stage
import tools
from tools.translate import _
from tools import html2plaintext
from datetime import date

class crm_lead(osv.osv):
    _inherit = 'crm.lead'
    _columns={
        
        ###General###
        'application_date':fields.datetime('Application Date'),
        'condition_of_financing_date':fields.char('Condition of Financing Date',size=120),
        'expected_closing_date':fields.char('Expected Closing Date',size=120),
        
        'sales_associate':fields.char('Sales Associate',size=120),
        'assistant':fields.many2one('res.partner','Assistant'),
        'underwriter':fields.char('Underwriter',size=240),
        'referred_source':fields.char('Referred Source',size=240),
        'training_associate_referral':fields.char('Training Associate Referral',size=240),
        'lead_source':fields.char('Lead Source',size=240),
        'realtor':fields.char('Realtor',size=240),

        

        'Broker':fields.many2one('res.partner','Broker.'),
        'applicant_record_line': fields.one2many('applicant.record', 'applicant_id', 'Applicant Lines'),
        'broker':fields.many2one('res.partner','Broker'),
        
        'application_start_time':fields.datetime('Application Start Time'),
        
        
        'whatisyourlendinggoal':fields.selection([('1','Pre-Approved'),('2','Approved'),('3','Refinance')],'Lending Goal'),
        'preapprovedimlookingfora':fields.selection([('1','Condo/Mobile Home'),('2','House/Townhouse/Duplex/Acreage'),('3','Rental Property'),('4','Raw Land Leased land'),('5','Vacation Property/Second Home'),('6',"Not sure, I just want to know the maximum I can borrow.")],"I'm Looking for a"),
        'approvedimlookingfora':fields.selection([('1','Build a property'),('2','Buy an existing finished property(House, Acreage, Condo, Land)'),('3','Get additional funds to renovate and purchase to increase the value of my property?'),('4','Keep my existing mortgage and port it to my new property?')],"I'm looking for a"),
        'refinancelookingfora':fields.selection([('1','Refinance my property to get money to purchase another property.'),('2','Reduce Interest Rate on My Mortgage.'),('3','Renew Mortgage'),('4','Increase Mortgage Amount')],"I'm looking for a"),









        'total_asset':fields.char('Total',size=128, readonly=True),
        'applicant_middle_name':fields.char('Middle Name', size=240),
        'applicant_last_name':fields.char('Last Name', size=240),
        'applicant_cell':fields.char('Cell Number',size=64),        
        'applicant_work':fields.char('Work Number',size=64),
        
        'co_applicant_name':fields.many2one('res.partner','First Name'),
        'co_applicant_middle_name':fields.char('Middle Name', size=240),
        'co_applicant_last_name':fields.char('Last Name', size=240),
        'date_created': fields.date('Date Created'),
        'co_applicant_work':fields.char('Work Number', size=64),
        'co_applicant_cell':fields.char('Cell Number', size=64),
        'co_applicant_phone':fields.char('Home Phone Number', size=64),
        'co_applicant_mail':fields.char('Email Address', size=128),        
        'ltv': fields.float('LTV (Loan to Value: %)',), 
        'gds': fields.float('GDS'),
        'tds': fields.float('TDS'),
#        'asset_type':fields.selection([('bank_account','Bank Account'),('insurance_policy','Insurance Policy'),('rrsp','RRSP'),('vehicle','Vehicle'),('investment','Investments'),('other','Others')],'Asset Type'),
#        'description':fields.char('Description', size=240),        
        'addition_asset_holder':fields.boolean('Are there any addition asset holder'),
        'dob_co_applicant': fields.date('DOB'),
        'date_created_co_applicant': fields.date('Date Created'),
        'Additional_asset_holder_details':fields.text('Additional asset holder (s) details'),
        
        ####################    personal detail
        'license_number':fields.char('Number', size=16),
        'license_issuing_province':fields.many2one('res.country.state','Issuing Province'),
        'credit_beacon_score':fields.char('Credit Beacon Score', size=240),
        'canadian_resident':fields.selection([('yes','YES'),('no','NO')],'Canadian Resident'),
        'marital_status':fields.selection([('Single','Single'),('Married','Married'),('Divorced','Divorced'),('Common-Law','Common Law'),('Separated','Separated')],'Marital Status'),
        'marital_status_separated':fields.char('Number Of Dependants', size=240),
        'issuing_province_canada':fields.many2one('res.country','country'),

         ################### employment/other income   
        'employment_status':fields.selection([('employed','Employed'),('self_employed','Self-Employed'),('commission_sales','Commission Sales'),('hourly_wage','Hourly Wage'),('retired','Retired'),('homemaker','Homemaker'),('other','Other')],'Status'),
        'company_name':fields.char('Company Name',size=240),
        'employment_type':fields.selection([('permanent_full_time','permanent full-time'),('permanent_part_time','permanent part-time'),('temporary_full_time','temporary full-time'),('temporary_part_time','temporary part-time'),('permanent_seasonal','permanent seasonal'),('temporary_seasonal','temporary seasonal')],'Type'),
        'industry_type':fields.selection([('Construction','Construction'),('Government','Government'),('Health','Health'),('Education','Education'),('HiTech','HiTech'),('Retail Sales','Retail Sales'),('Leisure/Entertainment','Leisure/Entertainment'),('Banking/Finance','Banking/Finance'),('Transport','Transport'),('Services','Services'),('Manufacturing','Manufacturing'),('Other','Other')],'Industry Type'),
        'occupation-type':fields.selection([('Clerical','Clerical'),('labourer_tradesperson','Labourer/Tradesperson'),('retired','Retired'),('professional','Professional'),('Self-Employed','Self-Employed'),('other','Other')],'Occupation Type'),
        'Job Title':fields.char('Job Title',size=240),
        'start_date':fields.date('Start Date'),
        'Add Income':fields.selection([('basic','Basic'),('overtime','Overtime'),('commission','Commission'),('Interest/Dividends','Interest/Dividends'),('government_pension','Government Pension'),('private_pension','Private Pension'),('other','Other')],'Add Income'),
        'amount':fields.float('Amount'),
        'frequency':fields.selection([('annually','Annually'),('semi-Annually','Semi-Annually'),('quarterly','Quarterly'),('monthly','Monthly'),('Semi-Monthly','Semi-Monthly'),('bi-Weekly','Bi-Weekly'),('weekly','Weekly')],'Frequency'),
        'other_income_description':fields.selection([('pension','Pension'),('support','Support'),('alimony','Alimony'),('car_allowance','Car Allowance'),('other','Other')],'Description'),
        'other_income_amount':fields.selection([('annually','Annually'),('semi-Annually','Semi-Annually'),('quarterly','Quarterly'),('monthly','Monthly'),('Semi-Monthly','Semi-Monthly'),('bi-Weekly','Bi-Weekly'),('weekly','Weekly')],'Amount'),
    
        ####################### Address Summary
        'lender':fields.many2one('res.partner','Lender'),
        'opportunity_street': fields.char('Street Number', size=128),
        'opportunity_street_name': fields.char('Street Number', size=128),
        'number_suffix':fields.many2one('number.suffix','Number Suffix'),        
        'unit_suit_apt':fields.char('Unit/Suit/Apt', size=128),
        'opportunity_province':fields.many2one('res.country.state','Province'),
        'opportunity_zip': fields.char('Zip', change_default=True, size=24),        
        'opportunity_state_id': fields.many2one("res.country.state", 'State'),
        'opportunity_country_id': fields.many2one('res.country', 'Country'),
        'street_type':fields.many2one('street.type','Street Type'),
        'direction':fields.many2one('street.direction','Direction'),
        'address_type':fields.selection([('Primary_Residence','Primary Residence'),('Correspondence','Correspondence'),('Previous','Previous'),('Additional_Current','Additional Current'),('Recreational','Recreational')],'Address Type'),
        'occupancy_status':fields.selection([('Owner_Occupied','Owner Occupied'),('Tenant','Tenant'),('Partial','Partial'),('Rental_Property','Rental Property')],'Occupancy Status'),
        'What_are_you_doing':fields.selection([('Selling','Selling'),('Not_Selling','Not Selling'),('Not_Selling_Renting','Not Selling-Renting')],'What are you doing with this property'),
        'total_time_address_calculation': fields.char('Total Time @ Address (Days)', size=128),
        'Date_Moved_In':fields.date('Date Moved In', ),
        'Date_Moved_out':fields.date('Date Moved Out',),
        'Property_Address': fields.char('Property Address', size=128),
        'Mortgage_Number': fields.char('Mortgage Number', size=128),
        
        'Previous_Closing_Date': fields.date('Previous Closing Date'),
        'Previous_Sale_Price':fields.float('Previous Sale Price'),
        'Maturity_Date': fields.date('Maturity Date'),
        'Interest_Rate':fields.float('Interest Rate'),
        'Original_Mortgage_Amount': fields.char('Original Mortgage Amount', size=128),
        'Balance_Mortgage_Amount': fields.char('Balance Mortgage Amount', size=128),
        'Monthly_Payment': fields.char('Monthly Payment', size=128),
        'Existing_Mortgages_charge_type':fields.selection([('first','First'),('second','Second'),('third','Third'),('fourth','Fourth'),('bridge','Bridge')],'Charge Type'),
        'Existing_Mortgages_Rate_Type':fields.selection([('Fixed','Fixed'),('arm','ARM'),('Floating_Rate','Floating Rate'),('Monthly_Charge','Monthly Charge')],'Rate Type'),
        'Existing_Mortgages_Payment':fields.selection([('Blended_P&I','Blended P&I'),('interest_only','Interest Only')],'Payment'),
        'Existing_Mortgages_status':fields.selection([('To_be_Paid','To be Paid'),('Remaining','Remaining')],'Status'),
        'Mortgage_Insurer':fields.selection([('CMHC','CMHC'),('Genworth','Genworth'),('Canada_Guaranty','Canada Guaranty'),('PMI','PMI'),('other','other'),('GMAC_Lender','GMAC Lender'),('Self_Insured_Lender_Fee','Self-Insured Lender Fee'),('Premium_Amount','Premium Amount'),('Insured_Amount','Insured Amount'),('Mortgage_Insurance_Number','Mortgage Insurance Number')],'Mortgage Insurer'),

######################## Loans/Liabilities
        'liability_detail':fields.one2many('crm.liability','liability_id','Liability'),
        'Liability_Type':fields.selection([('Personal_Loan','Personal Loan'),('Secured_Loan','Secured Loan'),('Car_Loan','Car Loan'),('Lease_Agreement','Lease Agreement'),('Credit_Card','Credit Card'),('Line_of_Credit','Line of Credit'),('Child_Support','Child Support'),('Other','Other')],'Liability Type'),
        'Liability_Type_Credit_Card':fields.selection([('Visa','Visa'),('Mastercard','Mastercard'),('American_Express','American Express'),('Store_Card','Store Card'),('other','Other')],'Credit Card'),
        'Outstanding_Balance':fields.float('Outstanding Balance'),
        'Monthly_Payment':fields.float('Monthly Payment'),
        'Credit_Limit':fields.float('Credit Limit'),
        'end_Date': fields.date('End Date'),
        
#        lender
        'Account_Number':fields.char('Account Number',size=240,),
        'Is_the_balance_to_be_repaid_by_completion_of_the_new_loan':fields.boolean('Is the balance to be repaid by completion of the new loan'),
        'Are there any additional loan/liabilities holders':fields.boolean('Are there any additional loan/liabilities holders'),
        'Exclude_from_TDS':fields.boolean('Exclude from TDS'),
        'Modify credit check results':fields.boolean('Modify credit check results'),
        'Explain modification from credit bureau':fields.text('Explain modification from credit bureau',),
        'Customer_Name':fields.many2one('res.partner', 'Customer Name'),
        'Amount_of_Debt':fields.float('Amount of Debt'),
        'Date_Declared': fields.date('Date Declared'),
        'monthly_payment':fields.float('Monthly Payment'),
        'Date_of_Decharge': fields.date('Date of Decharge'),
        'Other_Details':fields.text('Other Details',),
        
########  Lender Interaction

        'Application_Details':fields.char('Application Details',size=240),
        'Transaction_Numer':fields.char('Transaction Numer',size=240),
        'Application_Priority':fields.char('Application Priority',size=240),
        'Application_Status':fields.selection([('New application','New application'),('New quotation','New quotation'),('Submitted','Submitted'),('Partially submitted','Partially submitted'),('Decision Pending','Decision Pending'),('Approved','Approved'),('Partially approved','Partially approved'),('Funded','Funded'),('Partially funded','Partially funded')],'Application Status'),
        'Agent':fields.many2one('res.partner','Agent'),
        
        'Adminstrator':fields.many2one('res.partner','Adminstrator'),
        'Application Owner':fields.many2one('res.partner','Application Owner'),
#        'Lender Submissions':fields.selection([('Quotation','Quotation'),('Lender','Lender'),('Time','Time'),('Status','Status'),('PAPP','PAPP')],'Lender Submissions'),
        'Lender_Submissions_Quotation':fields.char('Quotation',size=240),
        'Lender Submissions_lender':fields.many2one('res.partner','Lender'),
        'Lender Submissions_time':fields.datetime('Time'),
        'Lender Submissions_Status':fields.char('Status',size=240),
        'papp':fields.char('PAPP',size=240),
        #'Underwriter':fields.char('Underwriter',size=240),
        'Quotation_Status':fields.selection([('Approved','Approved'),('Declined','Declined'),('funded','funded')],'Quotation Status'),
#        'Lender Response':fields.selection([('type','Type'),('date','Date'),('user','User'),('Comments','Comments')],'Quotation Status'),
        'lender_responce_type':fields.char('Type',size=240),
        'lender_responce_user':fields.many2one('res.partner','User'),
        'lender_responce_date':fields.date('Date'),
        'Comments':fields.char('Commments',size=240),
        
#        'Conditions':fields.selection([('type','Type'),('date','Date'),('user','User'),('Comments','Comments')],'Quotation Status'),
        
        'lender_responce_condition_name':fields.char('Name',size=240),
        'lender_responce_condition_status':fields.char('Status',size=240),
        'lender_responce_condition_type':fields.char('Type',size=240),
        'lender_responce_condition_updated_by':fields.many2one('res.partner','Updated by'),
        'lender_responce_condition_time':fields.datetime('Time'),
        
        'condition_status':fields.selection([('Required','Required'),('Received','Received'),('Accepted','Accepted'),('UnAccepted','UnAccepted'),('waived','Waived')],'Condition Status'),
        'documents':fields.text('Documents',),
        
#        
        'initial_submisson':fields.date('Initial Submisson'),
        'communication':fields.char('Communication',size=124),
        'Full 2 way feeb to lender specific system':fields.char('Full 2 way feeb to lender specific system',size=124),
        'submitter_of_record_agent':fields.many2one('res.partner','Agent'),
        'submitter_of_record_broker':fields.many2one('res.partner','Broker'),
       
       
##################   loan details

        'active_loan': fields.boolean('Active'),
        'submitted': fields.boolean('Submitted'),
        'pre_approval': fields.boolean('Pre-Approval'),
        'type_of_buyer':fields.selection([('first_time', 'First Time'),('repeat', 'Repeat')], 'Type Of Buyer'),
        'ltv':fields.float('LTV'),
        'funding_date': fields.date('Funding Date', ),
        'purpose_of_loan':fields.selection([('refinance','Refinance'),('equity_take_out','Equity Take Out'),('house_purpose','House Purpose'),('transfer','Transfer'),('increase_transfer','Increase Transfer'),('port','Port')],'Purpose of Loan'),
        'purchase_price':fields.float('Purchase Price'),
        'improvements':fields.char('Improvements',size=240),
        'amount_requested':fields.float('Amount Requested'),

#        downpayment
        'sources':fields.selection([('cash_from_own_resources','Cash From Own Resources'),('rrsp','RRSP'),('borrowed_agaisnt_liquid_assets','Borrowed Agaisnt Liquid Assets'),('gift','Gift'),('sale_of_other_property','Sal Of Other Property'),('government_grant','Government Grant'),('equity','Equity'),('sweat_equity ','Sweat Equity'),('other','Other')],'Sources'),
        'downpayment_amount':fields.char('Down Payment Amount',size=120),

        #cost details
        'first_mortgage':fields.float('First Mortgage'),
        'second_mortgage':fields.float('Second Mortgage'),
        'third_mortagage':fields.float('Third Mortgage'),

        #source
        'residential_application':fields.char('Residential Application',size=124),
        'Appraisal_or_Inspection':fields.char('Appraisal or Inspection',size=124),
        'Bridge':fields.float('Bridge'),
        'Commitment_Fee':fields.float('Commitment Fee'),
        'Property_Tax':fields.float('Property Tax'),
        'Broker_Fee':fields.float('Broker Fee'),
        'Survey_Cost':fields.float('Survey Cost'),
        'Lender_Legal_Fee/Disbursements':fields.float('Lender Legal Fee/Disbursements'),
        'Other_Legal_Fee/Disbursements':fields.float('Other Legal Fee/Disbursements'),
        'Pri_Mor_Fees':fields.float('Pri-Mor Fees'),
        'Other':fields.char('Other',size=240),

        #payor
        'payor':fields.selection([('Appraiser','Appraiser'),('Borrower','Borrower'),('Insurer','Insurer'),('Investor','Investor'),('Legal','Legal'),('Lender','Lender'),('Broker','Broker'),('Other','Other')],'Payor'),
        'Deduct':fields.boolean('Deduct'),
        'Payment':fields.float('Payment'),

        #charge Details
        'Charge_Type':fields.selection([('first','First',),('second','Second'),('third','Third'),('fourth','Fourth'),('bridge','Bridge')],'Charge Type'),
        'Insurance Type':fields.selection([('CMHC','CMHC',),('Genworth','Genworth'),('Canada Guaranty','Canada Guaranty'),('Other','Other'),('Self-Insured Lender Fee','Self-Insured Lender Fee'),('Amount','Amount'),('LTV','LTV')],'Insurance Type'),
        'Service Type':fields.selection([('Basic','Basic'),('Full','Full'),('Basic EE Rebate','Basic EE Rebate'),('Firm EE Rebate','Firm EE Rebate'),('Low Ratio','Low Ratio'),('GVS','GVS'),('Other','Other'),('Full Documentation','Full Documentation'),('Limit Documentation','Limit Documentation'),('Reduced Documentation','Reduced Documentation'),('Owner Occupied','Owner Occupied'),('Rental','Rental')],'Service Type'),
        'Amount':fields.float('Amount'),
        'LTV':fields.char('LTV'),
        'Repayment Type':fields.selection([('Blended P & I','Blended P & I'),('Interest Only','Interest Only')],'Repayment Type'),

        'term_years':fields.date('Term Years'),
        'Amortization_years':fields.date('Amortization Years'),
        'Net Rate':fields.float('Net Rate'),
        'Qualifying Rate':fields.float('Qualifying Rate'),

        #Lender Selection
        'Search Product':fields.many2one('product.product','Desired Product Type'),
        #All lenders
        'Institutional':fields.boolean('Institutional'),
        'Private':fields.boolean('Private'),
        #Rate Details
        'posted_rate':fields.float('Posted Rate'),
        'Adjustment':fields.float('Adjustment'),
        'Adj (buydown/buyup)':fields.float('Adj (buydown/buyup'),
        'rate_detail_Net rate':fields.float('Net rate'),
        'Max discount':fields.float('Max discount'),
        #reason
        'reason_Other':fields.char('Other', size=240),
        'reason_Credit_Satisfactory_with_explanation':fields.text('Credit Satisfactory with explanation',),
        'reson_Income_Verification_low_doc':fields.char('Income Verification Low Doc', size=240),
        'reson_Income_Verification_no_doc':fields.char('Income Verification No Doc', size=240),
        'reson_downpayment_Verification_low_doc':fields.char('Downpayment Verification Low Doc', size=240),
        'reson_downpayment_Verification_no_doc':fields.char('Downpayment Verification No Doc', size=240),
        'Blend':fields.char('Blend', size=240),        
        #Payment Frequency Dates
        'Funding_Date': fields.date('Funding Date'),
        'First_Payment_Date': fields.date('First Payment Date'),
        'Interest_Adjustment_Date': fields.date('Interest Adjustment Date'),
        'Maturity_Date': fields.date('Maturity Date'),
        'Interest_Adjustment':fields.char('Interest Adjustment', size=240),
        'Payment_Frequency':fields.selection([('Annually','Annually'),('Semi-Annually','Semi-Annually'),('Quarterly','Quarterly'),('Monthly','Monthly'),('Semi-Monthly','Semi-Monthly'),('Bi-Weekly','Bi-Weekly'),('Weekly','Weekly')],'Payment Frequency'),
        'Accelerated Payment':fields.selection([('yes','YES'),('no','NO')],'Accelerated Payment'),
        # Financial Summary
        #morweb
        'morweb_net_rate_gds': fields.float('NetRate GDS %',),
        'morweb_net_rate_tds': fields.float('NetRate TDS %',),        
        'qualifying_rate_gds': fields.float('QualifyingRate GDS %',),
        'qualifying_rate_tds': fields.float('QualifyingRate TDS %',),
        #CMHC
        'cmhc_net_rate_gds': fields.float('NetRate GDS %',),
        'cmhc_net_rate_tds': fields.float('NetRate TDS %',),
        'cmhc_qualifying_rate_gds': fields.float('QualifyingRate GDS %',),
        'cmhc_qualifying_rate_tds': fields.float('QualifyingRate TDS %',),
        #GE
        'ge_net_rate_gds': fields.float('NetRate GDS %',),
        'ge_net_rate_tds': fields.float('NetRate TDS %',),
        'ge_qualifying_rate_gds': fields.float('QualifyingRate GDS %',),
        'ge_qualifying_rate_tds': fields.float('QualifyingRate TDS %',),
        #Assets
        'Assets_description':fields.char('Description', size=240),
        'Assets_amount': fields.float('Amount',),
        'Assets_applicant':fields.char('Applicant', size=240),
        #liabilities
        'liabilitiy_description':fields.char('Description', size=240),
        'liabilitiy_amount': fields.float('Amount',),
        'liabilitiy_monthly_payment': fields.float('Monthly Payment',),
        'liabilitiy_applicant':fields.char('Applicant', size=240),
        'total_assets':fields.char('Total Assets', size=240),
        'total_libilities':fields.char('Total Liabilities', size=240),
        'Net_Worth':fields.char('Net Worth', size=240),
        'Total_Annual_Income': fields.float('Total Annual Income',),        
        #Completeness Check
        'Completeness_Check_id':fields.char('ID', size=240),
        'Completeness_Check_description':fields.char('Description', size=240),
        
        
        ##############  Property Details
        'Property_street': fields.char('Street', size=128),
        'Property_province': fields.char('ProvinceFrequencey', size=128),
        'Property_zip': fields.char('Zip', change_default=True, size=24),
        'Property_city': fields.char('City', size=128),
        'Property_state_id': fields.many2one("res.country.state", 'State'),
        'Property_country_id': fields.many2one('res.country', 'Country'),        
        'Property_direction':fields.selection([('SW','SW'),('SE','SE'),('NE','NE'),('NW','NW')],'Direction'),
        'Annual_Property_Taxes': fields.float('Annual Property Taxes'),
        'Amount of Taxes in Arrears': fields.float('Amount of Taxes in Arrears'),
        'Annual Heat': fields.float('Annual Heat'),
        'Tenure of Property':fields.selection([('Freehold','Freehold'),('Leasehold','Leasehold'),('Condo','Condo')],'Tenure of Property'),
        'Monthly Condo Fees': fields.float('Monthly Condo Fees'),
        'Annual Lease Amount': fields.float('Annual Lease Amount'),
        'Property Type':fields.selection([('Detached','Detached'),('Semi-Detached','Semi-Detached'),('Duplex','Duplex'),('Triplex','Triplex'),('Fourplex','Fourplex'),('Apartment','Apartment'),('Townhouse','Townhouse'),('Strip','Strip'),('High Rise','High Rise'),('Row','Row')
        ,('Mobile','Mobile'),('Modular Home','Modular Home'),('Co-op','Co-op'),('Fiveplex','Fiveplex'),('Sixplex','Sixplex'),('Other','Other')],'Property Type'),
        'Property Description':fields.selection([('Bungalow_One Storey','Bungalow or One Storey'),('Bi-Level','Bi-Level'),('Storey','1 0.5 Storey'),('2 Storey','2 Storey'),('3 Storey','3 Storey'),('Split Level','Split Level'),('other','Other')],'Property Description'),
        'Heating Type':fields.selection([('Electric Baseboard','Electric Baseboard'),('Forced Air/Gas/Oil/Electric','Forced Air/Gas/Oil/Electric'),('Hot Water','Hot Water'),('other','Other')],'Heating Type'),
        'Building Construction':fields.selection([('Brick/Stone','Brick/Stone'),('Insulbrick','Insulbrick'),('Stucco','Stucco'),('Aluminum Siding','Aluminum Siding'),('Vinyl Siding','Vinyl Siding'),('other','Other')],'Building Construction'),        
        'Year Built': fields.date('Year Built'),
        'Environmental Hazard':fields.selection([('yes','YES'),('no','NO')],'Environmental Hazard'),
        'Property Entirely for own use':fields.selection([('yes','YES'),('no','NO')],'Property Entirely for own use'),
        'Residential use only':fields.selection([('yes','YES'),('no','NO')],'Residential use only'),
        'New Construction':fields.selection([('yes','YES'),('no','NO')],'New Construction'),
        'Self Build':fields.selection([('yes','YES'),('no','NO')],'Self Build'),
        'Building_Unit Size': fields.float('Building/Unit Size',),
        'Lot Size': fields.float('Lot Size',),
        'feet_metre':fields.selection([('sq_ft','sq ft'),('metres_sq','metres sq')],'Feet/Metres'),
#        'sq_ft': fields.float('sq_ft',),
#        'metres_sq': fields.float('metres_sq',),
        'MLS':fields.char('MLS #', size=240),
        'COF Date': fields.date('COF Date'),
        'Roof Construction':fields.selection([('Tile/Slate','Tile/Slate'),('Aluminum Shingle/Sheet','Aluminum Shingle/Sheet'),('Asphalt/Shingle','Asphalt/Shingle'),('Cedar Stakes','Cedar Stakes'),('Steel','Steel'),('other','Other')],'Roof Construction'),
        'Total Land':fields.selection([('Less than 1 acres','Less than 1 acres'),('1-5 acres','1-5 acres'),('6-10 acres','6-10 acres'),('11-20 acres','11-20 acres'),('greater than 20 acres','greater than 20 acres')],'Total Land'),
        'Water Supply':fields.selection([('Municipal','Municipal'),('Private Well','Private Well'),('Shared Well','Shared Well'),('Cistern','Cistern'),('other','Other')],'Water Supply'),
        'Waste Disposal':fields.selection([('Sewer','Sewer'),('Septic','Septic'),('Holding Tank','Holding Tank'),('other','Other')],'Waste Disposal'),
        'Zoning':fields.selection([('Major Urban Residential','Major Urban Residential'),('Urban Residential','Urban Residential'),('Rural Residential','Rural Residential'),('Agricultural','Agricultural'),('Agricultural Land Reserve','Agricultural Land Reserve'),('Recreational/Cottage','Recreational/Cottage'),('Commercial','Commercial'),('Commercial/Residential','Commercial/Residential'),('other','Other')],'Zoning'),
        'First Nation Lease Land ':fields.boolean('First Nation Lease Land '),
        'Occupancy Status':fields.selection([('Owner Occupied','Owner Occupied'),('Partial Owner Occupied','Partial Owner Occupied'),('Rental Property','Rental Property')],'Occupancy Status'),
        '# of units':fields.char('# of units', size=240),
        '# of units rented':fields.char('# of units rented', size=240),
        #garage
        'garage_Attached':fields.selection([('single','Single'),('double','Double'),('tripal','Triple')],'Garage Attached'),
        'garage_detached':fields.selection([('single','Single'),('double','Double'),('tripal','Triple')],'Garage Detached'),
        #Appraisal section
        'Company Name':fields.char('Company Name', size=240),
        'NAS Search':fields.char('NAS Search', size=240),
        'Appraisal_First_Name':fields.char('First Name', size=240),
        'Appraisal_last_Name':fields.char('Last Name', size=240),
        'Appraisal_address':fields.char('Address', size=240),
        'Appraisal_email':fields.char('Email', size=240),
        'Appraisal_telephone':fields.char('Telephone', size=240),
        'Appraisal_fax':fields.char('Fax', size=240),
        'Appraiser Type':fields.selection([('appraiser','appraiser'),('insurer','insurer'),('valuation service','valuation service')],'Appraiser Type'),
        'Appraiser':fields.selection([('full','Full'),('drive by','drive by'),('realty property tax assessment','realty property tax assessment'),('other','Other')],'Appraisal Type'),
        'appraisal_Fee_Amount':fields.float('Fee Amount'),
        'Appraised Value':fields.float('Appraised Value'),
        'Appraised date': fields.date('Appraised Date'),
        'Notes':fields.text('Notes'),
        #legal Description
        'block':fields.char('Block',size=124),
        'lot':fields.char('Lot',size=124),
        'plan':fields.char('Plan',size=124),
        'Condo Unit':fields.char('Condo Unit',size=124),
        'Level Number':fields.char('Level Number',size=124),
        'Legal Address Details':fields.text('Legal Address Details'),
        'asset_ids':fields.one2many('crm.asset','opportunity_id','Assets'),
        'draws_required':fields.char('Draws Required',size=124),
        'lookingto2':fields.selection([('1','Condo/Mobile Home'),('2','House/Townhouse/Duplex/Acreage'),('3','Rental Property'),('4','Raw Land Leased land'),('5','Vacation Property/Second Home'),('6',"Not sure, I just want to know the maximum I can borrow.")],"Looking To"),
        'lookingto3':fields.selection([('1','Condo/Mobile Home'),('2','House/Townhouse/Duplex/Acreage'),('3','Rental Property'),('4','Raw Land Leased land'),('5','Vacation Property/Second Home')],"Looking To"),
        'building_funds':fields.selection([('1','Funding When Complete'),('2','Builder Progress Funding'),('3','Self-Build Progress Funding')],"Building Funds"),
        'property_value':fields.float('Property Value'),
        'renovation_value':fields.char('Renovation Value',size=120),
        'desired_amortization':fields.char('Desired Amortization',size=120),
        'desired_term':fields.char('Desired Term',size=120),
        
        'desired_mortgage_amount':fields.float('Desired Mortgage Amount'),
        'desired_mortgage_type':fields.selection([('1','Desired Mortgage Type'),('2','Desired Mortgage Type'),('3','Desired Mortgage Type')],"Desired Mortgage Type"),
        'desired_product_type':fields.many2one('product.product','Desired Product Type'),

        

#        'personal_cash_amount':fields.float('Personal Cash Amount'),
#        'rrsp_amount':fields.float('RRSP Amount'),
#        'gifted_amount':fields.float('Gifted Amount'),
#        'borrowed_amount':fields.float('Borrowed Amount'),
#        'sale_of_existing_amount':fields.float('Sale of Existing Amount'),
#        'existing_equity_amount':fields.float('Existing Equity Amount'),
#        'sweat_equity_amount':fields.float('Sweat Equity Amount'),
#        'secondary_financing_amount':fields.float('Secondary Financing Amount'),
#        'other_amount':fields.float('Other Amount'),
        'down_payment_coming_from':fields.selection([('1','Bank Account Chequing/Savings'),('2','RRSPs or Investments'),('3','Borrowed(e.g LOC)'),('4','Sale of Asset/Sale of Existing Property'),('5','Gift'),('6','Other')],"Down Payment Coming From"),

        'job_5_years':fields.selection([('1','Job - 5 years'),('2','Job - 5 years'),('3','Job - 5 years')],"Job - 5 years"),
        'income_decreased_worried':fields.selection([('1','Income Decreased; Worried'),('2','Income Decreased; Worried'),('3','Income Decreased; Worried')],"Income Decreased; Worried"),
        'future_family':fields.selection([('1','Future Family'),('2','Future Family'),('3','Future Family')],"Future Family"),
        'buy_new_vehicle':fields.selection([('1','Buy New Vehicle'),('2','Buy New Vehicle'),('3','Buy New Vehicle')],"Buy New Vehicle"),

        'lifestyle_change':fields.selection([('1','Lifestyle Change'),('2','Lifestyle Change'),('3','Lifestyle Change')],"Lifestyle Change"),
        'financial_risk_taker':fields.selection([('1','Financial Risk Taker'),('2','Financial Risk Taker'),('3','Financial Risk Taker')],"Financial Risk Taker"),
        'property_less_then_5_years':fields.selection([('1','Property < 5 years'),('2','Property < 5 years'),('3','Property < 5 years')],"Property < 5 years"),

        'product_ids':fields.one2many('product.product','opportunity_id','Product'),
        'deal_ids':fields.one2many('deal','opportunity_id','Deal'),
        'internal_note':fields.text('Internal Notes'),



        'property_style':fields.selection([('1','Bungalow/One Story'),('2','BiLevel'),('3','Two Story'),('4','Split Level'),('5','Story and A Half'),('6','Three Story'),('7','Other')],"Property Style"),
        'property_type':fields.selection([('1','House'),('2','Duplex'),('3','Four Plex'),('4','Apartment Style Condo'),('5','Town house/Raw house'),('6','Mobile Home/Modular Home'),('7','Other')],'Property Type'),
        'apartment_style':fields.selection([('1','Apartment Style'),('2','Apartment Style'),('3','Apartment Style')],"Apartment Style"),
        'plan':fields.char('Plan', size=240),
        'block':fields.char('Block', size=240),
        'lot':fields.char('Lot', size=240),
        'mls':fields.char('MLS', size=240),
        'new_home_warranty':fields.char('New Home Warranty', size=240),

        


        'address':fields.char('Address', size=240),
        'city':fields.char('City', size=240),
        'age':fields.char('Age', size=240),
        'square_footage':fields.char('Square Footage', size=240),
        'lot_size':fields.char('Lot Size', size=240),
        'acres':fields.selection([('1','# of Acres'),('2','# of Acres'),('3','# of Acres')],"# of Acres"),
        'property_taxes':fields.char('Property Taxes', size=240),
        'min_heat_fee':fields.float('Minimum Heat Fee', size=240),

        'province':fields.char('Province', size=240),
        'postal_code':fields.char('Postal Code', size=240),
        'heating':fields.selection([('1','Furnace/ Forced Air'),('2','Electric Base board'),('3','Hot Water Baseboard In Floor Heating'),('4','Other')],"Heating"),
        'water':fields.selection([('1','Municipality'),('2','Well'),('3','Other')],"Water"),
        'sewage':fields.selection([('1','Municipality'),('2','Septic System'),('3','Holding Tank'),('4','Other')],"Sewage"),
        'condo_fees':fields.char('Condo Fees', size=240),


        'garage_type':fields.selection([('1','Attached'),('2','Detached'),('3','None')],"Garage Type"),
        'garage_size':fields.selection([('1','Single'),('2','Double'),('3','Triple'),('4','Quadruple')],"Garage Size"),
        'outbuildings_value':fields.char('Outbuildings Value', size=240),


        'living_in_property':fields.selection([('1','Owner (Self)'),('2','Renter'),('3','Owner and Renter'),('4','Second Home/Vacation property')],"Living In Property"),
        'renter_pay_heating':fields.selection([('1','Renter pay heating'),('2','Renter pay heating'),('3','Renter pay heating')],"Renter pay heating?"),
        'monthly_rental_income':fields.char('Monthly Rental Income', size=240),


        'is_country_residential':fields.boolean('Is Country Residential'),
        'is_condo':fields.boolean('Is Condo'),
        'is_agricultural_less_then_10_acres':fields.boolean('Is Agricultural < 10 Acres'),
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
        'min_heat_fee':fields.float('Minimum Heat Fee', size=240),
        'selected_product':fields.many2one('product.product','Selected Product'),
        'is_construction_mortgage':fields.boolean('Is Construction Mortgage'),
        'is_life_leased_property':fields.boolean('Is Life Leased Property'),
        'is_leased_land':fields.boolean('Is Leased Land'),
        'is_raw_land':fields.boolean('Is Raw Land'),
        'is_mobile_homes':fields.boolean('Is Mobile Homes'),
        'is_modular_homes':fields.boolean('Is Modular Homes'),
        'is_floating_homes':fields.boolean('Is Floating Homes'),
        'is_boarding_house':fields.boolean('Is Boarding Houses'),
        'is_rooming_houses':fields.boolean('Is Rooming Houses'),
        'is_non_conv_construction':fields.boolean('Is Non-Conv Construction'),
        'is_cottage_rec_property':fields.boolean('Is Cottage / Rec Property'),
        'is_rental_property':fields.boolean('Is Rental Property'),
        'is_high_ratio_2nd_home':fields.boolean('Is High Ratio 2nd Home'),
        'is_uninsured_conv_2nd_home':fields.boolean('Is Uninsured Conv 2nd Home'),
        'is_a_small_centre':fields.boolean('Is A Small Centre'),
        'internal_note_property':fields.text('Internal Notes'),





        ### Vijay Code
#        verification
        'task':fields.one2many('opp.task','opp_id','Task'),
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
        'insurerfee':fields.char('Insurer Fee'),
        'purchase_price':fields.char('Purchase Price'),
        'downpayment':fields.char('DownPayment'),
        'closingdate':fields.date('Closing Date'),
        'renewaldate':fields.date('Renewal Date'),
        'total_mortgage_amount':fields.integer('Total Mortgage Amount'),
        'rate':fields.integer('Rate %'),
        'term':fields.selection([('6month','6 Month'),('1year','1 Year'),('2year','2 Year'),('3year','3 Year'),('4year','4 Year'),('5year','5 Year'),('7year','7 Year'),('10year','10 Year'),('open','Open')],'Term'),
        'amortization':fields.integer('Amortization'),
        'monthly_payment':fields.integer('Monthly Payment'),
        'mortgage_type':fields.selection([('open','Open'),('closed','Closed')],'Mortgage Type'),
        'product_type':fields.selection([('fixed','Fixed'),('variable','Variable'),('loc','LOC')],'Product Type'),
        'cash_back':fields.integer('Cash Back'),
        'base_commission':fields.integer('Base Commissions'),
        'volume_commission':fields.integer('Volume Commissions'),
        'commitment_fee':fields.integer('Commitment Fee'),
        'lender_fee':fields.integer('Lender Fee'),
        'private_fee':fields.integer('Private Fee'),
        'verify_product':fields.boolean('Verify Product'),



        
    }
    
    _defaults = {
        'issuing_province_canada': 39,        
        }
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
            'asset_type':fields.many2one('asset.type','Type'),
            'name': fields.text('Description',),
            'value': fields.char('Value',size=120),
            }
crm_asset()

class asset_type(osv.osv):
    _name = "asset.type"
    _columns = {
            'name':fields.char('name',size=128),
        }
asset_type()

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
        'name':fields.char('Description',size=128),
        'note_type':fields.selection([('1','Note Type'),('2','Note Type'),('3','Note Type')],'Note Type'),
        'urgency':fields.selection([('1','Urgency'),('2','Urgency'),('3','Urgency')],'Urgency'),
        'opportunity_id':fields.many2one('crm.lead','Opportunity Reference'),
    }
deal()

class opp_task(osv.osv):
    _name = 'opp.task'
    _columns = {
                'name':fields.selection([('a','A'),('b','B'),('c','C')],'Note Type'),
                'done':fields.boolean('Done'),
                'urgency':fields.selection([('low','Low'),('medium','Medium'),('high','High'),('highest','Highest')],'Urgency'),
                'description':fields.text('Description'),
                'opp_id':fields.many2one('crm.lead','Opportunity'),
    }
opp_task()