import os
from datetime import datetime
from cudatext import *

import tempfile

plugin_name = __name__
fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_auto_save.ini')

opt_save_interval_seconds = 30
opt_save_max_mb_size_file = 5
opt_save_onclose = False
opt_save_ondeact = False
opt_save_ontabchange = False
opt_save_session = True
opt_session_flags = ''
opt_ignore_temp_files = False
opt_save_onchange = False

opt_ignore_saving_trim_spaces = False
global_prop_saving_trim_spaces = ed.get_prop(PROP_SAVING_TRIM_SPACES)


# Simple implementation of logger.
class Log:
    info_ = False
    debug_ = False

    @staticmethod
    def info(s):
        if Log.info_:
            print(datetime.now().strftime("%H:%M:%S") + ' [INFO] ' + plugin_name + ' - ' + s)

    @staticmethod
    def debug(s):
        if Log.debug_:
            print(datetime.now().strftime("%H:%M:%S") + ' [DEBUG] ' + plugin_name + ' - ' + s)


def bool_to_str(v): return '1' if v else '0'


def str_to_bool(s): return s == '1'


def get_log_file_size(fn_KB_size):
    msg = 'Max auto-saving file size: ' + \
          str(opt_save_max_mb_size_file * 1024) + \
          ' KBs / Current file size: ' + str(fn_KB_size) + ' KBs'
    return msg


def save_all(msg):
    global opt_save_session
    global opt_session_flags

    for h in ed_handles():
        e = Editor(h)
        save_one(e, 'Saving file (' + msg + ')')

    if opt_save_session:
        text = app_path(APP_FILE_SESSION)
        if app_api_version()>='1.0.415':
            text += ';'+opt_session_flags
            if msg=='By timer':
                text += 't'
        app_proc(PROC_SAVE_SESSION, text)
        Log.info('Saving session (' + msg + ')')


def save_one(e, msg):
    fn = e.get_filename()
    if not fn: return

    if opt_ignore_temp_files:
        tmpdir = tempfile.gettempdir() + os.sep
        if fn.startswith(tmpdir):
            return

    if not e.get_prop(PROP_MODIFIED, ''):
        return

    Log.debug('Processing file: ' + fn)
    if os.path.isfile(fn):
        fn_KB_size = os.path.getsize(fn) // 1024
        Log.debug(get_log_file_size(fn_KB_size))

        if opt_save_max_mb_size_file == 0 or fn_KB_size // 1024 <= opt_save_max_mb_size_file:
            check_ignore_saving_trim_spaces()
            e.save()
            check_ignore_saving_trim_spaces(True)
            Log.info(msg + ': ' + fn)
    else:
        Log.info('File was moved or deleted: ' + fn)

def check_ignore_saving_trim_spaces(return_option = False):
    if opt_ignore_saving_trim_spaces:
        if return_option:
            if global_prop_saving_trim_spaces:
                ed.set_prop(PROP_SAVING_TRIM_SPACES, True)
        else:
            ed.set_prop(PROP_SAVING_TRIM_SPACES, False)

def timer_tick(tag='', info=''):
    save_all('By timer')


