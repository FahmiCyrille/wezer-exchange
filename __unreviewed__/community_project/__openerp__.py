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
    'name': 'Odoo for Communities - Project',
    'version': '1.0',
    'category': 'Community',
    'author': 'Yannick Buron and Valeureux',
    'license': 'AGPL-3',
    'description': """
Odoo for Communities - Project
=================================
""",
    'website': 'http://www.wezer.org',
    'depends': [
        'community',
        'project_groups',
        'website_project',
    ],
    'data': ['security/community_project_security.xml'],
    'installable': True,
}
