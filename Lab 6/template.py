	for key, group in groupby(list_of_dicts,itemgetter('Surname')):
		print key
		for record in group:
			print record



v = {}

 for key, value in sorted(d.iteritems()):
   v.setdefault(value, []).append(key)