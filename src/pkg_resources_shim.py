"""
Compatibility shim for legacy libraries (face_recognition_models, webrtcvad)
that still depend on pkg_resources after setuptools >= 81 removed it.
"""
try:
    import pkg_resources
except ImportError:
    import sys
    import types
    import importlib.resources as _res
    import importlib.metadata as _meta

    _pkg_resources = types.ModuleType("pkg_resources")

    def _resource_filename(package_or_requirement, resource_name):
        return str(_res.files(package_or_requirement) / resource_name)

    def _get_distribution(dist_name):
        try:
            ver = _meta.version(dist_name)
        except Exception:
            ver = "1.0.0"
        return types.SimpleNamespace(version=ver)

    _pkg_resources.resource_filename = _resource_filename
    _pkg_resources.get_distribution = _get_distribution

    sys.modules["pkg_resources"] = _pkg_resources
