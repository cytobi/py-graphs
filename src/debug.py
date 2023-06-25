# simple debug utilities

def debug(to_print):
    if __debug__:
        print(to_print)