---
config:
  theme: base
---
classDiagram
class Frontend {
  <<layer>>
  +renderUI()
  +handleUserInput()
}
class API {
  <<layer>>
  +receiveRequest()
  +sendResponse()
}
namespace BusinessLayer {
  class Facade {
    <<pattern>>
    +callBusinessLogic()
  }
  class User {
    +id
    +email
    +password
  }
  class Place {
    +id
    +name
    +location
  }
  class Review {
    +id
    +text
    +rating
  }
  class Amenity {
    +id
    +name
  }
}
class DataAccess {
  <<layer>>
  +queryDB()
  +saveDB()
}
Frontend --> API : uses
API --> Facade : calls
Facade --> User : manages
Facade --> Place : manages
Facade --> Review : manages
Facade --> Amenity : manages
Facade --> DataAccess : accesses
DataAccess --> User : loads/saves
DataAccess --> Place : loads/saves
DataAccess --> Review : loads/saves
DataAccess --> Amenity : loads/saves
