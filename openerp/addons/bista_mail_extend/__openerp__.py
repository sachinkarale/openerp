# -*- coding: utf-8 -*-
{
    'name': 'Bista Mail Extend',
    'version': '1.1',
    'description': """
            - this module will allow you to send mail to partner without creating records in res.partner.
            - added email_cc functionality in mail_compose wizard
""",
    'author': 'Bista Solutions Pvt. Ltd',
    'website': 'http://www.bistasolutions.com',
    'images': ['images/mail.jpg'],
    'depends': ['mail','email_template'],
    'sequence': 16,
    'data': [
                'wizard/mail_compose_message_view.xml',
                'mail_message_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
