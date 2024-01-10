#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import re
import sys


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
LOGGER.setLevel(logging.DEBUG)

COMMIT_HASH_PATTERN = re.compile(r'#([0-9a-fA-F]{40})\b')

# TODO: how long can it be? Up to 8 digits for now.
ISSUE_NUMBER_PATTERN = re.compile(r'#([1-9][0-9]{0,7})\b')

# includes both commit hashes and issue numbers
ESCAPE_PATTERN = re.compile(r'\[#([0-9a-fA-F]{1,40})\]\(([^)]+)\)')

RECOVERY_PATTERN = re.compile(
    r'\[__ESCAPED_COMMIT_HASH_LINK_([0-9a-fA-F]{1,40})\]\(([^)]+)\)'
)


def process_markdown(markdown_path, owner, project):
    """Processes a given markdown file.

    Replaces every occurence of '#' + full SHA-1 hash (40 characters) with
    a link to the corresponding GitHub commit page.

    Replaces every occurence of '#' + issue number (1-8 digits) with a link
    to the corresponding GitHub issue page.

    Replaced markdown is written to the standard output.
    """
    commit_substitution = f'[#\\1](https://github.com/{owner}/{project}/commit/\\1)'
    issue_substitution = f'[#\\1](https://github.com/{owner}/{project}/issues/\\1)'
    escape_substitution = f'[__ESCAPED_COMMIT_HASH_LINK_\\1](\\2)'
    recovery_substitution = f'[#\\1](\\2)'
    with open(markdown_path, mode='r', encoding='utf-8') as markdown_in:
        for line in markdown_in:
            # prevents already replaced links from being replaced
            line = re.sub(ESCAPE_PATTERN, escape_substitution, line)
            # replaces commit hashes with links
            line = re.sub(COMMIT_HASH_PATTERN, commit_substitution, line)
            # replaces issue numbers with links
            line = re.sub(ISSUE_NUMBER_PATTERN, issue_substitution, line)
            # recovers the escaped links
            line = re.sub(RECOVERY_PATTERN, recovery_substitution, line)
            sys.stdout.write(line)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Replaces Git commit hashes with markdown links',
    )
    arg_parser.add_argument(
        '--owner',
        dest='owner',
        metavar='OWNER',
        type=str,
        required=True,
        help='owner of the repository (required)',
    )
    arg_parser.add_argument(
        '--project',
        dest='project',
        metavar='PROJECT',
        type=str,
        required=True,
        help='project name of the repository (required)',
    )
    arg_parser.add_argument(
        'markdown_path',
        metavar='MARKDOWN',
        type=str,
        help='path to a markdown file to process',
    )
    args = arg_parser.parse_args()
    LOGGER.debug(f'owner={args.owner}, project={args.project}')
    LOGGER.debug(f'processing: {args.markdown_path}')
    process_markdown(args.markdown_path, owner=args.owner, project=args.project)
