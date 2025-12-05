import random
from enum import Enum
from abc import ABC, abstractmethod

# Game data
clues = [
    "There is a scorch mark along the floorboards where something burned furiously.",
    "There is a dried smear of mud that peters out into a trail of faint footprints.",
    "There is a broken shard of glass tucked against the skirting, glinting unexpectedly.",
    "There is a folded letter creased with many fingerprints and a hurried tear.",
    "There is a faint, sweet scent lingering in the air like perfume long-unused.",
    "There is a loose floorboard hiding a shallow, hastily dug cavity beneath.",
    "There is a series of shallow gouges on the wall at varying heights.",
    "There is an overturned piece of furniture with scuff marks leading away.",
    "There is a single, small button caught in the weave of the floor covering.",
    "There is a dark stain on the floor that rings colder than its surroundings."
]

sense_exp = [
    "You see tapestries hanging heavy with dust and patterns that shift at the edge of your vision.",
    "You hear a distant drip that measures time in slow, irregular heartbeats.",
    "You smell smoke braided with lavender and something metallic underneath.",
    "You feel the cold of the stone through the soles of your boots, as if the floor remembers each footprint.",
    "You sense a brief, absent pressure in the corner, like someone who was just there stepping away.",
    "You see a single candle guttering as though leaning toward an unseen listener.",
    "You hear a low creak of wood that sounds like a name being exhaled.",
    "You smell wet straw and something sweeter, an old fruit left forgotten in a chest.",
    "You feel a subtle vibration through the floor, whether passing carriage or the building's slow pulse.",
    "You sense a whisper at the edge of thought, a memory trying to slip back into words.",
    "You see motes turning in a shaft of light, moving as if replaying some long-ago motion.",
    "You hear a thin, deliberate scrape along the wall, suggesting someone moved in careful circles."
]


# Enumerations
class encounter_outcome(Enum):
    """Enumeration for adventure encounter outcomes."""
    CONTINUE = "continue"
    END = "end"


# Utility classes
class RandomItemSelector:
    """Selects random items from a pool without repeating until all items are used."""

    def __init__(self, items):
        self.items = list(items) if items is not None else []
        self.used_items = []

    def add_item(self, item):
        """Add a new item to the selection pool."""
        self.items.append(item)

    def pull_random_item(self):
        """Return a random unused item; resets when all used."""
        if not self.items:
            self.reset()
            return None

        available = [it for it in self.items if it not in self.used_items]

        if not available:
            self.reset()
            available = [it for it in self.items if it not in self.used_items]
            if not available:
                return None

        choice = random.choice(available)
        self.used_items.append(choice)
        return choice

    def reset(self):
        """Make all items available for selection again."""
        self.used_items.clear()


class SenseClueGenerator:
    """Singleton that combines clues and sensory experiences into narratives."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.clue_selector = RandomItemSelector(clues)
            cls._instance.sense_selector = RandomItemSelector(sense_exp)
        return cls._instance

    def get_senseclue(self):
        """Combine a random clue and sensory experience into a narrative."""
        clue = self.clue_selector.pull_random_item()
        sense = self.sense_selector.pull_random_item()

        if clue is None or sense is None:
            return "The room remains silent and still."

        return f"{sense} {clue}"


# Abstract base class
class Encounter(ABC):
    """Abstract base class for adventure encounters."""

    @abstractmethod
    def run_encounter(self) -> encounter_outcome:
        """Execute the encounter and return its outcome."""
        pass


# Encounter implementations
class DefaultEncounter(Encounter):
    """Default encounter that generates a narrative and may end the game."""

    def __init__(self):
        self.generator = SenseClueGenerator()
        self.encounter_count = 0

    def run_encounter(self) -> encounter_outcome:
        """Execute the default encounter and potentially end the game."""
        self.encounter_count += 1
        narrative = self.generator.get_senseclue()
        print(narrative)

        # After 3 encounters, 50% chance to end the game
        if self.encounter_count >= 3 and random.random() < 0.5:
            print("\n✨ You discover the hidden treasure and find the exit!")
            return encounter_outcome.END

        return encounter_outcome.CONTINUE


# Room and Castle
class Room:
    """Represents a room in the adventure."""

    def __init__(self, name: str, encounter: Encounter):
        self.name = name
        self.encounter = encounter

    def visit_room(self) -> encounter_outcome:
        """Visit the room and run its encounter."""
        return self.encounter.run_encounter()


# Create default encounter and rooms
default_encounter = DefaultEncounter()
rooms = [
    Room("The Grand Throne Room", default_encounter),
    Room("The Ancient Library", default_encounter),
    Room("The Spiral Staircase", default_encounter),
    Room("The Dungeon Chamber", default_encounter),
    Room("The Tower Observatory", default_encounter),
    Room("The Courtyard Garden", default_encounter),
]


class Castle:
    """Manages the castle adventure with room selection and navigation."""

    def __init__(self):
        self.room_selector = RandomItemSelector(rooms)

    def select_door(self) -> int:
        """Prompt the user to select a door (2-4 doors available)."""
        num_doors = random.randint(2, 4)
        print(f"\n{'=' * 50}")
        print(f"You stand before {num_doors} doors...")
        for door_num in range(1, num_doors + 1):
            print(f"  Door {door_num}")
        print(f"{'=' * 50}")

        while True:
            try:
                choice = input(f"Select a door (1-{num_doors}): ").strip()
                door_number = int(choice)
                if 1 <= door_number <= num_doors:
                    return door_number
                else:
                    print(f"Invalid choice. Please select a door between 1 and {num_doors}.")
            except ValueError:
                print("Invalid input. Please enter a valid door number.")

    def next_room(self) -> encounter_outcome:
        """Navigate to the next room."""
        selected_door = self.select_door()
        print(f"\nYou open Door {selected_door}...\n")

        room = self.room_selector.pull_random_item()
        if room is None:
            print("The room seems empty and void.")
            return encounter_outcome.CONTINUE

        print(f"You enter: {room.name}")
        print("-" * 50)
        result = room.visit_room()
        print("-" * 50)
        return result

    def reset(self):
        """Reset the room selector."""
        self.room_selector.reset()


class Game:
    """Main game controller for the castle adventure."""

    def __init__(self):
        self.castle = Castle()

    def play_game(self):
        """Start and run the main game loop."""
        print("\n" + "=" * 60)
        print("WELCOME TO THE CASTLE ADVENTURE")
        print("=" * 60)
        print("\nObjective: Navigate through the mysterious castle,")
        print("exploring each room and uncovering its secrets.")
        print("Your goal is to find the hidden treasure and escape!\n")
        print("=" * 60 + "\n")

        while True:
            outcome = self.castle.next_room()

            if outcome == encounter_outcome.END:
                print("\n" + "=" * 60)
                print("🏰 ADVENTURE COMPLETE 🏰")
                print("=" * 60)

                replay = input("\nWould you like another adventure? (yes/no): ").strip().lower()
                if replay in ['yes', 'y']:
                    print("\nPreparing a new castle...\n")
                    self.castle = Castle()
                    continue
                else:
                    print("\nThank you for playing! Farewell, adventurer.\n")
                    print("=" * 60 + "\n")
                    break


def main():
    """Main entry point for the game."""
    game = Game()
    game.play_game()


if __name__ == "__main__":
    main()
