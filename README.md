
<a id="readme-top"></a>

<h1 align="center">OOP Coursework</h1>

<p align="center">
  <h2 align="center">Dungeons & Dragons Character Sheet Creator</h2>
</p>

---

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#running-the-program">Running the Program</a></li>
        <li><a href="#running-tests">Running Tests</a></li>
        <li><a href="#using-the-program">Using the Program</a></li>
      </ul>
    </li>
    <li>
      <a href="#implementation-of-4-oop-pillars">Implementation of 4 OOP Pillars</a>
      <ul>
        <li><a href="#polymorphism">Polymorphism</a></li>
        <li><a href="#inheritance">Inheritance</a></li>
        <li><a href="#abstraction">Abstraction</a></li>
        <li><a href="#encapsulation">Encapsulation</a></li>
      </ul>
    </li>
    <li><a href="#pattern-implementation">Pattern Implementation</a></li>
    <li><a href="#composition">Composition</a></li>
    <li><a href="#reading-from-file-and-writing-to-file">Reading From File And Writing to File</a></li>
    <li>
      <a href="#results-and-conclusions">Results and Conclusions</a>
      <ul>
        <li><a href="#results">Results</a></li>
        <li><a href="#conclusions">Conclusions</a></li>
        <li><a href="#room-to-grow">Room to Grow</a></li>
      </ul>
    </li>
  </ol>
</details>

---

## About the Project

My goal for this project was to learn practical Object-Oriented Programming implementations.
This Dungeons & Dragons Character Sheet Creator allows users to create, manage, and store character data.

The program allows you to:

* Create a character
* Assign ability scores
* Choose a class
* Add inventory
* Calculate stats (HP and AC)
* Save and load characters from files

The program was initially developed as a single-file implementation and later refactored into a modular structure to improve readability, maintainability, and scalability.
---

### Running the Program

* Open terminal in your project folder
* Paste this line:

```sh
python3 main.py
```

* The program interface will appear

---

### Running Tests

* Open terminal in your project folder
* Run:

```sh
python3 -m unittest test_dnd_character_sheet.py
```

* Test results will be displayed

---

### Using the Program

* Navigate the menu by entering numbers:

1. Create character
2. View character sheet
3. Save character
4. Load character
5. Level up character
6. Exit

Example workflow:

* Create a character
* Enter ability scores
* Add inventory items
* Save the character
* Load it later

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

# Functional Requirements

## Implementation of 4 OOP Pillars

### Polymorphism

Polymorphism is used in character classes:

```python
class Fighter(CharacterClass):
    def calculate_starting_hp(self, constitution_modifier):
        return self.hit_die + constitution_modifier


class Wizard(CharacterClass):
    def calculate_starting_hp(self, constitution_modifier):
        return self.hit_die + constitution_modifier
```

Each class uses the same method but can behave differently depending on implementation.

---

### Inheritance

Inheritance is used as all classes extend a base class:

```python
class CharacterClass(ABC):
    @abstractmethod
    def calculate_starting_hp(self, constitution_modifier):
        pass
```

```python
class Fighter(CharacterClass):
```

All character types inherit from `CharacterClass`.

---

### Abstraction

Abstraction is implemented in the base class:

```python
class CharacterClass(ABC):
    @abstractmethod
    def calculate_starting_hp(self, constitution_modifier):
        pass
```

This ensures all subclasses implement this method.

---

### Encapsulation

Encapsulation is used in `AbilityScores`:

```python
class AbilityScores:
    def __init__(...):
        self.__scores = {...}
```

```python
def get_score(self, ability):
    return self.__scores[ability]
```

The data is private and accessed through methods.

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Pattern Implementation

I chose the Factory Method pattern and implemented it as `CharacterClassFactory`.

```python
class CharacterClassFactory:
    @staticmethod
    def create_class(class_name):
        if class_name == "fighter":
            return Fighter()
        elif class_name == "wizard":
            return Wizard()
```

This pattern centralizes object creation and avoids multiple condition checks in the main program.

---

## Composition

Used in the `Character` class:

```python
class Character:
    def __init__(...):
        self.ability_scores = ability_scores
        self.inventory = inventory
        self.character_class = character_class
```

A character is composed of multiple smaller objects.

---

## Reading From File And Writing to File

The program uses JSON files to store character data. The `CharacterFileManager` class handles file operations. The `save_to_file` method writes character data to a file, while `load_from_file` reads the data and reconstructs the object. JSON was chosen because it is easy to use and integrates well with Python dictionaries.

```python
json.dump(character.to_dict(), file)
```

```python
data = json.load(file)
```

This allows persistent storage and retrieval of character data.

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

# Results and Conclusions

## Results

* Successfully implemented all OOP pillars
* Factory Method pattern improved flexibility
* File saving and loading works correctly
* Program structure is modular and readable
* Faced challenges with input validation and file paths

---

## Conclusions

This project helped me understand how to structure a real Python application using OOP.
I learned how to organize code into classes, apply design patterns, and write unit tests.

The program is functional but can be expanded further.

---

## Room to Grow

* Add graphical interface (GUI)
* Add more character classes
* Add spell system
* Improve inventory system
* Store multiple characters

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>
