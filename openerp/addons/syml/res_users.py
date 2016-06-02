from osv import fields,osv
import datetime
from base_status.base_stage import base_stage
import tools
from tools.translate import _
from tools import html2plaintext


class res_users(osv.osv):
    _inherit = "res.users"
    _columns={
        "atmail_name": fields.char("Email Name", size=32),
        "atmail_usr_name": fields.char("Email", size=32),
        "atmail_passwrd": fields.char("Password", size=32),
        "hr_department_id": fields.many2one("hr.department", 'Team'),
        "designation":fields.selection([('admin','Admin'),('underwriter','Underwriter'),('assistant','Assistant'),('broker','Broker'),('other','Other')],'Position'),
    }
    
    def create(self, cr, uid, values, context=None):
        print "valuessssss",values
        emp_vals={}
        if values:
            name=values.get('name')
            department=values.get('hr_department_id')
            print "name------------department",name,department


        usr_id =super(res_users, self).create(cr, uid, values, context=context)
#
        print "usridddddddddddddddd",usr_id
        if name and department:
            emp_obj=self.pool.get('hr.employee')
            epl_val={'name':name,'department_id':department,'user_id':usr_id}
            emp_obj.create(cr,uid,epl_val,context=None)
#        eroooooooo
        return usr_id


#    def onchange_department_id(self, cr, uid, ids, hr_department_id, context={}):
#        value={}
#        if hr_department_id:
#            print "hr_department_idhr_department_id",hr_department_id
#            name=self.pool.get('hr.department').browse(cr,uid,hr_department_id).user_new_groups_id.name
#            print "nameeeeeeeeeeeeeeeeeeee",name
##            if name:
##                if name=='Broker':
##                    value.update({''})
##        eroooooooooo
        return True


res_users()    