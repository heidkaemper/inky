#!/usr/bin/env python3

import argparse
from ai import show_ai
from comic import show_comic
from status import show_status

parser = argparse.ArgumentParser()

parser.add_argument("--type", "-t", choices=['ai', 'comic', 'status'], default='ai')

args = parser.parse_args()

match args.type:
    case 'ai':
        show_ai()
    case 'comic':
        show_comic()
    case 'status':
        show_status()
