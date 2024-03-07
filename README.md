# grepbible

`grepbible` is a command-line interface (CLI) tool designed to make searching for Bible verses (in ca. 70 languages) locally (like grepping) and looking up the Bible quotes fast and intuitive. It also represents a new channel for Bible distribution, and helps language learners as well since parallel Bible translations were used for languages learning for centuries.

Wikipedia article on [Bible citations](https://en.wikipedia.org/wiki/Bible_citation)
The raw text is taken from [Wordproject®](https://www.wordproject.org)

## Features

- **Versatile Search Capabilities**: Look up individual verses, ranges of chapters, or specific passages across multiple translations.
- **Multiple Bible Versions**: Easily switch between different Bible translations to compare interpretations and wording.
- **Local Caching**: Bible versions are downloaded and stored locally for quick access and offline use.
- **Customizable**: Set your preferred Bible version and customize search options to suit your study needs.

## Installation

To install `grepbible`, ensure you have Python 3.9 or higher installed on your system. You can install `grepbible` directly from PyPI:

```sh
pip install grepbible
```

This command installs the `grepbible` package and makes the `gbib` command available in your shell.

## Usage

`grepbible` is designed to be straightforward and easy to use from the command line. The default version (unless the flag `-v` is specified) is 'kj' ([KJV](https://en.wikipedia.org/wiki/King_James_Version)), in English.

Below are some common usage examples:

### Look Up a Single Verse

```sh
gbib -c "John 3:11"
```

```sh
Verily, verily, I say unto thee, We speak that we do know, and testify that we have seen; and ye receive not our witness.
```

### Compare Verses in Different Translations

```sh
gbib -v kj,pl -c "Romans 8:20"
```

```sh
For the creature was made subject to vanity, not willingly, but by reason of him who hath subjected the same in hope,
Gdyż stworzenie marności jest poddane, nie dobrowolnie, ale dla tego, który je poddał,
```

### Lookup a Chapter

```sh
gbib -c "Psalms 23"
```

### Show a Range of Verses

```sh
gbib -c "Genesis 1:1–3"
```

### Fetch Multiple Disjoint Verses

```sh
gbib -c "Genesis 1:1–3"
```

### Fetch Multiple Disjoint Verses

Show interleave translation of Latin Vulgata to English KJV (line-by-line)
```sh
gbib -c "Genesis 1:1–3" -v vg,kj -i
```

For more information on command options and additional features, you can run:

```sh
gbib --help
```

### Use with grep

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

Result:
```sh
./grepbible_data/kj/Matthew/10.txt:16:Behold, I send you forth as sheep in the midst of wolves: be ye therefore wise as serpents, and harmless as doves.
./grepbible_data/kj/Matthew/7.txt:15:Beware of false prophets, which come to you in sheep's clothing, but inwardly they are ravening wolves.
```

## Contributing

Contributions to `grepbible` are welcome! Whether it's adding new features, improving existing functionality, or reporting issues, your input is valuable.
To raise an issue, go to 'Issues' tab, and click on 'New issue'.

To contribute code:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear, descriptive messages.
4. Push your branch and submit a pull request.

Please ensure your code adheres to the project's style and quality standards. For major changes, please open an issue first to discuss what you would like to change.

## License

`grepbible` is open-source software licensed under the MIT License. See the LICENSE file for more details.
