from osv import fields,osv
import datetime
from base_status.base_stage import base_stage
import tools
from tools.translate import _
from tools import html2plaintext
AVAILABLE_STATES = [
    ('draft', 'New'),
    ('cancel', 'Cancelled'),
    ('open', 'In Progress'),
    ('pending', 'Pending'),
    ('done', 'Closed'),
    ('task','Task'),
    ('all_product','All Product'),
    ('post_selection','Post Selection'),
    ('lender_submission','Lender Submission'),
]
class crm_cases(osv.osv):
    _name = "crm.cases"
    _description = "cases for underwiter"
    _columns = {
                'title':fields.char('Title',size=240,required=True),
                'name':fields.many2one('hr.employee','Assigned TO',required=True),
                'description':fields.text('Description'),
                'underwriter_stage':fields.selection([('application_pending','Application Pending'),('credir_check','Credit Check'),('partial_appliaction','Partial Appliaction'),
                    ('collection_docs','Collection Docs'),('verifying_info','Verifying Info'),('at_lender','At Lender'),('match_product','Match Product'),
                    ('pending_file_complete','Pending File Complete'),('pending_compensation','Pending Compensation'),('partial_paid','Partial Paid'),
                    ('paid_closed','Paid Closed'),('lost','Lost')]),
                'creadted_by':fields.many2one('res.users','Creadted By',readonly=True),    
    }
    _defaults = {
        'underwriter_stage':'application_pending',
        'creadted_by': lambda obj, cr, uid, context: uid,
    }
    
crm_cases()

class crm_case_stage(osv.osv):
    _inherit='crm.case.stage'
    _columns={
        'state': fields.selection(AVAILABLE_STATES, 'Related Status', required=True,
            help="The status of your document will automatically change regarding the selected stage. " \
                "For example, if a stage is related to the status 'Close', when your document reaches this stage, it is automatically closed."),

    }
