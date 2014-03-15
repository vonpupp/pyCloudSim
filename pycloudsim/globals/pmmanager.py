from pycloudsim.classes.phisicalmachine import PhysicalMachine

class PMManager:
    def __init__(self, total_pm):
        self.items = [PhysicalMachine(i)
                          for i in range(total_pm)]

    def __str__(self):
        result = 'PMPool['
        for item in self.items:
            result += str(item) + ', '
        result += ']'
        return result

