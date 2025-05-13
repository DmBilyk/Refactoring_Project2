# Computer Shop System

A Django-based web application that allows users to configure and order custom computers using modern design patterns.

## Project Overview

The Computer Shop System is a sophisticated web application built with Django that implements several design patterns to create a maintainable, scalable e-commerce platform for custom computer configurations. Users can build custom computers by selecting components step by step and place orders through an intuitive interface.

## Design Patterns Implementation

### 1. Facade Pattern (`ComputerShopFacade`)

The Facade pattern provides a simplified interface to the complex subsystem of computer configuration and ordering:

```python
# Usage example from views
computer = ComputerShopFacade.create_computer(request.user, **request.session['computer_builder'])
order = ComputerShopFacade.place_order(request.user, computer)
```

Key methods:
- `create_computer()`: Handles the complete process of creating a customized computer
- `place_order()`: Manages order placement
- `get_computer_details()`: Retrieves detailed computer information
- `get_user_orders()`: Fetches all orders for a specific user

Benefits:
- Simplifies client interaction with the complex system
- Decouples the presentation layer from business logic
- Provides a clean, unified API for views

### 2. Builder Pattern (`ComputerBuilder`)

The Builder pattern separates the construction of complex Computer objects from their representation:

- `ComputerBuilder` (abstract class): Defines the interface for building each part
- `ConcreteComputerBuilder`: Implements the step-by-step construction process
- Fluent interface allows chaining method calls:

```python
computer_details = (
    builder.build_case(case_type)
           .install_processor(processor)
           .install_memory(memory)
           .install_storage(storage)
           .install_graphics(graphics_card)
           .apply_color(color)
           .add_peripherals(peripherals)
           .set_device_type(is_laptop)
           .calculate_price()
           .get_computer()
)
```

Benefits:
- Allows creating different configurations of computers
- Keeps construction code separate from representation
- Provides fine control over the construction process

### 3. Director (`ComputerDirector`)

Works with the Builder pattern to create predefined computer configurations:

```python
director = ComputerDirector()
gaming_pc = director.make_gaming_desktop("i9-12900K", 32, 2048, "RTX-3080", "Black", ["keyboard", "mouse"])
```

Methods:
- `make_gaming_desktop()`: Creates a high-performance gaming desktop
- `make_business_laptop()`: Creates a business-oriented laptop

Benefits:
- Encapsulates common configurations
- Simplifies creation of standard computer types
- Can be extended with additional presets

### 4. Singleton Pattern (`DatabaseConnectionSingleton`)

Ensures only one database connection instance exists with thread safety:

```python
# Usage example
db_connection = DatabaseConnectionSingleton()
```

Implementation details:
- Thread-safe with double-checked locking mechanism
- Lazy initialization of the connection
- Methods to handle connection state

Benefits:
- Prevents resource waste from multiple connections
- Ensures consistent state across the application
- Thread safety for concurrent access

## System Architecture

The application follows a typical Django MVC (Model-View-Controller) architecture with design patterns enhancing specific functionalities:

1. **Views** (`views.py`): Handle HTTP requests, user interactions, and form processing
2. **Models** (`models.py`, not shown in provided code): Computer and Order database models
3. **Forms** (referenced in `views.py`): Handle user input validation
4. **Facade** (`facade.py`): Simplifies interaction with the complex subsystem
5. **Builder** (`builder.py`): Handles step-by-step computer construction
6. **Singleton** (`singleton.py`): Manages database connections

### User Flow

1. User navigates through a series of forms to configure their computer:
   - Case selection
   - Processor selection
   - Memory selection
   - Storage selection
   - Graphics card selection
   - Color selection
   - Peripherals selection
   - Device type selection (laptop/desktop)

2. The system presents a summary with calculated price

3. Upon confirmation, the system:
   - Creates the computer configuration in the database
   - Creates an order linked to the user
   - Shows order success page

4. Users can view their order history and details

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- SonarQube Scanner (for code quality analysis)

### Docker Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/computer-shop-system.git
cd computer-shop-system
```

2. Build and start the Docker containers:
```bash
docker-compose up -d --build
```

This command builds the Docker images and starts the containers in detached mode.

3. Apply database migrations:
```bash
docker exec -it django_web python manage.py migrate
```

4. Create a superuser (optional):
```bash
docker exec -it django_web python manage.py createsuperuser
```

5. Access the application:
   - Web application: http://localhost:8000
   - Django admin: http://localhost:8000/admin

### Running Tests

To run tests with coverage:

```bash
docker exec -it django_web coverage run manage.py test
```

Generate coverage report in XML format (for SonarQube):

```bash
docker exec -it django_web coverage xml
```

### Code Quality Analysis

Run SonarQube Scanner to analyze code quality:

```bash
sonar-scanner
```

Make sure you have a `sonar-project.properties` file in your project root with appropriate configuration:

```properties
sonar.projectKey=computer_shop_system
sonar.projectName=Computer Shop System
sonar.sources=.
sonar.python.coverage.reportPaths=coverage.xml
sonar.host.url=http://localhost:9000
sonar.login=your-sonar-token
```

## Development Notes

### Adding New Computer Components

To add new computer components (e.g., new processors, graphics cards):

1. Update the pricing dictionaries in `ConcreteComputerBuilder` methods
2. Update the corresponding form choices in forms.py (not shown in provided code)

### Extended Features

Potential extensions to the system:

- Inventory management
- User reviews and ratings
- Recommendation system based on user preferences
- Payment gateway integration
- Admin dashboard for sales analytics

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.