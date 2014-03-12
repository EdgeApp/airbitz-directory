#!/usr/bin/env python

import sys
import json

input = sys.stdin.read()
# Try to break curl output
done = False
try:
    """ Split header and body so body can be pretty printed """
    (header, body) = input.split("\r\n\r\n")
    j = json.loads(body)

    print header
    print
    print json.dumps(j, indent=2)
    done = True
except:
    pass

# If we are only receiving JSON
if not done:
    try:
        j = json.loads(input)
        print json.dumps(j, indent=2)
        done = True
    except:
        pass

# If all else fails
if not done:
    print input
