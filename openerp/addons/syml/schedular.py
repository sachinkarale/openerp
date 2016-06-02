from osv import osv, fields
import time
import datetime
from datetime import timedelta
from datetime import date
from dateutil import relativedelta
from openerp import SUPERUSER_ID, tools
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare


class schedulars_function(osv.osv):
    _name='schedulars.function'

    def paperwork_deadline(self,cr,uid,context={}):
        curr_date=time.strftime('%Y-%m-%d %H:%M:%S')
        cur_date_time=datetime.datetime.now()
        crm_obj=self.pool.get('crm.lead')
        mod_obj = self.pool.get('ir.model.data')
        project_task = self.pool.get('project.task')
        res_users_obj=self.pool.get('res.users')
#        event_ids=event_obj.search(cr,uid,[('recurring_next_date','=',datetime.date.today()),('duplicate_end_month','!=',datetime.date.today())])
        cr.execute("select id from crm_lead where deadline <= '%s' and dup_task_created=False"%(curr_date))
        lead_ids=filter(None, map(lambda x:x[0], cr.fetchall()))
        referral_name,app_name,assig_to='','',uid
        for each in lead_ids:

            lead_brw=crm_obj.browse(cr,uid,each)
            context.update({'crm_id':lead_brw})
            create_date=datetime.datetime.strptime(lead_brw.create_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
            create_date=(create_date + datetime.timedelta(hours=72)).strftime('%Y-%m-%d %H:%M:%S')
            if lead_brw.app_rec_ids:
                app_name=lead_brw.app_rec_ids[0].applicant_name
            if lead_brw.referred_source:
                referral_name=lead_brw.referred_source.partner_id.name
            name='Followup' + "  " + app_name + "  " + \
            'with a phone call and email to get the Documentation which was required for all applicants but not yet received.' \
            'Also send an email to' + " " + referral_name +" " +\
            'using the docs still outstanding template.'
            assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','broker'),('hr_department_id','=',lead_brw.hr_department_id.id)])
            if assig_to_ids:
                assig_to=assig_to_ids[0]
            project_task.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': name  ,
                    'date_deadline': str(create_date) ,
                    'hr_department_id':lead_brw.hr_department_id.id,
                    'related_to':each  or False,
                    'user_id': assig_to,
                    'create_date':datetime.datetime.now(),
                    'state':'open',
                    
                    },context=context)
            crm_obj.write(cr,uid,[each],{'dup_task_created':True},context)

        cr.execute("select id from crm_lead where delayed_app_date <= '%s' and delayed_app_task=False and stage_id in (select id from crm_case_stage where name='Partial App') "%(cur_date_time))
        del_app_ids=filter(None, map(lambda x:x[0], cr.fetchall()))
        print"del_app_ids",del_app_ids
        if del_app_ids:
            for each in del_app_ids:

                lead_brw=crm_obj.browse(cr,uid,each)
                if lead_brw.app_rec_ids:
                    app_name=lead_brw.app_rec_ids[0].applicant_name
                name='Followup' + "  " + app_name + "  " + \
                'with a phone call and complete Application by phone.'
                assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','broker'),('hr_department_id','=',lead_brw.hr_department_id.id)])
                if assig_to_ids:
                    assig_to=assig_to_ids[0]

                create_date=datetime.datetime.strptime(lead_brw.create_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
                create_date=(create_date + datetime.timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')

                project_task.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': name  ,
                    'date_deadline': str(create_date) ,
                    'hr_department_id':lead_brw.hr_department_id.id,
                    'related_to':each  or False,
                    'user_id': assig_to,
                    'create_date':datetime.datetime.now(),
                    'state':'open',

                    },context=context)
                crm_obj.write(cr,uid,[each],{'delayed_app_task':True},context)
        cr.execute("select id from crm_lead where lead_followup_date <= '%s' and lead_followed=False and stage_id in (select id from crm_case_stage where name='Partial App') "%(cur_date_time))
        del_app_ids=filter(None, map(lambda x:x[0], cr.fetchall()))
        print"del_app_ids",del_app_ids
        if del_app_ids:
            
            for each in del_app_ids:
                lead_name=''
                lead_brw=crm_obj.browse(cr,uid,each)
                context.update({'crm_id':lead_brw})
