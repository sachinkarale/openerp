
#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

from osv import fields,osv

class visdom_form(osv.osv):
    _name = 'visdom.form'
    _columns = {
            'name':fields.char('login', size=120),
            'password':fields.char('Password', size=120),
            'email':fields.char('Email', size=120),
            
#            fields on Visdom website           WELCOME PAGE
            'wdrprelationship':fields.char('W2DrpRelationship',size=120),
            
            'second_applicant':fields.selection([('1','Yes'),('2','No')],'yes/no'),
            'why_sec':fields.char('Why',size=120),
            'firstname_sec':fields.char('Firstname sec',size=120),
            'middlename_sec':fields.char('Middlename sec',size=120),
            'lastname_sec':fields.char('Lastname sec',size=120),
            'email_sec':fields.char('Email sec',size=120),
            'cell_sec':fields.char('Cell sec',size=120),
            'home_sec':fields.char('Home sec',size=120),
            'work_sec':fields.char('Work sec',size=120),
            'best_sec':fields.selection([('Mobile','Mobile'),('Work','Work'),('Home','Home')],'Best#'),
            'street_sec':fields.char('StreetSec',size=120),
            'city_sec':fields.char('CitySec',size=120),
            'province_sec':fields.char('ProvinceSec',size=120),
            'code_sec':fields.char('CodeSec',size=120),

#            /** Legal Matters **/
            'appsign':fields.char('W0TxtAppSign',size=120),
            'coappsign':fields.char('W0TxtCoAppSign',size=120),
                
#            /** Current Lending Goal **/
          
            'whatisyourlendinggoal':fields.selection([('1','Pre-Approved'),('2','Approved'),('3','Refinance')],'Lending Goal'),
            'preapprovedimlookingfora':fields.selection([('1','Condo/Mobile Home'),('2','House/Townhouse/Duplex/Acreage'),('3','Rental Property'),('4','Raw Land Leased land'),('5','Vacation Property/Second Home'),('6',"Not sure, I just want to know the maximum I can borrow.")],"I'm looking for a"),
            'approvedimlookingfora':fields.selection([('1','Build a property'),('2','Buy an existing finished property(House, Acreage, Condo, Land)'),('3','Get additional funds to renovate and purchase to increase the value of my property?'),('4','Raw Land Leased land'),('5','Vacation Property/Second Home'),('6','Not sure, I just want to know the maximum I can borrow.')],"I'm looking for a"),
            'approvedfund':fields.selection([('1','Funding When Complete'),('2','Builder Progress Funding'),('3','Self-Build Progress Funding')],'Approved Fund'),
            'approvedbuilding':fields.selection([('1','Condo/Mobile Home'),('2','House/Townhouse/Duplex/Acreage'),('3','Rental Property'),('4','Raw Land Leased land'),('5','Vacation Property/Second Home')],"I'm Building a:"),
            'refinance':fields.selection([('1','Refinance my property to get money to purchase another property.'),('2','Reduce Interest Rate on My Mortgage.'),('3','Renew Mortgage'),('4','Increase Mortgage Amount')],"I'm looking for a:"),
            'refinancerenewing':fields.selection([('1','Condo/Mobile Home'),('2','House/Townhouse/Duplex/Acreage'),('3','Rental Property'),('4','Raw Land Leased land'),('5','Vacation Property/Second Home')],"I'm renewing / refinancing a:"),

#            pre-approved
           'property_you_planning_to_purchase':fields.char('What value of property are you planning to purchase?',size=120),
           'money_you_intending_a_down_payment':fields.char('How much money are you intending a down payment?',size=120),
           'your_down_payment_coming_from':fields.selection([('1','Bank Account Chequing/Savings'),('2',"RRSP's or Investments"),('3',"Borrowed(e.g LOC)"),('4',"Sale of Asset/Sale of Existing Property"),('5','Gift'),('6','Other')],'Where is your down payment coming from?'),
           'giftiscomingfrom':fields.char('Gift is Coming From',size=120),
           'describe_down_payment_coming_from':fields.text('Describe down payment coming from'),        
           
           
           

           'living_in_the_property_you_are_financing':fields.selection([('1','Owner(Self)'),('2','Renter'),('3','Owner and Renter'),('4','Second Home/Vacation property')],'Who will be living in the property you are financing?'),
           'monthly_rental_income_do_you_receive':fields.char('How much MONTHLY rental income do you receive?',size=120),
           'does_your_rental_property_have_a_legal_suite':fields.selection([('1','Yes'),('2','No')],'Does your rental property have a legal suite?'),
           'does_renter_pay_for_heating_property_as_part_rent_separately':fields.selection([('1','Heat Included'),('2','Heat Separate')],'Does your renter pay for heating of the property as part of the rent or separately?'),
           'mortgage_in_mind':fields.selection([('0','Line of Credit'),('1','Fixed'),('2','Variable'),('3','Cashback'),('4','What is my Best Option?')],'Do you currently have a type of mortgage in mind?'),
           'line_of_credit_is':fields.selection([('1','5 Years')],'Line of Credit is'),
           'do_you_currently_have_a_term_length_in_mind':fields.selection([('1','My best option'),('2','6 Months'),('3','1 Year'),('4','2 Years'),('5','3 Years'),('6','4 Years'),('7','5 Years'),('8','7 Years'),('9','10 Years')],'Do you currently have a term length in mind?'),
           'variable_mortgage_in_mind':fields.selection([('1','Capped'),('2','Closed Variable'),('3','Open Variable')],'Do you currently have a type of variable Mortgage in mind?'),
           'term_length_in_mind':fields.selection([('1','5 Years'),('2','7 Years')],'term length in mind'),
           'have_term_length_in_mind':fields.selection([('1','3 Years'),('2','5 Years')],'Do you currently have a term length in mind?'),
           
           'your_best_option_is':fields.selection([('1','10 Years')],'Your Best Option is'),
           'i_would_like_a_payment_frequency_that_is':fields.selection([('1','Monthly e.g. 1st of the Month'),('2','Biweekly e.g. Every 2nd Friday'),('3','Weekly e.g. Every Friday'),('4','Semi Monthly e.g. 1st and 15th')],'I would like a payment frequency that is:'),
           'is_there_an_amortization_you_are_looking_for':fields.selection([('1','10 Years'),('2','15 Years'),('3','20 Years'),('4','25 Years'),('5','30 Years'),('6','How Long')],'Is there an amortization you are looking for?'),
           'how_long_amortization':fields.char('How Long',size=120),
           'same_job_five_years_from_now':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose Not to Answer')],"I easily imagine myself in the same job 5 years from now:"),
           'about_my_bills':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose Not to Answer')],"I would start to really worry about my bills:"),
           'larger_family_next_five_years':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose Not to Answer')],"I might have a larger family sometime over the next 5 years:"),
           'vehicle_in_next_six_months':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose Not to Answer')],"I am considering buying a new vehicle in the next 6-12 months:"),
           'much_more_storage_at_home':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose Not to Answer')],"require much more storage at home:"),
           'myself_financial_risk_taker':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose Not to Answer')],"I consider myself to be a financial risk taker:"),
           'property_for_less_than_three_years':fields.selection([('1','Strongly Disagree'),('2','Somewhat Disagree'),('3','Not Sure'),('4','Somewhat Agree'),('5','Strongly Agree'),('6','Choose Not to Answer')],'I think it is very likely that I will have this property for less than 3 years:'),
           


#            /** Purchase Refinance  **/
           'street':fields.char('street',size=120),
           'street2':fields.char('street2',size=120),
           'city':fields.char('city',size=120),
           'province':fields.char('province',size=120),
           'code':fields.char('code',size=120),

           'street_other':fields.char('street',size=120),
           'street2_other':fields.char('street2',size=120),
           'city_other':fields.char('city',size=120),
           'province_other':fields.char('province',size=120),
           'code_other':fields.char('code',size=120),

           'address':fields.selection([('1','Yes this is the Address'),('2','No, this is not the Address')]),
           'mls':fields.char('mls',size=120),
           'plan':fields.char('plan',size=120),
           'lot':fields.char('lot',size=120),
           'block':fields.char('block',size=120),
           'pid':fields.char('pid',size=120),
           'prop':fields.selection([('1','Bungalow/One Story'),('2','BiLevel'),('3','Two Story'),('4','Split Level'),('5','Story and A Half'),('6','Three Story'),('7','Other')],'Prop'),
           'type':fields.selection([('1','House'),('2','Duplex'),('3','Four Plex'),('4','Apartment Style Condo'),('5','Town house/Raw house'),('6','Mobile Home/Modular Home'),('7','Other')],'Type'),
        
#          /** Property/Refinance  **/
            'property_heated':fields.selection([('1','Furnace/ Forced Air'),('2','Electric Base board'),('3','Hot Water Baseboard In Floor Heating'),('4','other')],'Property Heated'),
            'property_describe':fields.char('Description',size=240),
            'property_get_water':fields.selection([('1','Municipality'),('2','Well'),('3','other')],"get the water"),
            'property_get_water_describe':fields.char('property get water Describe',size=240),
            'sewage_and_waste_water':fields.selection([('1','Municipality'),('2','Septic System'),('3','Holding Tank'),('4','Other')],"sewage water"),
            'sewage_and_waste_water_describe':fields.char('sewage_and_waste_water describe',size=240),
            'garage_property':fields.selection([('1','Attached'),('2','Detached'),('3','None')],"Garage Property"),
            'garage_size':fields.selection([('1','Single'),('2','Double'),('3','Triple')],'Garage Size'),
            'additional_building':fields.selection([('1','Yes'),('2','No')],'additional building'),
            'additional_building_describe':fields.char('additional building',size=120),
            'old_property':fields.char('old property',size=120),
            'square_footage':fields.char('square footage',size=120),
            'annual_property':fields.char('Annual Property',size=120),
            'monthly_condo':fields.char('monthly Condo',size=124),
            'monthlylotrental':fields.char('monthly Lot Rental',size=120),

#               Approved
             'hourly_wagea':fields.char('How much is your hourly wage?',size=120),
            'property_purchase_price':fields.float('Purchase price of the property'),
           'purchase_price_include':fields.float('Purchase price include?'),
           'property_purchase_type':fields.selection([('1','Land and Dwelling'),('2',"Dwelling only"),('3',"Other")],'Property Type'),
           'is_member_of_warranty_program':fields.selection([('1','Yes'),('2',"No"),('3',"Unsure")],'Is your builder a member of a warranty program?'),
           'approx_value_of_land':fields.float('Approximate value of land(e.g. Completed sewer, water, access)($)'),
           'money_against_land':fields.float('Money is owed against the land($)'),
           'describe_purchase_price':fields.text('Description'),
           'total_amount_of_land':fields.selection([('1','<1 Acre'),('2',"1-5 Acres"),('3',"5-10 Acres"),('4',"11-20 Acres"),('5',">25 Acres")],'Total amount of land securing your loan'),
           'down_payment':fields.float('Money putting as down payment'),
           'down_payment_coming_from':fields.selection([('1','Bank Account Chequing/Savings'),('2',"RRSP's or Investments"),('3',"Borrowed(e.g LOC)"),('4',"Sale of Asset/Sale of Existing Property"),('5',"Gift"),('6',"Other")],'Down payment coming from'),
           'describe_down_payment':fields.text('Description'),
           'possessions_date': fields.char('Possession date'),
           'finance_date': fields.char('Financing Date'),
           'no_condition_of_finance':fields.selection([('1','This purchase has no condition of financing')],'No condition of financing'),


#          /** Employment Details */

           'income_earn':fields.selection([('1','Employed'),('2',"Self-Employed / Contractor"),('3',"Both"),('4',"Retired")],'How is your income earned?'),
           #Employment Details----Job
           'paid_on_the_basis':fields.selection([('1','Salary'),('2',"Hourly"),('3',"Commission"),('4',"Salary + Bonus / Commission"),('5',"Hourly+Commission"),('6',"Salary+Commission")],'How are you paid?'),
            'hourly_wage':fields.char('How much is your hourly wage?',size=240),
            'working_hour_in_a_week':fields.char('How many hours a week do you work?',size=240),
           'is_paid_overtime':fields.selection([('1','Yes'),('2',"No")],'Are you paid overtime?'),
           'overtime_income':fields.char('How much overtime income are you paid each month (on average)?',size=240),
           'paid_terms':fields.selection([('1','Weekly'),('2',"Bi-Weekly"),('3',"Semi-Monthly"),('4',"Monthly")],'How frequently are you paid?'),
            'amount_get':fields.char('How much are you paid every Period?',size=240),
                'annualbonus':fields.char('How much is your average annual bonus / commission (in addition to salary) over the past two years?',size=240),
                'annual_income_over_past_two_year':fields.char('How much is your average annual income over the past two years?',size=240),
           'current_job':fields.selection([('1','Less Than 1 Year'),('2',"1-3 Year"),('3',"3-5 Years"),('4',"5+ Years")],'How long have you been at your current job?'),
           'industry':fields.selection([('1','Banking / Finance'),('2',"Government"),('3',"Education"),('4',"Health"),('5',"Manufacturing"),('6',"Services"),('7',"Resources / Transportation"),('8',"Other")],'Which best describes the industry you work in?'),
           'describe_industry':fields.text('Description'),
           'consider':fields.selection([('1','Full-time'),('2',"Part-time"),('3',"Seasonal")],'Are you considered:'),
                'job_title':fields.char('What is your Job Title?',size=240),
                'company_name':fields.char('What is the name of the company that employs you?',size=240),
           'is_child_support':fields.selection([('1','Yes'),('2',"No")],'Do you receive any Child Support or Spousal Support?'),
           'support_amount':fields.char('How much is the monthly support you receive?',size=240),
           'is_other_employment':fields.selection([('1','Yes'),('2',"No")],'Do you have any other employment?'),
           'is_other_income':fields.selection([('1','Yes'),('2',"No")],'Do you any other sources of income?'),
                'amounts':fields.char('Amount',size=240),
           'describe_other_income':fields.text('Description'),
           #'previous_employment_o2m':fields.one2many('previous.employment', '','Companies that refers to partner'),

           #Employment Details----Job2

           #'income_earn_2':fields.selection([('1','Employed'),('2',"Self-Employed / Contractor"),('3',"Both"),('4',"Retired")],'How is your income earned?'),
           'paid_on_the_basis2':fields.selection([('1','Salary'),('2',"Hourly"),('3',"Commission"),('4',"Salary + Bonus / Commission"),('5',"Hourly+Commission"),('6',"Salary+Commission")],'How are you paid?'),
           'hourly_wage2':fields.char('How much is your hourly wage?',size=240),
           'working_hour_in_a_week2':fields.char('How many hours a week do you work?',size=240),
           'is_paid_overtime2':fields.selection([('1','Yes'),('2',"No")],'Are you paid overtime?'),
           'overtime_income2':fields.char('How much overtime income are you paid each month (on average)?',size=240),
           'paid_terms2':fields.selection([('1','Weekly'),('2',"Bi-Weekly"),('3',"Semi-Monthly"),('4',"Monthly")],'How frequently are you paid?'),
           'amount_get2':fields.char('How much are you paid every Period?',size=240),
           'annualbonus2':fields.char('How much is your average annual bonus / commission (in addition to salary) over the past two years?',size=240),
           'annual_income_over_past_two_year2':fields.char('How much is your average annual income over the past two years?'),
           'current_job2':fields.selection([('1','Less Than 1 Year'),('2',"1-3 Year"),('3',"3-5 Years"),('4',"5+ Years")],'How long have you been at your current job?'),
           'industry2':fields.selection([('1','Banking / Finance'),('2',"Government"),('3',"Education"),('4',"Health"),('5',"Manufacturing"),('6',"Services"),('7',"Resources / Transportation"),('8',"Other")],'Which best describes the industry you work in?'),
           'describe_industry2':fields.text('Description'),
           'consider2':fields.selection([('1','Full-time'),('2',"Part-time"),('3',"Seasonal")],'Are you considered:'),
           'job_title2':fields.char('What is your Job Title?',size=240),
           'company_name2':fields.char('What is the name of the company that employs you?',size=240),
           #'is_child_support2':fields.selection([('1','Yes'),('2',"No")],'Do you receive any Child Support or Spousal Support?'),
           #'support_amount2':fields.char('How much is the monthly support you receive?'),
           'is_other_employment2':fields.selection([('1','Yes'),('2',"No")],'Do you have any other employment?'),
           'is_other_income2':fields.selection([('1','Yes'),('2',"No")],'Do you any other sources of income?'),
           'amounts2':fields.char('Amount'),
           'describe_other_income2':fields.text('Description'),


           #Employment Details----job3

           'paid_on_the_basis3':fields.selection([('1','Salary'),('2',"Hourly"),('3',"Commission"),('4',"Salary + Bonus / Commission"),('5',"Hourly+Commission"),('6',"Salary+Commission")],'How are you paid?'),
           'hourly_wage3':fields.char('How much is your hourly wage?',size=240),
           'working_hour_in_a_week3':fields.char('How many hours a week do you work?',size=240),
           'is_paid_overtime3':fields.selection([('1','Yes'),('2',"No")],'Are you paid overtime?'),
           'overtime_income3':fields.char('How much overtime income are you paid each month (on average)?',size=240),
           'paid_terms3':fields.selection([('1','Weekly'),('2',"Bi-Weekly"),('3',"Semi-Monthly"),('4',"Monthly")],'How frequently are you paid?'),
           'amount_get3':fields.char('How much are you paid every Period?',size=240),
           'annualbonus3':fields.char('How much is your average annual bonus / commission (in addition to salary) over the past two years?',size=240),
           'annual_income_over_past_two_year3':fields.char('How much is your average annual income over the past two years?',size=240),
           'current_job3':fields.selection([('1','Less Than 1 Year'),('2',"1-3 Year"),('3',"3-5 Years"),('4',"5+ Years")],'How long have you been at your current job?'),
           'industry3':fields.selection([('1','Banking / Finance'),('2',"Government"),('3',"Education"),('4',"Health"),('5',"Manufacturing"),('6',"Services"),('7',"Resources / Transportation"),('8',"Other")],'Which best describes the industry you work in?'),
           'describe_industry3':fields.text('Description'),
           'consider3':fields.selection([('1','Full-time'),('2',"Part-time"),('3',"Seasonal")],'Are you considered:'),
           'job_title3':fields.char('What is your Job Title?',size=240),
           'company_name3':fields.char('What is the name of the company that employs you?',size=240),


           #Self-Employed / Contractor ----job
           'avg_annual_income':fields.char('How much is your average annual income over the past two years?(The income number Lender will consider for selfemployed income is Line 150 from your last 2 Tax Returns or Notice of Assessments)',size=240),
           'self_company_name':fields.char('What is the name of your company?',size=240),
           'business_classified':fields.selection([('1','Corporation'),('2',"Sole Proprietorship")],'How is your business classified?'),
           'self_employed_frm':fields.selection([('1','Less Than 1 Year'),('2',"1-3 Year"),('3',"3-5 Years"),('4',"5+ Years")],'How long have you been self Employed?'),
           'self_industry_type':fields.selection([('1','Banking / Finance'),('2',"Government"),('3',"Education"),('4',"Health"),('5',"Manufacturing"),('6',"Services"),('7',"Resources / Transportation"),('8',"Other")],'Which best describes the industry?'),
           'describe_self_industry':fields.text('Description'),
           'self_contract_emp':fields.selection([('1','Yes'),('2',"No")],'Do you contract to your previous employer?'),

           #Self-Employed / Contractor ----job2
           'avg_annual_income2':fields.char('How much is your average annual income over the past two years?(The income number Lender will consider for selfemployed income is Line 150 from your last 2 Tax Returns or Notice of Assessments)',size=240),
           'self_company_name2':fields.char('What is the name of your company?',size=240),
           'business_classified2':fields.selection([('1','Corporation'),('2',"Sole Proprietorship")],'How is your business classified?'),
           'self_employed_frm2':fields.selection([('1','Less Than 1 Year'),('2',"1-3 Year"),('3',"3-5 Years"),('4',"5+ Years")],'How long have you been self Employed?'),
           'self_industry_type2':fields.selection([('1','Banking / Finance'),('2',"Government"),('3',"Education"),('4',"Health"),('5',"Manufacturing"),('6',"Services"),('7',"Resources / Transportation"),('8',"Other")],'Which best describes the industry?'),
           #'describe_self_industry2':fields.text('Description'),
           'self_contract_emp2':fields.selection([('1','Yes'),('2',"No")],'Do you contract to your previous employer?'),

           #Self-Employed / Contractor ----job3
           'avg_annual_income3':fields.char('How much is your average annual income over the past two years?(The income number Lender will consider for selfemployed income is Line 150 from your last 2 Tax Returns or Notice of Assessments)',size=240),
           'self_company_name3':fields.char('What is the name of your company?',size=240),
           'business_classified3':fields.selection([('1','Corporation'),('2',"Sole Proprietorship")],'How is your business classified?'),
           'self_employed_frm3':fields.selection([('1','Less Than 1 Year'),('2',"1-3 Year"),('3',"3-5 Years"),('4',"5+ Years")],'How long have you been self Employed?'),
           'self_industry_type3':fields.selection([('1','Banking / Finance'),('2',"Government"),('3',"Education"),('4',"Health"),('5',"Manufacturing"),('6',"Services"),('7',"Resources / Transportation"),('8',"Other")],'Which best describes the industry?'),
           'describe_self_industry3':fields.text('Description'),
           'self_contract_emp3':fields.selection([('1','Yes'),('2',"No")],'Do you contract to your previous employer?'),


           #Both

           #Retired
           'ret_get_month':fields.char('How much are you get a month?',size=240),


#            /* Asset Details **/

           'money_account':fields.char('How much money do you normally have in your chequing and savings accounts after payday?',size=240),
           'vehicles':fields.selection([('1','Yes'),('2',"No")],'Do you have any vehicles'),
           'rrsps':fields.selection([('1','Yes'),('2',"No")],'Do you have any RRSPs?'),
           'non_rsp':fields.selection([('1','Yes'),('2',"No")],'Do you have any non- RRSP,s investments (E.g. GICs, Term Deposits, Mutual Funds, Stocks or other investments)?'),
           're_state':fields.selection([('1','Yes'),('2',"No")],'Do you own any Real Estate?'),
           'contents':fields.char('How much have you insured the contents of your properties for?',size=240),

           'estimated_value':fields.char('Estimated Value',size=240),
           'monthly_rent':fields.char('Monthly Rent',size=240),
           'prop_taxes':fields.char('Property Taxes / Month',size=240),
           'fees':fields.char('Condo / Strata Fees',size=240),

           'estimated_value1':fields.char('Estimated Value',size=240),
           'monthly_rent1':fields.char('Monthly Rent',size=240),
           'prop_taxes1':fields.char('Property Taxes / Month',size=240),
           'fees1':fields.char('Condo / Strata Fees',size=240),

           'estimated_value2':fields.char('Estimated Value',size=240),
           'monthly_rent2':fields.char('Monthly Rent',size=240),
           'prop_taxes2':fields.char('Property Taxes / Month',size=240),
           'fees2':fields.char('Condo / Strata Fees',size=240),

#         Loan Details fields
           'refn_c_balance':fields.char('What is the current balance owing on your mortgage? (Approximately)',size=240), #W6TxtRefnCBalance
           'refn_interest_rate':fields.char('What is your current Mortgage Interest Rate?',size=240), #W6TxtRefnInterestRate
           'refn_mortgage_payment':fields.char('What is your current Mortgage Payment?',size=240), #W6TxtRefnMortgagePayment
           'refn_payment_schedule':fields.selection([('1','Monthly (e.g. 1st of the Month)'),('2','Biweekly (e.g. Every 2nd Friday)'),('3','Weekly (e.g. Every Friday)'),('4','Semi Monthly (e.g. 1st and 15th)'),],'My current Mortgage Payments are on the Following Schedule:'),#W6RefnPaymentSchedule
           'refn_included_amount':fields.selection([('1','Yes'),('2','No')],'Are your Property Taxes included in the payment amount above?'), #W6RefnIncludedAmount
           'refn_date':fields.char('When is the Renewal Date on your current Mortgage?',size=240), #W6TxtRefnDate


#          Liabilities Details
           'liabilities_owed':fields.selection([('1','Yes'),('2','No')],'Do you have existing loans (e.g. Credit Card, Car Loan, etc) that you want to pay off'), #W9LiabilitiesOwed
           'liabilities_detail_line': fields.one2many('liabilities.detail', 'visdom_id', 'Liabilities Detail Line'),


#         relationation fields
            'previous_employment_line': fields.one2many('previous.employment', 'visdom_id', 'Visdom Lines'),
            'previous_employment_line2': fields.one2many('previous.employment2', 'visdom_id', 'Visdom Lines2'),
            'previous_employment_line3': fields.one2many('previous.employment3', 'visdom_id', 'Visdom Lines3'),
            'self_previous_employment_line': fields.one2many('self.previous.employment', 'visdom_id', 'Visdom Lines'),
            'self_previous_employment_line2': fields.one2many('self.previous.employment2', 'visdom_id', 'Visdom Lines2'),
            'self_previous_employment_line3': fields.one2many('self.previous.employment3', 'visdom_id', 'Visdom Lines3'),
            'vehicles_detail_line': fields.one2many('vehicles.detail', 'visdom_id', 'Vehicles Detail Lines'),
            'rrsp_detail_line': fields.one2many('rrsp.detail', 'visdom_id', 'RRSPs Lines'),
            'non_rrsp_detail_line': fields.one2many('non.rrsp.detail', 'visdom_id', 'Non RRSPs Lines'),
            'own_any_real_estate_line': fields.one2many('own.any.real.estate', 'visdom_id', 'Own Any Real Estate Lines'),
            'own_any_real_estate_line2': fields.one2many('own.any.real.estate2', 'visdom_id', 'Own Any Real Estate Lines2'),
            'own_any_real_estate_line3': fields.one2many('own.any.real.estate3', 'visdom_id', 'Own Any Real Estate Lines3'),
            'lender_line': fields.one2many('lender', 'visdom_id', 'Lender Lines'),
            'lender_line2': fields.one2many('lender2', 'visdom_id', 'Lender Lines2'),
            'lender_line3': fields.one2many('lender3', 'visdom_id', 'Lender Lines3'),
            'partner_id': fields.many2one('res.partner', 'Partner'),
            



        }   
