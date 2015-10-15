# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Yannick Buron and Valeureux  Copyright Valeureux.org
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Membership Users',
    'version': '1.0',
    'category': 'Association',
    'author': 'Yannick Buron and Valeureux',
    'license': 'AGPL-3',
    'description': """
Membership Users
================

Add users management in the association part of Odoo
----------------------------------------------------
    * Add users list with simplified form
    * Modify and improve members list
    * Add "My account"
    * Add a membership moderator group
""",
    'website': 'http://www.wezer.org',
    'depends': ['membership'],
    'data': [
        'security/membership_users_security.xml',
        'security/ir.model.access.csv',
        'membership_users_view.xml'
    ],
    'installable': True,
}
