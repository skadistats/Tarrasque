MAX_COORD_INTEGER = 16384

def cell_to_coords(cell_x, cell_y, offset_x, offset_y, cellbits):
  cellwidth = 1 << cellbits
  x = ((cell_x * cellwidth) - MAX_COORD_INTEGER) + offset_x
  y = ((cell_y * cellwidth) - MAX_COORD_INTEGER) + offset_y
  return (x, y)

def none_or_nonzero(val):
  if val == 0:
    return
  else:
    return val
