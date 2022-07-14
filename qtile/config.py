# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import shlex
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger
import subprocess

mod = "mod4"
terminal = guess_terminal()


def window_to_previous_screen(qtile, switch_group=False):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[(i - 1) % 3].group.name
    qtile.current_window.togroup(group, switch_group=switch_group)


def window_to_next_screen(qtile, switch_group=False):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[(i + 1) % 3].group.name
    qtile.current_window.togroup(group, switch_group=switch_group)


def rofi_bye(qtile):
    home = os.path.expanduser("~/.config/qtile/rofi_bye.sh")
    subprocess.run([home])


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod], "f", lazy.window.toggle_floating()),
    Key(
        [mod, "shift"],
        "Tab",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "t", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.function(rofi_bye), desc="Shutdown Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key(
        [mod],
        "Return",
        lazy.spawn("rofi -show drun"),
        desc="Spawn a command using a prompt widget",
    ),
    Key([mod], "Right", lazy.function(window_to_next_screen)),
    Key([mod], "Left", lazy.function(window_to_previous_screen)),
]


groups_names = {1: "DEV", 2: "WWW", 3: "EXE", 4: "MEDIA"}

groups = [Group(groups_names[x]) for x in groups_names]


def go_to_group(qtile, group):
    if group in "12":
        qtile.cmd_to_screen(0)
        qtile.groups_map[groups_names[int(group)]].cmd_toscreen()
    elif group in "3":
        qtile.cmd_to_screen(1)
        qtile.groups_map[groups_names[int(group)]].cmd_toscreen()
    else:
        qtile.cmd_to_screen(2)
        qtile.groups_map[groups_names[int(group)]].cmd_toscreen()


for i in "1234":
    keys.append(Key([mod], i, lazy.function(go_to_group, group=i))),


layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=2, margin=5),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=2,margin = 5),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

## for fetching the current input method
def get_keyboard_layout():
    s = (
        subprocess.check_output(["xkblayout-state", "print", '"%s"'])
        .decode("utf-8")
        .strip()[1:3]
    )
    return s


# colors = [["#282c34", "#282c34"],
#           ["#1c1f24", "#1c1f24"],
#           ["#dfdfdf", "#dfdfdf"],
#           ["#ff6c6b", "#ff6c6b"],
#           ["#98be65", "#98be65"],
#           ["#da8548", "#da8548"],
#           ["#51afef", "#51afef"],
#           ["#c678dd", "#c678dd"],
#           ["#46d9ff", "#46d9ff"],
#           ["#a9a1e1", "#a9a1e1"]]
colors = [
    ["#282828", "#282828"],  # 0
    ["#32302f", "#32302f"],  # 1
    ["#ebdbb2", "#ebdbb2"],  # 2
    ["#ff6c6b", "#ff6c6b"],  # 3
    ["#b8bb26", "#b8bb26"],  # 4
    ["#3c3836", "#3c3836"],  # 5
    ["#b16286", "#b16286"],  # 6
    ["#458588", "#458588"],  # 7
    ["#fabd2f", "#fabd2f"],  # 8
    ["#00000000", "#00000000"],
]  # 9
##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(font="Ubuntu Bold", fontsize=10, padding=2, background=colors[2])

extension_defaults = widget_defaults.copy()


