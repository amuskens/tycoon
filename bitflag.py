class BitFlag():
    """
    BitFlag - bit flag 

    Enables bit setting and testing of a flag.

    f = BitFlag()

    f.get() <- returns value of flag
    f.get(mask) <- returns value of flag & mask, to test specific bits

    f.set(flag) <- sets the flag 
    f.set(flag, mask) <- clears the flag at the 1 positions of mask, and 
        sets the bits in flag that match the 1s in the mask
    In both cases, the previous value of the flag is returned in case you
    want to restore the flag.

    >>> from bitflag import BitFlag
    >>> f = BitFlag()
    >>> f._flag 
    0
    >>> old_value = f.set(2)
    >>> old_value
    0
    >>> f.set(old_value)
    2
    >>> f.set(5)
    0
    >>> f.get()
    5
    >>> f.get(4)
    4
    >>> f.get(2)
    0
    >>> f.get(6)
    4
    >>> # clear bit 2
    >>> f.set(0, 4)
    >>> # previous value is 5
    5
    >>> f.get()
    1
    >>> f.set(6, 4)
    1
    >>> f.get()
    5
    """

    def __init__(self):
        self._flag = 0

    def get(self, mask=None):
        if mask == None:
            return self._flag
        return mask & self._flag

    def set(self, new_flag, mask=None):
        orig_flag = self._flag
        if mask != None:
            print("mask is", mask)
            # clear bits in flag corresponding to 1's i mask
            self._flag = self._flag & ( ~ mask )
            print("flag is", self._flag)
            # keep only the bit positions corresponding to 1s in mask
            new_flag = new_flag & mask
            # set any 1s in the new_flag value
            self._flag = self._flag | new_flag
            print("flag is", self._flag)
        else:
            self._flag = new_flag

        return orig_flag

if __name__ == '__main__':
    import doctest
    doctest.testmod()