visdom_form()


class loan_detail(osv.osv):
    _name = 'loan.detail'
    _columns = {
            'name':fields.char('Company',size=120),
            'type':fields.selection([('1','Credit Card'),('2','Line of Credit')],'Loan Type'),
            'amount':fields.float('Amount'),
    }
loan_detail()


class liabilities_detail(osv.osv):
    _name = 'liabilities.detail'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'type':fields.selection([('CreditCard','Credit Card'),('LineOfCredit','Line of Credit')],'Type of Loan'),
                'company':fields.char('Company (e.g. Shell Credit Card)',size=240),
                'amount_being_paid':fields.char('Amount Being Paid',size=240),
        }
liabilities_detail()


class previous_employment(osv.osv):
    _name = 'previous.employment'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'previous_employment':fields.char('Previous Employment',size=240),
                'job_title':fields.char('Job Title',size=240),
                'annual':fields.char('Annual',size=240),
                'of_months':fields.char('# of Months',size=240),
        }
previous_employment()

class previous_employment2(osv.osv):
    _name = 'previous.employment2'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference2', ondelete='cascade'),
                'previous_employment':fields.char('Previous Employment',size=240),
                'job_title':fields.char('Job Title',size=240),
                'annual':fields.char('Annual',size=240),
                'of_months':fields.char('# of Months',size=240),
        }
