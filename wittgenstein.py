#!/usr/bin/env python3

import sys, os.path, markdown, re
from types import new_class

def print_help():
    print(f"""Usage: $ python3 wittgenstein [input file path] [output file path]
""")

def print_error(error):
    print(f"""
Error: {error}
""", file=sys.stderr)
    print_help()
    sys.exit()

# https://stackoverflow.com/a/3663505
def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def lchop(s, prefix):
    if prefix and s.startswith(prefix):
        return s[len(prefix):]
    return s


# Check if enough arguments have been given.
if len(sys.argv) < 2:
    print_error("Please provide an input file path (and, optionally, an output file path)!")

input_path = sys.argv[1]
if not (os.path.isfile(input_path)):
    print_error("Either file path is malformed or there is a permissions issue?")
if not (input_path.lower().endswith('.wit')):
    print_error("Input is not a '.wit' file!")

output_path = ''
if len(sys.argv) > 2:
    output_path = sys.argv[2]
else:
    # by default, we'll assume Markdown
    output_path = rchop(input_path, '.wit') + '.md'

output_format = "html"
if len(sys.argv) > 3:
    output_format = sys.argv[3] # for now, this in undocumented behavior

load_open = True
if len(sys.argv) > 4:
    load_open = sys.argv[4] != 'load-collapsed'

USE_HTML_FOR_NESTED_COUNTERS = output_format == 'html'
SPACES = "    "

def OPEN_OL(id, class_name = ''):
    return f'<ol class="wit-nest {class_name}" markdown="1" id="{id}">'
CLOSE_OL = '</ol>'
def OPEN_LI(id):
    return f'<li class="wit-item" markdown="1" data-wit-content-id="{id}">'
CLOSE_LI = '</li>'

with open(input_path) as fin:
    content = fin.readlines()

