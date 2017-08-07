# tzselect - A solution for generating a select field for timezones.
#
#       http://github.com/davidreynolds/tzselect
#
# Copyright 2010 David Reynolds
#
# Use and distribution licensed under the MIT license. See
# the LICENSE file for full text.

from datetime import datetime

import pytz
import sys

if sys.version_info >= (3,0):
    from webhelpers2.html.tags import select
    from webhelpers2.html import tags
else:
    from webhelpers.html.tags import select

def cmp_timezones(a, b):
    h1 = a[1]
    h2 = b[1]
    if h1 < h2:
        return -1
    if h1 > h2:
        return 1
    return 0


def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K


def tzselect(name, default, **attrs):
    zones = []
    usa = []
    ops = []
    utc = datetime.now(pytz.utc)

    if not default:
        default = 'US/Pacific'

    for tzname in pytz.common_timezones:
        tz = utc.astimezone(pytz.timezone(tzname))
        offset = tz.strftime('%z')
        hours = offset[:3]
        mins = offset[-2:]
        zones.append((tzname, int(hours), int(mins)))
        if tzname.split('/')[0] == 'US':
            usa.append((tzname, int(hours), int(mins)))
            
    if sys.version_info >= (3,0):
        zones.sort(key=cmp_to_key(cmp_timezones))
        usa.sort(key=cmp_to_key(cmp_timezones))
    else:
        zones.sort(cmp=cmp_timezones)
        usa.sort(cmp=cmp_timezones)

    def _hourstring(hours):
        if hours >= 0:
            return '+%s' % h
        return str(hours)

    for zname, h, m in usa:
        h = _hourstring(h)
        m = str(m).zfill(2)
        human_name = zname.split('/')[-1]
        human_name = human_name.replace('_', ' ')

        ops.append((zname, '(GMT%s:%s) ' % (h, m) + human_name))

    ops.append(('', '--------------'))

    for zname, h, m in zones:
        h = _hourstring(h)
        m = str(m).zfill(2)
        human_name = zname.split('/')[-1]
        human_name = human_name.replace('_', ' ')
        
        ops.append((zname, '(GMT%s:%s) ' % (h, m) + human_name))
    
    if sys.version_info >= (3,0):
        ops = (tags.Option(*reversed(o)) for o in ops)

    return select(name, [default], ops, **attrs)

if __name__ == '__main__':
    print(tzselect('timezone', 'US/Pacific'))
