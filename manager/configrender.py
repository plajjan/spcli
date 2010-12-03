#!/usr/bin/python
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
    import amara


xml_config = '''
<configuration>
<system>
	<domain-name>test</domain-name>
	<name-server>130.244.127.161</name-server>
	<name-server>130.244.127.169</name-server>
	<ntp>
		<server name="130.244.0.42"/>
		<server name="192.36.143.150"/>
	</ntp>
</system>
<interfaces>
	<interface name="lo0">
		<family name="inet">
			<address name="195.182.5.1/32"/>
			<address name="195.182.5.99/32"/>
		</family>
	</interface>
	<interface name="fe-0/0/0">
		<family name="inet">
			<address name="195.182.5.97/29"/>
		</family>
	</interface>
</interfaces>
<protocols>
	<bgp>
		<group>
			<name>IBGP</name>
		</group>
		<group>
			<name>EBGP</name>
		</group>
	</bgp>
</protocols>
</configuration>
'''
xml_config = '''
<configuration>
<system>
	<domain-name>test</domain-name>
	<name-server>130.244.127.161</name-server>
	<name-server>130.244.127.169</name-server>
	<ntp>
		<server name="130.244.0.42"/>
		<server name="192.36.143.150"/>
	</ntp>
</system>
<interfaces>
	<interface name="lo0">
		<family name="inet">
			<address name="195.182.5.1/32"/>
			<address name="195.182.5.99/32"/>
		</family>
	</interface>
	<interface name="fe-0/0/0">
		<family name="inet">
			<address name="195.182.5.97/29"/>
		</family>
	</interface>
</interfaces>
<protocols>
	<bgp>
		<group name="IBGP">
			<neighbor>1.3.3.7</neighbor>
			<neighbor>1.3.3.8</neighbor>
		</group>
		<group name="IBGP">
		</group>
	</bgp>
</protocols>
</configuration>
'''

app_name = 'ConfigRender'

env = Environment(loader=FileSystemLoader('.'))

t = env.get_template('resolv.conf.tpl')

var_nameservers = [ '195.182.5.3', '130.244.127.161' ]

doc = amara.parse(xml_config)

#for group in doc.configuration.protocols.bgp.group[0].neighbor:
#	print "hejsan", group

data = {	'app_name': app_name ,
			'config': doc,
			'var_system_domain': 'spritelink.net',
			'var_system_search_domain': [ 'tele2.net', 'tele2.se' ],
			'var_nameservers': var_nameservers }

print t.render(data)
