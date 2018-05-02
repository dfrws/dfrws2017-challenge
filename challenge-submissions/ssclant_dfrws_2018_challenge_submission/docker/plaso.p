diff --git a/plaso/formatters/__init__.py b/plaso/formatters/__init__.py
index 9d57cf7..bd7bb02 100644
--- a/plaso/formatters/__init__.py
+++ b/plaso/formatters/__init__.py
@@ -28,6 +28,7 @@ from plaso.formatters import file_system
 from plaso.formatters import firefox
 from plaso.formatters import firefox_cache
 from plaso.formatters import firefox_cookies
+from plaso.formatters import googlehangouts_messages
 from plaso.formatters import ganalytics
 from plaso.formatters import gdrive
 from plaso.formatters import hachoir
@@ -36,6 +37,7 @@ from plaso.formatters import imessage
 from plaso.formatters import ipod
 from plaso.formatters import java_idx
 from plaso.formatters import kik_ios
+from plaso.formatters import kodi
 from plaso.formatters import ls_quarantine
 from plaso.formatters import mac_appfirewall
 from plaso.formatters import mac_document_versions
@@ -64,6 +66,7 @@ from plaso.formatters import sccm
 from plaso.formatters import selinux
 from plaso.formatters import shell_items
 from plaso.formatters import shutdown
+from plaso.formatters import smartthings
 from plaso.formatters import skydrivelog
 from plaso.formatters import skype
 from plaso.formatters import sophos_av
diff --git a/plaso/formatters/googlehangouts_messages.py b/plaso/formatters/googlehangouts_messages.py
new file mode 100644
index 0000000..7296e34
--- /dev/null
+++ b/plaso/formatters/googlehangouts_messages.py
@@ -0,0 +1,27 @@
+# -*- coding: utf-8 -*-
+"""The googlehangouts messages database event formatter."""
+
+from __future__ import unicode_literals
+
+from plaso.formatters import interface
+from plaso.formatters import manager
+
+
+class GoogleMSGFormatter(interface.ConditionalEventFormatter):
+  """Formatter for an Google MSG event."""
+
+  DATA_TYPE = 'android:messaging:googlehangouts'
+
+  FORMAT_STRING_PIECES = [
+      'Sender: {sender}',
+      'Body: {body}',
+      'Status: {read}',
+      'Type: {msgtype}']
+
+  FORMAT_STRING_SHORT_PIECES = ['{body}']
+
+  SOURCE_LONG = 'Google Hangouts Message'
+  SOURCE_SHORT = 'GHM'
+
+
+manager.FormattersManager.RegisterFormatter(GoogleMSGFormatter)
diff --git a/plaso/formatters/kodi.py b/plaso/formatters/kodi.py
new file mode 100644
index 0000000..f5a628e
--- /dev/null
+++ b/plaso/formatters/kodi.py
@@ -0,0 +1,24 @@
+# -*- coding: utf-8 -*-
+"""The Kodi MyVideos database event formatter."""
+
+from __future__ import unicode_literals
+
+from plaso.formatters import interface
+from plaso.formatters import manager
+
+
+class KodiFormatter(interface.ConditionalEventFormatter):
+  """Formatter for an Kodi Video event."""
+
+  DATA_TYPE = 'kodi:videos:viewing'
+
+  FORMAT_STRING_PIECES = [
+      'Video: {FileName}']
+
+  FORMAT_STRING_SHORT_PIECES = ['{FileName}']
+
+  SOURCE_LONG = 'Kodi Video Viewed'
+  SOURCE_SHORT = 'KODI'
+
+
+manager.FormattersManager.RegisterFormatter(KodiFormatter)
diff --git a/plaso/formatters/smartthings.py b/plaso/formatters/smartthings.py
new file mode 100644
index 0000000..cd1e816
--- /dev/null
+++ b/plaso/formatters/smartthings.py
@@ -0,0 +1,30 @@
+# -*- coding: utf-8 -*-
+"""The Smartthings database event formatter."""
+
+from __future__ import unicode_literals
+
+from plaso.formatters import interface
+from plaso.formatters import manager
+
+
+class SmartthingsFormatter(interface.ConditionalEventFormatter):
+  """Formatter for an Smartthings Video event."""
+
+  DATA_TYPE = 'iot:smartthings:activity'
+
+  FORMAT_STRING_PIECES = [
+      'id: {id}',
+      'type: {type}',
+      'event_id: {event_id}',
+      'data: {data}',
+      'sesion_id: {session_id}',
+      'event_size: {event_size}'
+      ]
+
+  FORMAT_STRING_SHORT_PIECES = ['{data}']
+
+  SOURCE_LONG = 'SmartThingsEvent'
+  SOURCE_SHORT = 'STE'
+
+
+manager.FormattersManager.RegisterFormatter(SmartthingsFormatter)
diff --git a/plaso/parsers/sqlite_plugins/__init__.py b/plaso/parsers/sqlite_plugins/__init__.py
index 63e11ed..aa2bc33 100644
--- a/plaso/parsers/sqlite_plugins/__init__.py
+++ b/plaso/parsers/sqlite_plugins/__init__.py
@@ -9,14 +9,17 @@ from plaso.parsers.sqlite_plugins import appusage
 from plaso.parsers.sqlite_plugins import chrome
 from plaso.parsers.sqlite_plugins import chrome_cookies
 from plaso.parsers.sqlite_plugins import chrome_extension_activity
