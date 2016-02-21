import Image
from collections import namedtuple

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

class TileDescriptor(namedtuple('TileDescriptor', 'u0 v0 img')):
    """
    u0 and v0 are the world coords (with 'y is up' convention)
    corresponding to the centre of 'img'.  'img' will be of even width
    and height, so the coords refer to the central vertex, not the
    centre of any pixel.
    """
    @classmethod
    def from_world_image(cls, u0, v0, world_image):
        """
        u0 and v0 are interpreted in 'y is up' coords, with bottom-left
        being the origin.  I.e., (0, 0) refers to the bottom-left vertex
        of the bottom-left pixel.  The returned TileDescriptor has an
        'img' such that its central vertex corresponds to the vertex
        with world coords (u0, v0) in the world image.
        """
        world_ht = world_image.size[1]
        tl_x = u0 - Constants.viewport_half_wd
        tl_y = world_ht - (Constants.viewport_half_ht + v0)
        tile_wd = 2 * Constants.viewport_half_wd
        tile_ht = 2 * Constants.viewport_half_ht
        tile_img = world_image.crop((tl_x, tl_y, tl_x + tile_wd, tl_y + tile_ht))
        return cls(u0, v0, tile_img)
