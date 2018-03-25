import signal

from daemon import DaemonContext
# indirection for daemon module, in case we want to customize some of it, or use internals.




def set_signal_handlers(signal_handler_map):
    """ Set the signal handlers as specified.

        :param signal_handler_map: A map from signal number to handler
            object.
        :return: ``None``.

        See the `signal` module for details on signal numbers and signal
        handlers.

        """

    print("setting signal handlers : ")
    for (signal_number, handler) in signal_handler_map.items():
        print("\t - {signal_number} -> {handler}".format(**locals()))
        signal.signal(signal_number, handler)


__all__ = [
    'set_signal_handlers',
]