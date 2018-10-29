# -*- coding: utf-8 -*-

from SpellBook import Spell, SpellBook
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.listview import ListItemButton
from kivy.config import Config
from kivy.clock import Clock

import json

with open("DnD.json", encoding="utf8") as f:
    data = json.load(f)

inF = open("dnd-spells.txt")

###############################################################################################
								#Getting Spell Stats#
###############################################################################################

master_spell_list = []

for spell in inF.readlines():
    spell = spell.replace("\n", "")
    master_spell_list.append(spell)

personal_spellbook = SpellBook()
master_spellbook = SpellBook()



#Fills Master Spellbook with DND spells
for spell in master_spell_list:
    ID = master_spell_list.index(spell)
    temp = Spell(data[ID][master_spell_list[ID]]["Spell Name"],
                 data[ID][master_spell_list[ID]]["School of Magic"],
                 data[ID][master_spell_list[ID]]["Level"],
                 data[ID][master_spell_list[ID]]["Casting Time"],
                 data[ID][master_spell_list[ID]]["Range"],
                 data[ID][master_spell_list[ID]]["Components"],
                 data[ID][master_spell_list[ID]]["Duration"],
                 data[ID][master_spell_list[ID]]["Description"],
                 data[ID][master_spell_list[ID]]["Definition"],
                 data[ID][master_spell_list[ID]]["Higher Level Bonus"],
                 data[ID][master_spell_list[ID]]["Classes"])
    master_spellbook.add_spell(temp)


#App Starts here
class SchoolListButton(ListItemButton):
    school = StringProperty()


class SpellListButton(ListItemButton):
    spell = StringProperty()


class Pages(GridLayout):
    current_spellbook = "personal"
    current_school = ''
    current_page = ''
    personal_message = "Add to Personal Spells"

    school_list = ObjectProperty()
    spell_list = ObjectProperty()
    add_to_personal_button = ObjectProperty()

    spell_stats = ListProperty(['', '', '', '', '', '', '', '', '', '', ''])

    def load_schools(self, book):
        print(book)
        schools = []
        if book == "master":
            temp_spellbook = master_spellbook
            self.current_spellbook = "master"
        else:
            temp_spellbook = personal_spellbook
            self.current_spellbook = "personal"
        print(len(temp_spellbook.spells))
        for spell in temp_spellbook.spells:
            if spell.school not in schools:
                schools.append(spell.school)
        print(schools)
        self.school_list.adapter.data = schools
        self.school_list._trigger_reset_populate()

    def load_spells(self, school):
        self.current_school = school
        spells = []
        if self.current_spellbook == "master":
            temp_spellbook = master_spellbook
        else:
            temp_spellbook = personal_spellbook
        for spell in temp_spellbook.spells:
            if school == spell.school:
                spells.append(spell.name)

        self.spell_list.adapter.data = spells
        self.spell_list._trigger_reset_populate()

    def load_page(self, spell_name):
        self.current_page = spell_name
        selected_spell = Spell("ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR")
        for spell_id in master_spellbook.spells:
            if spell_id.name == spell_name:
                selected_spell = spell_id
                break

        #################################################################################################
        #                                   Various Grammar Fixes                                       #
        #################################################################################################
        if len(selected_spell.definition) == 0:
            selected_spell.definition = selected_spell.description
            selected_spell.description = ""

        selected_spell.classes = selected_spell.classes.replace(", ", "\n-")

        selected_spell.higher_level_bonus = selected_spell.higher_level_bonus.replace("; ", "\n-")
        ##################################################################################################

        self.spell_stats = [selected_spell.name,
                            selected_spell.school,
                            selected_spell.level,
                            selected_spell.cast_time,
                            selected_spell.spell_range,
                            selected_spell.components,
                            selected_spell.duration,
                            selected_spell.description,
                            selected_spell.definition,
                            "-" + selected_spell.higher_level_bonus,
                            "-" + selected_spell.classes]

        if selected_spell in personal_spellbook.spells:
            self.personal_message = "Remove from Personal Spells"
        else:
            self.personal_message = "Add to Personal Spells"

        self.add_to_personal_button.text = self.personal_message

    def edit_personal(self):
        print("NAME: " + self.spell_stats[0])
        if self.spell_stats[0] == "ERROR":
            pass
        else:
            selected_spell = Spell("ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR",
                                   "ERROR", "ERROR")
            for spell_id in master_spellbook.spells:
                if spell_id.name == self.spell_stats[0]:
                    selected_spell = spell_id
                    break

            if self.personal_message == "Add to Personal Spells":
                if selected_spell.name != "ERROR" and selected_spell not in personal_spellbook.spells:
                    personal_spellbook.add_spell(selected_spell)
                    print("Spell Added")
            else:
                personal_spellbook.remove_spell(selected_spell)
                print("Spell Removed")
        print(personal_spellbook)
        Clock.schedule_once(self.update)

    def update(self, *args):
        self.load_page(self.current_page)
        self.load_schools(self.current_spellbook)
        self.load_spells(self.current_school)


class MainApp(App):

    def build(self):
        self.title = "SpellBook"
        Config.set('graphics', 'width', '1200')
        Config.set('graphics', 'height', '700')
        return Pages()

    def on_school_selection(self, school):
        self.root.load_spells(school)

    def on_spell_selection(self, spell):
        self.root.load_page(spell)


if __name__ == "__main__":
    app = MainApp()
    app.run()



