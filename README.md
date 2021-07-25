<style>
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
        </style># Wittgenstein Markup Language (`.wit`)
The markup language dedicated to writing complicated, nested lists. You could use it to write the next _Tractatus Logico-Philosophicus_ and not have to worry about the numberings (they're all done automatically). 🙂

## What Wittgenstein Does
Aren't truth tables a great way of organizing the values of logical expressions?
Don't forget that Wittgenstein _invented_ truth tables as (basically) an aside in his _Tractatus Logico-Philosophicus_. The organizational structure of that work itself is also a great organizational system — it provides a powerful way of organizing related comments/statements/propositions/sections. Whoever wants to make notes quickly in that style can now rejoice, because the Wittgenstein Markup Language takes care of all the hard numbering/sub-sectioning work!

Why not just use Markdown? Markdown doesn't support nested numbering like the following:

<ol class="wit-nest wit-root" markdown="1" id="witroot_1"><li class="wit-item" markdown="1" data-wit-content-id="t1_n1._content"><p>First item</p><ol class="wit-nest " markdown="1" id="t1_n1._content"><li class="wit-item" markdown="1" data-wit-content-id="t1_n1.1._content"><p>First item's first sub-item</p></li></ol></li><li class="wit-item" markdown="1" data-wit-content-id="t1_n2._content"><p>Second Item</p></li></ol>

If you _tried_ to do it, you might _write_ something like this:

```markdown
1. First item
    1.1. First item's first sub-item
2. Second Item
```

But you would unfortunately get something that looks like this:
1. First item
    1.1. First item's first sub-item
2. Second Item

While you could manage the numbering by hand manually via [some hacky solutions](https://meta.stackexchange.com/questions/85474/how-to-write-nested-numbered-lists), if you later need to _insert_ an item, you have to do a lot of renumbering. It sucks and is not something you can do easily once you start having to manage larger nested lists.

Our renumbering concern applies to the normal ordered lists that Markdown supports. They might seem nice in principle:
```markdown
1. First Item
2. Second Item
3. Third Item
```

(Which produces the following:)
1. First Item
2. Second Item
3. Third Item

But, again, there's something really annoying about having to renumber extensive lists.

So, as an alternate syntax, how about this instead?:
```wittgenstein
1* First Item
* Second Item
* Third Item
```
It should be enough to show that the intent was an ordered list using numbers with the _first_ list element by simply doing `1*` and using only `*` for the subsequent list elements. (In the future, we ought to be able to support `a*`, too.)

And, it works:

<ol class="wit-nest wit-root" markdown="1" id="witroot_2"><li class="wit-item" markdown="1" data-wit-content-id="t2_n1._content"><p>First Item</p></li><li class="wit-item" markdown="1" data-wit-content-id="t2_n2._content"><p>Second Item</p></li><li class="wit-item" markdown="1" data-wit-content-id="t2_n3._content"><p>Third Item</p></li></ol>

Now, taking the previous innovation in mind, we added support for our numbered nesting simply by indicating each level clearly.

So, here is the original markup for the first example we gave:
```wittgenstein
1* First item
    * First item's first sub-item
* Second Item
```

And it works, too, because this very README used this Wittgenstein-influenced markup language to produce its examples. (The very first example of a list we gave in this README was originally written in this style.)

So, basically, when nesting, indent (with 4 spaces) and use `*`s as you would normally, and Wittgenstein does the rest! Just remember to preface your first star with a `1`. 


## How Wittgenstein Works
Keep in mind this is a proof-of-concept written on a Saturday night. Currently, it's a simply Python3 script that does a relatively light transformation on the lines of an inputted text file that start with `*` or `1*` (excluding whitespace to also handle lines that correspond to sub-items).

It was first a simple generator of indentions for plaintext files and then I decided I wanted to be able to generate Markdown files. Since Markdown supports HTML, the way Wittgenstein works _for Markdown_ is to simply generate HTML tags and let CSS handle the numbering. (Since I added support for Markdown _after_ I had figured out the more-straightforward indention logic for plaintext (which didn't actually require me to do any lookaheads or lookbacks), the logic I added for handling nested HTML tags is confusing as heck — but it works.)

Apparently, GitHub doesn't support `<styles>` in Markdown, so the numbering appears slightly incorrect there — instead of `1.1.1.`, we get `1.i.a`. 😭 

There's still support for the plain, indention-based numbering. I'm leaving the HTML mode as the default because it is more impressive.


## Complicated Examples
The following is a complicated nesting example (I'm actually using this README to hold the test cases since this README is written in the `.wit` markup language and is simple being exported to Markdown.).

<ol class="wit-nest wit-root" markdown="1" id="witroot_3"><li class="wit-item" markdown="1" data-wit-content-id="t3_n1._content"><p>The world is all that is the case.</p><ol class="wit-nest " markdown="1" id="t3_n1._content"><li class="wit-item" markdown="1" data-wit-content-id="t3_n1.1._content"><p>The world is the totality of facts, not of things.</p><ol class="wit-nest " markdown="1" id="t3_n1.1._content"><li class="wit-item" markdown="1" data-wit-content-id="t3_n1.1.1._content"><p>The world is determined by the facts, and by their being all the facts.</p></li><li class="wit-item" markdown="1" data-wit-content-id="t3_n1.1.2._content"><p>For the totality of facts determines what is the case, and also whatever is not the case.</p></li><li class="wit-item" markdown="1" data-wit-content-id="t3_n1.1.3._content"><p>The facts in logical space are the world.</p></li></ol></li><li class="wit-item" markdown="1" data-wit-content-id="t3_n1.2._content"><p>The world divides into facts.</p><ol class="wit-nest " markdown="1" id="t3_n1.2._content"><li class="wit-item" markdown="1" data-wit-content-id="t3_n1.2.1._content"><p>Each item can be the case or not the case while everything else remains the same.</p></li></ol></ol></ol>

And because I don't wish to include the full _Tractatus Logico-Philosophicus_ in this README, we'll provide an nesting edge-case:

<ol class="wit-nest wit-root" markdown="1" id="witroot_4"><li class="wit-item" markdown="1" data-wit-content-id="t4_n1._content"><p>This is a simple item</p><ol class="wit-nest " markdown="1" id="t4_n1._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n1.1._content"><ol class="wit-nest " markdown="1" id="t4_n1.1._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n1.1.1._content"><ol class="wit-nest " markdown="1" id="t4_n1.1.1._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n1.1.1.1._content"><p>This is a complicated item with some empty parent nodes</p></li></ol></li><li class="wit-item" markdown="1" data-wit-content-id="t4_n1.1.2._content"><p>This is actually a more complicated item</p><ol class="wit-nest " markdown="1" id="t4_n1.1.2._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n1.1.2.1._content"><p>An earlier version had bugs and gave the wrong numbers in these situations</p></li></ol></li></ol></li></ol></li><li class="wit-item" markdown="1" data-wit-content-id="t4_n2._content"><p>This is another simple item</p><ol class="wit-nest " markdown="1" id="t4_n2._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n2.1._content"><p>We want to make sure that this item (and its successors) is numbered properly</p><ol class="wit-nest " markdown="1" id="t4_n2.1._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n2.1.1._content"><p>Is this one numbered correctly?</p><ol class="wit-nest " markdown="1" id="t4_n2.1.1._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n2.1.1.1._content"><p>What about this one?</p></li><li class="wit-item" markdown="1" data-wit-content-id="t4_n2.1.1.2._content"><p>Don't forget this one!</p></li></ol></li></ol></li></ol></li><li class="wit-item" markdown="1" data-wit-content-id="t4_n3._content"><p><em>What about support for Markdown syntax in the items themselves?</em></p></li><li class="wit-item" markdown="1" data-wit-content-id="t4_n4._content"><p><a name="id"></a>If I want to be <em>able</em> to link, I have to give the line an ID</p><ol class="wit-nest " markdown="1" id="t4_n4._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n4.1._content"><p><a name="nested_id"></a>Don't forget nested ones!</p></li></ol></li><li class="wit-item" markdown="1" data-wit-content-id="t4_n5._content"><p>Then, if I want to make a link, I can simply refer to <a href="#id">§4</a>.</p><ol class="wit-nest " markdown="1" id="t4_n5._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n5.1._content"><p>I can also refer to <a href="#nested_id">§4.1</a> (as well as <a href="#id">§4</a> in the same line)</p><ol class="wit-nest " markdown="1" id="t4_n5.1._content"><li class="wit-item" markdown="1" data-wit-content-id="t4_n5.1.1._content"><p>And I can refer to <a href="#forward_ref">§6</a></p></li></ol></li></ol></li><li class="wit-item" markdown="1" data-wit-content-id="t4_n6._content"><p><a name="forward_ref"></a>Despite the line break above, <em>we</em> have decided we want to consider this part of the same list to allow for more formatting flexibility</p></li></ol>



* BUT, this line starts a new list (because there's two blank lines) (and isn't numbered because it doesn't start with `1*`)

## Dependencies
```
pip3 install markdown
```


## Future Changes
* Support LaTeX as an output.
* Support `a*` listing.
* Support `N*` listing, where `N` is any number (right now we can only start at `1`)
* Support `w*` listing (one that uses the exact style of numbering that the _Tractatus Logico-Philosophicus_ does — though I like the style of this version more, we handle empty nodes differently than the TLP and end up with different numbers.)
* There's some other stuff I'd like have a markup language support (such as simple diagrams), though I'm undecided on a syntax for the time being — this project may grow to support other newish markup features.
* Support numbering in `>`s
<script>
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
        
            witItems[i].click();
        }</script>