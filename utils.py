import enum

class myEnums(enum.Enum):
    def __str__(self) -> str:
        return str(self.value)
    def __repr__(self) -> str:
        return self.value
    
class table_name(myEnums):
    students="students"
    advisers="advisers"
    courses="courses"
    year="year"
    organization="organization"
    enrollment_status="enrollment_status"
    test=':memory:'

class limit(myEnums):
    One=(1)
    All=(0)