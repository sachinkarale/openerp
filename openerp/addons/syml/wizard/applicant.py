from openerp.osv import fields, osv
from openerp.tools.translate import _
from urllib import urlencode
from urlparse import urljoin


class applicant_wizard(osv.osv_memory):
    _name = 'applicant.wizard'
    _columns = {
        'name':fields.char('Applicant',size=256, readonly=True),
    }

    _defaults = {
#            'name':'http://localhost:8069/?db=pentaho&ts=1395810495933#id=10&view_type=form&model=applicant.record&action=491'
    }

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        applicant_id = context.get('active_ids',False)
        print "applicant_iddddd:",applicant_id        
        res = super(applicant_wizard, self).default_get(cr, uid, fields, context=context)       
        
#        generate a URL for the given applicant id
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
        print "base_urllllllll",base_url
        query = {'db': cr.dbname}
        fragment = {}
        fragment['id'] = applicant_id[0]
        fragment['view_type'] = 'form'        
        fragment['model'] = 'applicant.record'        
        print "fragmentttttt",fragment
        if applicant_id:
            url = urljoin(base_url,"?%s#%s"%(urlencode(query),urlencode(fragment)))
#            print "urllllllllllll",url
#            url = "http://localhost:8069/?db=%s&ts=1395810495933#id=%s&view_type=form&model=applicant.record&action=491"%(db,applicant_id[0])
            print "urlllllllllllll",url
            res.update({'name':url})
        return res
applicant_wizard()