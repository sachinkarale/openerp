
import subprocess
from openerp.osv import osv, fields


class moreweb_request(osv.osv):
    _name = 'moreweb.request'
    _description = "class to send request to morEWB "
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer', ondelete='set null', track_visibility='onchange', select=True, required=True),
        'title':fields.char('Salutation',size=20),
        'name': fields.char('First Name', size=128, select=True, required=True),
        'middle_name': fields.char('Middle Name', size=128, select=True,),
        'last_name': fields.char('Last Name', size=128, select=True,required=True),
        'application_no':fields.char('Application No',size=20, readonly=True),
        'maritalStatus': fields.selection([('1', 'Single'),('2','Married'),('3','Widowed'),('4','Separated'),('5','Divorced'),('6','Common law'),('7','Other')], 'MaritalStatus'),
        'birth_date': fields.date('Birth Date', required=True),
        'numberOfDependents':fields.char('Number of Depends',size=20),
        'state_field': fields.selection([
            ('draft', 'Draft Quotation'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done')
            ], 'State'),
       'asset_type':fields.char('Asset Type',size=120),   
       'asset_value':fields.char('Asset Value',size=120),
       'asset_description':fields.char('Asset Description',size=120),
       'street':fields.char('Street',size=120),
       'city':fields.char('City',size=120),
       'po':fields.char('po',size=120),
       'email':fields.char('email',size=120),
       'job_position':fields.char('Job Position',size=120),
#       'opportunity_id':fields.many2one('crm.lead','lead'),
#       'crm_asset_ids':fields.related('opportunity_id','asset_ids',type='one2many',relation='crm.asset',string='Crm Asset',store=True),
       
    }

    def onchange_contact(self, cr, uid, ids, partner_id = False):
        obj_res_partner = self.pool.get('res.partner').browse(cr,uid,partner_id)
#        crm_obj = self.pool.get('crm.lead')
#        opp_ids = crm_obj.search(cr, uid, [('partner_id','=',partner_id)])        
#        print "opp_idsopp_idsopp_idsopp_idsopp_idsopp_ids",opp_ids
#        browsed_data = crm_obj.browse(cr,uid,opp_ids[0])        
#        print "browsed_databrowsed_databrowsed_databrowsed_data",browsed_data
#        for each_crm_asset_object in browsed_data.asset_ids:
#            print "inside for loop"
#            asset_type = each_crm_asset_object.asset_type.name 
#            asset_description = each_crm_asset_object.name
#            asset_value = each_crm_asset_object.value
        title = obj_res_partner.name_title.name or ''        
        po = obj_res_partner.po_box or ''
        city = obj_res_partner.city or ''
        street = obj_res_partner.street or ''     
        job_position = obj_res_partner.function or ''     
        name = obj_res_partner.name or ''
        last_name = obj_res_partner.last_name or ''
        middle_name = obj_res_partner.middle_name or ''
        email = obj_res_partner.email or ''
        spouse = obj_res_partner.spouse or ''
        
        
        print "spouse",spouse
        print "name and last_name",name,last_name
        return {'value':{'title':title, 'name': name, 'middle_name':middle_name, 'last_name':last_name, 'email':email,'job_position':job_position, 'street':street, 'city':city, 'po':po}}
    
    def send_morweb_request(self,cr,uid,ids,context=None):
        print "inside send_morweb_request++++++++++++++++++"
        print "uid",uid
        print "ids",ids
        
        title = self.browse(cr,uid,ids[0]).title or ''
        fstname = self.browse(cr,uid,ids[0]).name or ''
        middleName = self.browse(cr,uid,ids[0]).middle_name or ''
        email = self.browse(cr,uid,ids[0]).email or ''
        function = self.browse(cr,uid,ids[0]).job_position or ''
        maritalStatus = self.browse(cr,uid,ids[0]).maritalStatus or ''
        print "maritalStatusmaritalStatusmaritalStatus",maritalStatus
        
        dateBirth = self.browse(cr,uid,ids[0]).birth_date or ''
        print "dateBirth",dateBirth
        numberOfDependents= self.browse(cr,uid,ids[0]).numberOfDependents or ''
        print "numberOfDependents",numberOfDependents
        
        po = self.browse(cr,uid,ids[0]).po or ''
        city =self.browse(cr,uid,ids[0]).city or ''
        street = self.browse(cr,uid,ids[0]).street or ''
        city_street = city +" , "+ street
        print "street",street
        
        print "city_streettttttttt",city_street
        lstname = self.browse(cr,uid,ids[0]).last_name or ''
        state_field = self.browse(cr,uid,ids[0]).state_field or ''
        print "state_field?????????" ,state_field
        
        print "lastname///////////////////",lstname
        print "firstname///////////////",fstname
        fo = open('/opt/lampp/htdocs/syml/phptest.php', 'r')
        lines = fo.readlines()
        temp=lines[47]
        temp1=lines[49]
        temp2=lines[40]
        temp3=lines[34]
        temp4=lines[35]
        fo.close()
        print "before repalceeeeee temp",temp
        print "before repalceeeeee temp3",temp3        
        print "before repalceeeeee temp4",temp4
        
        newsting = '<CustomerBorrower key="MainCustomerKey1" honorific="1" lastName="%s" firstName="%s" emailAddress1="%s" maritalStatus="%s" dateBirth="%s" numberOfDependents="%s">  \n'%(lstname,fstname,email,maritalStatus,dateBirth,numberOfDependents)
        newsting1 ='<Employment employmentType="1" employmentStatus="10" dateStart="2008-03-30" jobTitle="%s" companyName="bistasolutions"> \n'%(function)
        newstring2 ='<ApplicationAddressCanada key="MainCurrentAddKey3" cityTown="%s" provinceCode="10" postalCode="M1M1M1" countryCode="1"> \n'%(city_street)
        newstring3 ='<ApplicationAddressCanada key="MainCurrentAddKey1" cityTown="%s" provinceCode="10" postalCode="V2A1A5" countryCode="1"> \n'%(city)
        newstring4 ='<PostalAddressStreetAddress unitNumber="0" streetNumber="0" streetName="%s" streetType="-1" streetDirection="-1" POBoxRRNumber=""/> \n'%(street)
        temp = temp.replace(temp,newsting)
        temp1 = temp1.replace(temp1,newsting1)
        temp2 = temp2.replace(temp2,newstring2)
        temp3 = temp3.replace(temp3,newstring3)
        temp4 = temp4.replace(temp4,newstring4)
        
        lines[47]=temp
        lines[49]=temp1
        lines[40]=temp2
        lines[34]=temp3
        lines[35]=temp4
        
        out = open('/opt/lampp/htdocs/syml/phptest.php', 'w')
        out.writelines(lines)
        out.close()

        # if you want output        
        proc = subprocess.Popen("php /opt/lampp/htdocs/syml/phptest.php", shell=True, stdout=subprocess.PIPE)
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
        
        return True
        
        
moreweb_request()