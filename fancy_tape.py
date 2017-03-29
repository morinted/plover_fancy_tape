
import time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import (
    QLabel,
    QBoxLayout, QGraphicsDropShadowEffect)

from plover import system
from plover.gui_qt.fancy_tape_ui import Ui_FancyTape

from plover.gui_qt.i18n import get_gettext
from plover.gui_qt.utils import ToolBar
from plover.gui_qt.tool import Tool
from plover.steno import Stroke

_ = get_gettext()


class FancyTape(Tool, Ui_FancyTape):

    ''' Paper tape display of strokes. '''

    TITLE = _('Fancy Tape')
    ICON = ':/tape.svg'
    ROLE = 'fancy_tape'

    def __init__(self, engine):
        super(FancyTape, self).__init__(engine)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.NoDropShadowWindowHint |
            Qt.X11BypassWindowManagerHint
        )
        self.setParent(None)
        self.setGeometry(0, 0, 0, 0)
        self.setupUi(self)
        self.verticalLayout.setDirection(QBoxLayout.BottomToTop)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self._strokes = []
        self._all_keys = None
        self._history_size = 2000000
        self._font_color = QColor(0x2B, 0xFA, 0x33)
        self._glow_color = QColor(0, 0, 0)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.on_timer_tick)
        self._timer.setInterval(100)
        self._timer.start()
        engine.signal_connect('config_changed', self.on_config_changed)
        self.on_config_changed(engine.config)
        self.on_stroke(Stroke(system.KEYS))
        engine.signal_connect('stroked', self.on_stroke)

    @staticmethod
    def _set_label_color(label, color, opacity=255):
        label.setStyleSheet(
            'color: rgba(%s, %s, %s, %s)' % (
                color.red(), color.green(), color.blue(), opacity
            )
        )

    def on_timer_tick(self):
        strokes = []
        for label, opacity in self._strokes:
            opacity -= 10
            if 0 < opacity < 255:
                self._set_label_color(label, self._font_color, opacity)
            if opacity > 0:
                strokes.append((label, opacity))
            else:
                self.verticalLayout.removeWidget(label)
                label.deleteLater()
        self._strokes = strokes
        self.repaint()
        self.update()

    def on_config_changed(self, config):
        if 'system_name' in config:
            self._all_keys = ''.join(key.strip('-') for key in system.KEYS)
            self._numbers = set(system.NUMBERS.values())

    def _paper_format(self, stroke):
        text = [' '] * len(self._all_keys)
        keys = stroke.steno_keys[:]
        if any(key in self._numbers for key in keys):
            keys.append('#')
        for key in keys:
            index = system.KEY_ORDER[key]
            text[index] = self._all_keys[index]
        return ''.join(text)

    def _show_stroke(self, stroke):
        text = self._paper_format(stroke)
        label = QLabel(self)
        effect = QGraphicsDropShadowEffect()
        effect.setXOffset(0)
        effect.setYOffset(0)
        effect.setBlurRadius(10)
        effect.setColor(self._glow_color)
        self._set_label_color(label, self._font_color)
        label.setText(text)
        label.setGraphicsEffect(effect)
        font = QFont()
        font.setFamily("Anonymous Pro")
        font.setPointSize(23)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)
        label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        label.setObjectName("label")
        self._strokes.append((label, 500))
        self.verticalLayout.addWidget(label)

    def on_stroke(self, stroke):
        self._show_stroke(stroke)
