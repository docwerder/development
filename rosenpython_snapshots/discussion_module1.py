class BaseClass:
    def __init__(self, value):
        print("Base Class Starting")
        self.value = value
        
        #<print("Self.value", self.value)
        print("Base Class Finished")

class SpecialClass(BaseClass):
    def __init__(self):
        #% Hiermit wird alles, was in der "Elternklasse" steht, 
        #% initialiert, also das was in dem def __init__ aus der Elternklasse steht!!
        #super().__init__(self) 

        super().__init__(10) 

        
        print("Special Class Staring")
        print("value?", self.value)
        self.unit = "m"
        print("Special Class Finished")

  

if __name__ == '__main__':
    special_class = SpecialClass()
    print("Unit: ", special_class.unit)