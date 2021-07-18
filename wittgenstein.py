#!/usr/bin/env python3

import sys, os.path, markdown, re

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

OPEN_OL = '<ol class="wit-nest" markdown="1">'
CLOSE_OL = '</ol>'
OPEN_LI = '<li class="wit-item" markdown="1">'
CLOSE_LI = '</li>'

with open(input_path) as fin:
    content = fin.readlines()

def count_your_lucky_stars(line):
    stars = 0
    is_start_of_numbered_stars = False
    clean_line = line.lstrip()
    if clean_line.startswith('*') or clean_line.startswith('1*'):
        leadingWhiteSpace = re.match(r"\s*", line).group() # TODO: performance testing (other approaches)
        leadingWhiteSpace = leadingWhiteSpace.replace('\t', SPACES)
        stars = (len(leadingWhiteSpace) // len(SPACES)) + 1
        if clean_line[0] == '1':
            is_start_of_numbered_stars = True
    return stars, is_start_of_numbered_stars, clean_line

# https://stackoverflow.com/a/3663505
def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def lchop(s, prefix):
    if prefix and s.startswith(prefix):
        return s[len(prefix):]
    return s

output = []

lucky_stars_are_numbered = False
added_css = False
star_counts = {}
previous_num_stars = 0
disable = False
previous_line_blank = False

def close_old_list(line):
    global lucky_stars_are_numbered, previous_num_stars, star_counts, previous_line_blank
    # the stars just ended
    if lucky_stars_are_numbered:
        line = ((CLOSE_OL * (previous_num_stars)) + '\n\n') + line
    output.append(line)
    lucky_stars_are_numbered = False
    star_counts = {}
    previous_num_stars = 0
    previous_line_blank = False


for idx, line in enumerate(content):
    # We'll allow empty lines to be put inbetween stars (for the purpose of formatting)
    if str.isspace(line) and previous_num_stars > 0:
        if previous_line_blank:
            close_old_list(line)
        else:
            previous_line_blank = True
        continue

    if line.startswith('```'):
        disable = not disable
    num_stars, is_start_of_numbered_stars, clean_line = count_your_lucky_stars(line)
    if num_stars > 0:
        if disable:
            num_stars = 0
        else:
            line = clean_line
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
ol.wit-nest p {
    display: inline;
}
</style>
""")
        added_css = True

    if num_stars > 0:
        num_characters = 0
        if not USE_HTML_FOR_NESTED_COUNTERS and lucky_stars_are_numbered:
            num_characters = 1
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
                sanitized_line = lchop(line, '* ')
                htmlized_line = markdown.markdown(sanitized_line.strip())
                line = html + opens + htmlized_line + closes
            else:
                line = (SPACES * (num_stars - 1)) + num + line
            lucky_stars_are_numbered = True
        else:
            line = line

        output.append(line)
        previous_num_stars = num_stars
    else:
        close_old_list(line)

with open(output_path, 'w+') as fout:
    fout.writelines(output)
    fout.close()

print("""
Success!
""")