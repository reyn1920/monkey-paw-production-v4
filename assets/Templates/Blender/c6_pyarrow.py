""" support pyarrow compatibility across versions """

from __future__ import annotations

from pandas.util.version import Version

try:
    import pyarrow as pa

    _palv = Version(Version(pa.__version__).base_version)
    pa_version_under10p1 = _palv < Version("1001")
    pa_version_under11p0 = _palv < Version("1100")
    pa_version_under12p0 = _palv < Version("1200")
    pa_version_under13p0 = _palv < Version("1300")
    pa_version_under14p0 = _palv < Version("1400")
    pa_version_under14p1 = _palv < Version("1401")
    pa_version_under15p0 = _palv < Version("1500")
    pa_version_under16p0 = _palv < Version("1600")
    pa_version_under17p0 = _palv < Version("1700")
    pa_version_under18p0 = _palv < Version("1800")
    pa_version_under19p0 = _palv < Version("1900")
    pa_version_under20p0 = _palv < Version("2000")
    pa_version_under21p0 = _palv < Version("2100")
    HAS_PYARROW = True
except ImportError:
    pa_version_under10p1 = True
    pa_version_under11p0 = True
    pa_version_under12p0 = True
    pa_version_under13p0 = True
    pa_version_under14p0 = True
    pa_version_under14p1 = True
    pa_version_under15p0 = True
    pa_version_under16p0 = True
    pa_version_under17p0 = True
    pa_version_under18p0 = True
    pa_version_under19p0 = True
    pa_version_under20p0 = True
    pa_version_under21p0 = True
    HAS_PYARROW = False