#!/usr/bin/env python
# @Author  : pengyun

from werkzeug._reloader import ReloaderLoop, _log
import time
import threading
import sys
import os
from datetime import datetime


class Restart(ReloaderLoop):
    name = 'restart'

    def log_reload(self, workname):
        _log('info', '{} restart in {}'.format(workname, datetime.now()))
        #logging.info('info', '{} restart in {}'.format(workname, datetime.now()))


    def trigger_reload(self, workname):
        self.log_reload(workname)
        sys.exit(3)

    def run(self, workname, stime, retime):
        print(stime)
        while 1:
            if time.time()-stime > retime:
                self.trigger_reload(workname)
            self._sleep(self.interval)


def run_with_restart(main_func, stime, retime, interval=1, workname='default'):
    import signal
    restart = Restart(interval=interval)
    signal.signal(signal.SIGTERM, lambda *args: sys.exit(0))
    try:
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            t = threading.Thread(target=main_func, args=())
            t.setDaemon(True)
            t.start()
            restart.run(workname, stime, retime)
        else:
            sys.exit(restart.restart_with_reloader())
    except KeyboardInterrupt:
        pass

test = lambda : 1
if __name__ == '__main__':
    run_with_restart(test, stime=time.time(), retime=6)

