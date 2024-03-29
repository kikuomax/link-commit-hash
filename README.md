# link-commit-hash

A simple Python script that replaces commit hashes and issue numbers in a markdown file with a link to the corresponding GitHub commit and issue pages respectively.

## Prerequisites

Python 3.7 or later.

## How to use

Running `python link-commit-hash.py -h` will print something similar to the following,

```
usage: link-commit-hash.py [-h] --owner OWNER --project PROJECT MARKDOWN

Replaces Git commit hashes and issue numbers with markdown links

positional arguments:
  MARKDOWN           path to a markdown file to process

options:
  -h, --help         show this help message and exit
  --owner OWNER      owner of the repository (required)
  --project PROJECT  project name of the repository (required)
```

[`link-commit-hash.py`](./link-commit-hash.py) replaces every occurrence of a full SHA-1 hash, like `#0123456789abcdef0123456789ABCDEF01234567`, in a given markdown file (`MARKDOWN`) with a link to the corresponding GitHub commit page in a given project (`PROJECT`) of a given owner (`OWNER`), and writes results to the standard output.
It also replaces every occurrence of an issue number, like `#123`, with a link to the corresponding GitHub issue page.

## Example

Given a markdown file ([`sample.md`](./sample.md)),

```md
The initial commit: #f1433174bc39fa37e7179d6aecfac420d415f34c.

Issues:
- The first: #1
- The second: #2
```

The following command,

```sh
python link-commit-hash.py --owner kikuomax --project link-commit-hash sample.md
```

Will produce the following [output](./sample-after.md),

```md
The initial commit: [#f1433174bc39fa37e7179d6aecfac420d415f34c](https://github.com/kikuomax/link-commit-hash/commit/f1433174bc39fa37e7179d6aecfac420d415f34c).

Issues:
- The first: [#1](https://github.com/kikuomax/link-commit-hash/issues/1)
- The second: [#2](https://github.com/kikuomax/link-commit-hash/issues/2)
```

## Development

### Testing

Make sure that the following commands exit with 0 (success with no differences):

1. Make sure conversion succeeds:

    ```sh
    python link-commit-hash.py \
      --owner kikuomax \
      --project link-commit-hash \
      sample.md | diff - sample-after.md
    ```

2. Make sure already converted links are not converted:

    ```sh
    python link-commit-hash.py \
      --owner kikuomax \
      --project link-commit-hash \
      sample-after.md | diff - sample-after.md
    ```