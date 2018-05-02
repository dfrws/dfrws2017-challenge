# -*- coding: utf-8 -*-
"""The Smartthings database event formatter."""

from __future__ import unicode_literals

from plaso.formatters import interface
from plaso.formatters import manager


class SmartthingsFormatter(interface.ConditionalEventFormatter):
  """Formatter for an Smartthings Video event."""

  DATA_TYPE = 'iot:smartthings:activity'

  FORMAT_STRING_PIECES = [
      'id: {id}',
      'type: {type}',
      'event_id: {event_id}',
      'data: {data}',
      'sesion_id: {session_id}',
      'event_size: {event_size}'
      ]

  FORMAT_STRING_SHORT_PIECES = ['{data}']

  SOURCE_LONG = 'SmartThingsEvent'
  SOURCE_SHORT = 'STE'


manager.FormattersManager.RegisterFormatter(SmartthingsFormatter)
