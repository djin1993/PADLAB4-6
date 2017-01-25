from  collections import OrderedDict
from itertools import  groupby
from collections import Counter
import requests
from  operator import  itemgetter
from lxml import etree
from StringIO import *
from xml.dom.minidom import parseString
import xmltodict
from dicttoxml import dicttoxml

proxy_add = 'http://127.0.0.8'
xml_schema_add = 'Schema.xsd'

ronnie = '''    {
		"Department": "HR",
		"Name": "Ronnie",
		"Salary": 7500,
		"Surname": "O'Sullivan"
	}'''

marko = '''    {
		"Department": "Production",
		"Name": "Marko",
		"Salary": 3500,
		"Surname": "Fu"
	}'''

john = '''    {
		"Department": "Production",
		"Name": "John",
		"Salary": 5500,
		"Surname": "Higgins"
	}'''

asis = '''    {
		"Department": "P",
		"Name": "J",
		"Salary": 50,
		"Surname": "H",
		"id": 100
	}'''

xml = '''<?xml version="1.0" encoding="UTF-8" ?>
<root>
<item>
<Department>Aperture</Department>
<Salary>3000</Salary>
<Surname>Smith</Surname>
<Name>John</Name>
</item>
</root>'''

def validate(xml_doc, xml_schema):
	f = StringIO(xml_schema)
	xmlschema_doc = etree.parse(f)
	xmlschema = etree.XMLSchema(xmlschema_doc)

	valid = StringIO(xml_doc)
	doc = etree.parse(valid)
	return xmlschema.validate(doc)

def get(add):
	print 'GET ', add
	r = requests.get(add)
	dom = parseString(r.text)
	xml_doc = dom.toprettyxml()

	print xml_doc
	if validate(xml_doc, xml_schema):
		print "XML is valid"
	else:
		print "XML is invalid"

def get_all():
	add = proxy_add + '/worker/'
	get(add)

def get_one(id):
	add = proxy_add + '/worker/' + str(id) + '/'
	get(add)

def put_one(da):
	add = proxy_add + '/worker/'
	print 'PUT ', add
	print da
	r = requests.put( add, data = da )
	print 'id = ', r.text

def head_one(id):
	add = proxy_add + '/worker/' + str(id) + '/'
	print 'HEAD ', add
	r = requests.head( add )
	print r
	print r.headers


def test_xml(add):
	add = 'http://' + add

	print "Good"
	r = requests.get(add + '/worker/')
	print r
	print r.text

	r = requests.get(add + '/worker/10001/')
	print r
	print r.text

	r = requests.put(add + '/worker/', data = xml)
	print r
	print r.text

	# r = requests.put(add + '/worker/asis/', data = asis)
	# print r
	# print r.text	

	r = requests.head(add + '/worker/10001/')
	print r
	print r.headers


	print "Bad"
	r = requests.get(add + '/worker/1/')
	print r
	print r.text

	r = requests.head(add + '/worker/10/')
	print r
	print r.headers


	print "Wrong"
	r = requests.get(add + '/worer/')
	print r
	print r.text
	r = requests.get(add + '/worker')
	print r
	print r.text

	r = requests.get(add + '/worker/10001')
	print r
	print r.text
	r = requests.get(add + '/worer/10001/')
	print r
	print r.text

	r = requests.put(add + '/worer/', data = xml)
	print r
	print r.text
	r = requests.put(add + '/worker', data = xml)
	print r
	print r.text

	r = requests.head(add + '/worker/10001')
	print r
	print r.headers
	r = requests.head(add + '/worer/10001/')
	print r
	print r.headers

