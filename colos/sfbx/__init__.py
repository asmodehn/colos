# The aim of this package is to :
# - guarantee protected code execution is safe and *will* happen (eventually)
# - report usage via colosstat
# - recover when code fails ( possibly recording previous state, for example )

# one possibility is to implement another levelof abstraction ( like a language - cstk aim )
# another is to just isolate portions of python code with postconditions to guarantee success...
