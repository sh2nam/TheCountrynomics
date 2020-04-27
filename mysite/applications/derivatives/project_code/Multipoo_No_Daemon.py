import multiprocessing.pool


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class MyPool(multiprocessing.pool.Pool):
    # We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
    # because the latter is only a wrapper function, not a proper class.
    Process = NoDaemonProcess
