from typing import Iterable, Callable
from .utils import clear
from .fzf import fzf
import sys
import inspect

class Option:
    """ General class to represent a single option inside a Menu """
    def __init__(self, label: str, terminal: bool=True, prev='root'):
        self.label = label
        self.terminal = terminal
        self.prev = prev

    def choose(self):
        if isinstance(self, Menu):
            self.navigate()
        elif isinstance(self, Action):
            self.execute()
        elif isinstance(self, Pick):
            self.pick()

    def back(self):
        if self.prev == 'root':
            clear()
            sys.exit()
        else:
            self.prev.navigate()

class Menu(Option):
    """A class used to create a Menu Option object."""
    def __init__(self, label: str, options: Iterable):
        super().__init__(label, terminal=False)
        self.options = list(options)
        self.picks = []

        for opt in options:
            opt.prev = self

    def navigate(self, choice=0, limit=25, title="", reverse=False):
        return fzf(self.options, choice=choice, limit=limit, msg=title, reverse=reverse)

    def tree_view(self, tabbing: int=0):
        """Method to see nested tree structure of Menus."""
        for opt in self.options:
            if isinstance(opt, Menu):
                print('\t' * tabbing + opt.label)
                opt.tree_view(tabbing + 1)
            elif isinstance(opt, Action):
                print('\t' * tabbing + opt.label)

class Action(Option):
    """A class used to create a callable Option object."""
    def __init__(self, label: str, *funcs: Callable):
        super().__init__(label)
        self.funcs = funcs

    def execute(self):
        for func in self.funcs:
            funcargs = inspect.getfullargspec(func).args
            if len(funcargs) == 0:
                func()
            else:
                func(self)

class Pick(Option):
    """A class used to create a pickable Option object."""
    def __init__(self, label: str, picked=False):
        super().__init__(label)
        self.picked = picked

    def pick(self, keep=True):
        self.picked = not self.picked
        if self.picked:
            self.prev.picks.append(self.label)
        else:
            self.prev.picks.remove(self.label)
        if keep:
            self.prev.navigate(choice=sorted(self.prev.options, key=lambda x: x.label).index(self))