def init_widgets_list(secondary=False):
    widgets_list = [
        widget.Sep(linewidth=0, padding=6, foreground=colors[2], background=colors[0]),
        widget.GroupBox(
            font="Ubuntu Bold",
            fontsize=9,
            margin_y=3,
            margin_x=0,
            padding_y=5,
            padding_x=3,
            borderwidth=3,
            active=colors[2],
            inactive=colors[7],
            rounded=False,
            highlight_color=colors[1],
            highlight_method="line",
            this_current_screen_border=colors[6],
            this_screen_border=colors[4],
            other_current_screen_border=colors[6],
            other_screen_border=colors[4],
            foreground=colors[2],
            background=colors[0],
        ),
        widget.TextBox(
            text="|",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="474747",
            padding=2,
            fontsize=14,
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[2],
            background=colors[0],
            padding=0,
            scale=0.7,
        ),
        widget.CurrentLayout(foreground=colors[2], background=colors[0], padding=5),
        widget.TextBox(
            text="|",
            font="Ubuntu Mono",
            background=colors[0],
            foreground="474747",
            padding=2,
            fontsize=14,
        ),
        widget.WindowName(foreground=colors[6], background=colors[0], padding=0),
        widget.TextBox(
            text="", foreground=colors[1], background=colors[0], padding=0, fontsize=20
        ),
        widget.Systray(background=colors[1], padding=10),
        widget.Sep(linewidth=0, padding=6, foreground=colors[1], background=colors[1]),
        widget.TextBox(
            text="",
            foreground=colors[7],
            background=colors[1] if secondary is False else colors[0],
            padding=0,
            fontsize=20,
        ),
        widget.Volume(
            foreground=colors[1],
            background=colors[7],
            mouse_callbacks={"Button3": lambda: qtile.cmd_spawn("pavucontrol")},
            fmt="{}",
            padding=5,
        ),
        widget.TextBox(
            text="", foreground=colors[8], background=colors[7], padding=0, fontsize=20
        ),
        widget.GenPollText(
            foreground=colors[1],
            background=colors[8],
            padding=5,
            func=get_keyboard_layout,
            update_interval=0.5,
        ),
        widget.TextBox(
            text="", foreground=colors[7], background=colors[8], padding=0, fontsize=20
        ),
        widget.Memory(
            foreground=colors[1],
            background=colors[7],
            format="{MemUsed:.1f}{mm}",
            measure_mem="G",
        ),
        widget.TextBox(
            text="", foreground=colors[8], background=colors[7], padding=0, fontsize=20
        ),
        widget.CPU(
            foreground=colors[1],
            background=colors[8],
            format="{load_percent: 1.0f}%",
        ),
        widget.TextBox(
            text="",
            foreground=colors[7],
            background=colors[8] if secondary is False else colors[0],
            padding=0,
            fontsize=20,
        ),
        widget.Clock(foreground=colors[1], background=colors[7], format="%H:%M %d/%m"),
    ]
    return widgets_list


def init_widgets_sec():
    widgets_screen1 = init_widgets_list(True)
    del widgets_screen1[
        7:18
    ]  # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1


def init_widgets_main():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2


screens = [
    Screen(top=bar.Bar(widgets=init_widgets_main(), opacity=1.0, size=20)),
    Screen(top=bar.Bar(widgets=init_widgets_sec(), opacity=1.0, size=20)),
    Screen(top=bar.Bar(widgets=init_widgets_sec(), opacity=1.0, size=20)),
]


# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3Ddnf "


def runone(cmdline):
    """Check if another instance of an app is running, otherwise start a new one."""
    cmd = shlex.split(cmdline)
    try:
        subprocess.check_call(["pgrep", cmd[0]])
    except:
        run(cmdline)


def run(cmdline):
    subprocess.Popen(shlex.split(cmdline))


@hook.subscribe.startup_once
def auto_start():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([home])
    runone("kdeconnect-indicator")
    runone("flatpak run io.github.mimbrero.WhatsAppDesktop")


@hook.subscribe.startup_complete
def set_group_layout():
    qtile.cmd_to_screen(0)
    qtile.groups_map["DEV"].cmd_toscreen()
    qtile.cmd_to_screen(1)
    qtile.groups_map["EXE"].cmd_toscreen()
    qtile.cmd_to_screen(2)
    qtile.groups_map["MEDIA"].cmd_toscreen()


@hook.subscribe.client_new
def set_window_group(window):

    media = ["WhatsApp", None]
    dev = []

    logger.warning(window.name)
    if window.name in media:
        window.cmd_togroup("MEDIA")
