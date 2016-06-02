import time

from openerp.report import report_sxw

class product_choice(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(product_choice, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'name_convention_desired':self._name_convention_desired,
            'name_convention_fixed':self._name_convention_fixed,
            'name_convention_variable':self._name_convention_variable,
            'name_convention_varvsfixed':self._name_convention_varvsfixed,
            'name_convention_recommendation':self._name_convention_recommendation,
            'name_convention_paymentoption':self._name_convention_paymentoption,
            'get_name':self._get_name,
            'get_add':self._get_add,
            'suitability_func':self._suitability_func,
            'borderline_notes':self._borderline_notes,
            'suitalibilty_notes':self._suitalibilty_notes,
        })



    def _get_name(self,o):
        
        name=""
        for applicant_rec in o.applicant_record_line:            
            if applicant_rec.primary:
                name+=" "+applicant_rec.applicant_name+","

        name=name[:-1]
        return name


    def _suitability_func(self,no):        
        a=int(no)
        str=""
        if a==1:
            str="Strongly Disagree"            
            return str
        elif a==2:
            str="Somewhat Disagree"           
            return str
        elif a==3:
            str="Not Sure"            
            return str
        elif a==4:
            str="Somewhat Agree"
            return str
        elif a==5:
            str="Strongly Agree"
            return str
        elif a==6:
            str="Choose not to Answer"
            return str

        return str
        



    def _get_add(self,line):
        add=""
        i=0

        if line.primary:
            for add_id in line.address_ids:                
                add+=add_id.name+","+add_id.street+"\n"
                add+=add_id.city+","+add_id.province+","+add_id.postal_code
                break
        
        return add

    def _name_convention_fixed(self,o):        
        i=0
        desired=""
        for deal_id in o.deal_ids:
            if deal_id.marketing_field=='FixedAnalysis' and deal_id.note_type=='ProposalInfo':
                i+=1
                num=i
                desired+="      "+deal_id.name+" "+'FixedAnalysis'+str(num)+","
        desired = desired[:-1]
        return desired
    def _name_convention_desired(self,o):        
        i=0
        desired=""
        for deal_id in o.deal_ids:
            print "deal note",deal_id.note_type
            if deal_id.marketing_field=='DesiredAnalysis' and deal_id.note_type=='ProposalInfo':
                i+=1
                num=i
                desired+="      "+deal_id.name+" "+'DesiredAnalysis'+str(num)+","
        desired = desired[:-1]
        return desired

    def _name_convention_variable(self,o):        
        i=0
        desired=""
        for deal_id in o.deal_ids:
            print "deal note",deal_id.note_type
            if deal_id.marketing_field=='VariableAnalysis' and deal_id.note_type=='ProposalInfo':
                i+=1
                num=i
                desired+="      "+deal_id.name+" "+'VariableAnalysis'+str(num)+","
        desired = desired[:-1]
        return desired

    def _name_convention_varvsfixed(self,o):        
        i=0
        desired=""
        for deal_id in o.deal_ids:
            print "deal note",deal_id.note_type
            if deal_id.marketing_field=='VarVsFixedAnalysis' and deal_id.note_type=='ProposalInfo':
                i+=1
                num=i
                desired+="      "+deal_id.name+" "+'VarVsFixedAnalysis'+str(num)+","
        desired = desired[:-1]
        return desired

    def _name_convention_recommendation(self,o):        
        i=0
        desired=""
        for deal_id in o.deal_ids:
            print "deal note",deal_id.note_type
            if deal_id.marketing_field=='Recommendation' and deal_id.note_type=='ProposalInfo':
                i+=1
                num=i
                desired+="      "+deal_id.name+" "+'Recommendation'+str(num)+","
        desired = desired[:-1]
        return desired

    def _name_convention_paymentoption(self,o):        
        i=0
        desired=""
        for deal_id in o.deal_ids:
            print "deal note",deal_id.note_type
            if deal_id.marketing_field=='PaymentOption' and deal_id.note_type=='ProposalInfo':
                i+=1
                num=i
                desired+="      "+deal_id.name+" "+'PaymentOption'+str(num)+","

        desired = desired[:-1]
        return desired

    def _suitalibilty_notes(self,o):
        i=0
        desired=""
        for deal_id in o.deal_ids:
            print "deal note",deal_id.note_type
            if deal_id.marketing_field=='Suitability' and deal_id.note_type=='ProposalInfo':
                i+=1
                num=i
                desired+="      "+deal_id.name+" "+'Suitability'+str(num)+","

        desired = desired[:-1]
        return desired

    def _borderline_notes(self,o):
        i=0
        desired=""
        for deal_id in o.deal_ids:
            print "deal note",deal_id.note_type
            if deal_id.marketing_field=='Borderline' and deal_id.note_type=='ProposalInfo':
                i+=1
                num=i
                desired+="      "+deal_id.name+" "+'Borderline'+str(num)+","

        desired = desired[:-1]
        return desired


report_sxw.report_sxw('report.crm.lead4', 'crm.lead', 'syml/report/product_choice.rml', parser=product_choice, header="external")
