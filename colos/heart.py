#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  very basic python daemon, keeping colos alive
import argparse
import inspect
import multiprocessing
import queue
import sys
import os
import signal

import functools
import lockfile
import asyncio

import pathlib
import collections

# import oslash


# relative import
try:
    # importing our locally patched daemon module
    from . import _daemon as daemon
except SystemError:
    import _daemon as daemon


# Internal coroutines implementing state transitions
# as triggered by commands


#@cmd('start', origin_state_list=['init'])
async def running(future):
    print('sleep1')
    await asyncio.sleep(1)
    asyncio.ensure_future(running(future))

# TODO : coroutines implementing lambda calculus | kernel + continuation
# TODO : LATER implement process calculi in coroutines ( via different future chains ). Might not be efficient as multiprocess, but still possible.


#@cmd('stop', origin_state_list=['running'])
async def dothis():
    print ("doing this")
    return 'This is done!'

async def dothat():
    print ("doing that")
    return 'That is done!'

#@cmd('stop', origin_state_list=['running'])
async def cleanup():
    print("cleaning up...")
    return 'Future is done!'


# eventloop
def mainsub():
    """
    Main function, potentially running in a child process or a thread
    :return:
    """
    loop = asyncio.get_event_loop()
    done = asyncio.Future()

    # communicating via process variable or Signals only
    receive_task = None  # no task started yet

    async def receive(loop, end_future, **coros):
        """
        Loops checking the queue for messages
        :param end_future: future set when everything is done
        :param coros: List of coroutines callablefrom outside : our IPC API
        :return:
        """
        nonlocal receive_task
        try:
            print("checking messages...")
            try:
                m = msgs.get_nowait()
                if m in coros:  #  keeping linearizability of coro calls
                    print(m)
                    loop.create_task(coros.get(m)())
            except queue.Empty:
                pass
            except asyncio.QueueEmpty:
                pass
            if end_future.done():
                # doing clean shutdown
                print("end future")
                pass
            else:
                # keep looping
                await asyncio.sleep(1)  # TODO PID Controller to manage queue length
                receive_task = asyncio.ensure_future(receive(loop, end_future, **coros))
                print("scheduled {receive_task}".format(**locals()))
        except asyncio.CancelledError:
            print("Receive Task has been cancelled. terminating...")
            await cleanup()
            loop.stop()


    receive_task = asyncio.ensure_future(receive(loop, done, **{
        dothis.__name__:  dothis,
        dothat.__name__: dothat,
        cleanup.__name__: cleanup,
    }))
    print("scheduled {receive_task}".format(**locals()))

    def signal_hndl(signum, frame):
        nonlocal receive_task
        print("Signal {signum} caught at {frame}. cancelling receive {receive_task}...".format(**locals()))
        receive_task.cancel()

    async_signal_map = {
        signal.SIGTERM: signal_hndl,
        signal.SIGTSTP: signal_hndl,
        signal.SIGINT: signal_hndl,
    }

    #preparing async signal handlers
    daemon.set_signal_handlers(async_signal_map)


    def got_result(future):
        print(future.result())
        print("done!")
        msgs.join()
        loop.stop()

    # setting up callback for termination
    done.add_done_callback(got_result)
    try:
        print("looping")
        loop.run_forever()
    finally:
        loop.close()

    print("done")


# def sigchld():



# def mainsub():



def main(nodaemon=False, noroot=False):
    print("nodaemon {}".format(nodaemon))
    print("noroot {}".format(noroot))


    if nodaemon:
        daemon.set_signal_handlers(signal_map)

        try:
            print("starting as normal process...")
            res = mainsub()
        except KeyboardInterrupt:
            # should be handled by signal handlers...
            res = 127
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
            signal_map=signal_map,
            pidfile=lockfile.FileLock('/var/run/heart.pid')
        ):
            try:
                res = mainsub()
            except KeyboardInterrupt:
                # should be handled by signal handlers...
                res = 127

    return res



###############
# IPC Interface
###############

# Design : we use oly the Signal interface to communicate and supervise processes.
# more complete communication pattern will be handled somewhere else

#ref : http://www.open-std.org/jtc1/sc22/wg14/www/standards.html
# SIGINT : interrupt (terminal Ctrl-C) -> usually graceful shutdown  "user initiated happy"
# SIGQUIT : dump core  (terminal Ctrl-|) "user initiated unhappy"
# SIGTERM : cleanup and terminate
# SIGTSTP : interactively pausing (terminal Ctrl-Z)
# SIGHUP : Hangup (terminal Ctrl-D)
# SIGSTOP / SIGCONT : pause & resume process (OS)

# signals send messages to the queue, just like any other process
# TODO : CAREFUL the nature of the queue (threading; multiprocessing, async)
msgs = queue.Queue()

def shutdown(signum, frame):  # signum and frame are mandatory
    # we need here to make every attempt to shutdown properly
    msgs.put('cleanup')
    pass

def state(signum, frame):  # signum and frame are mandatory
    pass

signal_map = {
    signal.SIGTERM: shutdown,
    signal.SIGTSTP: shutdown,
    signal.SIGINT : shutdown,
}


############
# Public API
############

def start(children, nodaemon = False, noroot=False):
    """
    Starting heart (will spawn a sub process)
    :param nodaemon:
    :param noroot:
    :param children: processes to launch and supervise)
    :return:
    """
    main(nodaemon=nodaemon, noroot=noroot)

def stop():
    """
    Stopping heart (using IPC)
    :return:
    """
    pass  # TODO

def reload():
    """
    Reloading heart (using IPC)
    :return:
    """
    pass  #TODO



###############
# CLI interface
###############
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

    res = 127

    if args.stop:
        res = stop()
    elif args.reload:
        res = reload()
    else:
        res = start(children = [], nodaemon=args.nodaemon, noroot=args.noroot)

    sys.exit(res)
