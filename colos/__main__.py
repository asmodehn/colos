#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import click

from . import heart


# Process structure :


# - glances  # providing a useful view of the system, yet we do not want to rely on it for anything else than view
# - heart:   # doing one thing only : checking that colos stays alive L1 : OS process check L2 : IPC message
# - colos:   # parent of all colos process. keeps heart alive by aggressive restart.
#   - colosmntr    # replying to heart L2 IPC, and detecting catastrophic failures in colos processes
#   - colosstat    # persisting and sending usage statistics. even on crash...
#   - colossfbx    # implementing safe dynamic functional programming.
#   - more


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)




async def heartlaunch(wait=5):
    """
    Wait for colosmntr to start, and upon success detach from foreground ( to run as daemon )
    :param wait: time to wait for colosmntr to be launched before aborting
    :return:
    """



async def coloslaunch():
    """
    Launches colos, with colosmntr first, and then other processes
    :return:
    """
    pass


async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y


async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))



if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(heart_launch)
    # heart is launched, we are safe from crash now.


    loop.run_until_complete(print_sum(1, 2))
    loop.close()
