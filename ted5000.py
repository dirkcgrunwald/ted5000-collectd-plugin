import collectd

from base64 import b64encode
from httplib import HTTPConnection
from xml.etree import ElementTree

TED5000_HOST = "ted5000"
TED5000_USERNAME = "admin"
TED5000_PASSWORD = "admin"
VERBOSE = False

def configure_callback(conf):
    global TED5000_HOST, TED5000_USERNAME, TED5000_PASSWORD, VERBOSE
    for node in conf.children:
        if node.key == 'Host':
            TED5000_HOST = node.values[0]
        elif node.key == 'User':
            TED5000_USERNAME = node.values[0]
        elif node.key == 'Verbose':
            VERBOSE = bool(node.values[0])
        elif node.key == 'Password':
            TED5000_PASSWORD = node.values[0]
        else:
            collectd.warning('ted5000 plugin: Unknown config key: %s.' % node.key)
    if VERBOSE:
        collectd.info(
            'ted5000 plugin: Configured with host=%s, user=%s' % (TED5000_HOST, TED5000_USERNAME))


def read_callback():
    user_and_pass = b64encode(b"%s:%s" % (TED5000_USERNAME, TED5000_PASSWORD)).decode("ascii")
    http = HTTPConnection(TED5000_HOST)
    headers = {'Authorization': 'Basic %s' % user_and_pass}

    http.request('GET', '/api/LiveData.xml', headers=headers)
    response = http.getresponse()
    xml = response.read()

    root = ElementTree.fromstring(xml)

    mtus = int(root.find(".//*/NumberMTU").text)

    for mtu in range(1, mtus + 1):
        power = int(root.find(".//*/MTU%d/PowerNow" % mtu).text)
        voltage = int(root.find(".//*/MTU%d/VoltageNow" % mtu).text)

        val = collectd.Values(plugin='python.ted5000', type='gauge')
        val.type_instance = 'power.mtu%d' % mtu
        val.values = [power]
        val.dispatch()

        val.type_instance = 'voltage.mtu%d' % mtu
        val.values = [voltage]
        val.dispatch()

collectd.register_config(configure_callback)
collectd.register_read(read_callback)


