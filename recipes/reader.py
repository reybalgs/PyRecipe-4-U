#!/usr/bin/python

# reader.py
#
# This program reads a .rcpe file, parses its JSON content and then displays
# everything in a neat and organized manner.

import simplejson as json

import sys

file = open(sys.argv[1], 'r') # Open the file passed as an argument
print 'File loaded!'
recipe = json.loads(file.read())
print recipe

# Print them one by one
print 'RECIPE DETAILS'
print '\nName: ' + recipe[0]['name']
print 'Course: ' + recipe[1]['course']
print 'Serving Size: ' + str(recipe[2]['serving_size'])
print '\nIngredients:'

counter = 1 # Counter variable

for ingredient in recipe[3]['ingredients']:
    print str(counter) + '. ' + ingredient[0]['name'] + ' - ' + str(ingredient[1]['quantity']) + ' ' + ingredient[2]['unit']
    counter += 1

print '\nInstructions:'

counter = 1

for instruction in recipe[4]['instructions']:
    print str(counter) + '. ' + instruction
    counter += 1