previous_employment2()

class previous_employment3(osv.osv):
    _name = 'previous.employment3'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference3', ondelete='cascade'),
                'previous_employment':fields.char('Previous Employment',size=240),
                'job_title':fields.char('Job Title',size=240),
                'annual':fields.char('Annual',size=240),
                'of_months':fields.char('# of Months',size=240),
        }
previous_employment3()


class self_previous_employment(osv.osv):
    _name = 'self.previous.employment'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'previous_employment':fields.char('Previous Employment',size=240),
                'job_title':fields.char('Job Title',size=240),
                'annual':fields.char('Annual',size=240),
                'of_months':fields.char('# of Months',size=240),
        }
self_previous_employment()


class self_previous_employment2(osv.osv):
    _name = 'self.previous.employment2'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'previous_employment':fields.char('Previous Employment',size=240),
                'job_title':fields.char('Job Title',size=240),
                'annual':fields.char('Annual',size=240),
                'of_months':fields.char('# of Months',size=240),
        }
self_previous_employment2()

class self_previous_employment3(osv.osv):
    _name = 'self.previous.employment3'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'previous_employment':fields.char('Previous Employment',size=240),
                'job_title':fields.char('Job Title',size=240),
                'annual':fields.char('Annual',size=240),
                'of_months':fields.char('# of Months',size=240),
        }
