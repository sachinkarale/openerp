import time

from openerp.report import report_sxw

class appl_snap(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(appl_snap, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            '_get_address':self._get_address,
        })

    def _get_address(self,line):
        add=""
        

        if line.address_ids:
            for add_id in line.address_ids:
                add += add_id.name or ''+","+add_id.street or ''+"\n"
                add += add_id.city or ''+","+add_id.province or ''+","+add_id.postal_code or ''+ "\n"
                
            print"add",add

        return add
report_sxw.report_sxw('report.appl.snap3', 'crm.lead', 'syml/report/applicant_snapshot.rml', parser=appl_snap, header="external")
