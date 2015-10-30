# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Genpex It SOlution (<http://www.genpex.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
import time
from datetime import datetime
from datetime import date, timedelta
from openerp import SUPERUSER_ID
from dateutil.relativedelta import relativedelta
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, ustr
from openerp.addons.base.ir.ir_mail_server import MailDeliveryException


class marketplace_proposition(osv.Model):
    _inherit = 'marketplace.proposition'
    
    def get_unpaid_announcement(self,cr,uid,context=None):
        email_temp = self.pool.get('email.template')
        mail_mail_pool = self.pool.get('mail.mail')
        proposition_ids = self.search(cr, uid, [('state','=','invoiced')])
        for ids in proposition_ids:
            proposition_obj = self.browse(cr,uid,ids)
            if proposition_obj.announcement_id:
                if proposition_obj.announcement_id.expiration_date:
                    expire_date = datetime.strptime(proposition_obj.announcement_id.expiration_date, '%Y-%m-%d')
                    system_date = datetime.strptime(time.strftime("%Y-%m-%d"), '%Y-%m-%d')
                    total_days = (system_date - expire_date).days
                    print "\n\nTOTAL DAYS",total_days
                    if total_days == 5:
                        template_id = self.pool.get('ir.model.data').get_object_reference(cr,uid,'send_notification_wezer','email_template_marketplace_announcement_unpaid')[1]
                        email_temp.send_mail(cr, uid, template_id, ids, force_send=False, context=context)
                        print "\n\n====Mail Sent="
        outgoing_mail_ids = mail_mail_pool.search(cr,uid,[('state','=','outgoing')])
        print "\n\n**********outgoing_mail_ids==============",outgoing_mail_ids
        if outgoing_mail_ids:
            for outgoing_ids in outgoing_mail_ids:
                print "\n\n======",outgoing_ids
                mail_mail_obj = mail_mail_pool.browse(cr,uid,outgoing_ids)
                print "\n\nmail_mail_obj.recipient_ids",mail_mail_obj.recipient_ids
                mail_mail_pool.send(cr, uid, [outgoing_ids], auto_commit=False, raise_exception=False, context=context)
                print "\n\n**********Mail Forcefully Send=============="
        return True
marketplace_proposition()


class marketplace_announcement(osv.Model):
    _inherit = 'marketplace.announcement'
    
    def get_start_date(self, dt, d_years=0, d_months=0):
        y,m = dt.year + d_years ,dt.month + d_months
        a,m = divmod(m-1,12)
        start_date = date(y+a,m+1,1)
        return start_date
    
    def get_end_date(self,dt):
        end_date = self.get_start_date(dt, 0, 1) + timedelta(-1)
        return end_date   
    
    def send_published_announcement_mail(self,cr,uid,context=None):
        email_temp = self.pool.get('email.template')
        mail_mail_pool = self.pool.get('mail.mail')
        offer_announcement_obj_list = []
        current_date = date.today()
        start_date = self.get_start_date(current_date)
        end_date = self.get_end_date(current_date)
        published_announcement_ids = self.search(cr,uid,[('state','=','open')])
        if published_announcement_ids:
            for ids in published_announcement_ids:
                announcement_obj = self.browse(cr,uid,ids)
                published_date_time = announcement_obj.publish_date
                published_date = datetime.strptime(published_date_time.split(' ')[0] , '%Y-%m-%d').date()
                if published_date > start_date and published_date < end_date:
                    template_id = self.pool.get('ir.model.data').get_object_reference(cr,uid,'send_notification_wezer','email_template_published_announcement')[1]
                    email_temp.send_mail(cr, uid, template_id, ids, force_send=False, context=context)
                    return True

    def get_offer_published_announcement(self,cr,uid,context=None):
        offer_announcement_obj_list = []
        current_date = date.today()
        start_date = self.get_start_date(current_date)
        end_date = self.get_end_date(current_date)
        published_announcement_ids = self.search(cr,uid,[('state','=','open')])
        if published_announcement_ids:
            for ids in published_announcement_ids:
                announcement_obj = self.browse(cr,uid,ids)
                published_date_time = announcement_obj.publish_date
                published_date = datetime.strptime(published_date_time.split(' ')[0] , '%Y-%m-%d').date()
                if published_date > start_date and published_date < end_date:
                    if announcement_obj.type == 'offer':
                        offer_announcement_obj_list.append(announcement_obj)
        print "\n\noffer_announcement_obj_list=",offer_announcement_obj_list
        return offer_announcement_obj_list

    def get_want_published_announcement(self,cr,uid,context=None):
        want_announcement_obj_list = []
        current_date = date.today()
        start_date = self.get_start_date(current_date)
        end_date = self.get_end_date(current_date)
        published_announcement_ids = self.search(cr,uid,[('state','=','open')])
        if published_announcement_ids:
            for ids in published_announcement_ids:
                announcement_obj = self.browse(cr,uid,ids)
                published_date_time = announcement_obj.publish_date
                published_date = datetime.strptime(published_date_time.split(' ')[0] , '%Y-%m-%d').date()
                if published_date > start_date and published_date < end_date:
                    if announcement_obj.type == 'want':
                        want_announcement_obj_list.append(announcement_obj)
        print "\n\nwant_announcement_obj_list=",want_announcement_obj_list
        return want_announcement_obj_list


