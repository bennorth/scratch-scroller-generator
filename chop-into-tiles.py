from functools import partial
import Image, sys
import kurt
import image_tiling as T


B = kurt.Block
V = partial(B, 'readVariable')
sV = partial(B, 'setVar:to:')


def display_script(u0, v0):
    """
    Return kurt.Script object for the repositioning script for a tile
    whose centre is to appear at (``u0``, ``v0``) in world coordinates.
    Assumes the existence of the following variables:

        global variables ``centre-x``, ``centre-y`` --- world
            coordinates of the current centre of the viewport

        sprite-local variables ``s``, ``t`` --- intermediate calculation
            for this sprite: (s, t) = (u0, v0) - (centre-x, centre-y),
            i.e., where on the screen this tile should be positioned
            (before allowing for hiding when off-screen)
    """
    hat = B('whenIReceive', 'reposition-map-tiles')

    set_s = sV('s', B('-', u0, V('centre-x')))
    set_t = sV('t', B('-', v0, V('centre-y')))

    var_s = V('s')
    var_t = V('t')
    move = B('gotoX:y:', var_s, var_t)
    if_clause = [move, B('show')]
    else_clause = [B('hide')]
    s_test = B('&',
               B('not', B('<', var_s, -T.Constants.u_stride)),
               B('<', var_s, T.Constants.u_stride))
    t_test = B('&',
               B('not', B('<', var_t, -T.Constants.v_stride)),
               B('<', var_t, T.Constants.v_stride))
    both_test = B('&', s_test, t_test)
    maybe_move_show = B('doIfElse', both_test,
                        if_clause, else_clause)

    return kurt.Script([hat,
                        B('hide'),
                        set_s,
                        set_t,
                        maybe_move_show])


def sprite_from_tile(project, tile):
    """
    Create and return a new Sprite belonging to ``project`` for the
    given ``tile``.  It is given a single costume equal to the tile's
    image, and a single script which positions the tile on the screen
    correctly for the tile's (u0, v0) coordinates.
    """
    sprite = kurt.Sprite(project, 'tile-%02d-%02d' % (tile.u0, tile.v0))
    sprite.costumes = [kurt.Costume('img', kurt.Image(tile.img))]
    sprite.scripts = [display_script(tile.u0, tile.v0)]
    sprite.variables = {'s': kurt.Variable(0), 't': kurt.Variable(0)}
    return sprite


if __name__ == '__main__':
    source_image_fname = sys.argv[1]
    source_image = Image.open(source_image_fname)
    padded_image = T.padded_image(source_image)

    project = kurt.Project()

    tiles = T.TileDescriptor.list_from_image(padded_image)

    sprites = [sprite_from_tile(project, tile) for tile in tiles]

    project.sprites = sprites

    project.variables = {'centre-x': kurt.Variable(0),
                         'centre-y': kurt.Variable(0)}

    project.save(sys.argv[2])


"""
Notes from observations:

A full-size (480x360) bitmap sprite can be positioned up to limits of

full left: x = -465
full right: x = 465
full down: y = -345
full up: y = 345

Manually dragging sprite can take it outside these bounds, but, e.g., if
y is set in this way to 350, then 'change y by 1' is executed, y will
end up as 345.

Costume centre is set to corners of pixels, not centres.
"""
