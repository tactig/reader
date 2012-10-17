#! /usr/bin/python

import getopt,sys,os

def panic():
	print 'Please input proper arguments.';
	sys.exit(-1);

def selector_info(selector):
	print 'Selector info:'
	print '\tRPL:',selector&0x3;
	ti = 'GDT';
	if bool(selector&0x4):
		ti = 'LDT';
	print '\tTI:',ti;
	print 'Selected entry of',ti,":",hex((selector&0xFFF8)>>3);

def printi(name,value,tp):
	print '%(name)-15s: %(val)-20s' % {"name":name,"val":value};

def match_des(v):
	#fields
	field={	"Granularity":23+32,\
		"DB":22+32, "Long":21+32,\
		"AVL":20+32,\
		"Present":15+32,\
		"DPL":13+32,\
		"System":12+32,\
		"Type":8+32};

	base_address=(v>>32)&0xFF000000 + (v>>16)&0xFF0000 + (v>>16)&0xFFFF;
	limit = ((v>>16)&0xFF0000) + (v&0xFFFF);


	field_value=dict();
	for f in field.keys():
		field_value[f]=(v>>field[f])&0x1;

	field_value["DPL"]=(v>>field["DPL"])&0x3;
	field_value["Type"]=(v>>field["Type"])&0xF;
		
	field_type={	"Granularity":{0x0:"Byte unit",0x1:"4-KByte unit"},\
			"DB":{0x0:"0x0",0x1:"0x1"},\
			"Long":{0x0:"0x0",0x1:"0x1"},\
			"AVL":{0x0:"0x0",0x1:"0x1"},\
			"Present":{0x0:"No",0x1:"Yes"},\
			"DPL":{0x0:"0",0x1:"1",0x2:"2",0x3:"3"},\
			"System":{0x0:"System seg.",0x1:"Non-system seg."},\
			"Type":None};

	type_nonsys={	0:  'Data, Read-Only, Expand-Up', \
			1:  'Data, Read-Only, Expand-Up, Accessed',\
			2:  'Data, Read/Write, Expand-Up', \
			3:  'Data, Read/Write, Expand-Up, Accessed', \
			4:  'Data, Read-Only, Expand-Up', \
			5:  'Data, Read-Only, Expand-Up, Accessed', \
			6:  'Data, Read/Write, Expand-Up', \
			7:  'Data, Read/Write, Expand-Up, Accessed', \
			8:  'Code, Execute-Only, Nonconforming ', \
			9:  'Code, Execute-Only, Nonconforming, Accessed', \
			10: 'Code, Execute/Read, Nonconforming ', \
			11: 'Code, Execute/Read, Nonconforming, Accessed', \
			12: 'Code, Execute-Only, Conforming', \
			13: 'Code, Execute-Only, Conforming, Accessed',\
			14: 'Code, Execute/Read, Conforming',\
			15: 'Code, Execute/Read, Conforming, Accessed'};

	type_sys={	0:  'System Segment, Reserved',\
			1:  'System Segment, 16-bit TSS (Available) ',\
			2:  'System Segment, LDT',\
			3:  'System Segment, 16-bit TSS (Busy) ',\
			4:  'System Segment, 16-bit Call Gate ',\
			5:  'System Segment, Task Gate',\
			6:  'System Segment, 16-bit Interrupt Gate ',\
			7:  'System Segment, 16-bit Trap Gate ',\
			8:  'System Segment, Reserved',\
			9:  'System Segment, 32-bit TSS (Available) ',\
			10: 'System Segment, Reserved',\
			11: 'System Segment, 32-bit TSS (Busy) ',\
			12: 'System Segment, 32-bit Call Gate ',\
			13: 'System Segment, Reserved',\
			14: 'System Segment, 32-bit Interrupt Gate ',\
			15: 'System Segment, 32-bit Trap Gate '};

#*****************************************Print infomation***********************************************************
	for t in field_value.keys()[:-2]:
		value=field_value[t];
		print '%(name)-15s: %(val)-20s' % {"name":t,"val":str(field_type[t][value])};
	
	if field_value["System"]:
		print '%(name)-15s: %(val)-20s' % {"name":"Infomation","val":type_nonsys[field_value["Type"]]};
	else:
		print '%(name)-15s: %(val)-20s' % {"name":"Infomation","val":type_sys[field_value["Type"]]};
		
	print '%(name)-15s: 0x%(#)X' % {"name":"Base Address","#":base_address};
	print '%(name)-15s: 0x%(val)X' % {"name":"Segment Limit","val":limit};
	if field_value["Granularity"]:
		print '%(name)-15s: 0x%(val)X' % {"name":"Segment Size","val":(limit+1)*4096};
	else:
		print '%(name)-15s: 0x%(val)X' % {"name":"Segment Size","val":limit+1};

def type_test(v,o=None):
	if bool(v) and  bool(o):
		panic();

	elif bool(v) and not bool(o):
		try:
			v = int(v[0],16);
		except ValueError:
			panic();

		if not  v.bit_length() <= 64:
			panic();
		match_des(v);
	elif not bool(v) and bool(o):
		if not bool(o):
			panic();
		#for x in o:					#I can't fix this;
		elif o[0][0] == '-s':
			try:
				selector=int(o[0][1],16);
			except ValueError:
				panic();

			selector_info(selector);
		#elif o[0][0] == '-p':
			
		else:
			panic();
	
			

def main(argv):
	if not len(argv):
		panic();

	try:
		opts, args = getopt.getopt(argv[1:],"s:p");
	except getopt.GetoptError:
		panic();
	
	#for o, a in opts, hanle later


	type_test(args,opts);

if __name__ == "__main__":
	main(sys.argv);
