from openerp.osv import fields, osv
import time
import datetime
from datetime import timedelta
from datetime import date
from openerp.tools.translate import _
from openerp.addons.base_status.base_stage import base_stage
import tools
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class task(base_stage, osv.osv):
    _inherit='project.task'
    _columns={
        'related_to':fields.many2one('crm.lead','Related To'),
        'hr_department_id':fields.many2one('hr.department','Team'),
#        'opportunity_id':fields.many2one('crm.lead','Opportunity'),
        'name': fields.char('Task Summary', size=256, required=True, select=True),
        'date_deadline': fields.datetime('Deadline',select=True),
        'related_call':fields.many2one('crm.phonecall','Related Call'), 
        'uw_app':fields.char('uwapp',size=256),
        'stage_id': fields.many2one('project.task.type', 'Stage', track_visibility='onchange',
                        ),
                        
    }




    def action_close(self, cr, uid, ids, context=None):
        """ This action closes the task
        """
        task_id = len(ids) and ids[0] or False
        self._check_child_task(cr, uid, ids, context=context)
        cr.execute("select id from project_task_type where name ilike 'Completed'")
        stage_id= filter(None, map(lambda x:x[0], cr.fetchall()))
        self.write(cr,uid,ids,{'stage_id':stage_id[0]})
        if not task_id: return False
        print"action close-------(cr, uid, [task_id], context=context)",cr, uid, [task_id], context
        return self.do_close(cr, uid, [task_id], context=context)

    def create(self, cr, uid, vals, context=None):
        
        print "values>>>>",vals
        deadline=vals.get('date_deadline')
#        DATETIME_FORMAT = "%Y-%m-%d"
        lead_obj=self.pool.get('crm.lead')
        if vals.get('related_to'):
            print "vals.get('related_to')-----------",vals.get('related_to')
            opp_name=lead_obj.browse(cr,uid,vals.get('related_to')).name
            project_obj=self.pool.get('project.project')
            if vals.get('project_id'):
                print "project_id===========",vals.get('project_id')
                project_obj.write(cr,uid,[vals.get('project_id')],{'name':opp_name})
            else:
                project_id=project_obj.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': opp_name  ,

                    },context=context)
                vals['project_id']= project_id

#                eroooooooo
#        ero
        if vals.get('date_deadline'):
            print "date_deadline============",vals.get('date_deadline')
            vals['date_end']= vals.get('date_deadline')
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            deadline=datetime.datetime.strptime(deadline,tools.DEFAULT_SERVER_DATETIME_FORMAT)
            start_date=(deadline - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
            vals['date_start']= start_date
            vals['date_end']= vals.get('date_deadline')
#            start_date=(vals.get('date_deadline') - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
#            ero
#        eroooooooo
        newid = super(task, self).create(cr, uid, vals, context)
        return newid

    def write(self, cr, uid, ids, vals, context=None):
        print"vals11345667",vals

        lead_obj=self.pool.get('crm.lead')
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        deadline=vals.get('date_deadline')
        project_obj=self.pool.get('project.project')
        if vals.get('stage_id',False):
                cr.execute('select id from project_task_type where id = %s and "name" ilike %s',(vals.get('stage_id',False),'completed',))
                stage_id = cr.fetchone()
                print "stage_id=========",stage_id
                if stage_id:
                    vals['user_id']=uid
                    user = self.pool.get('res.users').browse(cr ,uid ,uid)
                    subject = ('''Task has been completed''')
                    details = ('''User "%s" has completed the task''') % (user.name)

                    self.message_post(cr, uid, ids, body=details, subject=subject, context=context)


        if vals.has_key('date_deadline'):
            if vals['date_deadline'] != False:
                deadline=datetime.datetime.strptime(deadline,tools.DEFAULT_SERVER_DATETIME_FORMAT)
                start_date=(deadline - datetime.timedelta(hours=1))
                vals['date_end']= vals.get('date_deadline')
                vals['date_start']= start_date

        if vals.get('related_to'):
            print "vals.getrelatedto-------",vals.get('related_to')
            opp_name=lead_obj.browse(cr,uid,vals.get('related_to')).name
            print "name-----------------",opp_name
            if vals.get('project_id'):
                print "vals.projectedto-------",vals.get('project_id')
                project_obj.write(cr,uid,[vals.get('project_id')],{'name':opp_name})
            elif self.browse(cr,uid,ids[0]).project_id:
                proj_obj=self.browse(cr,uid,ids[0]).project_id
                proj_obj.write({'name':opp_name})
            else:
                project_id=project_obj.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': opp_name  ,

                    },context=context)
                vals['project_id']= project_id

        
        res = super(task, self).write(cr, uid, ids, vals)
        stage=self.browse(cr,uid,ids[0]).stage_id.name

        
        return res

    


    def open_team_task(self, cr, uid, ids, context=None):
        task = self.pool.get('project.task')
        if context is None:
            context = {}
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        result = mod_obj.get_object_reference(cr, uid, 'syml', 'action_view_team_task_syml')#view_quotation_tree,view_order_tree
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        uid_brw=self.pool.get('res.users').browse(cr,uid,uid)
        task_ids = task.search(cr, uid, [('hr_department_id','=', uid_brw.hr_department_id.id)], context=context)
        print"task_ids",task_ids
        result['domain'] = "[('id','in',["+','.join(map(str, task_ids))+"])]"
        #print "result2..........",result

        return result

    def case_close(self, cr, uid, ids, context=None):
        print "ids",ids
        """ Closes Task """
        if not isinstance(ids, list): ids = [ids]
        for task in self.browse(cr, uid, ids, context=context):

            vals = {}
            project = task.project_id
            for parent_id in task.parent_ids:
                if parent_id.state in ('pending','draft'):
                    reopen = True
                    for child in parent_id.child_ids:
                        if child.id != task.id and child.state not in ('done','cancelled'):
                            reopen = False
                    if reopen:
                        self.do_reopen(cr, uid, [parent_id.id], context=context)
            # close task
            vals['remaining_hours'] = 0.0
            if not task.date_end:
                vals['date_end'] = fields.datetime.now()
            vals['user_id']=uid
            user = self.pool.get('res.users').browse(cr ,uid ,uid)
            subject = ('''Task has been completed''')
            details = ('''User "%s" has completed the task''') % (user.name)

            self.message_post(cr, uid, ids, body=details, subject=subject, context=context)
            self.case_set(cr, uid, [task.id], 'done', vals, context=context)
        return True
task()