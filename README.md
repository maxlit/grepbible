# grepbible

`grepbible` is a command-line interface (CLI) tool designed to make searching for Bible verses locally fast and intuitive. Whether you're looking for a specific passage, comparing verses across different translations, or exploring ranges of chapters and verses, `grepbible` streamlines the process by bringing the power of Bible study directly to your terminal.

Wikipedia article on [Bible citations](https://en.wikipedia.org/wiki/Bible_citation)
The raw text is taken from [Wordproject®](https://www.wordproject.org)

## Features

- **Versatile Search Capabilities**: Look up individual verses, ranges of chapters, or specific passages across multiple translations.
- **Multiple Bible Versions**: Easily switch between different Bible translations to compare interpretations and wording.
- **Local Caching**: Bible versions are downloaded and stored locally for quick access and offline use.
- **Customizable**: Set your preferred Bible version and customize search options to suit your study needs.

## Installation

To install `grepbible`, ensure you have Python 3.6 or higher installed on your system. You can install `grepbible` directly from PyPI:

```sh
pip install grepbible
```

This command installs the `grepbible` package and makes the `gbib` command available in your shell.

## Usage

`grepbible` is designed to be straightforward and easy to use from the command line. Below are some common usage examples:

### Look Up a Single Verse

```sh
gbib -v kjv -c "John 3:16"
```

### Compare Verses in Different Translations

```sh
gbib -v kjv,pl -c "Romans 8:28"
```

### Show a Range of Verses

```sh
gbib -v kjv -c "Psalms 23"
```

### Fetch Multiple Disjoint Verses
```sh
gbib -v kjv -c "Genesis 1:1–3"
```

For more information on command options and additional features, you can run:

```sh
gbib --help
```

## Contributing

Contributions to `grepbible` are welcome! Whether it's adding new features, improving existing functionality, or reporting issues, your input is valuable. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes with clear, descriptive messages.
4. Push your branch and submit a pull request.

Please ensure your code adheres to the project's style and quality standards. For major changes, please open an issue first to discuss what you would like to change.

## License

`grepbible` is open-source software licensed under the MIT License. See the LICENSE file for more details.
