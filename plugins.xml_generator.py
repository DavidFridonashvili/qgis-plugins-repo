import os
import xml.etree.ElementTree as ET
from datetime import datetime

PLUGIN_DIR = "."

def create_plugins_xml():
    root = ET.Element("plugins")

    for plugin_name in os.listdir(PLUGIN_DIR):
        plugin_path = os.path.join(PLUGIN_DIR, plugin_name)
        if not os.path.isdir(plugin_path):
            continue

        metadata_path = os.path.join(plugin_path, "metadata.txt")
        zip_path = os.path.join(plugin_path, f"{plugin_name}.zip")
        icon_path = os.path.join(plugin_path, "icon.png")

        if not os.path.exists(metadata_path) or not os.path.exists(zip_path):
            print(f"Skipping {plugin_name}: missing metadata or zip.")
            continue

        metadata = {}
        with open(metadata_path, encoding='utf-8') as f:
            for line in f:
                if '=' in line:
                    key, val = line.strip().split('=', 1)
                    metadata[key.strip()] = val.strip()

        plugin_elem = ET.SubElement(root, "pyqgis_plugin", name=plugin_name, version=metadata.get("version", "1.0.0"))
        for tag in ["description", "about", "version", "homepage", "author_name", "tracker", "changelog", "experimental"]:
            if tag in metadata:
                ET.SubElement(plugin_elem, tag).text = metadata[tag]

        ET.SubElement(plugin_elem, "download_url").text = f"{plugin_name}/{plugin_name}.zip"
        ET.SubElement(plugin_elem, "file_name").text = f"{plugin_name}.zip"
        ET.SubElement(plugin_elem, "icon").text = f"{plugin_name}/icon.png" if os.path.exists(icon_path) else ""
        ET.SubElement(plugin_elem, "qgis_minimum_version").text = metadata.get("qgis_minimum_version", "3.10")
        ET.SubElement(plugin_elem, "qgis_maximum_version").text = metadata.get("qgis_maximum_version", "3.99")
        ET.SubElement(plugin_elem, "created_date").text = datetime.now().strftime("%Y-%m-%d")

    tree = ET.ElementTree(root)
    tree.write("plugins.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    create_plugins_xml()
    print("✅ plugins.xml generated.")
