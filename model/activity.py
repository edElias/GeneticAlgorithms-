#Currently working on ED

class Activity:

    def __init__(self, name, expected_enrollment, preferred_facilitators, other_facilitators):
        self.name = name
        self.expected_enrollment = expected_enrollment
        self.preferred_facilitators = list(preferred_facilitators)
        self.other_facilitators = list(other_facilitators)

    def __repr__(self):
        return self.name