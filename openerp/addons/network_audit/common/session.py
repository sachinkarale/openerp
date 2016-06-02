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

import time
from datetime import datetime,timedelta
from tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from web.session import OpenERPSession
#----------------------------------------------------------
# OpenERPSession RPC openerp backend access
#----------------------------------------------------------

def authenticate(self, db, login, password, env):
    # TODO use the openerplib API once it exposes authenticate()
    uid = self.proxy('common').authenticate(db, login, password, env)
    self.bind(db, uid, login, password)
    
    if uid: self.get_context()
    try:
        log_obj = self.model('network.audit.log')
        line_obj = self.model('network.audit.log.line')
        today = time.strftime(DEFAULT_SERVER_DATE_FORMAT)
        today_datetime = time.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        today = datetime.strptime(today,'%Y-%m-%d')
        tm_tuple = today.timetuple()
        month = tm_tuple.tm_mon
        year = tm_tuple.tm_year
        today = today + timedelta(hours=5,minutes=30)
        today = today.strftime("%Y-%m-%d %H:%M:%S")
        old_ids = log_obj.search([('name','=',today)])
        new_ids = False
        if not old_ids:
            new_ids = log_obj.create({'name':today,'month':month,'year':year})
        if new_ids:
            old_ids = [new_ids]
        if old_ids:
            log_line = line_obj.search([('user_id','=',uid),('user_ip','=',env['REMOTE_ADDR']),('log_id','=',old_ids[0])])
            if not log_line:
                line_obj.create({'name':today_datetime,'month':month,'year':year,'user_id':uid,'user_ip':env['REMOTE_ADDR'],'log_id':old_ids[0]})
    except:
        pass
            
    return uid

OpenERPSession.authenticate = authenticate
