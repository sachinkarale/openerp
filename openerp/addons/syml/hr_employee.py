from osv import fields,osv
import datetime
from base_status.base_stage import base_stage
import tools
from tools.translate import _
from tools import html2plaintext


class hr_employee(osv.osv):
    _inherit = 'hr.employee'
    
    _columns = {
        'job_id': fields.many2one('hr.job','Role'),
        'parent_id': fields.many2one('hr.employee', 'Reporting Manager'),
        'parent_compensation_id': fields.many2one('hr.employee', 'Compensation manager'),
        'child_compensation_ids': fields.one2many('hr.employee', 'parent_compensation_id', 'Compensation'),
#        'get_ids': fields.function(get_ids, string="fetch ids", type="integer", store=True),
    #    'employee_ids': fields.one2many('hr.employee', 'parent_id', 'Related employees'),
        }

hr_employee()