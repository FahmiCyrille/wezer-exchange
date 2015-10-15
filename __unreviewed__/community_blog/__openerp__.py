# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Yannick Buron for Valeureux.org Copyright Valeureux.org
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
    'name': 'Odoo for Communities - Website Blog',
    'version': '1.0',
    'category': 'Community',
    'author': 'Yannick Buron',
    'license': 'AGPL-3',
    'description': """
Odoo for Communities - Blog
===========================
""",
    'website': 'http://www.wezer.org',
    'depends': [
        'community',
        'website_blog',
    ],
    'data': ['security/community_blog_security.xml'],
    'installable': True,
}
