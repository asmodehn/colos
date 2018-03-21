# ColOS

Collaborative OS : Multiprocess python, optimized by relying on OS features.

While considering a "machine" and an OS with the sysadmin perspective, we aim to find a set of assumptions, that are followed by most OSes, upon which python is designed, in order to allow implementing robust multiprocess software logic on it.

Examples may be: files, sockets, CPU, memory, etc.

Another way to put it would be "let's build an erlang VM in python, for python, except it s not a VM, everything happens when it happens, dynamically."

It is intended mostly as a trial framework for distributed algorithms on a single machine, optimizing for local use where it i safe, without losing the robustness that can come from distribution.

Disclaimers 
-----------

- If you dont *need* a multiprocess framework, just use a monoprocess one, as in "your favorite programming language". It will spare you years of pain.
- If you *need* a distributed system (as in "over the network") go look elsewhere, we're just not there yet (although we plan to integrate with some later)


First steps 
===========

- check psutil in details to extract usable concepts (files, processes, etc.)
- implement an automated test library in order to make it simple to test any kinds of failure in a system (with the hypothesis perspective : ensuring a property of the system)
- use erlang VM and paradigm to design colos feature set, and make them usable by any library wanting to build on top of it
- implement live monitoring, so that any OS problems affecting the system is quickly identified, isolated, and mitigated as much as possible.
- make it easily introspectable (open files, connect terminals)
- track how people use it to inform evolution


Roadmap and long term goals
=========================== 

- [ ]  HW system Monitoring UI, through OS features (glances ?). 
- [ ]  Central Website to access KPI and metrics (for all, anonymously).
- [ ]  Automated occasional HW stress tests, regular basic consistency checks.
- [ ]  API for handling failures in HW & OS (even unexpected ones)
- [ ]  Fully Dynamic Python (pypy interpreted, minimal abstraction between code and machine)
- [ ]  Fully Introspectable (manually, just check your file system)
- [ ]  Fully Reflexive (API for automated introspection)


Constraints
===========

- Keep it in one unique package, usable as a library by anyone wanting to build something on top
- Keep OS requirement minimal (lowest commin denominator, including embedded RTOSes, and otheresoteric systems out there)
- Keep it local, since we rely on the OS. Network included.
- Expect the OS & HW to fail, permanently monitor, and eventually recover.
- Let the python code errors be managed by usual python tools.
- focus on pypy, but must be usable from CPython.
- focus on async
- think about docker usecase
- think about embedded usecase

