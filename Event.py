import datetime

class AbstractEvent:
    __date = None
    __name = None

 
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



class Birthday(AbstractEvent):
    __person = None

    def display(self):        
        return super().display() + ' ' + self.person


    @property
    def person(self):      
        return self.__person

    @person.setter
    def person(self, person):        
        self.name = "День рождения: "
        print(self.name)
        self.__person = person


class Meeting(AbstractEvent):
    __place = None    

    def display(self):        
        return super().display() + '\n' + self.place

    @property
    def place(self):      
        return self.__place

    @place.setter
    def place(self, place):            
        self.__place = "Место встречи: " + place

class Reminder(AbstractEvent):
    __note = None

    def display(self):        
        return super().display() + '\n' + self.note

    @property
    def note(self):      
        return self.__note

    @note.setter
    def note(self, note):        
        self.__note = "Примечание: " + note