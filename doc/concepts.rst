Design Document
===============


Overview
--------

ColOS is a collaborative OS, as in a manager of processes that are made to collaborate (by opposition to the traditional OS definition where processes compete for resources - RAM and CPU).
As such ColOS could be embedded in a traditional OS, but could also be ( via network ) interfaced with other ColOS instances running on remote machines to transparently aggregate computing resources.

This could be useful in a number of applications, from large HPC environment, to embedded distributed systems.


Constraints
-----------

ColOS comes playing in the Erlang backyard, however we want to keep close connection with the hardware (for simple use in small devices via MicroPython or so).
Therefore we do not want to have a VM, instead we will rely on OS features (POSIX and other standards : signals, pipes, etc.) to manage the network of processes.

On the other hand we want to be fully dynamic and leverage python tooling, so all processes will run an small interpreter (possibly pypy),
guaranteeing the completion and correctness of the computation, in a best effort model, in the face of potentially faulty hardware and underlying software (OS, etc.).

Usual Python code will be provided to make use of ColOS features. Python, as a language, is not intended to be a target for distribution (given its operative nature it would be too much effort - and is already attempted by some),
however we should provide enough building blocks for using ColOS from inside a Python environment. Possibly developing some kind of DSL for distribution on top of Python...

Eventually ColOS could go to lower layers in the machine (embed Python, in OS, in hardware, etc.) however this would be a very costly effort, so we will currently shy away from it.