self_previous_employment3()




class vehicles_detail(osv.osv):
    _name = 'vehicles.detail'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'model':fields.char('Model',size=240),
                'value':fields.char('Value',size=240),
                'year':fields.char('Year',size=240),
        }
vehicles_detail()

class rrsp_detail(osv.osv):
    _name = 'rrsp.detail'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'company':fields.char('Company',size=240),
                'value':fields.char('Value',size=240),
        }
rrsp_detail()

class non_rrsp_detail(osv.osv):
    _name = 'non.rrsp.detail'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'company':fields.char('Company',size=240),
                'value':fields.char('Value',size=240),
                'type':fields.selection([('GICs','GICs'),('TermDeposits','TermDeposits'),('MutualFunds','MutualFunds'),('Stocks','Stocks'),('Insurance','Insurance'),('Other','Other')],'Type'),
        }
non_rrsp_detail()


class own_any_real_estate(osv.osv):
    _name = 'own.any.real.estate'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'address':fields.char('Address',size=240),
                'city':fields.char('City',size=240),
                'province':fields.char('Province',size=240),
                'postal_code':fields.char('Postal Code',size=240),
        }
own_any_real_estate()

class lender(osv.osv):
    _name = 'lender'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'holding_mortgage':fields.char('Company holding Mortgage',size=240),
                'amount':fields.char('Mortgage Amount',size=240),
                'pay_month':fields.char('Payment / Month',size=240),
                'rate':fields.char('Interest Rate',size=240),
                'renewal_date': fields.char('Renewal Date'),
        }
