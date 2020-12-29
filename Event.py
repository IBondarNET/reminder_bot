import datetime

class AbstractEvent:
    __date = None
    __name = None

    typeName :str
 
    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def display(self):
        return self.name + '\n' + str(self.date)

    def toString(self):
        return self.typeName + "," + str(self.date) + "," + self.name    

    
class Birthday(AbstractEvent):
    __person = None

    def __init__(self):
        self.typeName = "Birthday"

    def display(self):             
        return super().display() + ' ' + self.person

    @property
    def person(self):      
        return self.__person

    @person.setter
    def person(self, person):        
        self.name = "День рождения: "        
        self.__person = person

    def toString(self):
        return super().toString() + "," + self.person


class Meeting(AbstractEvent):
    __place = None    

    def __init__(self):
       self.typeName = "Meeting"

    def display(self):        
        return super().display() + '\n' + "Место встречи: " + self.place

    @property
    def place(self):      
        return self.__place

    @place.setter
    def place(self, place):            
        self.__place = place

    def toString(self):
        return super().toString() + "," + self.place

class Reminder(AbstractEvent):
    __note = None

    def __init__(self):
        self.typeName = "Reminder"

    def display(self):        
        return super().display() + '\n' +"Примечание: " + self.note

    @property
    def note(self):      
        return self.__note

    @note.setter
    def note(self, note):        
        self.__note = note

    def toString(self):
        return super().toString() + "," + self.note

 class RepeatingReminder(Reminder):
    __interval = None

    def __init__(self):
        self.typeName = "RepeatingReminder"

    def display(self):        
        return super().display() + '\nПовторение каждые ' + self.interval

    @property
    def interval(self):      
        return self.__interval

    @interval.setter
    def interval(self, interval):                
        self.__interval = interval

    def toString(self):
        return super().toString() + "," + self.note + "," + self.interval       