marketplace_announcement()

class SignupError(Exception):
    pass

def random_token():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for i in xrange(20))

def now(**kwargs):
    dt = datetime.now() + timedelta(**kwargs)
    return dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)


class res_users(osv.Model):
    _inherit = 'res.users'
    
    def action_reset_password(self, cr, uid, ids, context=None):
        """ create signup token for each user, and send their signup url by email """
        # prepare reset password signup
        res_partner = self.pool.get('res.partner')
        partner_ids = [user.partner_id.id for user in self.browse(cr, uid, ids, context)]
        res_partner.signup_prepare(cr, uid, partner_ids, signup_type="reset", expiration=now(days=+1), context=context)

        if not context:
            context = {}

        # send email to users with their signup url
        template = False
        template_id =False
        if context.get('create_user'):
            try:
                # get_object() raises ValueError if record does not exist
                template = self.pool.get('ir.model.data').get_object(cr, uid, 'auth_signup', 'set_password_email')
            except ValueError:
                pass
        if not bool(template):
            template = self.pool.get('ir.model.data').get_object(cr, uid, 'auth_signup', 'reset_password_email')
            template_id = self.pool.get('ir.model.data').get_object(cr,uid,'send_notification_wezer','email_template_reset_password')
        assert template._name == 'email.template'

        for user in self.browse(cr, uid, ids, context):
            if not user.email:
                raise osv.except_osv(_("Cannot send email: user has no email address."), user.name)
            self.pool.get('email.template').send_mail(cr, uid, template.id, user.id, force_send=True, raise_exception=True, context=context)
            self.pool.get('email.template').send_mail(cr, uid, template_id.id, user.id, force_send=False,raise_exception=True, context=context)

    def get_server_link(self, cr, uid, ids, context=None):
        signup_url = str(self.pool.get('res.users').browse(cr, uid, uid).signup_url)
        server_url = signup_url.split('/web')[0]
        print "\n\n==============",signup_url,server_url
        return server_url
res_users()


class mail_mail(osv.Model):
    _inherit = 'mail.mail'
    
    def _get_partner_access_link(self, cr, uid, mail, partner=None, context=None):
        """Generate URLs for links in mails: partner has access (is user):
        link to action_mail_redirect action that will redirect to doc or Inbox """
        if context is None:
            context = {}
        if partner and partner.user_ids:
            base_url = self.pool.get('ir.config_parameter').get_param(cr, SUPERUSER_ID, 'web.base.url')
            mail_model = mail.model or 'mail.thread'
            if mail_model == 'res.users':
            	return None
            url = urljoin(base_url, self.pool[mail_model]._get_access_link(cr, uid, mail, partner, context=context))
            return "<span class='oe_mail_footer_access'><small>%(access_msg)s <a style='color:inherit' href='%(portal_link)s'>%(portal_msg)s</a></small></span>" % {
                'access_msg': _('about') if mail.record_name else _('access'),
                'portal_link': url,
                'portal_msg': '%s %s' % (context.get('model_name', ''), mail.record_name) if mail.record_name else _('your messages'),
            }
        else:
            return None

    
mail_mail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
