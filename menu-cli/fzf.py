import string
from typing import Iterable
from fuzzyfinder import fuzzyfinder as ff
from .utils import clear, getch

def fzf(options: Iterable, msg: str="", reverse: bool=False, limit: int=15, choice: int=0):
    """Live FuzzyFinder over an Iterable."""
    valid_chars = string.ascii_letters + string.digits + " ,.;:-_´áéíóúñÁÉÍÓÚ"
    substr, ch = "", ""
    opt_list = []
    pickstringlist = []

    for opt in options:
        if hasattr(opt, "label"):
            pickstring = ""
            if hasattr(opt, "picked"):
                pickstring = " [X]"  if opt.picked else " [ ]"
            opt_list.append(opt.label)
            pickstringlist.append(pickstring)
    pickdict = dict(zip(opt_list, pickstringlist))

    while True:
        candidates = list(ff(substr, opt_list))
        prevch = ch
        clear()
        if reverse:
            print(msg + substr)
        if len(candidates) > limit:
            candidates = candidates[:limit]
        for cand in candidates:
            if cand == candidates[choice]:
                print(f"\033[92m> {cand + pickdict[cand]}\033[0m")
            else:
                print(cand + pickdict[cand])
        if not reverse:
            print(msg + substr)

        ch = getch()
        if type(ch) != str and ch not in ['\x1b', '[']:
            ch = ch.decode('utf-8')

        if ch == '\r':
            chosen = candidates[choice]
            break
        elif ch == '\t':
            choice = (choice + 1) % len(candidates)
            continue
        elif ch == 'C' and prevch == '[':
            chosen = candidates[choice]
            break
        elif ch == 'B' and prevch == '[':
            choice = (choice + 1) % len(candidates)
            continue
        elif ch == 'A' and prevch == '[':
            choice = (choice - 1) % len(candidates)
            continue
        elif ch == 'D' and prevch == '[':
            options[0].prev.back()
            return
        elif ch in valid_chars:
            choice = 0
            substr += ch
            continue
        elif ch in ['\x1b', '[']:
            continue
        else:
            substr = substr[:-1]
    clear()

    #  if isinstance(options[0], (Menu, Action, Pick)):
    for opt in options:
        if opt.label == chosen:
            opt.choose()
            break
    return

    return choice
