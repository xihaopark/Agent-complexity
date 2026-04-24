from __future__ import annotations

import xml.etree.ElementTree as ET


def local_name(tag: str) -> str:
    """Return local name of an XML tag (drop namespace)."""

    return tag.split("}")[-1] if "}" in tag else tag


def findall_local(elem: ET.Element, name: str) -> list[ET.Element]:
    """Find all descendants by local tag name (namespace-agnostic)."""

    return [e for e in elem.iter() if local_name(e.tag) == name]
