import os
from cudatext import *
import cudatext_cmd as cmds

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_auto_save.ini')

opt_save_interval = 30
opt_save_onclose = False
opt_save_ondeact = False

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

def save_all(msg):

    for h in ed_handles():
        e = Editor(h)
        fn = e.get_filename()
        if fn and e.get_prop(PROP_MODIFIED, ''):
            e.save()
            print('Auto-saved ('+msg+'):', fn)

def timer_tick(tag='', info=''):

    save_all('by timer')

class Command:

    def __init__(self):

        global opt_save_interval
        global opt_save_onclose
        global opt_save_ondeact
        opt_save_interval = int(ini_read(fn_config, 'op', 'save_interval', str(opt_save_interval)))
        opt_save_onclose = str_to_bool(ini_read(fn_config, 'op', 'save_before_closing_tab', bool_to_str(opt_save_onclose)))
        opt_save_ondeact = str_to_bool(ini_read(fn_config, 'op', 'on_deactivate', bool_to_str(opt_save_ondeact)))

    def on_start(self, ed_self):

        if opt_save_interval>0:
            timer_proc(TIMER_START, 'module=cuda_auto_save;func=timer_tick;', opt_save_interval*1000)

    def config(self):

        ini_write(fn_config, 'op', 'save_interval', str(opt_save_interval))
        ini_write(fn_config, 'op', 'save_before_closing_tab', bool_to_str(opt_save_onclose))
        ini_write(fn_config, 'op', 'on_deactivate', bool_to_str(opt_save_ondeact))
        file_open(fn_config)

    def on_close_pre(self, ed_self):

        if not opt_save_onclose:
            return
        fn = ed_self.get_filename()
        if not fn: return
        if ed_self.get_prop(PROP_MODIFIED, ''):
            ed_self.save()
            print('Auto-saved (file closes):', fn)

    def on_app_deactivate(self, ed_self):

        if not opt_save_ondeact:
            return
        save_all('app deactivated')