def test_json(add):
	add = 'http://' + add

	print "Good"
	r = requests.get(add + '/worker/')
	print r
	print r.text

	r = requests.get(add + '/worker/10001/')
	print r
	print r.text

	r = requests.put(add + '/worker/', data = john)
	print r
	print r.text

	# r = requests.put(add + '/worker/asis/', data = asis)
	# print r
	# print r.text	

	r = requests.head(add + '/worker/10001/')
	print r
	print r.headers


	print "Bad"
	r = requests.get(add + '/worker/1/')
	print r
	print r.text

	r = requests.head(add + '/worker/10/')
	print r
	print r.headers


	print "Wrong"
	r = requests.get(add + '/worer/')
	print r
	print r.text
	r = requests.get(add + '/worker')
	print r
	print r.text

	r = requests.get(add + '/worker/10001')
	print r
	print r.text
	r = requests.get(add + '/worer/10001/')
	print r
	print r.text

	r = requests.put(add + '/worer/', data = john)
	print r
	print r.text
	r = requests.put(add + '/worker', data = john)
	print r
	print r.text

	r = requests.head(add + '/worker/10001')
	print r
	print r.headers
	r = requests.head(add + '/worer/10001/')
	print r
	print r.headers

def filter_file (xmldoc,filter_parameter,parameteter_value):
	list_for_sorting =[]
	content_dict = xmltodict.parse(xmldoc)
	for i in content_dict["root"]["item"]:
		print i
		if filter_parameter=="Name" and i["Name"]==parameteter_value:
			list_for_sorting.append(i)
		elif filter_parameter =="Salary" and i["Salary"]==parameteter_value:
			list_for_sorting.append(i)
		elif filter_parameter== "Department"and i["Department"]==parameteter_value:
			list_for_sorting.append(i)
		elif filter_parameter=="Surname" and i["Surmame"]==parameteter_value:
			list_for_sorting.append(i)
		elif filter_parameter == "id"and i["id"]==parameteter_value:
			list_for_sorting.append(i)
	print list_for_sorting

def group_file(xmldoc):
	list_for_group =[]
	list_of_dicts =[]
	final_list=[]
	content_dict = xmltodict.parse(xmldoc)
	for i in content_dict["root"]["item"]:
		list_of_dicts.append(i)
	for key, group in groupby(list_of_dicts,itemgetter('Name')):
		list_for_group.append(key)
	cnt=Counter(list_for_group)
	grouped_dict=dict(cnt)
	for key, group in groupby(list_of_dicts,itemgetter('Name')):
		for record in group:
			if key==record["Name"]:
				final_list.append('item {} number "{}"'.format(record,grouped_dict[key]))
	    		final_set=set(final_list)
	print final_set
def sort_file(xmldoc,sorting_criteria):
	sorted_list =[]
	list_of_dicts =[]
	content_dict = xmltodict.parse(xmldoc)
	for i in content_dict["root"]["item"]:
		print i
		list_of_dicts.append(i)
	#newlist = sorted(list_for_sorting, key=lambda k: k['Name'])
	#print newlist
	if sorting_criteria=="Name":
		newlist = sorted(list_of_dicts, key=lambda k: k['Name'])
		print newlist
		sorted_list=newlist
	elif sorting_criteria =="Salary":
		newlist = sorted(list_of_dicts, key=lambda k: k['Salary'])
		print newlist
		sorted_list=newlist
	elif sorting_criteria== "Department":
		newlist = sorted(list_of_dicts, key=lambda k: k['Department'])
		print newlist
		sorted_list=newlist
	elif sorting_criteria=="Surname":
		newlist = sorted(list_of_dicts, key=lambda k: k['Surname'])
		print newlist
	elif sorting_criteria=="id":
		newlist = sorted(list_of_dicts, key=lambda k: k['id'])
		sorted_list=newlist
	print sorted_list


def get_dic_list():
	add = proxy_add + '/worker/'
	print 'GET ', add
	r = requests.get(add)
	dom = parseString(r.text)
	xml_doc = dom.toprettyxml()
	return xml_doc

if __name__ == '__main__':

	with open(xml_schema_add, 'r') as f:
		xml_schema = f.read()

	#get_all()

	#get_one('10004')

	#put_one(xml)

	#head_one('10002')
	xml_document= get_dic_list()
	#print  xml_document
	#filter_file(xml_document,"Name","John")
	#sort_file(xml_document,"Salary")

	group_file(xml_document)
