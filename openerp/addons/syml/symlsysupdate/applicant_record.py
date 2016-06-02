from osv import fields,osv
from openerp.tools.translate import _


class applicant_record(osv.osv):
    _name = 'applicant.record'
    _rec_name ='applicant_name'
    _columns = {
        'applicant_id': fields.many2one('crm.lead', 'Applicant Reference', ondelete='cascade'),
        'applicant_name':fields.char('Applicant Name',size=120,required=True),
        'applicant_last_name':fields.char('Last Name',size=120,required=True),
        'email_personal':fields.char('Email(personal)',size=120,required=True),

#        personal info

        'email_work':fields.char('Email(work)',size=120),
        'cell':fields.char('Cell',size=120),
        'work':fields.char('Work',size=120),
        'home':fields.char('Home',size=120),
        'relationship_status':fields.selection([('Single','Single'),('Married','Married'),('Common_Law','Common-Law'),('Divorced','Divorced'),('Separated','Separated')],'Relationship Status'),
        'best_number':fields.selection([('Mobile','Mobile'),('Work','Work'),('Home','Home')],'Best Number'),
        'opportunity':fields.many2one('crm.lead','Opportunity'),
        'sales_Associates':fields.many2one('res.users','Sales Associate'),
        'dob':fields.date('Date of Birth'),
        'sin':fields.char('Social Insurance #',size=120),
        'passport':fields.char('Passport (non-res)',size=120),
        'contact_record':fields.char('Contact Record',size=120),
        'signature':fields.char('Signature',size=120),
        'signature_ip':fields.char('Signature IP',size=120),
        'consent_dateTime': fields.datetime('Date Consent Obtained'),
        'identity_attached':fields.boolean('Identity Attached'),
        'non_resident':fields.boolean('Non-Resident'),
        'address_ids':fields.one2many('applicant.address','applicant_id','Addresses'),
        'immigration_date': fields.datetime('Immigration Date'),
        

#       credit/liabilities
        'beacon_score':fields.char('Beacon9 Score',size=120),
        'beacon_5_score':fields.char('Beacon5 Score',size=120),
        'total_inquires':fields.char('Total Inquires',size=120),
        'bankruptcy':fields.boolean('Bankruptcy'),
        'bankruptcy_discharge_date':fields.date('Bankruptcy Discharge Date'),
        'monthly_support_payment':fields.char('Monthly Support Payments',size=120),
        'date_time_bureau_obtained':fields.datetime('Date Bureau Obtained'),
        'orderly_debt_payment':fields.boolean('Orderly Debt Payment'),
        'odp_discharge_date':fields.date('ODP Discharge Date'),
        'mortgage':fields.one2many('applicant.mortgage','applicant_id','Mortgages'),
        'liabilities':fields.one2many('applicant.liabilities','applicant_id','Liabilities'),
        'collection':fields.one2many('applicant.collection','applicant_id','Collections'),
        'late_payments':fields.one2many('applicant.payment','applicant_id','Late Payments'),
        'ers_2_score':fields.char('ER 2 Score',size=120),
        'ers_3_score':fields.char('CRP 3 Score',size=120),

    
#   Employment/home
        'monthlychildsupport':fields.char('Monthly Child/Spousal Support',size=120),
        'total_employed_income':fields.char('Total Employed Income',size=120),
        'total_self_employed':fields.char('Total Self Employed',size=120),
        #'income':fields.char('Income',size=120),
        'total_rental_income':fields.char('Total Rental Income',size=120),
        'total_other_income':fields.char('Total Other Income',size=120),
        'total_income':fields.char('Total Income',size=120),
        'income_ids':fields.one2many('income.employer','applicant_id','Incomes & Employers'),

#        Asset
        'total_asset':fields.char('Total Asset',size=120),
        'total_net_worth':fields.char('Net Worth',size=120),
        'asset_ids':fields.one2many('crm.asset','opportunity_id','Assets'),
        'property_ids':fields.one2many('applicant.property','applicant_id','Properties'),

        'money':fields.char('Money that you normally have in your chequing and savings accounts after payday',size=240),

#        credit/liabilities


         'primary':fields.boolean('Primary'),
        
    }
applicant_record()



class applicant_property(osv.osv):
    _name = 'applicant.property'
    _columns = {
        'name':fields.char('Address',size=240),
        'value':fields.integer('Value'),
        'owed':fields.integer('Owed'),
        'annual_tax':fields.integer('Annual Taxes'),
        'mo_condo_fees':fields.integer('Mo Condo Fees'),
        'selling':fields.boolean('Selling'),
        'applicant_id':fields.many2one('applicant.record','Opportunity Reference'),
        'property_id':fields.char('PropertyID',size=120),
        }
