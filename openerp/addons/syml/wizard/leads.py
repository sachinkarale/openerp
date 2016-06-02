from openerp.osv import fields, osv
from openerp.tools.translate import _


class create_leads(osv.osv_memory):
    _name = 'create.leads'
    _columns = {
        'name':fields.char('Name',size=124),
        'lead_ids':fields.many2many('res.partner','contact_leads_rel','contactid','leadid','Lead(s)'),
    }

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        record_ids = context.get('active_ids',False)
        print "record_idssss:",record_ids
        res = super(create_leads, self).default_get(cr, uid, fields, context=context)
        if record_ids:
            ress_ids = []
            browse_data = self.pool.get('res.partner').browse(cr, uid, record_ids, context=context)
            for rs in browse_data:
                if rs.newclientlead or rs.newhrlead or rs.newduallead:
                    ress_ids.append(rs.id)
            res.update({'lead_ids':ress_ids})
        return res
              
    def leads(self, cr, uid, fields, context=None):
        print "inside leads method##############################################"
        if context is None:
            context = {}
        
        active_ids = context.get('active_ids')
        print "active idssss",active_ids
        crm_lead = self.pool.get('crm.lead')
        hr_lead = self.pool.get('hr.applicant')
        res_partner = self.pool.get('res.partner')
        
        for id in active_ids:        
            print "id",id
            res_data = res_partner.browse(cr, uid, id)
            if res_data.newclientlead:                
                id = crm_lead.create(cr, uid,{
                                        'name': _('lead for %s' ) % res_data.name or '' ,
                                        'partner_id': res_data.id,
                                        'Spouse':res_data.spouse or '',
                                        'email_from':res_data.email or '',
                                        'phone':res_data.phone or '',
                                        'mobile':res_data.mobile or '',
                                        'fax':res_data.fax or '',
                                    })
                print "lead id",id                        
            if res_data.newhrlead:                
                id = hr_lead.create(cr, uid, {
                                     'name': _('HR lead for %s') % res_data.name or '' ,
                                     'partner_id': res_data.id,
                                     'contact':res_data.name or ''+' '+res_data.middle_name or ''+' ' +res_data.last_name or '',
                                     'email_from': res_data.email or '',
                                     'partner_phone':res_data.phone or '',
                                     'partner_mobile':res_data.mobile or ''
                                    })
                print "hr lead id:",id
            if res_data.newduallead:
                fname = res_data.name or ''
                mname = res_data.middle_name or ''
                lname = res_data.last_name or ''
                contact = fname +' '+ mname +' ' +lname
                print "contact:",contact
                
                crm_id = crm_lead.create(cr, uid,{
                                        'name': _('lead for %s' ) % res_data.name or '' ,
                                        'partner_id': res_data.id,
                                        'Spouse':res_data.spouse or '',
                                        'email_from':res_data.email or '',
                                        'phone':res_data.phone or '',
                                        'mobile':res_data.mobile or '',
                                        'fax':res_data.fax or '',
                                    }) 
                hr_id = hr_lead.create(cr, uid, {
                                     'name': _('HR lead for %s') % res_data.name or '' ,
                                     'partner_id': res_data.id,
                                     'contact':contact,
                                     'email_from': res_data.email or '',
                                     'partner_phone':res_data.phone or '',
                                     'partner_mobile':res_data.mobile or ''
                                    })
                print "crm_id %s and hr_id %s"%(crm_id,hr_id)
                
        return True

create_leads()