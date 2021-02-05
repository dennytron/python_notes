"""
    Style formatting functions for Fire Risk Pro"
    https://convertingcolors.com/decimal-color-0.html?search=Decimal(0)
"""
from osgeo.ogr import Feature


def get_zip_style(feature: Feature) -> str:
    zippy: str = feature.GetField("zip")

    if int(zippy[-1]) % 2 == 0:
        return 'PEN(w:2px,c:#0000FF,id:"mapinfo-pen-1,ogr-pen-0");BRUSH(fc:#FFFF00,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-2")'
    else:
        return 'PEN(w:2px,c:#0000FF,id:"mapinfo-pen-1,ogr-pen-0");BRUSH(fc:#E8BEFF,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-2")'


def get_fire_style(feature: Feature) -> str:
    """Function that determines which style to use, based on the feature description"""
    riskdesc: str = feature.GetField("riskdesc")
    risktype: str = feature.GetField("risktype")
    description: str = " ".join([risktype, riskdesc])

    if description == "IF Smoke Risk":
        return 'PEN(w:2px,c:#0000FF,id:"mapinfo-pen-1,ogr-pen-0");BRUSH(fc:#FFFF00,bc:#FFFFFF,id:"mapinfo-brush-1,ogr-brush-0")'

    if description == "IF Low":
        return 'PEN(w:2px,c:#0000FF,id:"mapinfo-pen-1,ogr-pen-0");BRUSH(fc:#E8BEFF,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "IF Moderate":
        return 'PEN(w:2px,c:#0000FF,id:"mapinfo-pen-1,ogr-pen-0");BRUSH(fc:#C500FF,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "IF High":
        return 'PEN(w:2px,c:#0000FF,id:"mapinfo-pen-1,ogr-pen-0");BRUSH(fc:#4C0073,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "IM Low":
        return 'PEN(w:1px,c:#000000,id:"mapinfo-pen-2,ogr-pen-0");BRUSH(fc:#55FF00,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "IM Moderate":
        return 'PEN(w:1px,c:#000000,id:"mapinfo-pen-2,ogr-pen-0");BRUSH(fc:#FFFF00,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "IM High":
        return 'PEN(w:1px,c:#000000,id:"mapinfo-pen-2,ogr-pen-0");BRUSH(fc:#FFAA00,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "IM Very High":
        return 'PEN(w:1px,c:#000000,id:"mapinfo-pen-2,ogr-pen-0");BRUSH(fc:#E60000,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "WL Low":
        return 'PEN(w:1px,c:#FFFFFF,id:"mapinfo-pen-2,ogr-pen-0");BRUSH(fc:#55FF00,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "WL Moderate":
        return 'PEN(w:1px,c:#FFFFFF,id:"mapinfo-pen-2,ogr-pen-0");BRUSH(fc:#FFFF00,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "WL High":
        return 'PEN(w:1px,c:#FFFFFF,id:"mapinfo-pen-2,ogr-pen-0");BRUSH(fc:#FFAA00,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'

    if description == "WL Very High":
        return 'PEN(w:1px,c:#FFFFFF,id:"mapinfo-pen-2,ogr-pen-0");BRUSH(fc:#E60000,bc:#FFFFFF,id:"mapinfo-brush-2,ogr-brush-0")'
