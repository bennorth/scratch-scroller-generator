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

def tile_stride(viewport_half_size, overlap):
    return 2 * viewport_half_size - overlap

def padded_size(raw_size, viewport_half_size, overlap):
    """
    Return the size which we must pad the original image to (along one
    dimension) such that an integer number of overlapping tiles cover
    it.
    """
    stride = tile_stride(viewport_half_size, overlap)
    viewport_size = 2 * viewport_half_size
    clamped_below_size = max(raw_size, viewport_size)
    return (viewport_size
            + round_up_to_multiple(clamped_below_size - viewport_size, stride))
