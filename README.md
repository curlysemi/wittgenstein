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
</style>
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
</style>
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
</style>
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
</style>
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
</style>
# Wittgenstein Markup Language (`.wit`)
The markup language you would use to write the _Tractatus Logico-Philosophicus_ and not have to worry about the numbering. 🙂

## What Wittgenstein Does
Markdown doesn't support nested numbering like the following:

<ol class="wit-nest"><li class="wit-item">First item<ol class="wit-nest"><li class="wit-item">First item's first sub-item</li></ol></li><li class="wit-item">Second Item</li>
</ol>
If you tried to do it, you might write something like this:

```
1. First item
    1.1. First item's first sub-item
2. Second Item
```

But you would unfortunately get something that looks like this:
1. First item
    1.1. First item's first sub-item
2. Second Item



While you could manage the numbering by hand manually via some hacky solutions, if you later need to _insert_ an item, you have to do a lot of renumbering. It sucks and is not something you can do easily once you start having to manage larger nested lists.

Our renumbering concern applies to the normal ordered lists that Markdown supports. They might seem nice in principle:
```
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
```
1* First Item
* Second Item
* Third Item
```
It should be enough to show that the intent was an ordered list using numbers with the _first_ list element by simply doing `1*` and using only `*` for the subsequent list elements. (In the future, we ought to be able to support `a*`, too.)

And, it works:

<ol class="wit-nest"><li class="wit-item">First Item</li><li class="wit-item">Second Item</li><li class="wit-item">Third Item</li>
</ol>

Now, taking the previous innovation in mind, we added support for our numbered nesting simply by indicating each level clearly. (This theoretically could be done with whitespace alone, but this proof-of-concept opted for multiple star characters instead.)

So, here is the original markup for the first example we gave:
```
1* First item
** First item's first sub-item
* Second Item
```

And it works, too, because this very README used this Wittgenstein-influenced markup language to produce its examples. (The very first example of a list we gave in this README was originally written in this style.)


## How Wittgenstein Works
Keep in mind this is a proof-of-concept written on a Saturday night. Currently, it's a simply Python3 script that does a relatively light transformation on the lines of an inputted text file that start with `*` or `1*`.

It was first a simple generator of indentions for plaintext files and then I decided I wanted to be able to generate Markdown files. Since Markdown supports HTML, the way Wittgenstein works _for Markdown_ is to simply generate HTML tags and let CSS handle the numbering. (Since I added support for Markdown _after_ I had figured out the more-straightforward indention logic for plaintext (which didn't actually require me to do any lookaheads or lookbacks), the logic I added for handling nested HTML tags is confusing as heck — but it works.)

There's still support for the plain, indention-based numbering. I'm leaving the HTML mode as the default because it is more impressive.


## Complicated Examples
The following is a complicated nesting example (I'm actually using this README to hold the test cases since this README is written in the `.wit` markup language and is simple being exported to Markdown.).

<ol class="wit-nest"><li class="wit-item">The world is all that is the case.<ol class="wit-nest"><li class="wit-item">The world is the totality of facts, not of things.<ol class="wit-nest"><li class="wit-item">The world is determined by the facts, and by their being all the facts.</li><li class="wit-item">For the totality of facts determines what is the case, and also whatever is not the case.</li><li class="wit-item">The facts in logical space are the world.</li></ol></li><li class="wit-item">The world divides into facts.<ol class="wit-nest"><li class="wit-item">Each item can be the case or not the case while everything else remains the same.</li>
</ol></ol></ol>
And because I don't wish to include the full _Tractatus Logico-Philosophicus_ in this README, we'll provide an nesting edge-case:


<ol class="wit-nest"><li class="wit-item">This is a simple item<ol class="wit-nest"><li class="wit-item"><ol class="wit-nest"><li class="wit-item"><ol class="wit-nest"><li class="wit-item">This is a complicated item with some empty parent nodes</li></ol></li><li class="wit-item">This is actually a more complicated item<ol class="wit-nest"><li class="wit-item">An earlier version had bugs and gave the wrong numbers in these situations</li></ol></li></ol></li></ol></li><li class="wit-item">This is another simple item<ol class="wit-nest"><li class="wit-item">We want to make sure that this item (and its successors) is numbered properly<ol class="wit-nest"><li class="wit-item">Is this one numbered correctly?<ol class="wit-nest"><li class="wit-item">What about this one?</li><li class="wit-item">Don't forget this one!</li>
</ol></ol></ol></ol>

## Future Changes
* Support LaTeX as an output.

* Support `a*` listing.

* Support `N*` listing, where `N` is any number (right now we can only start at `1`)

* Support `w*` listing (one that uses the exact style of numbering that the _Tractatus Logico-Philosophicus_ does — though I like the style of this version more, we handle empty nodes differently than the TLP and end up with different numbers.)

* Consider how we might reference another item by number? (We'd have to add support for IDs)

* There's some other stuff I'd like have a markup language support (such as simple diagrams), though I'm undecided on a syntax for the time being — this project may grow to support other newish markup features.

