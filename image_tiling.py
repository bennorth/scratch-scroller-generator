import Image

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

class Constants:
    viewport_half_wd = 240
    viewport_half_ht = 180
    tile_overlap = 20
    u_stride = tile_stride(viewport_half_wd, tile_overlap)
    v_stride = tile_stride(viewport_half_ht, tile_overlap)

def padded_image(world_image):
    """
    Return an image containing the given ``world_image`` in its centre,
    with dimensions such that it is an integer number of tiles in each
    dimension.
    """
    raw_wd, raw_ht = world_image.size
    padded_wd = padded_size(raw_wd, Constants.viewport_half_wd, Constants.tile_overlap)
    padded_ht = padded_size(raw_ht, Constants.viewport_half_ht, Constants.tile_overlap)
    padded_img = Image.new(world_image.mode, (padded_wd, padded_ht), "black")
    x0 = (padded_wd - raw_wd) // 2
    y0 = (padded_ht - raw_ht) // 2
    padded_img.paste(world_image, (x0, y0))
    return padded_img
