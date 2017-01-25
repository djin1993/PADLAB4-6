from xml.etree.ElementTree import ElementTree

tree = ElementTree()

# Test input
tree.parse("sample.xml")

# List containing names you want to keep
inputID = ['name1', 'name2', 'name3']

for node in tree.findall('.//data'):
    # Remove node if the name attribute value is not in inputID
    if not node.attrib.get('name') in inputID:
        tree.getroot().remove(node)

# Do what you want with the modified xml
tree.write('sample_out.xml')