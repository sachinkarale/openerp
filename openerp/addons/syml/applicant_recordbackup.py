
from osv import fields,osv
from openerp.tools.translate import _
import pyodbc
import base64
from datetime import timedelta
from datetime import datetime
import os
import re
os.environ['TDSVER'] = '8.0'
class applicant_record(osv.osv):
    _name = 'applicant.record'
    _rec_name ='applicant_name'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _columns = {
        'opp_rec_ids': fields.many2many('crm.lead','opportunity_applicant_rel','app_id','opp_id','Opportunity'),
        'opp_id':fields.many2one('crm.lead','Opportunity'),	
        'credit_report':fields.text('Credit Report'),
        'opp_app_rel':fields.one2many('crm.lead','opportunity_id','Opportunity'),
        'applicant_id': fields.many2one('crm.lead', 'Opportunity', ondelete='cascade'),
        'applicant_name':fields.char('Applicant Name',size=120,required=True),
        'applicant_opportunity':fields.many2one('applicant.record','Applicant Name',ondelete='cascade'),
        'applicant_last_name':fields.char('Last Name',size=120,required=True),
        'email_personal':fields.char('Email(personal)',size=120,required=True),

#        personal info

        'email_work':fields.char('Email(work)',size=120),
        'cell':fields.char('Cell',size=120),
        'work':fields.char('Work',size=120),
        'home':fields.char('Home',size=120),
        'relationship_status':fields.selection([('Single','Single'),('Married','Married'),('Common_Law','Common-Law'),('Divorced','Divorced'),('Separated','Separated'),('Other','Other')],'Relationship Status'),
        'best_number':fields.selection([('Mobile','Mobile'),('Work','Work'),('Home','Home')],'Best Number'),
        #'opportunity':fields.many2one('crm.lead','Opportunity'),
        'sales_associates':fields.many2one('res.users','Sales Associate'),
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
        'immigration_date': fields.date('Immigration Date'),
        "hr_department_id": fields.many2one("hr.department", 'Team'),
        
        

#       credit/liabilities
        'beacon_9_score':fields.integer('Beacon9 Score'),
        'beacon_5_score':fields.integer('Beacon5 Score'),
        'total_inquires':fields.integer('Total Inquires'),
        'bankruptcy':fields.boolean('Bankruptcy'),
        'bankruptcy_discharge_date':fields.date('Bankruptcy Discharge Date'),
        'monthly_support_payment':fields.float('Monthly Support Payments'),
        'date_time_bureau_obtained':fields.datetime('Date Bureau Obtained'),
        'orderly_debt_payment':fields.boolean('Orderly Debt Payment'),
        'odp_discharge_date':fields.date('ODP Discharge Date'),
        'mortgage':fields.one2many('applicant.mortgage','applicant_id','Mortgages'),
        'liabilities':fields.one2many('applicant.liabilities','applicant_id','Liabilities'),
        'collection':fields.one2many('applicant.collection','applicant_id','Collections'),
        'late_payments':fields.one2many('applicant.payment','applicant_id','Late Payments'),
        'ers_2_score':fields.integer('ER 2 Score'),
        'crp_3_score':fields.integer('CRP 3 Score'),

    
#   Employment/home
        'monthlychildsupport':fields.float('Monthly Child/Spousal Support'),
        'total_employed_income':fields.char('Total Employed Income',size=120),
        'total_self_employed':fields.char('Total Self Employed',size=120),
        #'income':fields.char('Income',size=120),
        'total_rental_income':fields.char('Total Rental Income',size=120),
        'total_other_income':fields.char('Total Other Income',size=120),
        'total_income':fields.float('Total Income'),
        'incomes':fields.one2many('income.employer','applicant_id','Incomes & Employers'),

#        Asset
        'total_asset':fields.integer('Total Asset'),
        'total_net_worth':fields.char('Net Worth',size=120),
        'asset_ids':fields.one2many('crm.asset','opportunity_id','Assets'),
        'properties':fields.one2many('applicant.property','applicant_id','Properties'),

        'money':fields.char('Money that you normally have in your chequing and savings accounts after payday',size=240),

#        credit/liabilities


         'primary':fields.boolean('Primary'),
#       equifax
         'ninqidx':fields.integer('Equifax Inquiry ID'),

         'include_in_opportunity':fields.boolean('Include In Opportunity'),
#         audit trail
        #'credit_report':fields.text('Credit Report',invisible=True ,track_visibility='always'),


        ######documents#######
            'document_ids':fields.one2many('app.documents','applicant_id','Applicant'),
        
    }

    _defaults = {
        'include_in_opportunity':True
    }

    #_order = 'applicant_name'

    def onchange_applicant(self, cr, uid, ids, applicant_id):
      print "inside onchange applicant ################################################",applicant_id
      
      print "context",ids
      this_browse = self.browse(cr, uid, applicant_id)
      last_name = this_browse.applicant_last_name or ''
      email = this_browse.email_personal or ''
      home = this_browse.home or ''
      beacon_9 = this_browse.beacon_9_score or ''
      total_income =this_browse.total_income   or ''

      return {'value':{'applicant_last_name':last_name,'email_personal':email,
                                'home':home,'beacon_9_score':beacon_9,
                                'total_income':total_income
                                }}

    def unlink(self, cr, uid, ids, context=None):
        if not isinstance(ids, list):
            ids=[ids]
        if ids:
            cr.execute('select opp_id from opportunity_applicant_rel where app_id = %s', (ids))
            app_unlink = cr.fetchall()
            print "app_unlink====",app_unlink
            if app_unlink:
                raise osv.except_osv((''),('You cannot delete the record...!!! \
                                            First Remove Applicant from associated Opportunities..'))
        
        return osv.osv.unlink(self, cr, uid, ids, context=context)


    def create(self, cr, uid, vals, context=None):
        ids_hr_employee = self.pool.get('hr.employee').search(cr,uid, [('user_id', '=', uid)])
        dep_id=self.pool.get('hr.employee').browse(cr,uid,ids_hr_employee[0]).department_id.id
        
        if dep_id:
            vals.update({'hr_department_id':dep_id})
        new_id = super(applicant_record, self).create(cr, uid, vals, context=context)
        if vals.has_key('opp_id'):
            cr.execute('insert into opportunity_applicant_rel (opp_id,app_id) \
                                values (%s,%s)', (vals['opp_id'], new_id))
        liability_lines = self.browse(cr,uid,new_id).liabilities
        if liability_lines:
            app_liablity_obj = self.pool.get('applicant.liabilities')
            seq_no = 0
            for line in liability_lines:
                seq_no +=1
                print "seq_no(create)>>>>",seq_no
                app_liablity_obj.write(cr,uid,[line.id],{'seq_no':seq_no})

        print "new_id>>>",new_id
        payment_lines = self.browse(cr,uid,new_id).late_payments
        if payment_lines:
            app_payment_obj = self.pool.get('applicant.payment')
            seq_no = 0
            rec = {}
            applicant_id = app_liablity_obj.search(cr, uid, [('applicant_id','=',new_id)])
            if applicant_id:
                for business_id in applicant_id:
                    business = app_liablity_obj.browse(cr,uid,business_id).business
                    seq_no = app_liablity_obj.browse(cr,uid,business_id).seq_no
                    if rec.has_key(business):
                        pass
                    else:
                        rec[business] = seq_no
            for line in payment_lines:
                business = line.name
                if business:

                    if rec.has_key(business):
                        seq_no = rec[business]
                        app_payment_obj.write(cr,uid,[line.id],{'seq_no':seq_no})
        return new_id


    def write(self, cr, uid, ids, vals, context=None):
        if context==None:
            context={}
        if not isinstance(ids,list):
           ids = [ids]
        crm_browse = self.browse(cr,uid,ids[0])
        context.update({'crm_id':crm_browse})
        
        new_id = super(applicant_record, self).write(cr, uid, ids, vals, context=context)
        #if vals.has_key('signature'):
            #context.update({'lead_id':ids[0],'user_id':uid})
            #mod_obj = self.pool.get('ir.model.data')
            #template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_applicant_personal')
            #template_id = template and template[1] or False
            #if template_id:
                #print"template_id",template_id
                #self.pool.get('email.template').send_mail(cr,uid,template_id,ids[0],'True',context)
            #vals['consent_dateTime'] = datetime.now()
            #subject = ('''Credit Consent Provided:''')
            #details = ('''<b>Date / Time:</b> %s <br/> <b>Signature:</b>%s <br/> <b>Ip Address:</b>%s''') % (datetime.now(),vals.get('signature',False),vals.get('signature_ip',False))

            #self.message_post(cr, uid, ids, body=details, subject=subject, context=context)
        if vals.has_key('opp_id'):
            cr.execute('insert into opportunity_applicant_rel (opp_id,app_id) \
                                values (%s,%s)', (vals['opp_id'], ids))
        if not isinstance(ids, list):
            ids=[ids]
        liability_lines = self.browse(cr,uid,ids[0]).liabilities
        app_liablity_obj = self.pool.get('applicant.liabilities')
        if liability_lines:
            seq_no = 0
            for line in liability_lines:
                seq_no +=1
                app_liablity_obj.write(cr,uid,[line.id],{'seq_no':seq_no})

        payment_lines = self.browse(cr,uid,ids[0]).late_payments
        if payment_lines:
            app_payment_obj = self.pool.get('applicant.payment')
            seq_no = 0
            rec = {}
            applicant_id = app_liablity_obj.search(cr, uid, [('applicant_id','=',ids[0])])
            if applicant_id:
                for business_id in applicant_id:
                    business = app_liablity_obj.browse(cr,uid,business_id).business
                    seq_no = app_liablity_obj.browse(cr,uid,business_id).seq_no
                    if rec.has_key(business):
                        pass
                    else:
                        rec[business] = seq_no
            for line in payment_lines:
                business = line.name
                if business:

                    if rec.has_key(business):
                        seq_no = rec[business]
                        app_payment_obj.write(cr,uid,[line.id],{'seq_no':seq_no})

        

        return new_id

    def get_opportunity(self, cr, uid, ids, context=None):
        """ Escalates case to parent level """
        uid = 1
        print "ids>>>",ids
        crm_obj = self.pool.get('crm.lead')
        if ids:
            cr.execute('select opp_id from opportunity_applicant_rel where app_id in %s',(tuple(ids),))
            opp_ids= filter(None, map(lambda x:x[0], cr.fetchall()))
            res = self.pool.get('ir.model.data')
            tree_res = res.get_object_reference(cr, uid, 'crm', 'crm_case_tree_view_oppor')
            tree_id = tree_res and tree_res[1] or False
            form_res = res.get_object_reference(cr, uid, 'crm', 'crm_case_form_view_oppor')
            form_id = form_res and form_res[1] or False

            return {
                'name': _('Opp'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'crm.lead',
                'res_id': False,
                'view_id': False,
                'views': [(tree_id, 'tree'), (form_id, 'form')],
                'target': 'current',
                'type': 'ir.actions.act_window',
                'domain': [('id','in',opp_ids)]
            }

    def send_to_equifax(self, cr, uid, id, context=None):
        print " equifax request ###########################"

#        cxcn = pyodbc.connect('DRIVER={FreeTDS};SERVER=107.23.158.12;PORT=1433;DATABASE=MCE;UID=MCE;PWD=qaz1QAZ!')
#        cxcn = pyodbc.connect('DRIVER={FreeTDS};SERVER=107.23.158.12;PORT=1433;DATABASE=MCE;UID=MCE;PWD=qaz1QAZ!')
	cxcn = pyodbc.connect('DRIVER={FreeTDS};SERVER=198.72.106.7;PORT=1433;DATABASE=MCE;UID=MCE;PWD=qaz1QAZ!')
        cursor = cxcn.cursor()
        cursor.execute("SELECT MAX(nInqIdx)+1 FROM Inquiry")
        next_ninqidx = cursor.fetchall()
        print 'next_ninqidx&&&&&&&&&&&&&&&&&&&&&&',next_ninqidx[0][0]
        if next_ninqidx:
            self.write(cr,uid,id,{'ninqidx':next_ninqidx[0][0]})
            browse_data = self.browse(cr,uid,id[0])
            last_name = browse_data.applicant_last_name or ''
            frst_name = browse_data.applicant_name or ''
            dob = browse_data.dob or ''
            dobf = dob.replace("-",'')
	    print "123-----dobf----",dobf
            sin = browse_data.sin or ''
	    sin=sin.replace('-', '')
	    sin=sin.replace(' ', '')
	    print "sin--------------------------",sin
            applicant_address_obj = self.pool.get('applicant.address')
#            get the id of latest address
            address_ids = applicant_address_obj.search(cr, uid, [('applicant_id','=',id[0])])
            print "address_ids&&&&&&&&&&&&&",address_ids
	    if address_ids:
	        addrbrowse = applicant_address_obj.browse(cr, uid, address_ids[0])
	        city = addrbrowse.city or ''
                province = addrbrowse.province or ''
                postal_code = addrbrowse.postal_code or ''


		name = addrbrowse.name or ''
                print"name---------------",name
                no=""
		apt=''
                if name[0].isdigit():
		    nm=name.replace(" ", "")
		    print "nm-----------------",nm
		    check=name.find('-')
		    if check != -1:
			apt=name[:check]
			print "apt----------------",apt
			name=name[check+1:]
			nm=nm.replace("-", "")
			ap=apt.replace(" ","")
			print "appppppppppppp",ap
			nm=nm.replace(ap,"")
			print "name----name-----",name
		        print "nm-----------------",nm
                    r = re.compile("([0-9]+)([a-zA-Z]+)")
		    print "rrrrrrr----------------",r
                    m = r.match(nm)
		    if m and m!=None:
                    	print "mmmmmmmmmm------------",m
                    	no=m.group(1)
			print "noooo----------------",no
                    	name=name.replace(no, '')
		print "final_name-------------------",name
		name=name.replace('-', '')
		print "name!!!!!!!!!!!!!!!!!!!!!!!========",name
		if len(name)>25:
		    name=name[:25]
		    print "25-------------------------name",name
		print "insert into inquiry( nInqIdx ,nUserIdx ,nInqStatus ,eBur ,sNameLast ,sNameFirst ,sDOB ,sAddrApt ,sAddrCity ,sAddrState ,sAddrZip ,sSIN,sAddrStrNum ,sAddrStrName)values(?,?,?,?,?,?,?,?,?,?,?,?)",next_ninqidx[0][0],'1','1','1',str(last_name),str(frst_name),str(dobf),str(apt),str(city),str(province),str(postal_code),str(sin),str(no),str(name)
		#ero
                cursor.execute("insert into inquiry"\
                "( nInqIdx ,nUserIdx ,nInqStatus ,eBur ,sNameLast ,sNameFirst ,sDOB ,sAddrApt ,sAddrCity ,sAddrState ,sAddrZip ,sSSN ,sAddrStrNum ,sAddrStrName)"\
                "values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",next_ninqidx[0][0],'1','1','1',str(last_name),str(frst_name),str(dobf),str(apt),str(city),str(province),str(postal_code),str(sin),str(no),str(name))
		
		#print "insert into inquiry( nInqIdx ,nUserIdx ,nInqStatus ,eBur ,sNameLast ,sNameFirst ,sDOB ,sAddrApt ,sAddrCity ,sAddrState ,sAddrZip ,sSIN)values(?,?,?,?,?,?,?,?,?,?,?,?)",next_ninqidx[0][0],'1','1','1',str(last_name),str(frst_name),str(dobf),'',str(city),str(province),str(postal_code),str(sin)
                cxcn.commit()
                cursor.execute("SELECT MAX(nInqIdx) FROM Inquiry")
                next_ninqidx = cursor.fetchall()
                print 'next_ninqidx&&&&&&&&&&&&&&&&&&&&&&',next_ninqidx[0][0]
                cxcn.close()
	    else:
                raise osv.except_osv((''),('proper address not found..'))
        return True


    def fetch_equifax_response(self, cr, uid, id, context=None):
        print " equifax response#############################",id
        applicant_record_obj = self.pool.get('applicant.record')
        browse_record = applicant_record_obj.browse(cr,uid,id[0])
        ninqidx = browse_record.ninqidx or ''
        print "ninqidx..........................",ninqidx

        if ninqidx:
            #cxcn = pyodbc.connect('DRIVER={FreeTDS};SERVER=107.23.158.12;PORT=1433;DATABASE=MCE;UID=MCE;PWD=qaz1QAZ!')
	    cxcn = pyodbc.connect('DRIVER={FreeTDS};SERVER=198.72.106.7;PORT=1433;DATABASE=MCE;UID=MCE;PWD=qaz1QAZ!')
            cursor = cxcn.cursor()
            cursor.execute("select * from RmAddr where ninqidx = ?",ninqidx)
            cust_address = cursor.fetchall()
            
            if cust_address:		
                applicant_address_obj = self.pool.get('applicant.address')
#               remove previous addresses to avoid duplication
                lines = applicant_address_obj.search(cr, uid, [('applicant_id','=',id[0]),('equifax_addr','=',True)], context=context)
                print "linessssssssssssssssssssssssssssssss:",lines
                if lines:
                    applicant_address_obj.unlink(cr, uid, lines, context=context)		
                for addr in cust_address:
                    applicant_address_obj.create(cr, uid, {'name':addr[5],'street':addr[9],'city':addr[10], 'province':addr[11],'postal_code':addr[12],'date':addr[17],'applicant_id':id[0],'equifax_addr':True},context=None)
	    else:
                raise osv.except_osv((''),("We were unable to retrieve complete credit information for this applicant.  Please confirm Name, Address, Date of Birth and Social Insurance number for accuracy."))
	
            cursor.execute("select * from RmModel where ninqidx = ?",ninqidx)
            cust_model = cursor.fetchall()
            if cust_model:
                for model in cust_model:
                    if model[5]=='BN':
                        applicant_record_obj.write(cr, uid, id, {'beacon_9_score':'', 'beacon_5_score':model[4],'ers_2_score':'','crp_3_score':''})

#           Bankruptcy Discharge Date
            cursor.execute("select dtSettled,sBurSeg from RmPubRec where nInqIdx = ?",ninqidx)
            rmpub = cursor.fetchall()
            if rmpub:
                if rmpub[0][1]=='BP':
                    applicant_record_obj.write(cr, uid, id,{'bankruptcy_discharge_date':rmpub[0][0]})
#           ODP Discharge Date
            cursor.execute("select dtSettled,sRecType from RmPubRec where nInqIdx = ?",ninqidx)
            odp_discharge = cursor.fetchall()
            if odp_discharge:
                if odp_discharge[0][1]=='R' or odp_discharge[0][1]=='s' or odp_discharge[0][1]=='T':
                    applicant_record_obj.write(cr, uid, id,{'odp__discharge_date':odp_discharge[0][0]})
#           Date Bureau Obtained
            cursor.execute("select dtburcreate,sburtime from Respgen where nInqIdx = ?",ninqidx)
            dt = cursor.fetchall()

            if dt:
                if dt[0][0] and dt[0][1]:
                    print dt[0][0]
                    print dt[0][1]
                    applicant_record_obj.write(cr, uid, id,{'date_time_bureau_obtained':dt[0][0]+' '+dt[0][1]})
                else:
                    a = datetime.strptime(dt[0][0], "%Y%m%d")
                    print "Date Bureau Obtaineddddddddddd",a
                    applicant_record_obj.write(cr, uid, id,{'date_time_bureau_obtained':a})
                
            date_format = "%Y%m%d"
#                a = datetime.strptime(dt[0][0], date_format)
#                b = datetime.strptime(dt[0][1], date_format)
#                delta = b - a
#                print "delta.days::::::",delta.days
#                delta = a + timedelta(days=delta.days)
#                print "delta::::",delta
#                applicant_record_obj.write(cr, uid, id,{'date_time_bureau_obtained':delta})


            cursor.execute("select fHasBankruptcy,nCntInq,sAlertCodes,sBurErrCodes,sBurErrText,sAlertKeywords from RptSummary where ninqidx = ?",ninqidx)
            cust_rptsummary = cursor.fetchall()
            if cust_rptsummary:
                print "cust_rptsummary:",cust_rptsummary
                bankruptcy = False
                if cust_rptsummary[0][0]==1:
                    bankruptcy = True                
                applicant_record_obj.write(cr, uid, id, {'bankruptcy':bankruptcy,'total_inquires':cust_rptsummary[0][1]})
                print "crm id*********************************",browse_record.applicant_id or ''
                opp_id = browse_record.applicant_id or ''
                opp_obj = self.pool.get('crm_lead')
                notes = cust_rptsummary[0][2]

#                opp_obj.write(cr, uid, opp_id, {'internal_note':notes})

#           libilities
            #cursor.execute("select sECOA,sMemName,sNarrCode_1,sType_RIOMC,nAmtLimit,nAmtBalance,nAmtMonthPay,dtOpened,dtReported,dtLastActive,sEvalCode from RmTrade where ninqidx = ?",ninqidx)
	    cursor.execute("select sECOA,sMemName,sNarrCode_1,sType_RIOMC,nAmtHighCred,nAmtBalance,nAmtMonthPay,dtOpened,dtReported,dtLastActive,sEvalCode from RmTrade where ninqidx = ?",ninqidx)
            cust_trade = cursor.fetchall()
	    print "cust_tradecust_tradecust_tradecust_trade==============",cust_trade
            if cust_trade:
#                remove previous liabilities to avoid duplication
                applicant_libilities_obj = self.pool.get('applicant.liabilities')
                lines = applicant_libilities_obj.search(cr, uid, [('applicant_id','=',id[0]),('equifax_liabilities','=',True)], context=context)
                
                if lines:
                    applicant_libilities_obj.unlink(cr, uid, lines, context=context)              
                for trade in cust_trade:
                    Status = ''
                    if trade[2] == 'AT' or trade[2] == 'AV' or trade[2] == 'HM':
                            Status = 'closed'
                    elif trade[2] == 'BD' or trade[2] == 'BE' or trade[2] == 'BH' or trade[2] == 'CG':
                            Status = 'paidnclosed'
                    elif trade[2] == 'BF' or trade[2] == 'BP' or trade[2] == 'BQ' or trade[2] == 'CX' or trade[2] == 'ER' or trade[2] == 'ET':
                            Status = 'paid'
                    elif trade[2] == 'BC' or trade[2] == 'EV':
                            Status = 'refinanced'
                    elif trade[2] == 'BI' or trade[2] == 'BJ':
                            Status = 'transfer_sold'
                    elif trade[2] == 'AK' or trade[2] == 'AL' or trade[2] == 'BT' or trade[2] == 'EU':
                            Status = 'written_off'
                    print "Status",Status
		    print "credit_limit------------------------------",trade[4]
                    applicant_libilities_obj.create(cr, uid,{'name':'a', 'business':trade[1],'status':Status,'type':trade[3],'credit_limit':trade[4],'credit_balance':trade[5],'monthly_payment':trade[6],'opened':trade[7],'reported':trade[8],'dla':trade[9],'rating':trade[10],'applicant_id':id[0], 'equifax_liabilities':True},context=None)

#        late payments
            cursor.execute("select dtPrev_1,dtPrev_2,dtPrev_3,sMemName,sEvalCode from RmTrade where ninqidx = ?",ninqidx)
            cust_payments = cursor.fetchall()
            
            if cust_payments:
                applicant_late_payment_obj = self.pool.get('applicant.payment')
		lines = applicant_late_payment_obj.search(cr, uid, [('applicant_id','=',id[0]),('equifax_applicant_payment','=',True)], context=context)
                
                if lines:
                    applicant_late_payment_obj.unlink(cr, uid, lines, context=context)
                for payment in  cust_payments:
                    if str(payment[0])!='None':
                        print "payment[0]::",payment[0]
                        days = ''
                        sevalcode = {'0':'New','1':'0','2':'30','3':'60','4':'90','5':'120','7':'Consol','8':'Repo','9':'Collect'}
                        if payment[4] in sevalcode.keys():
                            days = sevalcode[payment[4]]
                            print days
                            applicant_late_payment_obj.create(cr,uid,{'name':payment[3],'date':payment[0],'rating':payment[4],'days':days,'applicant_id':id[0],'equifax_applicant_payment':True})
                for payment in  cust_payments:
                    if str(payment[1])!='None':
                        
                        days = ''
                        sevalcode = {'0':'New','1':'0','2':'30','3':'60','4':'90','5':'120','7':'Consol','8':'Repo','9':'Collect'}
                        if payment[4] in sevalcode.keys():
                            days = sevalcode[payment[4]]
                            print days
                            applicant_late_payment_obj.create(cr,uid,{'name':payment[3],'date':payment[1],'rating':payment[4],'days':days,'applicant_id':id[0], 'equifax_applicant_payment':True})
                for payment in  cust_payments:
                    if str(payment[2])!='None':
                        
                        days = ''
                        sevalcode = {'0':'New','1':'0','2':'30','3':'60','4':'90','5':'120','7':'Consol','8':'Repo','9':'Collect'}
                        if payment[4] in sevalcode.keys():
                            days = sevalcode[payment[4]]
                            print days
                            applicant_late_payment_obj.create(cr,uid,{'name':payment[3],'date':payment[2],'rating':payment[4],'days':days,'applicant_id':id[0], 'equifax_applicant_payment':True})
#            collections
            cursor.execute("select sPlaintiff,nAmt,nAmtBalance,dtFiled,sEvalCode from RmPubRec where ninqidx = ?",ninqidx)
            cust_RmPubRec = cursor.fetchall()
	    applicant_collection_obj = self.pool.get('applicant.collection')
            if cust_RmPubRec:
		lines = applicant_collection_obj.search(cr, uid, [('applicant_id','=',id[0]),('equifax_applicant_collection','=',True)], context=context)
                if lines:
                    applicant_collection_obj.unlink(cr, uid, lines, context=context)               
                for rmpub in cust_RmPubRec:
                    print  "%%%%%%%%",rmpub
                    applicant_collection_obj.create(cr, uid, {'name':rmpub[0],'amount':rmpub[1],'balance':rmpub[2],'date':rmpub[3],'status':'closed','applicant_id':id[0],'equifax_applicant_collection':True})

#            Incomes & Employers
            cursor.execute("select sEmployer,sOccupation,sIndVerify,dtLeftPosted,dtEmployed from RmEmp where ninqidx = ?",ninqidx)
            cust_RmEmp = cursor.fetchall()
            if cust_RmEmp:
#                remove record to avoid duplication
                income_employer_obj = self.pool.get('income.employer')
		income_employer_obj = self.pool.get('income.employer')
                lines = income_employer_obj.search(cr, uid, [('applicant_id','=',id[0]),('equifax_income_employer','=',True)], context=context)
                if lines:
                    income_employer_obj.unlink(cr, uid, lines, context=context)

                for rmemp in cust_RmEmp:
#                    if rmemp[3] and rmemp[4]:
                    if '20030415' and '20030413':
                        a = datetime.strptime('20070915', date_format)
                        b = datetime.strptime('20030412', date_format)
                        delta = a - b
                        print "delta.days::::::",delta.days
                        delta = delta.days
                        month = ''
                        if delta < 365:
                                month = '1'
                        elif delta >= 365 and delta < 1095:
                                month = '2'
                        elif delta >= 1095 and delta < 1825:
                                month = '3'
                        elif delta >= 1825:
                                month = '4'
                        print "month::",month
                        income_employer_obj.create(cr, uid,{'business':rmemp[0],'position':rmemp[1],'industry':rmemp[2],'month':month ,'applicant_id':id[0], 'equifax_income_employer':True})
#          Audit trail            
            cursor = cxcn.cursor()
            cursor.execute("select srpt from Rpttext where ninqidx = ?",ninqidx)
            cust_notes = cursor.fetchall()
            if cust_notes:
                if cust_notes[0] and cust_notes[0][0]:
                    
                    applicant_record_obj.write(cr, uid, id, {'credit_report':cust_notes[0][0]})

#                result = base64.b64encode(cust_notes[0][0])
#                file_name = "Credit_Report.txt"
#                self.pool.get('ir.attachment').create(cr, uid,
#                                                      {
#                                                       'name': file_name,
#                                                       'datas': result,
#                                                       'datas_fname': file_name,
#                                                       'res_model': self._name,
#                                                       'res_id': id[0],
#                                                       'type': 'binary'
#                                                      },
#                                                      context=context)

        return True


applicant_record()



class applicant_property(osv.osv):
    _name = 'applicant.property'
    _columns = {
        'name':fields.char('Address',size=240),
        'value':fields.float('Value',size=240),
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
    _rec_name = "income_type"
    _columns={
            'income_type':fields.selection([('1','Employed'),('2','SelfEmployed'),('3','Retired'),('4','Commission'),('5','Interest'),('6','Pension'),('7','Overtime'),('8','Bonus'),('9','Rental'),('10','ChildTaxCredit'),('11','LivingAllowance'),('12','VehicleAllowance'),('13','Other'),('14','Maternity'),('15','Probation')],'Type'),
           # 'name':fields.selection([('1','Employed'),('2','SelfEmployed'),('3','Retired'),('4','Commission'),('5','Interest'),('6','Pension'),('7','Overtime'),('8','Bonus'),('9','Rental'),('10','ChildTaxCredit'),('11','LivingAllowance'),('12','VehicleAllowance'),('13','Other')],'Type'),
            'industry':fields.text('Industry'),
            'business':fields.char('Business',size=120),
            'position':fields.char('Job Title',size=120),
            'annual_income':fields.char('Annual Income',size=120),
            #'month':fields.selection([('1','Less Than 1 Year'),('2','1-3 Year'),('3','3-5 Years'),('4','5+ Years')],'Months'),
            'month':fields.integer('Months'),
            'applicant_id':fields.many2one('applicant.record','Applicant'),
	    'equifax_income_employer':fields.boolean('equifax_income_employer'),
	    'historical':fields.boolean('Historical'),
            'supplementary':fields.boolean('Supplementary'),
            'address_property':fields.integer('Address Property'),		
            'property_id':fields.char('PropertyID',size=120),
            'income':fields.integer('Income Source', help='it indicates the source of income from webform. 1-applicant income, 2-income2, 3-income3, 4-rental income'),
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
	'equifax_addr':fields.boolean('Equifax Address'),
    }
    _order = 'date desc'
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
       # 'status':fields.selection([('paid','Paid'),('closed','Closed'),('transfer_sold_paid','Transfer/Sold/Paid'),('lost_stolen','Lost/Stolen'),('refinanced','Refinanced'),('transfer_sold','Transfer/Sold'),('written_off','Written Off')],'Status'),
	'status':fields.selection([('paid','Paid'),('closed','Closed'),('transfer_sold_paid','Transfer/Sold/Paid'),('lost_stolen','Lost/Stolen'),('refinanced','Refinanced'),('transfer_sold','Transfer/Sold'),('written_off','Written Off'),('accountpaid','Account paid'),('paidnclosed','Paid And Closed')],'Status'),
        'type':fields.char('Type',size=120),
        'credit_limit':fields.float('Credit Limit'),
#        'credit_limit':fields.selection([('Yes','Yes'),('No','No')],'Credit Limit'),
        'credit_balance':fields.float('Credit Balance'),
        'monthly_payment':fields.char('Monthly Payment',size=120),
        'opened':fields.date('Opened'),
        'reported':fields.date('Reported'),
        'dla':fields.date('DLA'),
        'rating':fields.char('Rating',size=120),
        'pay_off':fields.float('Pay Off'),
        'applicant_id':fields.many2one('applicant.record','Applicant'),
        'seq_no':fields.integer('#'),
	'equifax_liabilities':fields.boolean('Equifax Liabilities'),	
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
	'equifax_applicant_collection':fields.boolean('equifax_applicant_collection')
    }
applicant_collection()

class applicant_payment(osv.osv):
    _name='applicant.payment'
    _order = 'seq_no,date'
    _columns={
        'name':fields.char('Business',size=120),
        #'status':fields.selection([('a','A'),('b','B')],'Status'),
        'date':fields.date('Date Late'),
        'rating':fields.char('Rating',size=120),
        'days':fields.char('Days',size=120),
        'reason':fields.char('Reason',size=120),
        'applicant_id':fields.many2one('applicant.record','Applicant'),
        'seq_no':fields.integer('#'),
	'equifax_applicant_payment':fields.boolean('equifax_applicant_payment')
    }
applicant_payment()