applicant_property()


class income_employer(osv.osv):
    _name='income.employer'
    _columns={
            'name':fields.selection([('1','Banking/Finance'),('2','Government'),('3','Education'),('4','Health'),('5','Manufacturing'),('6','Services'),('7','Resources / Transportation'),('8','Other')],'Type'),
            'industry':fields.text('Industry'),
            'business':fields.char('Business',size=120),
            'position':fields.char('Job Title',size=120),
            'annual_income':fields.char('Annual Income',size=120),
            'month':fields.selection([('1','Less Than 1 Year'),('2','1-3 Year'),('3','3-5 Years'),('4','5+ Years')],'Months'),
            'applicant_id':fields.many2one('applicant.record','Applicant'),
    }

income_employer()

class applicant_address(osv.osv):
    _name='applicant.address'
    _columns={
        'name':fields.char('Street Address',size=120),
        'street':fields.char('Street',size=120, nolabel=True),
        'city':fields.char('City',size=120),
        'province':fields.char('Province',size=120),
        'postal_code':fields.char('Postal Code',size=120),
        'date':fields.date('Date'),
        'applicant_id':fields.many2one('applicant.record','Applicant'),
    }  
applicant_address()

class applicant_mortgage(osv.osv):
    _name='applicant.mortgage'
    _columns={
        'name':fields.char('Lender',size=120),
        'interest_rate':fields.char('Interest Rate',size=120),
        'balance':fields.char('Balance',size=120),
        'monthly_payment':fields.char('Monthly Payment',size=120),
        'type':fields.selection([('open','Open'),('closed','Closed')],'Mortgage Type'),
        'renewal':fields.char('Renewal',size=240),
        'monthly_rent':fields.integer('Monthly Rent'),
        'pay_off':fields.integer('Pay Off'),
        'selling':fields.boolean('Selling'),
        'property_id':fields.char('Property ID',size=120),
        'applicant_id':fields.many2one('applicant.record','Applicant'),
    }
applicant_mortgage()

class applicant_liabilities(osv.osv):
    _name='applicant.liabilities'
    _columns = {
        'name':fields.selection([('a','A'),('b','B'),('c','C'),('i','I'),('j','J'),('m','M'),('s','S'),('t','T')],'Client'),
        'business':fields.char('Business',size=120),
        'status':fields.selection([('paid','Paid'),('closed','Closed'),('transfer_sold_paid','Transfer/Sold/Paid'),('lost_stolen','Lost/Stolen'),('refinanced','Refinanced'),('transfer_sold','Transfer/Sold'),('written_off','Written Off')],'Status'),
        'type':fields.selection([('CreditCard','Credit Card'),('LineOfCredit','Line Of Credit')],'Type'),
        'credit_limit':fields.char('Credit Limit',size=120),
        'credit_balance':fields.char('Credit Balance',size=120),
        'monthly_payment':fields.float('Monthly Payment'),
        'opened':fields.date('Opened'),
        'reported':fields.date('Reported'),
        'dla':fields.date('DLA'),
        'rating':fields.char('Rating',size=120),
        'pay_off':fields.integer('Pay Off'),
        'applicant_id':fields.many2one('applicant.record','Applicant'),
    }
applicant_liabilities()

class applicant_collection(osv.osv):
    _name='applicant.collection'
    _columns={
        'name':fields.char('Business',size=120),
        'amount':fields.integer('Amount'),
        'balance':fields.integer('Balance'),
        'date':fields.date('Date'),
        'status':fields.selection([('paid','Paid'),('closed','Closed'),('transfer_sold_paid','Transfer/Sold/Paid'),('lost_stolen','Lost/Stolen'),('refinanced','Refinanced'),('transfer_sold','Transfer/Sold'),('written_off','Written Off')],'Status'),
        'pay_off':fields.integer('Pay Off'),
        'applicant_id':fields.many2one('applicant.record','Applicant'),
    }
applicant_collection()

class applicant_payment(osv.osv):
    _name='applicant.payment'
    _columns={
        'name':fields.char('Business',size=120),
        #'status':fields.selection([('a','A'),('b','B')],'Status'),
        'date':fields.date('Date Late'),
        'rating':fields.char('Rating',size=120),
        'days':fields.char('Days',size=120),
        'reason':fields.char('Reason',size=120),
        'applicant_id':fields.many2one('applicant.record','Applicant'),
    }
applicant_payment()