#                if lead_brw.app_rec_ids:
                lead_name=lead_brw.partner_id.name
                print"lead_name",lead_brw.partner_id
                
                name='Followup' + "  " + str(lead_name) + "  " + \
                'with a phone call and discover when they will be completing the Mortgage Application.'
                assig_to_ids=res_users_obj.search(cr,uid,[('designation','=','broker'),('hr_department_id','=',lead_brw.hr_department_id.id)])
                if assig_to_ids:
                    assig_to=assig_to_ids[0]

                create_date=datetime.datetime.strptime(lead_brw.create_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
                create_date=(create_date + datetime.timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')

                project_task.create(cr, uid, {
                    #'name': '%s: Task for %s %s' % (cur_obj.name or '', cur_obj.name2 , cur_obj.name3),
                    'name': name  ,
                    'date_deadline': str(create_date) ,
                    'hr_department_id':lead_brw.hr_department_id.id,
                    'related_to':each or False,
                    'user_id': assig_to,
                    'create_date':datetime.datetime.now(),
                    'state':'open',

                    },context=context)
                crm_obj.write(cr,uid,each,{'lead_followed':True},context)
        cr.execute("select id from crm_lead where congrats_date <= '%s' and greeting_send=False"%(curr_date))
        c_lead_ids=filter(None, map(lambda x:x[0], cr.fetchall()))
        print"c_lead_idsc_lead_idsc_lead_ids",c_lead_ids
        for c_each in c_lead_ids:

            crm_brw=crm_obj.browse(cr,uid,c_each)
            context.update({'lead_id':c_each,'user_id':uid,'crm_id':crm_brw})

            template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_congrats_client')
            template_id = template and template[1] or False
            if template_id:
#                    context.update({'proposal':ids[0],'user_id':uid})
                self.pool.get('email.template').send_mail(cr,uid,template_id,c_each,'True',context)
                todays_date=datetime.datetime.strptime(curr_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
                client_surv_rem_date=(todays_date + datetime.timedelta(hours=72)).strftime('%Y-%m-%d %H:%M:%S')
                crm_obj.write(cr,uid,[c_each],{'greeting_send':True,'client_survey':client_surv_rem_date},context)
        cr.execute("select id from crm_lead where client_survey <= '%s' and client_remd=False and client_email_rem=False"%(curr_date))
        client_lead_ids=filter(None, map(lambda x:x[0], cr.fetchall()))
        for client_each in client_lead_ids:

            c_crm_brw=crm_obj.browse(cr,uid,client_each)
            context.update({'lead_id':client_each,'user_id':uid,'crm_id':c_crm_brw})

            template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_client_survey_reminder')
            template_id = template and template[1] or False
            if template_id:
#                    context.update({'proposal':ids[0],'user_id':uid})
                self.pool.get('email.template').send_mail(cr,uid,template_id,client_each,'True',context)
                
                crm_obj.write(cr,uid,[client_each],{'client_email_rem':client_surv_rem_date},context)
        cr.execute("select id from crm_lead where congrats_date <= '%s' and completed_ref=False"%(curr_date))
        c_lead_ids1=filter(None, map(lambda x:x[0], cr.fetchall()))
        for c_each in c_lead_ids1:
            congrat_crm_browse = crm_obj.browse(cr,uid,c_each)
            context.update({'crm_id':congrat_crm_browse})
            template2 = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_completed_ref_source')
            template_id2 = template2 and template2[1] or False
            if template_id2:
#                    context.update({'proposal':ids[0],'user_id':uid})
                self.pool.get('email.template').send_mail(cr,uid,template_id,c_each,'True',context)
                crm_obj.write(cr,uid,c_each,{'completed_ref':True},context)
        cr.execute("select id from crm_lead where renewal_reminder <= '%s' and renewal_email_send=False"%(curr_date))
        renewal_lead_ids=filter(None, map(lambda x:x[0], cr.fetchall()))
        print"renewal_lead_idsrenewal_lead_ids",renewal_lead_ids
        for renewal_each in renewal_lead_ids:
            crm_browse = crm_obj.browse(cr,uid,renewal_each)
            context.update({'crm_id':crm_browse})
            renewal_template = mod_obj.get_object_reference(cr, uid, 'syml', 'email_template_renewal_letter')
            renewal_template_id = renewal_template and renewal_template[1] or False
            if renewal_template_id:
#                    context.update({'proposal':ids[0],'user_id':uid})
                self.pool.get('email.template').send_mail(cr,uid,renewal_template_id,c_each,'True',context)
                crm_obj.write(cr,uid,renewal_each,{'renewal_email_send':True},context)
        return True

schedulars_function()