def count_your_lucky_stars(line):
    stars = 0
    is_start_of_numbered_stars = False
    clean_line = line.lstrip()
    is_new_bullet_point = clean_line.startswith('*') or clean_line.startswith('1*')
    try:
         leadingWhiteSpace = re.match(r"\s*", line).group() # TODO: performance testing (other approaches)
         leadingWhiteSpace = leadingWhiteSpace.replace('\t', SPACES)
         stars = (len(leadingWhiteSpace) // len(SPACES)) + 1
         if clean_line[0] == '1':
            is_start_of_numbered_stars = is_new_bullet_point
    except:
        pass
    return is_new_bullet_point, stars, is_start_of_numbered_stars, clean_line



output = []
output_og_idxs = []

item_ids = {}

lucky_stars_are_numbered = False
added_css = False
star_counts = {}
previous_num_stars = 0
disable = False
previous_line_blank = False
num_trees = 0

def close_old_list(idx, line):
    global lucky_stars_are_numbered, previous_num_stars, star_counts, previous_line_blank
    # the stars just ended
    if lucky_stars_are_numbered:
        line = ((CLOSE_OL * (previous_num_stars)) + '\n\n') + line
    output.append(line)
    output_og_idxs.append(idx)
    lucky_stars_are_numbered = False
    star_counts = {}
    previous_num_stars = 0
    previous_line_blank = False


for idx, line in enumerate(content):
    # We'll allow empty lines to be put inbetween stars (for the purpose of formatting)
    if str.isspace(line) and previous_num_stars > 0:
        if previous_line_blank:
            close_old_list(idx, line)
        else:
            previous_line_blank = True
        continue

    if line.startswith('```'):
        disable = not disable
    is_new_bullet_point, num_stars, is_start_of_numbered_stars, clean_line = count_your_lucky_stars(line)

    should_show_as_continuation = not is_new_bullet_point and num_stars == previous_num_stars and previous_num_stars > 0
    if not is_new_bullet_point:
        num_stars = 0

    if num_stars > 0:
        if disable:
            num_stars = 0
        else:
            line = clean_line
    is_start_of_stars = ((previous_num_stars == 0 and num_stars > 0) or is_start_of_numbered_stars) and not disable
    if is_start_of_stars:
        num_trees = num_trees + 1
    if is_start_of_numbered_stars and not disable:
        lucky_stars_are_numbered = True

    if USE_HTML_FOR_NESTED_COUNTERS and is_start_of_stars and not added_css:
        output_og_idxs.insert(0, -1)
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
            li.wit-collapsed:before {
                color: red;
            }
            ol.wit-nest p {
                display: inline;
            }
            .wit-hide {
                display: none;
            }
        </style>""" + '\n')
        added_css = True

    if is_new_bullet_point and num_stars > 0:
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
                html = OPEN_OL(f'witroot_{num_trees}', 'wit-root')
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
                num = str(star_counts[temp]) + "." + num
                temp = temp - 1
            if USE_HTML_FOR_NESTED_COUNTERS:
                opens = OPEN_LI(f't{num_trees}_n{num}_content')
                closes = CLOSE_LI
                if is_new_branch:
                    diff = (num_stars - previous_num_stars)
                    temp_opens = ''
                    for mini_diff in range(diff): # reverse range if wrong order
                        temp_num_data = num.split('.')[:-1]
                        this_num = num
                        if mini_diff != 0:
                            this_num = '.'.join(temp_num_data[:(-1 * (mini_diff))]) + '.'
                        content_num = '.'.join(temp_num_data[:(-1 * (mini_diff + 1))]) + '.'
                        temp_opens =  OPEN_OL(f't{num_trees}_n{content_num}_content') + OPEN_LI(f't{num_trees}_n{this_num}_content') + temp_opens
                    opens = temp_opens
                    # opens = (OPEN_OL(f't{num_trees}_n{content_num}_content') + opens) * diff
                    output[len(output)-1] = rchop(output[len(output)-1], CLOSE_LI)
                if is_end_branch:
                    diff = (previous_num_stars - num_stars)
                    opens = ((CLOSE_OL + CLOSE_LI) * diff) + opens
                sanitized_line = line
                if line.startswith('*{'):
                    try:
                        item_id = re.match(r'\*{([\w-]+)}', line).group(1)
                        if item_id in item_ids:
                            print_error(f'You are reusing the "{item_id}" item ID on line {idx + 1}')
                        else:
                            item_ids[item_id] = rchop(num, '.')
                            sanitized_line = lchop(line, f'*{{{item_id}}} ')
                            sanitized_line = f'<a name="{item_id}"></a>' + sanitized_line
                    except SystemExit:
                        raise
                    except:
                        print_error(f'You have a malformed item ID on line {idx + 1}')
                else:
                    sanitized_line = lchop(line, '* ')
                
                htmlized_line = markdown.markdown(sanitized_line.strip())
                line = html + opens + htmlized_line + closes
            else:
                line = (SPACES * (num_stars - 1)) + num + line
            lucky_stars_are_numbered = True
        else:
            line = line

        output.append(line)
        output_og_idxs.append(idx)
        previous_num_stars = num_stars
    else:
        if should_show_as_continuation > 0 and not previous_line_blank:
            output[len(output)-1] = rchop(output[len(output)-1], CLOSE_LI)
            output.append('<br />&emsp;' + line + CLOSE_LI)
            output_og_idxs.append(idx)
        else:
            close_old_list(idx, line)

for idx, line in enumerate(output):
    try:
        references = re.findall(r'@{([\w-]+)}', line)
        for ref in references:
            if ref in item_ids:
                item_num = item_ids[ref]
                output[idx] = output[idx].replace(f'@{{{ref}}}', f'<a href="#{ref}">§{item_num}</a>')
            else:
                print_error(f'You are using an undefined reference "{ref}" on line {output_og_idxs[idx] + 1}')
    except SystemExit:
            raise
    except:
        print_error(f'There is a problem (potentially with references) on line {output_og_idxs[idx] + 1}')

if added_css:
    script = """
        var witItems = document.getElementsByClassName("wit-item");
        for (var i = 0; i < witItems.length; i++) {
            witItems[i].addEventListener("click", function(event) {
                if (event.target !== this && event.target.nodeName === 'A' && event.target.href) {
                    return;
                }
                var contentID = this.getAttribute('data-wit-content-id');
                var content = document.getElementById(contentID);
                if (content) {
                    this.classList.toggle("wit-collapsed");
                    content.classList.toggle("wit-hide");
                }
                event.stopPropagation();
            });
        """
    if not load_open:
        script = script + """
            witItems[i].click();
        """
    script = script + "}"
    output.append(f'<script>{script}</script>')


with open(output_path, 'w+') as fout:
    fout.writelines(output)
    fout.close()

print("""
Success!
""")