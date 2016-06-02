# -*- encoding: utf-8 -*-
##############################################################################
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details, but reseller should inform 
#    or take permission from OpenERP4you before resell..
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#    
##############################################################################

from osv import osv,fields
from datetime import datetime

class network_audit_log(osv.osv):
    _name = 'network.audit.log'
    
    def _calculate_month(self, cr, uid, ids, name, args, context=None):
        res = {}
        for each in self.browse(cr, uid, ids):
            tm_tuple = datetime.strptime(each.name,'%Y-%m-%d').timetuple()
            month = tm_tuple.tm_mon
            res[each.id] = month     
        return res
    
    def _calculate_year(self, cr, uid, ids, name, args, context=None):
        res = {}
        for each in self.browse(cr, uid, ids):
            tm_tuple = datetime.strptime(each.name,'%Y-%m-%d').timetuple()
            year = tm_tuple.tm_year
            res[each.id] = year
        return res
    
    _columns = {
                'name':fields.date('Creation Date',readonly=True,required=True),
                'log_line':fields.one2many('network.audit.log.line','log_id','Logs'),
                'month':fields.function(_calculate_month,method=True,type='char',size=4,string='Month',store=True),
                'year':fields.function(_calculate_year,type='char',size=4,method=True,string='Year',store=True),
                }
    
    
    _sql_constraints = [
        ('number_uniq', 'unique(name)', 'Log date must br unique per day.!'),
                        ]
    
class network_audit_log_line(osv.osv):
    _name = 'network.audit.log.line'
    
    def _calculate_month(self, cr, uid, ids, name, args, context=None):
        res = {}
        for each in self.browse(cr, uid, ids):
            tm_tuple = datetime.strptime(each.name,'%Y-%m-%d %H:%M:%S').timetuple()
            month = tm_tuple.tm_mon
            res[each.id] = month     
        return res
    
    def _calculate_year(self, cr, uid, ids, name, args, context=None):
        res = {}
        for each in self.browse(cr, uid, ids):
            tm_tuple = datetime.strptime(each.name,'%Y-%m-%d %H:%M:%S').timetuple()
            year = tm_tuple.tm_year
            res[each.id] = year
        return res
    
    _columns = {
                'name':fields.datetime('Creation DateTime',readonly=True),
                'log_id':fields.many2one('network.audit.log','Creation Date',ondelete='cascade'),
                'user_ip':fields.char('User IP',size=20,readonly=True),
                'user_id':fields.many2one('res.users','User Name',readonly=True),
                'month':fields.function(_calculate_month,method=True,type='char',size=4,string='Month',store=True),
                'year':fields.function(_calculate_year,type='char',size=4,method=True,string='Year',store=True),
                'creation_date':fields.related('log_id','name',relation='network.audit.log',type='date',string='Creation Date',store=True,readonly=True),
                }
    
