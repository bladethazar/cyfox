class Cyfox:
    def __init__(self):
        self.state = "idle"

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state
