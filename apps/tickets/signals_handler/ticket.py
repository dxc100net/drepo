# -*- coding: utf-8 -*-
#
from datetime import timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save

from common.utils.timezone import as_current_tz
from common.utils import get_logger
from tickets.models import Ticket
from ..signals import post_change_ticket_action

logger = get_logger(__name__)


@receiver(post_change_ticket_action, sender=Ticket)
def on_post_change_ticket_action(sender, ticket, action, **kwargs):
    ticket.handler.dispatch(action)


@receiver(post_save, sender=Ticket)
def on_pre_save_ensure_serial_num(sender, instance: Ticket, **kwargs):
    if not instance.serial_num:
        date_created = as_current_tz(instance.date_created)
        day_begin = date_created.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_begin + timedelta(days=1)
        ticket = Ticket.objects.filter(date_created__gte=day_begin, date_created__lt=day_end, serial_num__isnull=False).exclude(serial_num='').order_by('-date_created').first()
        date_prefix = day_begin.strftime('%Y%m%d')

        if ticket:
            # 202212010001
            num_str = ticket.serial_num[8:]
            num = int(num_str)
            num_suffix = '%04d' % (num+1)
        else:
            num_suffix = '0001'

        instance.serial_num = date_prefix + num_suffix
        instance.save(update_fields=('serial_num',))
