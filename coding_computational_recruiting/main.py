#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# This is a solution to HackTheBox "Computational Recruiting" challenge.
# https://app.hackthebox.com/challenges/Computational%2520Recruiting

# Change the variables as needed
HOST = '94.237.59.63'
PORT = 51520
list_file = './data.txt'
the_list = []


# Calculate the skills according the formula recived
# Formula: <skill>_score = round(6 * (int(s) * <skill>_weight)) + 10
def calculate_skill(skill_score, skill_weight):
    health_score = round(6 * (int(skill_score) * skill_weight)) + 10
    return health_score


# Calculate the overall skill accourding the formula we got
# Formula: overall_value = round(5 * ((health * 0.18) + (agility * 0.20) + (charisma * 0.21) + (knowledge * 0.08) + (energy * 0.17) + (resourcefulness * 0.16)))
def calculate_overall_skill(health_score, agility_score, charisma_score, knowledge_score, energy_score, resourcefulness_score):
    overall_value = round(5 * ((health_score * 0.18) + (agility_score * 0.20) + (charisma_score * 0.21) + (knowledge_score * 0.08) + (energy_score * 0.17) + (resourcefulness_score * 0.16)))
    return overall_value


# Class to fit and calculate the candidates skills
class Candidate:
    def __init__(self, vorname, nachname, health, agility, charisma, knowledge, energy, resourcefulness):
        self.name = "{0} {1}".format(vorname, nachname)
        self.health_score = calculate_skill(health, 0.2)
        self.agility_score = calculate_skill(agility, 0.3)
        self.charisma_score = calculate_skill(charisma, 0.1)
        self.knowledge_score = calculate_skill(knowledge, 0.05)
        self.energy_score = calculate_skill(energy, 0.05)
        self.resourcefulness_score = calculate_skill(resourcefulness, 0.3)
        self.overall_value = calculate_overall_skill(self.health_score, self.agility_score, self.charisma_score, self.knowledge_score, self.energy_score, self.resourcefulness_score
)


# Function to read the list, iterate on it's indexes and create a user according the Candidate class
def read_file(file_path):
    candidates_list = []
    for line in open(file_path, "r"):
        candidate_information = line.split()
        user = Candidate(
            candidate_information[0],  # First Name
            candidate_information[1],  # Last Name
            candidate_information[2],  # Health
            candidate_information[3],  # Agility
            candidate_information[4],  # Charisma
            candidate_information[5],  # Knowledge
            candidate_information[6],  # Energy
            candidate_information[7]   # Resourcefulness
        )
        user_info = [user.name, user.overall_value]
        candidates_list.append(user_info)
    return candidates_list
    

# Merge the 2nd level list to create a single string for each candidate
# Example: Name_1 Surname_1 - score_1, Name_2 Surname_2 - score_2, ..., Name_i Surname_i - score_i
def string_minus_array(array):
    stringed_user = "{0} - {1}".format(array[0], array[1])
    return stringed_user


# Communication with the server including data transfer
def comunicate_with_server(data_to_transfer):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("About to connect")
        s.connect((HOST, PORT))

        income_data = s.recv(1204)
        print('Income 01: ' + income_data.decode() + '\n')
        
        print("Sending the list")
        s.sendall(data_to_transfer.encode() + b'\n')  # Send as plain text, not pickled

        response = s.recv(1204)
        print('Server Answer: ' + response.decode())


# Transfer the main (1st) list into a string
def create_data_to_transfer(candidates_list):
    string_data = ''
    for user_array in candidates_list[:13]:  # Up to the second last candidate
        string_data += f'{string_minus_array(user_array)}, '
    string_data += string_minus_array(candidates_list[13])  # Add the last candidate without trailing comma
    return string_data


# Runnnnnnnnnnnnnnnnnnnnnnnn!!!!
def main():
    candidates_list = read_file(list_file)
    sorted_candidates = sorted(candidates_list, key=lambda candidate: candidate[1], reverse=True)
    top_candidates_string = create_data_to_transfer(sorted_candidates)
    
    comunicate_with_server(top_candidates_string)


if __name__ == '__main__':
    main()
