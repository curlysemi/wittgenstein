#!/usr/bin/env python3

import sys, os.path

def print_help():
    print(f"""Usage: $ python3 wittgenstein [input file path] [output file path]
""")

def print_error(error):
    print(f"""
Error: {error}
""", file=sys.stderr)
    print_help()
    sys.exit()

# Check if enough arguments have been given.
if len(sys.argv) < 3:
    print_error("Please provide an input file path and an output file path!")

input_path = sys.argv[1]
output_path = sys.argv[2]
output_format = "html"
if len(sys.argv) > 3:
    output_format = sys.argv[3] # for now, this in undocumented behavior

if not (os.path.isfile(input_path)):
    print_error("Either file path is malformed or there is a permissions issue?")

USE_HTML_FOR_NESTED_COUNTERS = output_format == 'html'
SPACES = "    "

OPEN_OL = '<ol class="wit-nest">'
CLOSE_OL = '</ol>'
OPEN_LI = '<li class="wit-item">'
CLOSE_LI = '</li>'

with open(input_path) as fin:
    content = fin.readlines()

def count_your_lucky_stars(line):
    stars = 0
    is_start_of_numbered_stars = False
    if line.startswith('*') or line.startswith('1*'):
        for i, c in enumerate(line):
            if c == '*':
                stars = stars + 1
            elif i == 0 and c == '1':
                is_start_of_numbered_stars = True
                continue
            else:
                break
    return stars, is_start_of_numbered_stars

# https://stackoverflow.com/a/3663505
def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

output = []

lucky_stars_are_numbered = False
added_css = False
star_counts = {}
previous_num_stars = 0
disable = False
for idx, line in enumerate(content):
    if line.startswith('```'):
        disable = not disable
    num_stars, is_start_of_numbered_stars = count_your_lucky_stars(line)
    if num_stars > 0 and disable:
        num_stars = 0
    isStartOfStars = ((previous_num_stars == 0 and num_stars > 0) or is_start_of_numbered_stars) and not disable
    if is_start_of_numbered_stars and not disable:
        lucky_stars_are_numbered = True

    if USE_HTML_FOR_NESTED_COUNTERS and isStartOfStars and not added_css:
        output.insert(0, """<style>
ol.wit-nest {
  counter-reset: item
}
li.wit-item {
  display: block
}
li.wit-item:before {
  content: counters(item, ".") ". ";
  counter-increment: item
}
</style>
""")
        added_css = True

    if num_stars > 0:
        num_characters = num_stars
        if is_start_of_numbered_stars:
            num_characters = num_characters + 1
        line = line[num_characters:]
        if lucky_stars_are_numbered:
            num = ""
            html = ""
            if is_start_of_numbered_stars:
                html = OPEN_OL
            temp = num_stars
            is_end_branch = False
            is_new_branch = False
            while temp > 0:
                innerTemp = 1
                while (innerTemp + num_stars) in star_counts:
                    del star_counts[innerTemp + num_stars]
                    innerTemp = innerTemp + 1
                    is_end_branch = True
                if temp in star_counts:
                    # we should only increment if we have the same exact amount of stars that the given index represents
                    if num_stars == temp:
                        star_counts[temp] = star_counts[temp] + 1
                else:
                    star_counts[temp] = 1
                    is_new_branch = num_stars > previous_num_stars and num_stars > 1
                if USE_HTML_FOR_NESTED_COUNTERS: # CSS will do the counting, so we only need to keep track of open/close tags
                    pass
                else:
                    num = str(star_counts[temp]) + "." + num
                temp = temp - 1
            if USE_HTML_FOR_NESTED_COUNTERS:
                opens = OPEN_LI
                closes = CLOSE_LI
                if is_new_branch:
                    diff = (num_stars - previous_num_stars)
                    opens = (OPEN_OL + OPEN_LI) * diff
                    output[len(output)-1] =  rchop(output[len(output)-1], CLOSE_LI)
                if is_end_branch:
                    diff = (previous_num_stars - num_stars)
                    opens = ((CLOSE_OL + CLOSE_LI) * diff) + opens
                line = html + opens + line.strip() + closes
            else:
                line = (SPACES * (num_stars - 1)) + num + line
            lucky_stars_are_numbered = True
        else:
            line = (SPACES * (num_stars - 1)) + "*" + line + '\n'

        output.append(line)
        previous_num_stars = num_stars
    else:
        if lucky_stars_are_numbered:
            line = line + (CLOSE_OL * (previous_num_stars)) + '\n'
        output.append(line)
        lucky_stars_are_numbered = False
        added_css = False
        star_counts = {}
        previous_num_stars = 0

with open(output_path, 'w+') as fout:
    fout.writelines(output)
    fout.close()

print("""
Success!
""")