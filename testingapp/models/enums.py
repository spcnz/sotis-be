import enum

class NavigationMode(enum.Enum):
    LINEAR = 1
    NON_LINEAR = 2




class SubmissionMode(enum.Enum):
    INDIVIDUAL = 1
    SIMULTANEOUS = 2



class Grade(enum.Enum):
    A = 10
    B = 9
    C = 8
    D = 7
    E = 6
    F = 5
