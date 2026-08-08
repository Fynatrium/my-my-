# Layout Scale Constants
WALL_TYPE_LABEL_W = 0.35
WALL_TYPE_WIDGET_SX = 1.0
WALL_TYPE_WIDGET_SY = 1.0
WALL_TYPE_ROW_SY = 1.0
WALL_TYPE_PREVIEW_X = 1.0
WALL_TYPE_PREVIEW_Y = 1.0

CONSTRAINTS_LABEL_W = 0.45
CONSTRAINTS_WIDGET_SX = 1.0
CONSTRAINTS_WIDGET_SY = 1.0
CONSTRAINTS_ROW_SY = 1.0

CROSS_LABEL_W = 0.45
CROSS_WIDGET_SX = 1.0
CROSS_WIDGET_SY = 1.0
CROSS_ROW_SY = 1.0

STRUCT_LABEL_W = 0.45
STRUCT_WIDGET_SX = 1.0
STRUCT_WIDGET_SY = 1.0
STRUCT_ROW_SY = 1.0

DIM_LABEL_W = 0.40
DIM_WIDGET_SX = 1.0
DIM_WIDGET_SY = 1.0
DIM_ROW_SY = 1.0

MODIFY_BTN_SX = 1.0
MODIFY_BTN_SY = 1.0
MODIFY_LABEL_W = 0.45
MODIFY_WIDGET_SX = 1.0
MODIFY_WIDGET_SY = 1.0
MODIFY_ROW_SY = 1.0

DRAW_BTN_SX = 1.0
DRAW_BTN_SY = 1.0
DRAW_LABEL_W = 0.45
DRAW_WIDGET_SX = 1.0
DRAW_WIDGET_SY = 1.0
DRAW_ROW_SY = 1.0


def split_prop(layout, data, prop_name, text, label_w, widget_sx, widget_sy, row_sy):
    row = layout.row(align=True)
    row.scale_y = row_sy
    split = row.split(factor=label_w, align=True)
    label_col = split.column(align=True)
    label_col.label(text=text)
    prop_col = split.column(align=True)
    prop_col.scale_x = widget_sx
    prop_col.scale_y = widget_sy
    prop_col.prop(data, prop_name, text="")
    return row
