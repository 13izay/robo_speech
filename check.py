import csv
import Levenshtein
#from fuzzywuzzy import fuzz   uncomment when using fuzzymatching

# CSV file path
csv_file = 'lookup.csv'

# Pre-defined name variants list
name_variants_list = [
    "rafiei", "andisheh rafiei", "andisheh", "schwiedel", "cinja schwiedel", "cinja",
    "weyrich", "michael weyrich", "michael", "doctor weyrich", "doctor michael weyrich",
    "professor weyrich", "professor michael weyrich", "professor doctor weyrich", 
    "professor doctor michael weyrich", "mueller", "marion mueller", "marion", 
    "jazdi", "nazer jazdi", "nazer", "doctor jazdi", "doctor nazer jazdi", 
    "professor jazdi", "professor nazer jazdi", "professor doctor jazdi", 
    "professor doctor nazer jazdi", "lenz", "britta lenz", "britta", "bodenstein", 
    "frederike bodenstein", "frederike", "gul", "baran gul", "baran can gul", 
    "baran", "ghasemi", "golsa ghasemi", "golsa", "takacs", "jonas takacs", "jonas", 
    "morozov", "andrey morozov", "andrey", "doctor morozov", "doctor andrey morozov", 
    "professor morozov", "professor andrey morozov", "professor doctor morozov", 
    "professor doctor andrey morozov"
]


class CheckData:
    
    def __init__(self, name_to_check, room_to_check):

        self.name_to_check = name_to_check
        self.room_to_check = room_to_check
        self.name_variants_list = name_variants_list
        self.csv_data = self.load_csv_data()


    def load_csv_data(self):   
        # Load CSV data into a list of dictionaries (name and room pairs)
        data = []
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append({"name": row["name"], "room": row["room"]})
        #print(data)
        return data


    def spell_check(self, name, threshold=4):  # Optional threshold parameter
        closest_name = min(self.name_variants_list, key=lambda variant: Levenshtein.distance(name.lower(), variant.lower()))
        min_distance = Levenshtein.distance(name.lower(), closest_name.lower())
        
        # Return the closest name only if it meets the threshold criteria
        if min_distance <= threshold:
            return closest_name
        else:
            return None  # or some other indicator of "no close match"


    def check_name_in_csv(self, name):
        name_words = name.lower().split()  # Split the input name into individual words
        
        for entry in self.csv_data:
            entry_name_words = entry["name"].lower().split()  # Split the CSV entry name

            # Check if all the words in the input name are in the CSV entry name
            if all(word in entry_name_words for word in name_words):
                return entry["name"], entry["room"]
        
        return None, None


    def check_room_in_csv(self, room):
        room = room.strip()  # Clean the room input
        
        # Iterate through CSV data for room match
        for entry in self.csv_data:
            if room == entry["room"].strip():  # Ensure clean comparison
                return entry["name"], entry["room"]
        
        return None, None


    def process_data(self):
        
        # Case 1: only name is given, no room info, works
        if self.name_to_check != "none" and self.room_to_check == "none":
            corrected_name = self.spell_check(self.name_to_check)
            print(corrected_name)
            name_match, room_match = self.check_name_in_csv(corrected_name)
            print(f"name match from case 1: {name_match}, {room_match}")
            return name_match, room_match

        # Case 2: only room is given, no name info, works
        elif self.name_to_check == "none" and self.room_to_check != "none":
            name_match, room_match = self.check_room_in_csv(self.room_to_check)
            print(f"name match from case 2: {name_match}, {room_match}")
            return name_match, room_match

        # Case 3: both name and room are provided
        elif self.name_to_check != "none" and self.room_to_check != "none" :
            corrected_name = self.spell_check(self.name_to_check)

            name_match, room_match = self.check_name_in_csv(corrected_name)
            if room_match == self.room_to_check:
                print(f"name and room match")
                return name_match, room_match
            
            else:
                print(f"{name_match} alternative room {room_match}")
                return name_match, room_match
            
        else:
            #corrected_name = self.spell_check(self.name_to_check) 
            return f"No match found"

    
if __name__ == "__main__":
    # Example inputs
    name_to_check = "professor morosob"
    room_to_check = "none"

    # Initialize the CheckData class
    matcher = CheckData(name_to_check = name_to_check, room_to_check = room_to_check)

    # Process and get the result
    result = matcher.process_data()

    # Output the result
    print(result)
    


