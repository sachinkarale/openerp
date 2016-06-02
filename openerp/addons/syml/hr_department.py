from openerp.osv import fields, osv
from openerp import tools

class hr_department(osv.osv):
    _inherit = 'hr.department'
    _columns={


    'user_new_groups_id':fields.many2one('user.new.groups','Groups'),
    'email':fields.char('Email', size=64),
    'extension':fields.integer('Extension'),
    'mail_server':fields.many2one('ir.mail_server','Email Server'),


    }

hr_department()


class user_new_groups(osv.osv):
    _name = 'user.new.groups'
    _columns={


    'name':fields.char('Name'),


    }

user_new_groups()