import logging
from pynput.keyboard import Controller, Key
from gesture_recognition import Gesture, Role

class KeyController:
    def __init__(self, role: Role):
        self.role = role
        self.keyboard = Controller()
        self.last_keys = set()
        self.keymap = {
            Role.LEFT: {
                Gesture.LEFT_JAB: 'w',
                Gesture.RIGHT_JAB: 's',
                Gesture.LEAN_UP: 'a',
                Gesture.LEAN_DOWN: 'd'
            },
            Role.RIGHT: {
                Gesture.LEFT_JAB: Key.down,
                Gesture.RIGHT_JAB: Key.up,
                Gesture.LEAN_UP: Key.right,
                Gesture.LEAN_DOWN: Key.left
            },
            Role.TWO_PLAYER: {
                Gesture.LEFT_JAB: 'w',
                Gesture.RIGHT_JAB: Key.up,
                Gesture.LEAN_UP: 'a',
                Gesture.LEAN_DOWN: Key.left
            }
        }
        logging.info(f"KeyController initialized for {self.role.name}")

    def handle_gestures(self, gestures):
        pressed = set()
        for gesture in gestures:
            key = self.keymap[self.role].get(gesture)
            if key:
                try:
                    self.keyboard.press(key)
                    pressed.add(key)
                    logging.info(f"Pressed key: {key} for gesture: {gesture.name}")
                except Exception as e:
                    logging.error(f"Error pressing key {key}: {e}")
        # Release keys that are no longer triggered
        for key in self.last_keys - pressed:
            try:
                self.keyboard.release(key)
                logging.info(f"Released key: {key}")
            except Exception as e:
                logging.error(f"Error releasing key {key}: {e}")
        self.last_keys = pressed