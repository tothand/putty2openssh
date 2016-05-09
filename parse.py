#!/usr/local/bin/python
import ConfigParser

bannedsections =[
'HKEY_CURRENT_USER\Software\SimonTatham',
'HKEY_CURRENT_USER\Software\SimonTatham\PuTTY',
'HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Jumplist',
'HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions',
'HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\SshHostKeys']

def NumberConvert(dwordStr):
    if dwordStr.startswith('dword'):
        hexstr = dwordStr.replace('dword:','')
        num = int(hexstr,16)
        return num
    return dwordStr

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            #print("exception on %s!" % option)
            dict1[option] = None
    return dict1


Config = ConfigParser.SafeConfigParser()
Config.read("./putty-utf8.reg")

for sec in Config.sections():
#    print sec
#    print bannedsections
#    exit(1)
    if sec in bannedsections:
        continue
    values = ConfigSectionMap(sec)
    try:
        if values['"protocol"'] == '"ssh"':
            print "Host %s" % sec[sec.rfind('\\')+1:]
            print "\tHostName %s" % values['"hostname"'].strip('"')
            if values['"username"']:
                print "\tUser %s" % values['"username"'].strip('"')
            if values['"portnumber"'] and values['"portnumber"'] != "dword:00000016":
                print "\tPort %s" % NumberConvert(values['"portnumber"'].strip('"'))
            if values['"publickeyfile"']:
                ifile = values['"publickeyfile"'].strip('"')
                print "\tIdentityFile ~/.ssh/%s.pem" % ifile[ifile.rfind('\\')+1:ifile.rfind('.')]
            if values['"portforwardings"']:
                portfw = values['"portforwardings"'].strip('"')
                if portfw.startswith('L') or portfw.startswith('4L'):
                    localport = portfw[portfw.find('L')+1:portfw.find('=')]
                    remote = portfw[portfw.find('=')+1:]
                    print "\tLocalForward %s %s" % (localport, remote)
            print ""
    except:
        continue
#    exit(1)