+from plaso.parsers.sqlite_plugins import googlehangouts_messages
 from plaso.parsers.sqlite_plugins import firefox
 from plaso.parsers.sqlite_plugins import firefox_cookies
 from plaso.parsers.sqlite_plugins import gdrive
 from plaso.parsers.sqlite_plugins import imessage
+from plaso.parsers.sqlite_plugins import kodi
 from plaso.parsers.sqlite_plugins import kik_ios
 from plaso.parsers.sqlite_plugins import ls_quarantine
 from plaso.parsers.sqlite_plugins import mac_document_versions
 from plaso.parsers.sqlite_plugins import mackeeper_cache
+from plaso.parsers.sqlite_plugins import smartthings
 from plaso.parsers.sqlite_plugins import skype
 from plaso.parsers.sqlite_plugins import twitter_ios
 from plaso.parsers.sqlite_plugins import zeitgeist
diff --git a/plaso/parsers/sqlite_plugins/googlehangouts_messages.py b/plaso/parsers/sqlite_plugins/googlehangouts_messages.py
new file mode 100644
index 0000000..783cb46
--- /dev/null
+++ b/plaso/parsers/sqlite_plugins/googlehangouts_messages.py
@@ -0,0 +1,301 @@
+# -*- coding: utf-8 -*-
+"""This file contains a parser for the Google Hangouts Active Conversations DB.
+
+/data/com.google.android.talk/databases/babel.db
+This SQLite database is the conversation database for active conversations,
+ participant names, messages, and information about the Google Hangout event.
+ There can be multiple babel.db databases, and each database name will be
+ followed by an integer starting with 0 (e.g., babel0.db,babel1.db,babel3.db)..
+"""
+
+from __future__ import unicode_literals
+
+from dfdatetime import posix_time as dfdatetime_posix_time
+
+from plaso.containers import events
+from plaso.containers import time_events
+from plaso.lib import definitions
+from plaso.parsers import sqlite
+from plaso.parsers.sqlite_plugins import interface
+
+
+class GoogleHangoutsMessageData(events.EventData):
+  """GoogleHangouts Message event data.
+
+  Attributes:
+    sender (str): Name with the sender.
+    body (str): content of the SMS text message.
+    read (str): message read status, either Read or Unread.
+    msgtype (str): message type, either Sent or Received.
+    time (integer) : time message was recieved
+  """
+
+  DATA_TYPE = 'android:messaging:googlehangouts'
+
+  def __init__(self):
+    """Initializes event data."""
+    super(GoogleHangoutsMessageData, self).__init__(data_type=self.DATA_TYPE)
+    self.sender = None
+    self.body = None
+    self.read = None
+    self.msgtype = None
+
+
+class GoogleHangoutsMessagePlugin(interface.SQLitePlugin):
+  """Parser for Google Hangouts databases."""
+
+  NAME = 'googlehangouts_messages'
+  DESCRIPTION = 'Parser for GoogleHangouts Messages SQLite database files.'
+
+  # Define the needed queries.
+  QUERIES = [
+      ('SELECT messages._id, participants.full_name, text, messages.timestamp, status, type FROM messages '
+      'INNER JOIN participants ON messages.author_chat_id=participants.chat_id;',
+       'ParseMessagesRow')]
+
+  # The required tables.
+  REQUIRED_TABLES = frozenset([ 'messages', 'blocked_people', 'participants'])
+
+  SCHEMAS = [{
+      'android_metadata': (
+          'CREATE TABLE android_metadata (locale TEXT)'),
+      'blocked_people': (
+          'CREATE TABLE blocked_people (_id INTEGER PRIMARY KEY, gaia_id '
+          'TEXT, chat_id TEXT, name TEXT, profile_photo_url TEXT, UNIQUE '
+          '(chat_id) ON CONFLICT REPLACE, UNIQUE (gaia_id) ON CONFLICT '
+          'REPLACE)'),
+      'conversation_participants': (
+          'CREATE TABLE conversation_participants (_id INTEGER PRIMARY KEY, '
+          'participant_row_id INT, participant_type INT, conversation_id '
+          'TEXT, sequence INT, active INT, invitation_status INT DEFAULT(0), '
+          'UNIQUE (conversation_id,participant_row_id) ON CONFLICT REPLACE, '
+          'FOREIGN KEY (conversation_id) REFERENCES '
+          'conversations(conversation_id) ON DELETE CASCADE ON UPDATE '
+          'CASCADE, FOREIGN KEY (participant_row_id) REFERENCES '
+          'participants(_id))'),
+      'conversations': (
+          'CREATE TABLE conversations (_id INTEGER PRIMARY KEY, '
+          'conversation_id TEXT, conversation_type INT, '
+          'latest_message_timestamp INT DEFAULT(0), '
+          'latest_message_expiration_timestamp INT, metadata_present '
+          'INT,notification_level INT, name TEXT, generated_name TEXT, '
+          'snippet_type INT, snippet_text TEXT, snippet_image_url TEXT, '
+          'snippet_author_gaia_id TEXT, snippet_author_chat_id TEXT, '
+          'snippet_message_row_id INT, snippet_selector INT, snippet_status '
+          'INT, snippet_new_conversation_name TEXT, snippet_participant_keys '
+          'TEXT, snippet_sms_type TEXT, previous_latest_timestamp INT, status '
+          'INT, view INT, inviter_gaia_id TEXT, inviter_chat_id TEXT, '
+          'inviter_affinity INT, is_pending_leave INT, account_id INT, is_otr '
+          'INT, packed_avatar_urls TEXT, self_avatar_url TEXT, self_watermark '
+          'INT DEFAULT(0), chat_watermark INT DEFAULT(0), hangout_watermark '
+          'INT DEFAULT(0), is_draft INT, sequence_number INT, call_media_type '
+          'INT DEFAULT(0), has_joined_hangout INT, has_chat_notifications '
+          'DEFAULT(0),has_video_notifications '
+          'DEFAULT(0),last_hangout_event_time INT, draft TEXT, otr_status '
+          'INT, otr_toggle INT, last_otr_modification_time INT, '
+          'continuation_token BLOB, continuation_event_timestamp INT, '
+          'has_oldest_message INT DEFAULT(0), sort_timestamp INT, '
+          'first_peak_scroll_time INT, first_peak_scroll_to_message_timestamp '
+          'INT, second_peak_scroll_time INT, '
+          'second_peak_scroll_to_message_timestamp INT, conversation_hash '
+          'BLOB, disposition INT DEFAULT(0), has_persistent_events INT '
+          'DEFAULT(-1), transport_type INT DEFAULT(1), '
+          'default_transport_phone TEXT, sms_service_center TEXT, '
+          'is_temporary INT DEFAULT (0), sms_thread_id INT DEFAULT (-1), '
+          'chat_ringtone_uri TEXT, hangout_ringtone_uri TEXT, '
+          'snippet_voicemail_duration INT DEFAULT (0), share_count INT '
+          'DEFAULT(0), has_unobserved TEXT, last_share_timestamp INT '
+          'DEFAULT(0), gls_status INT DEFAULT(0), gls_link TEXT, is_guest INT '
+          'DEFAULT(0), UNIQUE (conversation_id ))'),
+      'dismissed_contacts': (
+          'CREATE TABLE dismissed_contacts (_id INTEGER PRIMARY KEY, gaia_id '
+          'TEXT, chat_id TEXT, name TEXT, profile_photo_url TEXT, UNIQUE '
+          '(chat_id) ON CONFLICT REPLACE, UNIQUE (gaia_id) ON CONFLICT '
+          'REPLACE)'),
+      'event_suggestions': (
+          'CREATE TABLE event_suggestions (_id INTEGER PRIMARY KEY, '
+          'conversation_id TEXT, event_id TEXT, suggestion_id TEXT, timestamp '
+          'INT, expiration_time_usec INT, type INT, gem_asset_url STRING, '
+          'gem_horizontal_alignment INT, matched_message_substring TEXT, '
+          'FOREIGN KEY (conversation_id) REFERENCES '
+          'conversations(conversation_id) ON DELETE CASCADE ON UPDATE '
+          'CASCADE, UNIQUE (conversation_id,suggestion_id) ON CONFLICT '
+          'REPLACE)'),
+      'merge_keys': (
+          'CREATE TABLE merge_keys (_id INTEGER PRIMARY KEY, conversation_id '
+          'TEXT, merge_key TEXT, UNIQUE (conversation_id) ON CONFLICT '
+          'REPLACE, FOREIGN KEY (conversation_id) REFERENCES '
+          'conversations(conversation_id) ON DELETE CASCADE ON UPDATE CASCADE '
+          ')'),
+      'merged_contact_details': (
+          'CREATE TABLE merged_contact_details (_id INTEGER PRIMARY KEY, '
+          'merged_contact_id INT, lookup_data_type INT, lookup_data TEXT, '
+          'lookup_data_standardized TEXT, lookup_data_search TEXT, '
+          'lookup_data_label TEXT, needs_gaia_ids_resolved INT DEFAULT (1), '
+          'is_hangouts_user INT DEFAULT (0), gaia_id TEXT, avatar_url TEXT, '
+          'display_name TEXT, last_checked_ts INT DEFAULT (0), '
+          'lookup_data_display TEXT, detail_affinity_score REAL DEFAULT '
+          '(0.0), detail_logging_id TEXT, is_in_viewer_dasher_domain INT '
+          'DEFAULT (0), FOREIGN KEY (merged_contact_id) REFERENCES '
+          'merged_contacts(_id) ON DELETE CASCADE ON UPDATE CASCADE)'),
+      'merged_contacts': (
+          'CREATE TABLE merged_contacts (_id INTEGER PRIMARY KEY, '
+          'contact_lookup_key TEXT, contact_id INT, raw_contact_id INT, '
+          'display_name TEXT, avatar_url TEXT, is_frequent INT DEFAULT (0), '
+          'is_favorite INT DEFAULT (0), contact_source INT DEFAULT(0), '
+          'frequent_order INT, person_logging_id TEXT, person_affinity_score '
+          'REAL DEFAULT (0.0), is_in_same_domain INT DEFAULT (0))'),
+      'messages': (
+          'CREATE TABLE messages (_id INTEGER PRIMARY KEY, message_id TEXT, '
+          'message_type INT, conversation_id TEXT, author_chat_id TEXT, '
+          'author_gaia_id TEXT, text TEXT, timestamp INT, '
+          'delete_after_read_timetamp INT, status INT, type INT, local_url '
+          'TEXT, remote_url TEXT, attachment_content_type TEXT, width_pixels '
+          'INT, height_pixels INT, stream_id TEXT, image_id TEXT, album_id '
+          'TEXT, latitude DOUBLE, longitude DOUBLE, address ADDRESS, '
+          'notification_level INT, expiration_timestamp INT, '
+          'notified_for_failure INT DEFAULT(0), off_the_record INT '
+          'DEFAULT(0), transport_type INT NOT NULL DEFAULT(1), '
+          'transport_phone TEXT, external_ids TEXT, sms_timestamp_sent INT '
+          'DEFAULT(0), sms_priority INT DEFAULT(0), sms_message_size INT '
+          'DEFAULT(0), mms_subject TEXT, sms_raw_sender TEXT, '
+          'sms_raw_recipients TEXT, persisted INT DEFAULT(1), '
+          'sms_message_status INT DEFAULT(-1), sms_type INT DEFAULT(-1), '
+          'stream_url TEXT, attachment_target_url TEXT, attachment_name TEXT, '
+          'image_rotation INT DEFAULT (0), new_conversation_name TEXT, '
+          'participant_keys TEXT, forwarded_mms_url TEXT, forwarded_mms_count '
+          'INT DEFAULT(0), attachment_description TEXT, '
+          'attachment_target_url_description TEXT, attachment_target_url_name '
+          'TEXT, attachment_blob_data BLOB,attachment_uploading_progress INT '
+          'DEFAULT(0), sending_error INT DEFAULT(0), stream_expiration INT, '
+          'voicemail_length INT DEFAULT (0), call_media_type INT DEFAULT(0), '
+          'last_seen_timestamp INT DEFAULT(0), observed_status INT '
+          'DEFAULT(2), receive_type INT DEFAULT(0), init_timestamp INT '
+          'DEFAULT(0), in_app_msg_latency INT DEFAULT(0), notified INT '
+          'DEFAULT(0), alert_in_conversation_list INT DEFAULT(0), attachments '
+          'BLOB, is_user_mentioned INT DEFAULT(0), local_id TEXT, '
+          'request_task_row_id INT DEFAULT(-1), FOREIGN KEY (conversation_id) '
+          'REFERENCES conversations(conversation_id) ON DELETE CASCADE ON '
+          'UPDATE CASCADE, UNIQUE (conversation_id,message_id) ON CONFLICT '
+          'REPLACE)'),
+      'mms_notification_inds': (
+          'CREATE TABLE mms_notification_inds (_id INTEGER PRIMARY KEY, '
+          'content_location TEXT, transaction_id TEXT, from_address TEXT, '
+          'message_size INT DEFAULT(0), expiry INT)'),
+      'multipart_attachments': (
+          'CREATE TABLE multipart_attachments (_id INTEGER PRIMARY KEY, '
+          'message_id TEXT, conversation_id TEXT, url TEXT, content_type '
+          'TEXT, width INT, height INT, FOREIGN KEY (message_id, '
+          'conversation_id) REFERENCES messages(message_id, conversation_id) '
+          'ON DELETE CASCADE ON UPDATE CASCADE)'),
+      'participant_email_fts': (
+          'CREATE VIRTUAL TABLE participant_email_fts USING '
+          'fts4(content="merged_contact_details", gaia_id,lookup_data)'),
+      'participant_email_fts_docsize': (
+          'CREATE TABLE \'participant_email_fts_docsize\'(docid INTEGER '
+          'PRIMARY KEY, size BLOB)'),
+      'participant_email_fts_segdir': (
+          'CREATE TABLE \'participant_email_fts_segdir\'(level INTEGER,idx '
+          'INTEGER,start_block INTEGER,leaves_end_block INTEGER,end_block '
+          'INTEGER,root BLOB,PRIMARY KEY(level, idx))'),
+      'participant_email_fts_segments': (
+          'CREATE TABLE \'participant_email_fts_segments\'(blockid INTEGER '
+          'PRIMARY KEY, block BLOB)'),
+      'participant_email_fts_stat': (
+          'CREATE TABLE \'participant_email_fts_stat\'(id INTEGER PRIMARY '
+          'KEY, value BLOB)'),
+      'participants': (
+          'CREATE TABLE participants (_id INTEGER PRIMARY KEY, '
+          'participant_type INT DEFAULT 1, gaia_id TEXT, chat_id TEXT, '
+          'phone_id TEXT, circle_id TEXT, first_name TEXT, full_name TEXT, '
+          'fallback_name TEXT, profile_photo_url TEXT, batch_gebi_tag STRING '
+          'DEFAULT(\'-1\'), blocked INT DEFAULT(0), in_users_domain BOOLEAN, '
+          'UNIQUE (circle_id) ON CONFLICT REPLACE, UNIQUE (chat_id) ON '
+          'CONFLICT REPLACE, UNIQUE (gaia_id) ON CONFLICT REPLACE)'),
+      'participants_fts': (
+          'CREATE VIRTUAL TABLE participants_fts USING '
+          'fts4(content="participants",gaia_id,full_name)'),
+      'participants_fts_docsize': (
+          'CREATE TABLE \'participants_fts_docsize\'(docid INTEGER PRIMARY '
+          'KEY, size BLOB)'),
+      'participants_fts_segdir': (
+          'CREATE TABLE \'participants_fts_segdir\'(level INTEGER,idx '
+          'INTEGER,start_block INTEGER,leaves_end_block INTEGER,end_block '
+          'INTEGER,root BLOB,PRIMARY KEY(level, idx))'),
+      'participants_fts_segments': (
+          'CREATE TABLE \'participants_fts_segments\'(blockid INTEGER PRIMARY '
+          'KEY, block BLOB)'),
+      'participants_fts_stat': (
+          'CREATE TABLE \'participants_fts_stat\'(id INTEGER PRIMARY KEY, '
+          'value BLOB)'),
+      'presence': (
+          'CREATE TABLE presence (_id INTEGER PRIMARY KEY, gaia_id TEXT NOT '
+          'NULL, reachable INT DEFAULT(0), reachable_time INT DEFAULT(0), '
+          'available INT DEFAULT(0), available_time INT DEFAULT(0), '
+          'status_message TEXT, status_message_time INT DEFAULT(0), call_type '
+          'INT DEFAULT(0), call_type_time INT DEFAULT(0), device_status INT '
+          'DEFAULT(0), device_status_time INT DEFAULT(0), last_seen INT '
+          'DEFAULT(0), last_seen_time INT DEFAULT(0), location BLOB, '
+          'location_time INT DEFAULT(0), UNIQUE (gaia_id) ON CONFLICT '
+          'REPLACE)'),
+      'recent_calls': (
+          'CREATE TABLE recent_calls (_id INTEGER PRIMARY KEY, '
+          'normalized_number TEXT NOT NULL, phone_number TEXT, contact_id '
+          'TEXT, call_timestamp INT, call_type INT, contact_type INT, '
+          'call_rate TEXT, is_free_call BOOLEAN)'),
+      'search': (
+          'CREATE TABLE search (search_key TEXT NOT NULL,continuation_token '
+          'TEXT,PRIMARY KEY (search_key))'),
+      'sticker_albums': (
+          'CREATE TABLE sticker_albums (album_id TEXT NOT NULL, title TEXT, '
+          'cover_photo_id TEXT, last_used INT DEFAULT(0), PRIMARY KEY '
+          '(album_id))'),
+      'sticker_photos': (
+          'CREATE TABLE sticker_photos (photo_id TEXT NOT NULL, album_id TEXT '
+          'NOT NULL, url TEXT NOT NULL, file_name TEXT, last_used INT '
+          'DEFAULT(0), PRIMARY KEY (photo_id), FOREIGN KEY (album_id) '
+          'REFERENCES sticker_albums(album_id) ON DELETE CASCADE)'),
+      'suggested_contacts': (
+          'CREATE TABLE suggested_contacts (_id INTEGER PRIMARY KEY, gaia_id '
+          'TEXT, chat_id TEXT, name TEXT, first_name TEXT, packed_circle_ids '
+          'TEXT, profile_photo_url TEXT, sequence INT, suggestion_type INT, '
+          'logging_id TEXT, affinity_score REAL DEFAULT (0.0), '
+          'is_in_same_domain INT DEFAULT (0))')}]
+
+  # TODO: Move this functionality to the formatter.
+  MSG_TYPE = {
+      1: 'SENT',
+      2: 'RECIEVED'}
+  MSG_READ = {
+      0: 'UNREAD',
+      4: 'READ'}
+
+  def ParseMessagesRow(self, parser_mediator, query, row, **unused_kwargs):
+    """Parses an Messages row.
+
+    Args:
+      parser_mediator (ParserMediator): mediates interactions between parsers
+          and other components, such as storage and dfvfs.
+      query (str): query that created the row.
+      row (sqlite3.Row): row.
+    """
+    query_hash = hash(query)
+
+    msg_read = self._GetRowValue(query_hash, row, 'status')
+    msg_type = self._GetRowValue(query_hash, row, 'type')
+
+    event_data = GoogleHangoutsMessageData()
+    event_data.sender = self._GetRowValue(query_hash, row, 'full_name')
+    event_data.body = self._GetRowValue(query_hash, row, 'text')
+    event_data.offset = self._GetRowValue(query_hash, row, '_id')
+    event_data.query = query
+    event_data.msg_read = self.MSG_READ.get(msg_read, 'UNKNOWN')
+    event_data.msg_type = self.MSG_TYPE.get(msg_type, 'UNKNOWN')
+
+    timestamp = self._GetRowValue(query_hash, row, 'timestamp')
+    date_time = dfdatetime_posix_time.PosixTimeInMicroseconds(timestamp=timestamp)
+    event = time_events.DateTimeValuesEvent(
+        date_time, definitions.TIME_DESCRIPTION_CREATION)
+    parser_mediator.ProduceEventWithEventData(event, event_data)
+
+sqlite.SQLiteParser.RegisterPlugin(GoogleHangoutsMessagePlugin)
diff --git a/plaso/parsers/sqlite_plugins/kodi.py b/plaso/parsers/sqlite_plugins/kodi.py
new file mode 100644
index 0000000..a8ec37f
--- /dev/null
+++ b/plaso/parsers/sqlite_plugins/kodi.py
@@ -0,0 +1,183 @@
+# -*- coding: utf-8 -*-
+"""This file contains a parser for the Kodi MyVideos.db
+
+Kodi Videos are stored in a database called MyVideos.db
+"""
+
+from __future__ import unicode_literals
+
+from dfdatetime import time_elements as dfdatetime_time_elements
+
+from plaso.containers import events
+from plaso.containers import time_events
+from plaso.lib import definitions
+from plaso.parsers import sqlite
+from plaso.parsers.sqlite_plugins import interface
+
+
+class KodiEventData(events.EventData):
+  """Kodi event data.
+
+  Attributes:
+    FileName (str): Video FileName Viewed
+  """
+
+  DATA_TYPE = 'kodi:videos:viewing'
+
+  def __init__(self):
+    """Initializes event data."""
+    super(KodiEventData, self).__init__(data_type=self.DATA_TYPE)
+    self.FileName = None
+
+class KodiPlugin(interface.SQLitePlugin):
+  """Parser for Kodi Video databases."""
+
+  NAME = 'kodi'
+  DESCRIPTION = 'Parser for kodi myvideos database files.'
+
+  # Define the needed queries.
+  QUERIES = [
+      ('SELECT idFile,strFilename,playCount,lastPlayed FROM files;',
+       'ParseVideoRow')]
+
+  # The required tables.
+  REQUIRED_TABLES = frozenset(['files'])
+
+  SCHEMAS = [{
+        'actor': (
+          'CREATE TABLE actor ( actor_id INTEGER PRIMARY KEY, name TEXT, '
+          'art_urls TEXT )'),
+      'actor_link': (
+          'CREATE TABLE actor_link(actor_id INTEGER, media_id INTEGER, '
+          'media_type TEXT, role TEXT, cast_order INTEGER)'),
+      'art': (
+          'CREATE TABLE art(art_id INTEGER PRIMARY KEY, media_id INTEGER, '
+          'media_type TEXT, type TEXT, url TEXT)'),
+      'bookmark': (
+          'CREATE TABLE bookmark ( idBookmark integer primary key, idFile '
+          'integer, timeInSeconds double, totalTimeInSeconds double, '
+          'thumbNailImage text, player text, playerState text, type integer)'),
+      'country': (
+          'CREATE TABLE country ( country_id integer primary key, name TEXT)'),
+      'country_link': (
+          'CREATE TABLE country_link (country_id integer, media_id integer, '
+          'media_type TEXT)'),
+      'director_link': (
+          'CREATE TABLE director_link(actor_id INTEGER, media_id INTEGER, '
+          'media_type TEXT)'),
+      'episode': (
+          'CREATE TABLE episode ( idEpisode integer primary key, idFile '
+          'integer,c00 text,c01 text,c02 text,c03 text,c04 text,c05 text,c06 '
+          'text,c07 text,c08 text,c09 text,c10 text,c11 text,c12 '
+          'varchar(24),c13 varchar(24),c14 text,c15 text,c16 text,c17 '
+          'varchar(24),c18 text,c19 text,c20 text,c21 text,c22 text,c23 text, '
+          'idShow integer, userrating integer, idSeason integer)'),
+      'files': (
+          'CREATE TABLE files ( idFile integer primary key, idPath integer, '
+          'strFilename text, playCount integer, lastPlayed text, dateAdded '
+          'text)'),
+      'genre': (
+          'CREATE TABLE genre ( genre_id integer primary key, name TEXT)'),
+      'genre_link': (
+          'CREATE TABLE genre_link (genre_id integer, media_id integer, '
+          'media_type TEXT)'),
+      'movie': (
+          'CREATE TABLE movie ( idMovie integer primary key, idFile '
+          'integer,c00 text,c01 text,c02 text,c03 text,c04 text,c05 text,c06 '
+          'text,c07 text,c08 text,c09 text,c10 text,c11 text,c12 text,c13 '
+          'text,c14 text,c15 text,c16 text,c17 text,c18 text,c19 text,c20 '
+          'text,c21 text,c22 text,c23 text, idSet integer, userrating '
+          'integer, premiered text)'),
+      'movielinktvshow': (
+          'CREATE TABLE movielinktvshow ( idMovie integer, IdShow integer)'),
+      'musicvideo': (
+          'CREATE TABLE musicvideo ( idMVideo integer primary key, idFile '
+          'integer,c00 text,c01 text,c02 text,c03 text,c04 text,c05 text,c06 '
+          'text,c07 text,c08 text,c09 text,c10 text,c11 text,c12 text,c13 '
+          'text,c14 text,c15 text,c16 text,c17 text,c18 text,c19 text,c20 '
+          'text,c21 text,c22 text,c23 text, userrating integer, premiered '
+          'text)'),
+      'path': (
+          'CREATE TABLE path ( idPath integer primary key, strPath text, '
+          'strContent text, strScraper text, strHash text, scanRecursive '
+          'integer, useFolderNames bool, strSettings text, noUpdate bool, '
+          'exclude bool, dateAdded text, idParentPath integer)'),
+      'rating': (
+          'CREATE TABLE rating (rating_id INTEGER PRIMARY KEY, media_id '
+          'INTEGER, media_type TEXT, rating_type TEXT, rating FLOAT, votes '
+          'INTEGER)'),
+      'seasons': (
+          'CREATE TABLE seasons ( idSeason integer primary key, idShow '
+          'integer, season integer, name text, userrating integer)'),
+      'sets': (
+          'CREATE TABLE sets ( idSet integer primary key, strSet text, '
+          'strOverview text)'),
+      'settings': (
+          'CREATE TABLE settings ( idFile integer, Deinterlace bool,ViewMode '
+          'integer,ZoomAmount float, PixelRatio float, VerticalShift float, '
+          'AudioStream integer, SubtitleStream integer,SubtitleDelay float, '
+          'SubtitlesOn bool, Brightness float, Contrast float, Gamma '
+          'float,VolumeAmplification float, AudioDelay float, '
+          'OutputToAllSpeakers bool, ResumeTime integer,Sharpness float, '
+          'NoiseReduction float, NonLinStretch bool, PostProcess '
+          'bool,ScalingMethod integer, DeinterlaceMode integer, StereoMode '
+          'integer, StereoInvert bool, VideoStream integer)'),
+      'stacktimes': (
+          'CREATE TABLE stacktimes (idFile integer, times text)'),
+      'streamdetails': (
+          'CREATE TABLE streamdetails (idFile integer, iStreamType integer, '
+          'strVideoCodec text, fVideoAspect float, iVideoWidth integer, '
+          'iVideoHeight integer, strAudioCodec text, iAudioChannels integer, '
+          'strAudioLanguage text, strSubtitleLanguage text, iVideoDuration '
+          'integer, strStereoMode text, strVideoLanguage text)'),
+      'studio': (
+          'CREATE TABLE studio ( studio_id integer primary key, name TEXT)'),
+      'studio_link': (
+          'CREATE TABLE studio_link (studio_id integer, media_id integer, '
+          'media_type TEXT)'),
+      'tag': (
+          'CREATE TABLE tag (tag_id integer primary key, name TEXT)'),
+      'tag_link': (
+          'CREATE TABLE tag_link (tag_id integer, media_id integer, '
+          'media_type TEXT)'),
+      'tvshow': (
+          'CREATE TABLE tvshow ( idShow integer primary key,c00 text,c01 '
+          'text,c02 text,c03 text,c04 text,c05 text,c06 text,c07 text,c08 '
+          'text,c09 text,c10 text,c11 text,c12 text,c13 text,c14 text,c15 '
+          'text,c16 text,c17 text,c18 text,c19 text,c20 text,c21 text,c22 '
+          'text,c23 text, userrating integer, duration INTEGER)'),
+      'tvshowlinkpath': (
+          'CREATE TABLE tvshowlinkpath (idShow integer, idPath integer)'),
+      'uniqueid': (
+          'CREATE TABLE uniqueid (uniqueid_id INTEGER PRIMARY KEY, media_id '
+          'INTEGER, media_type TEXT, value TEXT, type TEXT)'),
+      'version': (
+          'CREATE TABLE version (idVersion integer, iCompressCount integer)'),
+      'writer_link': (
+          'CREATE TABLE writer_link(actor_id INTEGER, media_id INTEGER, '
+          'media_type TEXT)')}]
+  # TODO: Move this functionality to the formatter.
+
+  def ParseVideoRow(self, parser_mediator, query, row, **unused_kwargs):
+    """Parses a Video row.
+
+    Args:
+      parser_mediator (ParserMediator): mediates interactions between parsers
+          and other components, such as storage and dfvfs.
+      query (str): query that created the row.
+      row (sqlite3.Row): row.
+    """
+    query_hash = hash(query)
+
+    event_data = KodiEventData()
+    event_data.FileName = self._GetRowValue(query_hash, row, 'strFilename')
+    event_data.query = query
+
+    timestamp = self._GetRowValue(query_hash, row, 'lastPlayed').encode('utf-8')
+    date_time= dfdatetime_time_elements.TimeElements()
+    date_time.CopyFromDateTimeString(timestamp)
+    event = time_events.DateTimeValuesEvent(
+        date_time, definitions.TIME_DESCRIPTION_LAST_VISITED)
+    parser_mediator.ProduceEventWithEventData(event, event_data)
+
+sqlite.SQLiteParser.RegisterPlugin(KodiPlugin)
diff --git a/plaso/parsers/sqlite_plugins/smartthings.py b/plaso/parsers/sqlite_plugins/smartthings.py
new file mode 100644
index 0000000..12983bc
--- /dev/null
+++ b/plaso/parsers/sqlite_plugins/smartthings.py
@@ -0,0 +1,85 @@
+# -*- coding: utf-8 -*-
+"""This file contains a parser for the Smartthings ua_analytics.db
+
+"""
+
+from __future__ import unicode_literals
+
+from dfdatetime import posix_time as dfdatetime_posix_time
+
+from plaso.containers import events
+from plaso.containers import time_events
+from plaso.lib import definitions
+from plaso.parsers import sqlite
+from plaso.parsers.sqlite_plugins import interface
+
+
+class SmartthingsEventData(events.EventData):
+  """Smartthings event data.
+
+  Attributes:
+    FileName (str):
+  """
+
+  DATA_TYPE = 'iot:smartthings:activity'
+
+  def __init__(self):
+    """Initializes event data."""
+    super(SmartthingsEventData, self).__init__(data_type=self.DATA_TYPE)
+    self._id = None
+    self.type = None
+    self.event_id = None
+    self.data = None
+    self.session_id = None
+    self.event_size = None
+
+class SmartthingsPlugin(interface.SQLitePlugin):
+  """Parser for Smartthings databases."""
+
+  NAME = 'smartthings'
+  DESCRIPTION = 'Parser for smartthings ua_analytics database files.'
+
+  # Define the needed queries.
+  QUERIES = [
+      ('SELECT _id, type, event_id, time, data, session_id, event_size FROM events;',
+       'ParseActivityRow')]
+
+  # The required tables.
+  REQUIRED_TABLES = frozenset(['events'])
+
+  SCHEMAS = [{
+      'android_metadata': (
+          'CREATE TABLE android_metadata (locale TEXT)'),
+      'events': (
+          'CREATE TABLE events (_id INTEGER PRIMARY KEY AUTOINCREMENT,type '
+          'TEXT,event_id TEXT,time INTEGER,data TEXT,session_id '
+          'TEXT,event_size INTEGER)')}]
+
+  # TODO: Move this functionality to the formatter.
+
+  def ParseActivityRow(self, parser_mediator, query, row, **unused_kwargs):
+    """Parses a Activity row.
+
+    Args:
+      parser_mediator (ParserMediator): mediates interactions between parsers
+          and other components, such as storage and dfvfs.
+      query (str): query that created the row.
+      row (sqlite3.Row): row.
+    """
+    query_hash = hash(query)
+
+    event_data = SmartthingsEventData()
+    event_data.id = self._GetRowValue(query_hash, row, '_id')
+    event_data.type = self._GetRowValue(query_hash, row, 'type')
+    event_data.event_id = self._GetRowValue(query_hash, row, 'event_id')
+    event_data.data = self._GetRowValue(query_hash, row, 'data')
+    event_data.session_id = self._GetRowValue(query_hash, row, 'session_id')
+    event_data.event_size = self._GetRowValue(query_hash, row, 'event_size')
+    event_data.query = query
+
+    timestamp = self._GetRowValue(query_hash, row, 'time')
+    date_time = dfdatetime_posix_time.PosixTime(timestamp=timestamp)
+    event = time_events.DateTimeValuesEvent(date_time, 'Smart Things Event')
+    parser_mediator.ProduceEventWithEventData(event, event_data)
+
+sqlite.SQLiteParser.RegisterPlugin(SmartthingsPlugin)
