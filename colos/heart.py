#  very basic python daemon, keeping colos alive
import argparse
import sys
import os
import signal
import lockfile
import daemon
import asyncio

def shutdown(signum, frame):  # signum and frame are mandatory
    sys.exit(0)


# Internal coroutines
async def do_smthg(future):
    await asyncio.sleep(1)
    # future.set_result('Future is done!')


# eventloop
def main():
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(do_smthg(future))

    def got_result(future):
        print(future.result())
        loop.stop()

    future.add_done_callback(got_result)
    try:
        loop.run_forever()
    finally:
        loop.close()


# IPC Interface
def start(nodaemon=False):
    if nodaemon:
        main()
    else:
        # TODO : implement sensible defaults based on platform
        os.makedirs('/var/run/colos/.heart', exist_ok=True)
        with daemon.DaemonContext(
            chroot_directory=None,
            working_directory='/var/lib/colos/.heart',
            signal_map={
                signal.SIGTERM: shutdown,
                signal.SIGTSTP: shutdown
            },
            pidfile=lockfile.FileLock('/var/run/spam.pid')
        ):
            main()

def stop():
    pass

def reload():
    pass


# CLI interface
# --start (default)
# --stop
# --reload
# --nodetach
if '__main__' == __name__:
    parser = argparse.ArgumentParser(description='Launches the heart daemon')
    parser.add_argument('-s', '--stop', action='store_true',
                        help='stops the heart daemon')
    parser.add_argument('-r', '--reload', action='store_true',
                        help='reloads the heart daemon')
    parser.add_argument('--nodetach', action='store_true',
                        help='runs the heart daemon in the current process.')

    args = parser.parse_args()
    print(args)

    if '--stop' in args:
        stop()
    elif '--reload' in args:
        reload()
    else:
        if '--nodetach' in args:
            start(nodaemon=True)
        else:
            start()

