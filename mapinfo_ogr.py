"""build one or more indexes on your ogr-compatible spatial dataset -- optionally apply styling"""
import sys
from pathlib import Path
from typing import Tuple, Callable, Optional
from dataclasses import dataclass

from osgeo import ogr
from osgeo import gdal
from osgeo.ogr import (
    Layer, DataSource, Feature,
    FeatureDefn
)

from style_functions import get_zip_style


@dataclass(frozen=True)
class IO:
    """Represents the inputs and outputs of this script"""
    datasource: Path
    output: Path
    out_encoding: str


def check_gdal_version() -> None:
    """We need a minimum version of GDAL - so raise an exception if version not met"""
    version_num: int = int(gdal.VersionInfo('VERSION_NUM'))
    if version_num < 2400000:
        raise EnvironmentError("GDAL Version < 2.4.0 required to build an index")


def create_indexes(in_name: str, out_dataset: DataSource, cols: Tuple[str, ...]) -> None:
    """Create index on each column requested"""
    for column in cols:
        out_dataset.ExecuteSQL(f"CREATE INDEX ON {in_name} USING {column}")


def export(in_layer: Layer, out_layer: Layer, styler: Optional[Callable[[Feature], str]] = None) -> None:
    """Generate the output dataset from the input -- the difference being the style of the features"""
    for in_feature in in_layer:
        out_feature: Feature = ogr.Feature(out_layer.GetLayerDefn())
        out_feature.SetFrom(in_feature)

        if styler is not None:
            style: str = styler(in_feature)
            out_feature.SetStyleString(style)

        out_layer.CreateFeature(out_feature)
        in_feature.Destroy()
        out_feature.Destroy()


def create_fields(out_layer: Layer, in_def: FeatureDefn) -> None:
    """Generate the output dataset fields, using all the input fields"""
    for i in range(0, in_def.GetFieldCount()):
        out_layer.CreateField(in_def.GetFieldDefn(i))


def build_output(io: IO, cols: Tuple[str, ...], styler: Optional[Callable[[Feature], str]] = None) -> int:
    """rebuild the input data with indexed columns and / or styling"""
    in_dataset: DataSource = ogr.Open(str(io.datasource))
    in_layer: Layer = in_dataset.GetLayer()
    in_def: FeatureDefn = in_layer.GetLayerDefn()
    in_name: str = io.output.stem
    out_dataset: DataSource = in_dataset.GetDriver().CreateDataSource(str(io.output))

    out_layer: Layer = out_dataset.CreateLayer(
        in_name,
        srs=in_layer.GetSpatialRef(),
        geom_type=in_layer.GetLayerDefn().GetGeomType(),
        options=[io.out_encoding]
    )

    create_fields(out_layer, in_def)
    create_indexes(in_name, out_dataset, cols)
    export(in_layer, out_layer, styler)

    out_layer.SyncToDisk()
    out_dataset.Destroy()
    in_dataset.Destroy()

    return 0


def main() -> None:
    """Application Entry-point"""
    arg_len: int = len(sys.argv)
    io: IO = IO(datasource=Path(sys.argv[1]), output=Path(sys.argv[2]), out_encoding="ENCODING=ISO-8859-1")
    index_cols: Tuple[str, ...] = tuple(sys.argv[3].split(",")) if arg_len == 4 and sys.argv[3] else tuple()

    check_gdal_version()
    build_output(io, index_cols, styler=get_zip_style)


if __name__ == "__main__":
    main()
