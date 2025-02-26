from kivy.metrics import dp

from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import (
    MDNavigationLayout,
    MDNavigationDrawer,
    MDNavigationDrawerMenu,
    MDNavigationDrawerLabel,
    MDNavigationDrawerItem,
    MDNavigationDrawerItemLeadingIcon,
    MDNavigationDrawerItemText,
    MDNavigationDrawerItemTrailingText,
    MDNavigationDrawerDivider,
)
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp


class Example(MDApp):
    def build(self):
        return MDScreen(
            MDNavigationLayout(#which is also a screen
                MDScreenManager(# added to the navigation Layout
                    MDScreen( #Path Planning Screen, added to the screen manager
                        MDButton(
                            MDButtonText(
                                text="Open Drawer",
                            ),
                            on_release=lambda x: self.root.get_ids().nav_drawer.set_state(
                                "toggle"
                            ),
                            pos_hint={"center_x": 0.5, "center_y": 0.5},
                        ),
                    ),
                ),
                MDNavigationDrawer(
                    MDNavigationDrawerMenu(
                        MDNavigationDrawerLabel(
                            text="Navigation",
                        ),
                        MDNavigationDrawerItem(
                            MDNavigationDrawerItemLeadingIcon(
                                icon="account",
                            ),
                            MDNavigationDrawerItemText(
                                text="Inbox",
                            ),
                            MDNavigationDrawerItemTrailingText(
                                text="24",
                            ),
                            on_release=self.btn_func
                        ),
                        MDNavigationDrawerDivider(
                        ),
                    ),
                    anchor="right",
                    id="nav_drawer",
                    radius=(0, dp(16), dp(16), 0),
                ),
            ),
            md_bg_color=self.theme_cls.backgroundColor,
        )
    
    def btn_func(self, obj):
        print("Item Pressed")


Example().run()