ted5000-collectd-plugin
========================

A [TED 5000](http://www.theenergydetective.com/) plugin for [collectd](http://collectd.org) using collectd's [Python plugin](http://collectd.org/documentation/manpages/collectd-python.5.shtml).

Data captured:

 * Current Voltage for all MTUs
 * Current Power consumption for all MTUs

Install
-------
 1. Place ted5000.py in /opt/collectd/lib/collectd/plugins/python (assuming you have collectd installed to /opt/collectd).
 2. Configure the plugin (see below).
 3. Restart collectd.

Configuration
-------------
Add the following to your collectd config.

    <LoadPlugin python>
      Globals true
    </LoadPlugin>

    <Plugin python>
      ModulePath "/opt/collectd/lib/collectd/plugins/python"
      Import "ted5000"

      <Module ted5000>
        Host "yourhost"
        User "admin"
        Password "admin"
        SkipZeroes "true"
        Verbose "false"
      </Module>
    </Plugin>