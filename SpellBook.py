# -*- coding: utf-8 -*-

import random, inspect

class Spell:
    """A class for a spell in DND, includes all the rolls and stats"""
    def __init__(self, name, school, level, cast_time, spell_range, components, duration, description, definition, higher_level_bonus, classes):
        self.name = name
        self.school = school
        self.level = level
        self.cast_time = cast_time
        self.spell_range = spell_range
        self.components = components
        self.duration = duration
        self.description = description
        self.definition = definition
        self.higher_level_bonus = higher_level_bonus
        self.classes = classes


class SpellBook:
    """A class for a book that contains spells, also provide an interface for casting them"""
    def __init__(self):
        self.num_of_spells = 0
        self.spells = []

    def add_spell(self, spell):
        if isinstance(spell, Spell):
            self.spells.append(spell)
        else:
            print("TYPE ERROR: Can only add spells to spell book.")
        self.num_of_spells = len(self.spells)

    def remove_spell(self, spell):
        self.spells.remove(spell)
        self.num_of_spells = len(self.spells)

    def roll_dice(self, num_of_sides):
        return random.randint(1, num_of_sides)

    def print_spells(self):
        for spell in self.spells:
            print(spell.name)

    def get_num_of_spells(self):
        return self.num_of_spells


