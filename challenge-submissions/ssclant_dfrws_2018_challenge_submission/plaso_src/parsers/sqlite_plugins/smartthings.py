# -*- coding: utf-8 -*-
"""This file contains a parser for the Smartthings ua_analytics.db

"""

from __future__ import unicode_literals

from dfdatetime import posix_time as dfdatetime_posix_time

from plaso.containers import events
from plaso.containers import time_events
from plaso.lib import definitions
from plaso.parsers import sqlite
from plaso.parsers.sqlite_plugins import interface


class SmartthingsEventData(events.EventData):
  """Smartthings event data.

  Attributes:
    FileName (str):
  """

  DATA_TYPE = 'iot:smartthings:activity'

  def __init__(self):
    """Initializes event data."""
    super(SmartthingsEventData, self).__init__(data_type=self.DATA_TYPE)
    self._id = None
    self.type = None
    self.event_id = None
    self.data = None
    self.session_id = None
    self.event_size = None

class SmartthingsPlugin(interface.SQLitePlugin):
  """Parser for Smartthings databases."""

  NAME = 'smartthings'
  DESCRIPTION = 'Parser for smartthings ua_analytics database files.'

  # Define the needed queries.
  QUERIES = [
      ('SELECT _id, type, event_id, time, data, session_id, event_size FROM events;',
       'ParseActivityRow')]

  # The required tables.
  REQUIRED_TABLES = frozenset(['events'])

  SCHEMAS = [{
      'android_metadata': (
          'CREATE TABLE android_metadata (locale TEXT)'),
      'events': (
          'CREATE TABLE events (_id INTEGER PRIMARY KEY AUTOINCREMENT,type '
          'TEXT,event_id TEXT,time INTEGER,data TEXT,session_id '
          'TEXT,event_size INTEGER)')}]

  # TODO: Move this functionality to the formatter.

  def ParseActivityRow(self, parser_mediator, query, row, **unused_kwargs):
    """Parses a Activity row.

    Args:
      parser_mediator (ParserMediator): mediates interactions between parsers
          and other components, such as storage and dfvfs.
      query (str): query that created the row.
      row (sqlite3.Row): row.
    """
    query_hash = hash(query)

    event_data = SmartthingsEventData()
    event_data.id = self._GetRowValue(query_hash, row, '_id')
    event_data.type = self._GetRowValue(query_hash, row, 'type')
    event_data.event_id = self._GetRowValue(query_hash, row, 'event_id')
    event_data.data = self._GetRowValue(query_hash, row, 'data')
    event_data.session_id = self._GetRowValue(query_hash, row, 'session_id')
    event_data.event_size = self._GetRowValue(query_hash, row, 'event_size')
    event_data.query = query

    timestamp = self._GetRowValue(query_hash, row, 'time')
    date_time = dfdatetime_posix_time.PosixTime(timestamp=timestamp)
    event = time_events.DateTimeValuesEvent(date_time, 'Smart Things Event')
    parser_mediator.ProduceEventWithEventData(event, event_data)

sqlite.SQLiteParser.RegisterPlugin(SmartthingsPlugin)
