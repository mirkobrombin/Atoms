# window.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, GObject, Adw

from atoms.backend.utils.distribution import AtomsDistributionsUtils
from atoms.frontend.widgets.creation_step_entry import CreationStepEntry


@Gtk.Template(resource_path='/pm/mirko/Atoms/gtk/new-atom-window.ui')
class AtomsNewAtomWindow(Adw.Window):
    __gtype_name__ = 'AtomsNewAtomWindow'
    __distributions_registry = []

    btn_cancel_creation = Gtk.Template.Child()
    btn_cancel = Gtk.Template.Child()
    btn_create = Gtk.Template.Child()
    combo_distribution = Gtk.Template.Child()
    str_list_distributions = Gtk.Template.Child()
    combo_releases = Gtk.Template.Child()
    str_list_releases = Gtk.Template.Child()
    group_steps = Gtk.Template.Child()
    stack_main = Gtk.Template.Child()
    header_bar = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)
        self.__build_ui()
    
    def __build_ui(self):
        for distribution in AtomsDistributionsUtils.get_distributions():
            self.__distributions_registry.append(distribution)
            self.str_list_distributions.append(distribution.name)
        
        self.combo_distribution.set_selected(0)
        self.__on_combo_distribution_changed()

        self.group_steps.add(CreationStepEntry("Creating new Atom Configuration…"))
        self.group_steps.add(CreationStepEntry("Downloading Choosen Image…"))
        self.group_steps.add(CreationStepEntry("Unpacking Choosen Image…"))
        self.group_steps.add(CreationStepEntry("Finalizing…"))

        self.btn_cancel.connect('clicked', self.__on_btn_cancel_clicked)
        self.btn_create.connect('clicked', self.__on_btn_create_clicked)
        self.combo_distribution.connect('notify::selected', self.__on_combo_distribution_changed)
    
    def __on_btn_create_clicked(self, widget):
        self.set_size_request(450, 505)
        self.stack_main.set_visible_child_name("creation")
        self.btn_cancel_creation.set_visible(True)
        self.btn_cancel.set_visible(False)
        self.btn_create.set_visible(False)
        self.header_bar.add_css_class("flat")
    
    def __on_combo_distribution_changed(self, *args):
        self.str_list_releases.splice(0, len(self.str_list_releases))
        distribution = self.__distributions_registry[self.combo_distribution.get_selected()]
        
        for release in distribution.releases:
            self.str_list_releases.append(release)
        self.combo_releases.set_selected(0)

    def __on_btn_cancel_clicked(self, widget):
        self.destroy()