import time
from threading import Thread
from multiprocessing import Process
from typing import List, Tuple, Callable
import logging

from module.database import get_connection

logging.basicConfig(format='%(asctime)s [%(threadName)s] %(lineno)d %(message)s', level=logging.DEBUG)
#logging.basicConfig(format='%(asctime)s [%(processName)s] %(lineno)d %(message)s', level=logging.DEBUG)

class BaseCase:
    _logger = logging.getLogger('case')

    def _setup(self, conn):
        pass
    
    def _close(self, conn):
        pass

    def _get_routines(self) -> List[Callable]:
        raise NotImplementedError()

    def run(self):
        with get_connection() as conn:
            self._setup(conn)
            threads = [Thread(target=r, name=r.__name__, daemon=True) for r in self._get_routines()]
            [t.start() for t in threads]
            [t.join() for t in threads]
            #procs = [Process(target=r, name=r.__name__) for r in self._get_routines()]
            #[p.start() for p in procs]
            #[p.join() for p in procs]
            self._close(conn)
            input("Press Enter to continue...")

    def _begin(self, conn):
        conn.begin()
        self._logger.info('Begin')

    def _commit(self, conn):
        conn.commit()
        self._logger.info('Committed')
        
    def _sleep(self, sec: int):
        for i in range(sec, 0, -1):
            time.sleep(1)
            #self._logger.info(f'Sleep for {i} second...')
