""" Representation of a thesis proposal """

class Thesis(object):
    """Thesis Description of a thesis proposal"""

    def __init__(self, name, description="", by_entity=""):
        """__init__

        :param name: The thesis proposal name
        :param description: A description of the thesis, if avalible
        :param by: The entity which offers the thesis
        """
        self.name = name
        self.description = description
        self.by_entity = by_entity

    def __str__(self):
        """print Prints the thesis proposal"""
        res = "Proposed by : " + self.by_entity + "\n"
        res += "Name : " +  self.name + "\n"
        res += self.description
        return res

    def __eq__(self, other):
        return self.name == other.name and \
            self.description == other.description and \
            self.by_entity == other.by_entity

    def __neq__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self.name.__hash__() + \
            self.description.__hash__() + \
            self.by_entity.__hash__()
