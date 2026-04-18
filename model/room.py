class Room:
    """
    Represents a physical room where activities can be scheduled.
    Stores static data only — no assignments, time slots, or scheduling logic.
    """

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def __repr__(self):
        return self.name