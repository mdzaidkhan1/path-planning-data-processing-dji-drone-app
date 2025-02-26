from kivy.clock import Clock
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationrail import (
    MDNavigationRailItem,
    MDNavigationRail,
    MDNavigationRailMenuButton,
    MDNavigationRailFabButton,
    MDNavigationRailItemIcon,
    MDNavigationRailItemLabel,
)
from kivymd.uix.screen import MDScreen


class CommonNavigationRailItem(MDNavigationRailItem):
    text = StringProperty()
    icon = StringProperty()

    def on_icon(self, instance, value):
        def on_icon(*ars):
            self.add_widget(MDNavigationRailItemIcon(icon=value))
        Clock.schedule_once(on_icon)

    def on_text(self, instance, value):
        def on_text(*ars):
            self.add_widget(MDNavigationRailItemLabel(text=value))
        Clock.schedule_once(on_text)


class Example(MDApp):
    def build(self):
        return MDBoxLayout(
            MDNavigationRail(
                MDNavigationRailMenuButton(
                    icon="menu",
                ),
                MDNavigationRailFabButton(
                    icon="home",
                ),
                CommonNavigationRailItem(
                    icon="bookmark-outline",
                    text="Files",
                ),
                CommonNavigationRailItem(
                    icon="folder-outline",
                    text="Bookmark",
                ),
                CommonNavigationRailItem(
                    icon="library-outline",
                    text="Library",
                ),
                type="selected",
            ),
            MDScreen(
                md_bg_color=self.theme_cls.secondaryContainerColor,
            ),
        )


Example().run()