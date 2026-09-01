"""CartoSym coverage symbolizer fields -> MapLibre raster-ish layers.

MapLibre has no general equivalent to an OGC ``RasterSymbolizer`` — its
``raster``/``hillshade``/``color-relief`` layer types draw from an
already-rendered image (or, for ``hillshade``/``color-relief``, a
``raster-dem`` elevation encoding); none of them select source bands,
evaluate a formula over bands, or apply a colour/opacity ramp keyed on an
arbitrary computed value. Two narrow, spec-grounded exceptions exist and
are mapped here:

- ``singleChannel`` (a *plain* field reference, e.g. ``elevation``) +
  ``colorMap`` -> a ``color-relief`` layer (MapLibre >= 5.6), whose
  ``color-relief-color`` is an ``["interpolate", ["linear"], ["elevation"],
  …]`` ramp built straight from the ``colorMap`` stops.
- ``hillShading.sun.azimuth``/``.elevation`` -> a ``hillshade`` layer's
  ``hillshade-illumination-direction``/``-altitude`` (the sun-elevation
  convention — 0 at the horizon, 90 at zenith — matches
  ``hillshade-illumination-altitude`` directly, no inversion needed).

Both target a synthetic ``raster-dem`` source (:data:`DEM_SOURCE`) — same
idiom as the writer's synthetic vector ``cartosym`` source: this codec has
no data-source concept of its own, so a placeholder ``tiles`` URL is
declared, just enough to satisfy the style specification.

Everything else here is an honest gap, raised rather than approximated:

- ``colorChannels`` / ``alphaChannel`` (band selection / per-band alpha):
  no MapLibre layer selects or recombines source bands.
- ``singleChannel`` as a computed expression (band arithmetic, e.g. NDVI's
  ``(B08-B04)/(B08+B04)``): same reason — no band math in MapLibre.
- ``opacityMap`` (top-level or nested in ``hillShading``): no MapLibre
  layer applies an opacity ramp keyed on a channel/intensity value.
- ``hillShading.factor``: MapLibre's ``hillshade-exaggeration`` is a fixed
  0-1 shading *intensity*, not the unbounded vertical-exaggeration
  z-factor CartoSym's ``factor`` is (the same concept as SLD/SE's
  ``ReliefFactor`` — GeoServer's own worked examples use values like 55,
  matching this project's own ``examples/8-coverage-hillshading.cscss``
  ``factor: 56``). No faithful unit conversion exists between the two, so
  it is rejected rather than guessed at.
- ``hillShading.colorMap`` / ``.opacityMap`` (a ramp keyed on shading
  *intensity*, not elevation): ``hillshade`` paint only exposes 3 fixed
  colours (shadow/highlight/accent), not a ramp.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

DEM_SOURCE = "cartosym-dem"

# A placeholder tiles URL — this codec has no real data-source concept
# (see the writer's synthetic `cartosym` GeoJSON source), and unlike that
# source, a raster-dem source has no "empty literal" shape to fall back to.
_DEM_TILES_URL = "cartosym://raster-dem/{z}/{x}/{y}"

Literal = Callable[[Any, str], Any]


def _channel_property_name(channel: Any, ctx: str) -> str:
    """Return the field name of a plain ``singleChannel``/``colorChannels`` reference.

    Only a bare ``{"property": name}`` maps to MapLibre's ``["elevation"]``
    — a computed band expression has no MapLibre equivalent (see the
    module docstring).
    """
    if (
        isinstance(channel, dict)
        and set(channel) == {"property"}
        and isinstance(channel["property"], str)
    ):
        return channel["property"]
    raise NotImplementedError(
        f"{ctx}: only a plain field reference maps to MapLibre "
        '["elevation"] in this codec — a computed band expression (e.g. '
        "NDVI) has no MapLibre equivalent"
    )


def _color_map_stops(color_map: Any, literal: Literal) -> list[Any]:
    """Flatten a CartoSym ``colorMap`` into flat interpolate stops."""
    if not isinstance(color_map, list) or not color_map:
        raise NotImplementedError(f"colorMap {color_map!r} is not a supported shape")
    stops: list[Any] = []
    for entry in color_map:
        if not (isinstance(entry, (list, tuple)) and len(entry) == 2):
            raise NotImplementedError(
                f"colorMap entry {entry!r} is not a supported shape"
            )
        value, color = entry
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise NotImplementedError(
                f"colorMap entry value {value!r} must be a plain number"
            )
        stops.append(value)
        stops.append(literal(color, "colorMap entry color"))
    return stops


def color_relief_layer(
    layer_id: str, single_channel: Any, color_map: Any, literal: Literal
) -> dict[str, Any]:
    """Turn a ``singleChannel`` + ``colorMap`` pair into a ``color-relief`` layer."""
    _channel_property_name(single_channel, "singleChannel")
    stops = _color_map_stops(color_map, literal)
    return {
        "id": layer_id,
        "type": "color-relief",
        "source": DEM_SOURCE,
        "paint": {
            "color-relief-color": ["interpolate", ["linear"], ["elevation"], *stops]
        },
    }


def hillshade_layer(
    layer_id: str, hill_shading: Any, literal: Literal
) -> dict[str, Any]:
    """``hillShading.sun`` as a ``hillshade`` layer.

    See the module docstring for why ``factor``/``colorMap``/``opacityMap``
    are rejected rather than approximated.
    """
    if not isinstance(hill_shading, dict):
        raise NotImplementedError(
            f"hillShading {hill_shading!r} is not a supported shape"
        )
    if hill_shading.get("factor") is not None:
        raise NotImplementedError(
            "hillShading.factor has no MapLibre mapping in this codec — "
            "hillshade-exaggeration is a fixed 0-1 shading intensity, not "
            "the unbounded vertical-exaggeration z-factor CartoSym's "
            "factor is (see the module docstring)"
        )
    if hill_shading.get("colorMap") is not None or hill_shading.get("opacityMap"):
        raise NotImplementedError(
            "hillShading.colorMap/opacityMap has no MapLibre mapping in "
            "this codec — hillshade paint only exposes 3 fixed colours "
            "(shadow/highlight/accent), not a ramp"
        )
    sun = hill_shading.get("sun")
    paint: dict[str, Any] = {}
    if isinstance(sun, dict):
        azimuth = sun.get("azimuth")
        elevation = sun.get("elevation")
        if azimuth is not None:
            paint["hillshade-illumination-direction"] = literal(
                azimuth, "hillShading.sun.azimuth"
            )
        if elevation is not None:
            paint["hillshade-illumination-altitude"] = literal(
                elevation, "hillShading.sun.elevation"
            )
    if not paint:
        raise NotImplementedError(
            "hillShading with no sun.azimuth/sun.elevation has no MapLibre "
            "mapping in this codec"
        )
    return {"id": layer_id, "type": "hillshade", "source": DEM_SOURCE, "paint": paint}


def dem_source() -> dict[str, Any]:
    """Return the synthetic ``raster-dem`` source every raster layer here references."""
    return {"type": "raster-dem", "tiles": [_DEM_TILES_URL]}
