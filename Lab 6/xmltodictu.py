import json
import xmltodict
from dicttoxml import dicttoxml


# xml = '''<?xml version="1.0" encoding="UTF-8" ?><root>
# <item><Department>Marketing</Department><Salary>3000</Salary><Surname>Smith</Surname><Name>John</Name><id>10001</id></item>
# </root>'''
# namespaces = {}

# b = xmltodict.parse(xml, process_namespaces=True, namespaces=namespaces)
# print json.dumps(b['root']['item'],sort_keys=True, indent=4, separators=(',', ': '))


xml = '''<?xml version="1.0" encoding="UTF-8" ?>
<root>
<item>
<Department>Aperture</Department>
<Salary>3000</Salary>
<Surname>Smith</Surname>
<Name>John</Name>
</item>
</root>'''
print xml

b = xmltodict.parse(xml)
print b['root']['item']['Name']
b['root']['item']['id'] = "10"
xml2 = dicttoxml(b['root'], attr_type=False)

print xml2
