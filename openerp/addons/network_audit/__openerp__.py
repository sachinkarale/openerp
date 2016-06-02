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

{
    'name': 'Network Auditor ',
    'version': '1.0',
    'category': 'Advance',
    'description': """
                    This module provide network audit logs of each date,
                    information that available like who is login, by which IP,
                    on what datetime etc.
                    
                    """,
    'website':'http://www.openerp4you.in/',
    'author': 'Robin Bahadur',
    'depends': ["base","web"],
    'data': [
                'security/ir.model.access.csv',
                'network_audit_view.xml'
            ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': True,
    
}
