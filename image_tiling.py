def round_up_to_multiple(n, d):
    """
    Return smallest multiple of d not less than n.
    """
    if d <= 0:
        raise ValueError('expected positive divisor')
    q, r = divmod(n, d)
    if r:
        return n + d - r
    else:
        return n
