# grepbible

`grepbible` is a command-line interface (CLI) tool designed to make searching for Bible verses (in ca. 60 languages) locally (like grepping) and looking up the Bible quotes fast and intuitive.  
It also represents a new channel for Bible distribution and aids in language learning, as parallel Bible translations have been used for centuries to learn languages.

Wikipedia article on [Bible citations](https://en.wikipedia.org/wiki/Bible_citation)  
The raw text is taken from [Wordproject®](https://www.wordproject.org), and has undergone processing to fit the specific needs and format of this project.

There's a serparate project for the web UI: [grepbible-server](https://github.com/maxlit/grepbible-server.git). Its demo is available at [langtools.io/gb](https://langtools.io/gb)  

## Features

- **Search Capabilities**: Look up individual verses, ranges of chapters, or specific passages across multiple translations.
- **Multiple Bible Versions**: Easily switch between different Bible translations to compare interpretations and wording.
- **Local Caching**: Bible versions are downloaded and stored locally for quick access and offline use.
- **Parallel and interleave text**: Combine text blocks from different translations.

## Installation

To install `grepbible`, ensure you have Python 3.9 or higher installed on your system. You can install `grepbible` directly from PyPI:

```sh
pip install grepbible
```

This command installs the `grepbible` package and makes the `gbib` command available in your shell.

You might need to update your `PATH` as well (e.g. on Ubuntu):

```sh
export PATH=$PATH:$(python3 -m site --user-base)/bin
```
and add it to `~/.bashrc` to make it persistent

![demo](./gifs/240309_gbib_demo.gif)

## Usage

`grepbible` is designed to be straightforward and easy to use from the command line. The default version (unless the flag `-v` is specified) is 'kj' ([KJV](https://en.wikipedia.org/wiki/King_James_Version)), in English.

Below are some common usage examples:

### Look Up a Single Verse

```sh
gbib -c "John 3:11"
```

```
Verily, verily, I say unto thee, We speak that we do know, and testify that we have seen; and ye receive not our witness.
```

### Compare Verses in Different Translations

```sh
gbib -v kj,pl -c "Romans 8:20"
```

```
For the creature was made subject to vanity, not willingly, but by reason of him who hath subjected the same in hope,

Gdyż stworzenie marności jest poddane, nie dobrowolnie, ale dla tego, który je poddał,
```

### Lookup a Chapter

```sh
gbib -c 'Psalms 117'
```

```
O Praise the LORD, all ye nations: praise him, all ye people.
For his merciful kindness is great toward us: and the truth of the LORD endureth for ever. Praise ye the LORD.
```

### Show a Range of Verses

```sh
gbib -c "Gen 41:29-30"
```

```
Behold, there come seven years of great plenty throughout all the land of Egypt:
And there shall arise after them seven years of famine; and all the plenty shall be forgotten in the land of Egypt; and the famine shall consume the land;
```

### Fetch Multiple Disjoint Verses

```sh
gbib -c "Genesis 1:1,3"
```

### Compare different versions

Show interleave translation of Latin Vulgata to English KJV (line-by-line):
```sh
gbib -c 'Gen 41:29-30' -v kj,vg -i
```

![Compare different versions line-by-line](./gifs/5_range-of-verses-i.gif)

Block-by block translation (omit the flag `-i`):

```sh
 gbib -c 'Gen 41:29-30' -v kj,vg 
```

```
Behold, there come seven years of great plenty throughout all the land of Egypt:
And there shall arise after them seven years of famine; and all the plenty shall be forgotten in the land of Egypt; and the famine shall consume the land;

ecce septem anni venient fertilitatis magnae in universa terra Aegypti
quos sequentur septem anni alii tantae sterilitatis ut oblivioni tradatur cuncta retro abundantia consumptura est enim fames omnem terram
```
### Random quotes

Time for some fun! One can generate random quotes (in different languages and in parallel as well).

```sh
gbib -r
```

![demo](./gifs/240309_gbib_random-quotes.gif)

### Get help

For more information on command options and additional features, you can run:

```sh
gbib --help
```

![demo](./gifs/8_usage.gif)

### Search text

One can do three types of text search:  
- Exact search
- Approximate (fuzzy) search - it might catch the typos, words omission and grammar misspelling
- Semantic search - it looks for the quotes with the similar sense (AI augmented search)

Obviously, one can search with the fuzzy logic also the exact text.

### Fuzzy search

The `-s` option enables fuzzy search, which is helpful when you're not sure about the exact wording or struggling with the grammar of archaic language:

```sh
gbib --rag -s 'Every prudent man deals with knowledge'
```

```
(Proverbs 13:16) Every prudent man dealeth with knowledge: but a fool layeth open his folly.
```

If the quote deviates significantly from the original, the result might be empty.

```sh
gbib --rag -s 'Every honest man deals with knowledge'
```

However, one can adjust the threshold (current default is 0.85 which might change) of the similarity:

```sh
gbib --rag -s 'Every honest man deals with knowledge' --threshold 0.7
```
which gives the proper result (might lead to unexpected results for short queries).

```
(Proverbs 13:16) Every prudent man dealeth with knowledge: but a fool layeth open his folly.    
````

### Semantic search

Semantic search uses a technique called RAG (Retrieval-Augmented Generation), which retrieves relevant text chunks via vector embeddings and optionally generates answers using a language model.  
In this case, everything runs locally — no prompts are sent to any online services — although the search may be slower than simple keyword matching.  

To enable semantic search, you first need to install the extra packages:

```sh
pip install grepbible[ml]
```

Then, build the RAG index with:

```sh
gbib --rag
```

Or for a specific version (e.g. German), use:

```sh
gbib --rag -v de
```

You can now perform semantic search with the `--rag -s` option. For example:

```sh
gbib --rag -s 'Horses run on rocks'
```

```
(Joel 2:4) The appearance of them is as the appearance of horses; and as horsemen, so shall they run.
(Amos 6:12) Shall horses run upon the rock? will one plow there with oxen? for ye have turned judgment into gall, and the fruit of righteousness into hemlock 
(Isaiah 63:13) That led them through the deep, as an horse in the wilderness, that they should not stumble?
(Zechariah 6:6) The black horses which are therein go forth into the north country; and the white go forth after them; and the grisled go forth toward the south country.
```

Since the similar sense is not an exact science, some outcomes might be quite off. One can also set `--threshold` between 0 and 1 (the default value is/was 0.3) to adjust the similarity threshold, to extend or reduce the list of the outcomes.

#### Search with grep

One can literally use `grep` to look up the verses and leverage `gbib` only for downloading the sources. Here's how.

First, download KJV ('kj') and Vulgata ('vg'). The data is stored in `$HOME/grepbible_data`, thus, it makes sense to store it as a variable, e.g. the path to the 5th chapter of Exodus in KJV will be $HOME/grepbible_data/kj/Exodus/5.txt

```sh
gbib -d kj,vg
export GB=$HOME/grepbible_data/kj
```

#### Go to line

Example, jump 10th line of 5th chapter in Exodus:
```sh
less +10 $GB/Exodus/5.txt
```

#### Count occurences of words

How often the word 'camel' appears in the Bible:
```sh
grep -nr $GB -e camel | wc -l # 59
```

#### What was this quote about the sheep and wolves?

```sh
grep -nr $GB -e wolves | grep sheep
```

![local grep](./gifs/9_grep.gif)

## Contributing

Contributions to `grepbible` are welcome! Whether it's improving code, or reporting issues, or spreading the word, or financial support, your input is valuable.  

### Issues/bugs

To raise an issue, go to 'Issues' tab, and click on 'New issue'.

### Code

To contribute code:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear, descriptive messages.
4. Push your branch and submit a pull request.

Please ensure your code adheres to the project's style and quality standards. For major changes, please open an issue first to discuss what you would like to change.

### Social

Feel free to spread the word or/and use the hashtag `#grepbible` in social media.

### Financial

Feel free to buy me a coffee: [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/J3J1VEX6J)

## License

`grepbible` is open-source software licensed under the MIT License. See the LICENSE file for more details.
