import datetime
import json
from events import Event


class EventManager:
    def __init__(self):
        self.events = []

    def load_events(self):
        """
        Loads the list of events from the 'events.txt' file.
        Filters events that occur in the future.
        """
        try:
            with open('events.txt', 'r') as file:
                events_data = json.load(file)
                now = datetime.datetime.now()

                for event_data in events_data:
                    event = Event(**event_data)
                    event_datetime = datetime.datetime.strptime(event.date + ' ' + event.start_time, '%Y-%m-%d %H:%M')

                    if event_datetime > now:
                        self.events.append(event)

        except FileNotFoundError:
            pass

    def save_events(self):
        """
        Saves the list of events to the 'events.txt' file.
        """
        with open('events.txt', 'w') as file:
            events_data = [event.to_dict() for event in self.events]
            json.dump(events_data, file)

    def add_event(self):
        """
        Adds a new event to the list.
        """
        print("[------------------------------------]")
        print("Enter event information:")
        name = input("Name: ")
        date = self.get_valid_date_input("Date (YYYY-MM-DD): ")
        start_time = self.get_valid_time_input("Start time (HH:MM): ")
        end_time = self.get_valid_time_input("End time (HH:MM): ")
        location = input("Location: ")

        event = Event(name, date, start_time, end_time, location)
        self.events.append(event)
        self.save_events()
        print("Event added")

    def get_valid_date_input(self, message):
        """
        Checks the validity of the entered date.
        Returns the entered date if it is valid.
        """
        while True:
            date_input = input(message)
            try:
                datetime.datetime.strptime(date_input, "%Y-%m-%d")
                return date_input
            except ValueError:
                print("Incorrect date format. Please try again. Example: 2023-08-29")

    def get_valid_time_input(self, message):
        """
        Checks the validity of the entered time.
        Returns the entered time if it is valid.
        """
        while True:
            time_input = input(message)
            try:
                datetime.datetime.strptime(time_input, "%H:%M")
                return time_input
            except ValueError:
                print("Incorrect time format. Please try again. Example: 09:37")

    def view_events(self):
        """
        Displays the list of events or performs a search by date.
        """
        print("[------------------------------------]")
        if not self.events:
            print("No events available")
            return

        print("1. Show all events")
        print("2. Search by date")
        choice = input("Select an action:")
        print("[------------------------------------]")
        if choice == '1':
            sorted_events = sorted(
                self.events,
                key=lambda event: datetime.datetime.strptime(event.date + ' ' + event.start_time, '%Y-%m-%d %H:%M')
            )
            for i, event in enumerate(sorted_events):
                print(f"[{i + 1}] {event}")
        elif choice == '2':
            date = self.get_valid_date_input("Enter the date for the search (YYYY-MM-DD): ")
            filtered_events = [event for event in self.events if event.date == date]
            if filtered_events:
                for i, event in enumerate(filtered_events):
                    print(f"[{i + 1}] {event}")
            else:
                print("No events on the specified date")
        else:
            print("Invalid choice. Please try again.")

    def edit_event(self):
        """
        Edits the selected event from the list.
        """
        print("[------------------------------------]")
        self.view_events()

        event_number = input("Enter the event number to edit (0 - return to the action menu): ")
        if event_number == '0':
            return

        try:
            event_number = int(event_number)
            event_index = event_number - 1

            if 0 <= event_index < len(self.events):
                event = self.events[event_index]
                print("[------------------------------------]")
                print("Enter new event information:")
                name = input("Name: ")
                date = input("Date (YYYY-MM-DD): ")
                start_time = input("Start time (HH:MM): ")
                end_time = input("End time (HH:MM): ")
                location = input("Location: ")

                event.name = name
                event.date = date
                event.start_time = start_time
                event.end_time = end_time
                event.location = location

                self.save_events()
                print("Event edited successfully")
            else:
                print("Invalid event number")
        except ValueError:
            print("Invalid event number")

    def delete_event(self):
        """
        Deletes the selected event from the list.
        """
        self.view_events()
        print("[------------------------------------]")
        event_number = input("Enter the event number to delete (0 - return to the action menu): ")
        if event_number == '0':
            return

        try:
            event_number = int(event_number)
            event_index = event_number - 1

            if 0 <= event_index < len(self.events):
                event = self.events.pop(event_index)

                self.save_events()
                print("Event deleted and moved to the archive successfully")
            else:
                print("Invalid event number")
        except ValueError:
            print("Invalid event number")

    def display_menu(self):
        """
        Displays the main program menu.
        """
        current_event = self.get_current_event()
        print("[------------------------------------]")
        print(f"[Current] - {current_event}\n")
        print("Select an action:")
        print("1. View events")
        print("2. Add an event")
        print("3. Edit an event")
        print("4. Delete an event")
        print("0. Exit the program")

    def get_current_event(self):
        """
        Returns the nearest event that has not yet occurred.
        If there is no such event, returns an empty string.
        """
        now = datetime.datetime.now()
        for event in self.events:
            event_datetime = datetime.datetime.strptime(event.date + ' ' + event.start_time, '%Y-%m-%d %H:%M')
            if event_datetime > now:
                return event
        return ""

    def run(self):
        """
        Starts the program and executes the main loop.
        """
        self.load_events()

        while True:
            self.display_menu()
            choice = input("Enter the action number:")

            if choice == '1':
                self.view_events()
            elif choice == '2':
                self.add_event()
            elif choice == '3':
                self.edit_event()
            elif choice == '4':
                self.delete_event()
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

        print("Program finished.")
        self.save_events()

if __name__ == "__main__":
    event_manager = EventManager()
    event_manager.run()