lender()


class own_any_real_estate2(osv.osv):
    _name = 'own.any.real.estate2'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'address':fields.char('Address',size=240),
                'city':fields.char('City',size=240),
                'province':fields.char('Province',size=240),
                'postal_code':fields.char('Postal Code',size=240),
        }
own_any_real_estate2()

class lender2(osv.osv):
    _name = 'lender2'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'holding_mortgage':fields.char('Company holding Mortgage',size=240),
                'amount':fields.char('Mortgage Amount',size=240),
                'pay_month':fields.char('Payment / Month',size=240),
                'rate':fields.char('Interest Rate',size=240),
                'renewal_date': fields.char('Renewal Date'),
        }
lender2()

class own_any_real_estate3(osv.osv):
    _name = 'own.any.real.estate3'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'address':fields.char('Address',size=240),
                'city':fields.char('City',size=240),
                'province':fields.char('Province',size=240),
                'postal_code':fields.char('Postal Code',size=240),
        }
own_any_real_estate3()

class lender3(osv.osv):
    _name = 'lender3'
    _columns = {
                'visdom_id': fields.many2one('visdom.form', 'Visdom Reference', ondelete='cascade'),
                'holding_mortgage':fields.char('Company holding Mortgage',size=240),
                'amount':fields.char('Mortgage Amount',size=240),
                'pay_month':fields.char('Payment / Month',size=240),
                'rate':fields.char('Interest Rate',size=240),
                'renewal_date': fields.char('Renewal Date'),
        }
lender3()