#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  very basic python daemon, keeping colos alive
import argparse
import sys
import os
import signal
import lockfile
import daemon
import asyncio

import pathlib


def shutdown(signum, frame):  # signum and frame are mandatory
    sys.exit(0)


# Internal coroutines
async def do_smthg(future):
    print('sleep1')
    await asyncio.sleep(1)
    # future.set_result('Future is done!')
    asyncio.ensure_future(do_smthg(future))

# eventloop
def main():
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(do_smthg(future))

    def got_result(future):
        print(future.result())
        print("done!")
        loop.stop()

    #future.add_done_callback(got_result)
    try:
        print("looping")
        loop.run_forever()
    finally:
        loop.close()

    print("done")


# IPC Interface
def start(nodaemon=False, noroot=False):
    print("nodaemon {}".format(nodaemon))
    print("noroot {}".format(noroot))

    if nodaemon:
        print("started as normal process")
        res = main()
    else:
        # TODO : implement sensible defaults based on platform

        chroot_dir = '/var/run/colos/.heart'
        working_dir = os.getcwd()
        detach_me = not noroot

        if os.access('/var/run', os.W_OK | os.X_OK):  # we re probably root, anyway we have access to /var/run, so lets do this !
            path = pathlib.Path(chroot_dir)
            path.mkdir(parents=True, exist_ok=True)
        elif noroot:  # if it is started as non-root (usually for testing), we allow running in current dir.
            chroot_dir = None
        else:
            print("Current user cannot access /var/run. Try starting the daemon with --noroot option")
            return 1


        print("starting as daemon process, detaching from terminal. Otherwise try the --nodaemon option")
        with daemon.DaemonContext(
            chroot_directory=chroot_dir,
            working_directory=working_dir,
            detach_process=detach_me,
            #uid=1001,
            #gid=777,
            #umask=0o002,
            signal_map={
                signal.SIGTERM: shutdown,
                signal.SIGTSTP: shutdown
            },
            pidfile=lockfile.FileLock('/var/run/heart.pid')
        ):
            res = main()

    return res

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
    parser.add_argument('--nodaemon', action='store_true',
                        help='runs the heart daemon in the current process.')
    parser.add_argument('--noroot', action='store_true',
                        help='runs the heart daemon as the current user.')

    args = parser.parse_args()
    #print(args)

    res=127

    if args.stop:
        res = stop()
    elif args.reload:
        res = reload()
    else:
        res = start(nodaemon=args.nodaemon, noroot=args.noroot)

    sys.exit(res)
