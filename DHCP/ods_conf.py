#!/usr/bin/python3
#pip3 install pyexcel
#pip3 install pyexcel.ods --user
import re
import pyexcel as p
from datetime import datetime
import os

__author__="CABOS Matthieu"
__date__=14_09_2021

############################################################
# This script must be used in case of DHCP server :        #
#                                                          #
# Please tu use following instructions below :             #
#   * Usage : python ods_conf.py  in your dhcp repertory   #
#   * Update : This script update DHCP conf to allocate    #
# new ip only for newer users without updating others ip   #
#   * Warning : This script must be used carefully, any    #
# changes will not allow backup                            #
############################################################ 

vlans={
    'ICGM-DPT1-CMM':
    {
        "id":510,
        "gateway":"10.14.21.1",
        "nat":"193.50.7.131",
        "subnet":"10.14.21.0",
        "netmask":"255.255.255.0",
        "subdomain":"d1.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    },
    'ICGM-DPT2-CMMM':
    {
        "id":511,
        "gateway":"10.14.20.1",
        "nat":"193.50.7.132",
        "subnet":"10.14.20.0",
        "netmask":"255.255.255.0",
        "subdomain":"d2.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    },
    'ICGM-DPT3-MPH':
    {
        "id":512,
        "gateway":"10.14.19.1",
        "nat":"193.50.7.133",
        "subnet":"10.14.19.0",
        "netmask":"255.255.255.0",
        "subdomain":"d3.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    },
    'ICGM-DPT4-CMNME':
    {
        "id":513,
        "gateway":"10.14.18.1",
        "nat":"193.50.7.134",
        "netmask":"255.255.255.0",
        "subnet":"10.14.18.0",
        "subdomain":"d4.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    },
    'ICGM-DPT5-CPTM':
    {
        "id":514,
        "gateway":"10.14.17.1",
        "nat":"193.50.7.135",
        "subnet":"10.14.17.0",
        "netmask":"255.255.255.0",
        "subdomain":"d5.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    },
    'ICGM-SGAF':
    {
        "id":524,
        "gateway":"10.14.22.1",
        "nat":"193.50.7.145",
        "netmask":"255.255.255.0",
        "subnet":"10.14.22.0",
        "subdomain":"sgaf.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    },

    'ICGM-INSTRU-ON':
    {
        "id":515,
        "gateway":"10.14.16.1",
        "nat":"193.50.7.136",
        "netmask":"255.255.255.0",
        "subnet":"10.14.16.0",
        "subdomain":"instru.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    },
    'ICGM-SSI':
    {
        "id":525,
        "gateway":"10.14.23.1",
        "nat":"193.50.7.136",
        "netmask":"255.255.255.0",
        "subnet":"10.14.23.0",
        "subdomain":"ssi.icgm.fr",
        "init":200,
        "content":"",
        "dns":""";
vm-nas             IN      A       10.14.23.2
openmanage         IN      A       10.14.23.5
icgm-vpn           IN      A       10.14.23.9
proxmox1-adm-int   IN      A       10.14.23.11
proxmox2-adm-int   IN      A       10.14.23.12
proxmox3-adm-int   IN      A       10.14.23.13
nas1-adm-int       IN      A       10.14.23.14
nas2-adm-int       IN      A       10.14.23.15
graylog            IN      A       10.14.23.21
netw-ssh           IN      A       10.14.23.22
""",
        "rev":""";
2       IN      PTR     vm-nas.ssi.icgm.fr.
5       IN      PTR     openmanage.ssi.icgm.fr.
9       IN      PTR     icgm-vpn.ssi.icgm.fr.
11      IN      PTR     proxmox1-adm-int.ssi.icgm.fr.
12      IN      PTR     proxmox2-adm-int.ssi.icgm.fr.
13      IN      PTR     proxmox3-adm-int.ssi.icgm.fr.
14      IN      PTR     nas1-adm-int.ssi.icgm.fr.
15      IN      PTR     nas1-adm-int.ssi.icgm.fr.
21      IN      PTR     graylog.ssi.icgm.fr.
22      IN      PTR     netw-ssh.ssi.icgm.fr.
"""
    },
    'ICGM-INSTRU-OFF':
    {
        "id":516,
        "gateway":"10.14.15.1",
        "nat":"",
        "netmask":"255.255.255.0",
        "subnet":"10.14.15.0",
        "subdomain":"instruOff.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    },
    'ICGM-IMPRIM':
    {
        "id":518,
        "gateway":"10.14.13.1",
        "subnet":"10.14.13.0",
        "nat":"",
        "netmask":"255.255.255.0",
        "init":2,
        "subdomain":"print.icgm.fr",
        "content":"",
        "dns":"",
        "rev":""
    },
    'ICGM-IDRAC-CIN':
    {
        "id":528,
        "gateway":"10.14.26.1",
        "subnet":"10.14.26.0",
        "nat":"",
        "netmask":"255.255.254.0",
        "init":2,
        "subdomain":"idrac-cin.icgm.fr",
        "content":"",
        "dns":"",
        "rev":""

    },
       'ICGM-IDRAC':
    {
        "id":501,
        "gateway":"10.14.1.1",
        "subnet":"10.14.1.0",
        "nat":"",
        "netmask":"255.255.255.0",
        "init":11,
        "subdomain":"idrac.icgm.fr",
        "content":"",
        "dns":"",
        "rev":""

    },
    'ICGM-PT':
    {
        "id":530,
        "gateway":"10.14.29.1",
        "nat":"193.50.7.173",
        "netmask":"255.255.255.0",
        "subnet":"10.14.29.0",
        "subdomain":"pt.icgm.fr",
        "init":2,
        "content":"",
        "dns":"",
        "rev":""
    }
}

Conf_list=[
'dhcpd-501.conf',
'dhcpd-510.conf',
'dhcpd-511.conf',
'dhcpd-512.conf',
'dhcpd-513.conf',
'dhcpd-514.conf',
'dhcpd-515.conf',
'dhcpd-516.conf',
'dhcpd-518.conf',
'dhcpd-524.conf',
'dhcpd-525.conf',
'dhcpd-528.conf',
'dhcpd-530.conf'
]

def switch(x,*arg):
	dic ={}
	for i in range(int(len(arg)-1)):
		dic[arg[i]]=arg[i+1]
	return dic.get(x,'default')

def find_first_avaible_ip(dpt):
	tmp=0
	cnt=0
	rez=''
	for item in (list(Old_Address_list[dpt].items())[-1][1]):
		if item!='.':
			tmp*=10 
			tmp+=int(item)
		else:
			cnt+=1
			if(cnt<4):
				rez=rez+str(tmp)+'.'
				tmp=0
			else:
				rez=rez+str(tmp+1)
	rez=rez+str(tmp+1)
	return rez

def ip_data_getter():
    Old_Address_list=[]
    ip_mac_dict={}
    for conf in Conf_list:
    	ip_mac_dict={}
    	ip_mac_dict['Departement : ']=switch(conf,
            'dhcpd-501.conf','ICGM-IDRAC',
    		'dhcpd-510.conf','DPT1',
    		'dhcpd-511.conf','DPT2',
    		'dhcpd-512.conf','DPT3',
    		'dhcpd-513.conf','DPT4',
    		'dhcpd-514.conf','DPT5',
    		'dhcpd-515.conf','INSTRU-ON',
    		'dhcpd-516.conf','INSTRU-OFF',
    		'dhcpd-518.conf','IMPRIM',
    		'dhcpd-524.conf','SGAF',
    		'dhcpd-525.conf','SSI',
    		'dhcpd-528.conf','IDRAC',
            'dhcpd-530.conf','ICGM-PT')
    	nb_addr=int(os.popen('(cat '+str(conf)+' | grep \'hardware\' && cat '+str(conf)+ ' | grep \'fixed-address\') | wc -l').read())
    	stre=os.popen('cat '+str(conf)+' | grep \'hardware\' | cut -d " " -f7 | tr ";" " " && cat '+str(conf)+ ' | grep \'fixed-address\' | cut -d " " -f6 | tr ";" " "')
    	stream=stre.readlines()
    	for i in range(0,int(nb_addr/2)):
    		ip_mac_dict[stream[i].rstrip(' \n')]=stream[i+int((nb_addr/2))].rstrip(' \n')
    	Old_Address_list.append(ip_mac_dict)
    return Old_Address_list

    New_Address_list=[]
    dpt_mac_dict={}
    records = p.iget_records(file_name="./Ordinateurs.ods")
    for record in records:
    	dpt_mac_dict[record['Adresse Mac']]=record['Sous-réseau'].replace('ICGM-','').replace('-CMM','').replace('-CPTL','').replace('-CIN','').replace('-CPTM','').replace('-CMMM','').replace('-MPH','').replace('CMNME','')
    return Old_Address_list

Old_Address_list=ip_data_getter()
first_ip=''

##############
# Ods 2 dhcp #
##############

records = p.iget_records(file_name="./Ordinateurs.ods")
f1 = open("dhcpd.conf", "w")
f1.write("""
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
ignore client-updates;
default-lease-time 86400;
max-lease-time 86400;

option domain-name              "icgm.fr";
option domain-name-servers      193.49.132.10;
#option time-offset              +7200; # Europe/Paris
#one-lease-per-client            off;
default-lease-time              86400;
max-lease-time                  90480;
option                          ip-forwarding off;
deny unknown-clients;

subnet 10.14.14.0 netmask 255.255.255.0 {
# note that no range is given so dhcpd will not try to
# assign IP addresses
}
""");

for record in records:
    nom=record['Nom de la machine '].replace(' ','-').replace('_','-')
    if(record['Adresse Mac']=='')or(nom == ''):
        print("Ligne ignorée");
#        print(record);
    else:
        vlan=record['Sous-réseau'];
        if(vlan in vlans):
            info=vlans[vlan]
            DPTMT=switch(vlan,
                'ICGM-DPT1-CMM',0,
                'ICGM-DPT2-CMMM',1,
                'ICGM-DPT3-MPH',2,
                'ICGM-DPT4-CMNME',3,
                'ICGM-DPT5-CPTM',4,
                'ICGM-SGAF',8,
                'ICGM-INSTRU-ON',5,
                'ICGM-SSI',9,
                'ICGM-INSTRU-OFF',6,
                'ICGM-IMPRIM',7,
                'ICGM-IDRAC-CIN',10,
                'ICGM-IDRAC',11,
                'ICGM-PT',12
                )
            if(record['Adresse Mac'] in Old_Address_list[DPTMT].keys()):
                # L'@ IP est deja paramétérée
                ip = Old_Address_list[DPTMT][record['Adresse Mac']]
                # print("case n° 1  nom de la machine = " + str(record['Nom de la machine ']) +",@MAC = "+str(record['Adresse Mac'])+" | ip = "+str(ip))
            else:
                # L' @ IP n'est pas encore paramétrée
                ip = find_first_avaible_ip(DPTMT)
                Old_Address_list=ip_data_getter()
                # print("case n° 2 nom de la machine = " + str(record['Nom de la machine ']) +",@MAC = "+str(record['Adresse Mac'])+" | ip = "+str(ip))
                # print(ip)
            ip=re.sub(r'(\.1$)', "."+str(info["init"]), info["gateway"])
            info["init"]=info["init"]+1;
            info["content"]=info["content"]+"""
host %s {
    hardware ethernet %s;
    fixed-address %s;
    option routers %s;
    option ntp-servers %s;
    option domain-name-servers 10.14.14.6;
    option domain-name "%s";          
    option subnet-mask %s;
    option host-name "%s";
} """ % (nom, record['Adresse Mac'],ip, info['gateway'], info['gateway'], info['subdomain'],info['netmask'],nom)
            if (len(nom)>7):
                info["dns"]=info["dns"]+"%s\tIN\tA\t%s\n"%(nom, ip)
            else:
                info["dns"]=info["dns"]+"%s\t\tIN\tA\t%s\n"%(nom, ip)
            info["rev"]=info["rev"]+"%d\tIN\tPTR\t%s.%s.\n"%(info["init"]-1,nom,info["subdomain"])

        else:
            print("Vlan %s non trouvé" % (vlan))

for vlan in vlans:
    info=vlans[vlan];
    if info['content']!="":
        fvlan= open("dhcpd-%d.conf"%(info["id"]), "w")
        fvlan.write("#vlan: %d (%s)\n" %(info["id"],vlan));
        fvlan.write("subnet %s  netmask %s {" % (info['subnet'],info['netmask']))
        fvlan.write(info["content"]);
        f1.write("include \"/etc/dhcp/dhcpd-%d.conf\"; #vlan %s\n" % (info["id"], vlan));
        fvlan.write("\n}\n");
        fvlan.close();
        fzone=open("named-%d.conf"%(info["id"]),"w");
        arpa=re.sub(r'([0-9]+)[.]([0-9]+)[.]([0-9]+)[.]0',r'\3.\2.\1', info["subnet"])
        fzone.write("""zone "%s" {
    type master;
    file "/etc/named.zones/%d.host"; # zone file path
};
zone "%s.in-addr.arpa" {
    type master;
    file "/etc/named.zones/%d.rev";  # %s/%s subnet
};
"""%(info["subdomain"],info["id"],arpa,info["id"],info["subnet"],info["netmask"]))
        fzone.close();
        fhost=open("%d.host"%(info["id"]),"w")
        now = datetime.now() # current date and time
        serial = now.strftime("%Y%m%d00")
        fhost.write("""$TTL 43200
@               IN      SOA     dhcpd.srv-prive.icgm.fr.  Fabrice\.Boyrie.icgm.fr. (
                        %s ; serial
                        43200 ; refresh
                        3600 ; retry
                        3600000 ; expire
                        604800 ; default_ttl
                        )
;
;
@               IN      NS    dhcpd.srv-prive.icgm.fr.
_vlmcs._tcp     IN      SRV   0 0 1688  snkms.unistra.fr. 
"""%(serial))
        fhost.write(info["dns"])
        fhost.close()
        frev=open("%d.rev"%(info["id"]),"w")
        frev.write("""$TTL 43200
@               IN      SOA     dhcpd.srv-prive.icgm.fr.  Fabrice\.Boyrie.icgm.fr. (
                        %s ; serial
                        43200 ; refresh
                        3600 ; retry
                        3600000 ; expire
                        604800 ; default_ttl
                        )
;
;
@               IN      NS    dhcpd.srv-prive.icgm.fr.
"""%(serial))
        frev.write(info["rev"])
        frev.close()

f1.close()
