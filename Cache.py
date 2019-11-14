# Cache emulator

class Line:
    def __init__(self, age):
        self.age = age
        self.tag = None
    
    def updateTag(self, tag):
        self.tag = tag

    def updateAge(self, age_accessed):
        if(self.age == age_accessed):
            self.age = 0
        elif(self.age < age_accessed):
            self.age += 1

class Set:
    def __init__(self):
        self.lines = ( Line(2), Line(1), Line(0) )
    
    def contains(self, tag):
        for line in self.lines:
            if line.tag is tag:
                return True
        return False

    def lineToUse(self, tag):
        line_index = 0
        # Use the first tag that has either not been init or is a hit
        for line in self.lines:
            if line.tag is tag or line.tag is None:
                return (line_index, line.age)
            line_index += 1

        # If all self.lines are full and we have a tag miss we must pick a line
        # to evict.
        max_age = None
        line_with_max_age = None
        line_index = 0
        for line in self.lines:
            if max_age is None or line.age > max_age:
                max_age = line.age
                line_with_max_age = line_index
            line_index += 1
       
        print("Evict line", line_with_max_age)
        return (line_with_max_age, max_age)

    def updateAges(self, age_accessed):
        for line in self.lines:
            line.updateAge(age_accessed)

    def updateTag(self, tag):
        line = self.lineToUse(tag)
        self.lines[line[0]].updateTag(tag)
        return line

class Cache:
    def __init__(self):
        self.sets = ( Set(), Set() )

    def contains(self, set_id, tag):
        return self.sets[set_id].contains(tag)

    def updateTag(self, set_id, tag):
        return self.sets[set_id].updateTag(tag)

    def updateAges(self, set_id, age_accessed):
        self.sets[set_id].updateAges(age_accessed)
