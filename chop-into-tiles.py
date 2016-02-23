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
