"""
undo/redo implemented with the memento design pattern.

The memento pattern is simpler than the command pattern.
Here the memory cost of memento is affordable because we
only store snapshots of the GtkListStore object, not of
the whole PDF files.
"""


class Manager(object):
    """
    Stack of GtkListStore models (Memento design pattern)
    """

    def __init__(self, model):
        self.model = model
        self.states = []
        #: label of the previous undoable action
        self.label = None
        #: id of the current state
        self.current = 0
        self.undoaction = None
        self.redoaction = None

    def commit(self, label):
        """
        Must be called *BEFORE* each undoable actions
        :param label: label of the action
        """
        self.states = self.states[:self.current + 1]
        self.states.append(([tuple(row) for row in self.model], self.label,))
        self.current += 1
        self.label = label
        self.__refresh()

    def undo(self, action, param, unused):
        if self.current == len(self.states):
            self.states.append((list([tuple(row) for row in self.model]), self.label,))
        state, label = self.states[self.current - 1]
        self.__set_state(state)
        self.current -= 1
        self.__refresh()

    def redo(self, action, param, unused):
        state, label = self.states[self.current + 1]
        self.__set_state(state)
        self.current += 1
        self.__refresh()

    def set_actions(self, undo, redo):
        self.undoaction = undo
        self.redoaction = redo
        self.__refresh()

    def __set_state(self, state):
        self.model.clear()
        for row in state:
            self.model.append(row)

    def __refresh(self):
        if self.undoaction:
            self.undoaction.set_enabled(self.current >= 1)
        if self.redoaction:
            self.redoaction.set_enabled(self.current + 1 < len(self.states))
        # TODO: This is where to update the undo/redo menu items label to
        # show which action is going to be undone/redone. Because GtkImageMenuItem
        # will leads to many changes in translations this is currently postponed.
