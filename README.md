> **⚠️ Warning ⚠️**
> 
> This project is currently in an early development and prototyping phase.
> The Daedalus library is neither complete nor stable and should not be used in any production environment.


# Daedalus Python Library

Daedalus is a powerful and flexible Python library designed to simplify the process of creating APIs. It provides a clean, modular way to integrate services, controllers, and endpoints, making it easy to build scalable and maintainable applications. With support for FastAPI and Falcon frameworks, Daedalus gives you the freedom to choose the right tool for your needs.

## Features

- **Framework Agnostic:** Supports FastAPI and Falcon for building APIs.
- **Modular Design:** Easily inject services into controllers using simple decorators.
- **Service Layer:** Provides a service layer to encapsulate business logic.
- **Controller Layer:** Easily define API controllers and register endpoints.
- **Routing and Endpoint Decorators:** Create routes dynamically with minimal boilerplate code.

## Getting Started

### Prerequisites

- Python 3.13+ is required.
- Install the necessary dependencies:

```
pip install daedalus
```

### Example Project

Below is an example of how to use Daedalus to create an API with FastAPI:

#### 1. Application Setup

First, create the application instance using `DaedalusFactory` and specify the module and framework (FastAPI or Falcon).

```
from daedalus.core.factory import DaedalusFactory
from example.src.main_module import MainModule

app = DaedalusFactory(
    module=MainModule,
    framework='fastapi'  # or 'falcon' for Falcon
)

app.serve(
    port=8000,
    host='localhost',
    cors=True
)
```

#### 2. Defining Services

Next, define your services using the `@Service` decorator. Services are responsible for business logic and can be injected into controllers.

```
from daedalus.bootstrap.decorator.service import Service
from example.src.logger.logger_service import LoggerService

@Service()
class UserService:
    inject = ['LoggerService']

    def __init__(self, logger_service: LoggerService):
        self.logger = logger_service

    def create_user(self, username):
        self.logger.log(f"User created: {username}")
```

#### 3. Creating Controllers

Controllers are responsible for handling HTTP requests and responses. Define endpoints using the `@Controller` decorator and the `@endpoint` decorator to specify routes.

```
from typing import Any, Dict, List

from daedalus.api.decorators.endpoint import endpoint
from daedalus.api.interface.response import JanusResponse
from daedalus.bootstrap.decorator.controller import Controller
from example.src.user.user_service import UserService

@Controller()
class UserController:
    inject = ['UserService']

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @endpoint(path="/user")
    def create_user_route(self, req):
        self.user_service.create_user("John Doe")
        return JanusResponse(
            status_code=200,
            data={"message": "User created"}
        )
```

## Folder Structure

Here’s an example folder structure for your project:

```
. 
├── app.py 
└── example/ 
  └── src/
    ├── main_module.py 
    ├── user/ 
    │ ├── user_service.py 
    │ ├── user_controller.py
    │ └── user_module.py
    └── logger/ 
      ├── logger_service.py 
      └── logger_module.py
```

## Advanced Usage

### Customizing Services and Controllers

You can easily extend services and controllers with custom logic and routing. The Daedalus framework is highly flexible, allowing you to integrate other features like authentication, validation, and more.

### Using Falcon Framework

To use Falcon instead of FastAPI, simply replace the `framework` argument when initializing the app:

```
app = DaedalusFactory(
    module=MainModule,
    framework='falcon'
)
```

### Dependency Injection

Daedalus uses a simple and efficient dependency injection system. You can inject services into controllers and other services using the `inject` attribute.

```
class MyController:
    inject = ['MyService']
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

With Daedalus, creating APIs is as simple as pie, and you have full control over the structure and behavior of your application.