def recreate_events(inc_event='', setup_timer=1):
    global opt_save_interval_seconds
    global opt_save_max_mb_size_file
    global opt_save_onclose
    global opt_save_ondeact
    global opt_save_ontabchange
    global opt_save_session
    global opt_session_flags
    global opt_ignore_temp_files
    global opt_save_onchange
    global opt_ignore_saving_trim_spaces

    # Read settings if config file exists.
    if os.path.isfile(fn_config):
        opt_save_interval_seconds = int(ini_read(fn_config, 'op', 'save_interval_seconds', str(opt_save_interval_seconds)))
        opt_save_interval_seconds = max(10, opt_save_interval_seconds) if opt_save_interval_seconds > 0 else 0 # dont allow too small value
        opt_save_max_mb_size_file = int(ini_read(fn_config, 'op', 'save_max_MB_file_size', str(opt_save_max_mb_size_file)))
        opt_save_onclose = str_to_bool(ini_read(fn_config, 'op', 'save_before_closing_tab', bool_to_str(opt_save_onclose)))
        opt_save_ondeact = str_to_bool(ini_read(fn_config, 'op', 'save_on_deactivate', bool_to_str(opt_save_ondeact)))
        opt_save_ontabchange = str_to_bool(ini_read(fn_config, 'op', 'save_on_tab_change', bool_to_str(opt_save_ontabchange)))
        opt_save_session = str_to_bool(ini_read(fn_config, 'op', 'save_session', bool_to_str(opt_save_session)))
        opt_session_flags = ini_read(fn_config, 'op', 'session_flags', opt_session_flags)
        opt_ignore_temp_files = str_to_bool(ini_read(fn_config, 'op', 'ignore_temp_files', bool_to_str(opt_ignore_temp_files)))
        opt_save_onchange = str_to_bool(ini_read(fn_config, 'op', 'save_on_editor_change', bool_to_str(opt_save_onchange)))
        opt_ignore_saving_trim_spaces = str_to_bool(ini_read(fn_config, 'op', 'ignore_saving_trim_spaces', bool_to_str(opt_ignore_saving_trim_spaces)))

    events = []
    if inc_event: events.append(inc_event)
    # on_tab_change event is called before on_close_pre event
    if not opt_save_ontabchange and opt_save_onclose: events.append('on_close_pre')
    if opt_save_ondeact: events.append('on_app_deactivate')
    if opt_save_ontabchange: events.append('on_tab_change')
    if opt_save_onchange: events.append('on_change_slow')

    Log.info('Recreating events: ' + ','.join(events))
    app_proc(PROC_SET_EVENTS, plugin_name + ';' + ','.join(events) + ';;')

    if setup_timer != 1: return

    if opt_save_interval_seconds > 0:
        Log.info('Turning on timer_tick function.')
        timer_proc(TIMER_START, 'module=cuda_auto_save;func=timer_tick;',
                   opt_save_interval_seconds*1000)
    else:
        Log.info('Turning off timer_tick function.')
        timer_proc(TIMER_STOP, 'module=cuda_auto_save;func=timer_tick;', 0)


class Command:

    def __init__(self):
        recreate_events()

    def on_start(self, ed_self):
        # Created only to initialize this plugin.
        Log.debug('on_start event')
        pass

    def config(self):
        # Wait for config file closing in order do not need to restart CudaText
        # to get new option values.
        recreate_events(inc_event='on_close', setup_timer=0)

        # Delete file in case there are more settings of previous version
        if os.path.isfile(fn_config):
            os.remove(fn_config)

        # Add some comments to provide help guidelines in file config.
        with open(fn_config, "a") as f:
            f.write('; save_interval_seconds=0 to deactivate timer.\n')
            f.write('; save_max_MB_file_size=0 to deactivate size checks.\n')
            f.write('; session_flags can have chars "n", "u"; e.g. session_flags=nu\n')

        ini_write(fn_config, 'op', 'save_interval_seconds', str(opt_save_interval_seconds))
        ini_write(fn_config, 'op', 'save_max_MB_file_size', str(opt_save_max_mb_size_file))
        ini_write(fn_config, 'op', 'save_before_closing_tab', bool_to_str(opt_save_onclose))
        ini_write(fn_config, 'op', 'save_on_deactivate', bool_to_str(opt_save_ondeact))
        ini_write(fn_config, 'op', 'save_on_tab_change', bool_to_str(opt_save_ontabchange))
        ini_write(fn_config, 'op', 'save_session', bool_to_str(opt_save_session))
        ini_write(fn_config, 'op', 'session_flags', opt_session_flags)
        ini_write(fn_config, 'op', 'ignore_temp_files', bool_to_str(opt_ignore_temp_files))
        ini_write(fn_config, 'op', 'save_on_editor_change', bool_to_str(opt_save_onchange))
        ini_write(fn_config, 'op', 'ignore_saving_trim_spaces', bool_to_str(opt_ignore_saving_trim_spaces))
        file_open(fn_config)

    def on_close_pre(self, ed_self):
        Log.debug('on_close_pre event')
        save_one(ed_self, 'Closing file')

    def on_app_deactivate(self, ed_self):
        Log.debug('on_app_deactivate event')
        save_all('App deactivated')

    def on_tab_change(self, ed_self):
        Log.debug('on_tab_change event')
        save_all('Tab change')

    def on_change_slow(self, ed_self):
        Log.debug('on_change_slow event')
        save_one(ed_self, 'Editor change')

    def on_close(self, ed_self):
        # Used only to catch when Config file is modified and saved
        Log.debug('on_close event')

        fn = ed_self.get_filename()
        if not fn: return

        if fn == fn_config: recreate_events()
