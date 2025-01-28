'''
Matchmaking algorithm by Wahab Alereefi
'''

import pandas as pd
import itertools


# Load the data from an Excel file
def load_data(file_path):
    return pd.read_excel(file_path)

# Define MBTI compatibility scores for all 16 types
def mbti_compatibility_score(mbti1, mbti2):
    compatibility_matrix = {
        'INTJ': {'INTJ': 3, 'ENTP': 5, 'INFJ': 4, 'INTP': 4, 'ENTJ': 3, 'ENFP': 3, 'ISFP': 2, 'ISTP': 2, 'ESFP': 1, 'ESTP': 1, 'ESFJ': 2, 'ESTJ': 2, 'ISFJ': 3, 'ISTJ': 4, 'INFP': 3, 'ENFJ': 4},
        'ENTP': {'INTJ': 5, 'ENTP': 3, 'INFJ': 5, 'INTP': 4, 'ENTJ': 4, 'ENFP': 4, 'ISFP': 3, 'ISTP': 3, 'ESFP': 3, 'ESTP': 3, 'ESFJ': 2, 'ESTJ': 2, 'ISFJ': 2, 'ISTJ': 3, 'INFP': 4, 'ENFJ': 5},
        'INFJ': {'INTJ': 4, 'ENTP': 5, 'INFJ': 3, 'INTP': 5, 'ENTJ': 4, 'ENFP': 5, 'ISFP': 4, 'ISTP': 3, 'ESFP': 3, 'ESTP': 3, 'ESFJ': 4, 'ESTJ': 3, 'ISFJ': 5, 'ISTJ': 4, 'INFP': 5, 'ENFJ': 5},
        'INTP': {'INTJ': 4, 'ENTP': 4, 'INFJ': 5, 'INTP': 3, 'ENTJ': 4, 'ENFP': 4, 'ISFP': 3, 'ISTP': 4, 'ESFP': 3, 'ESTP': 3, 'ESFJ': 2, 'ESTJ': 2, 'ISFJ': 3, 'ISTJ': 3, 'INFP': 4, 'ENFJ': 4},
        'ENTJ': {'INTJ': 3, 'ENTP': 4, 'INFJ': 4, 'INTP': 4, 'ENTJ': 3, 'ENFP': 4, 'ISFP': 3, 'ISTP': 3, 'ESFP': 3, 'ESTP': 3, 'ESFJ': 3, 'ESTJ': 4, 'ISFJ': 3, 'ISTJ': 4, 'INFP': 4, 'ENFJ': 5},
        'ENFP': {'INTJ': 3, 'ENTP': 4, 'INFJ': 5, 'INTP': 4, 'ENTJ': 4, 'ENFP': 3, 'ISFP': 4, 'ISTP': 3, 'ESFP': 4, 'ESTP': 4, 'ESFJ': 4, 'ESTJ': 3, 'ISFJ': 4, 'ISTJ': 3, 'INFP': 5, 'ENFJ': 5},
        'ISFP': {'INTJ': 2, 'ENTP': 3, 'INFJ': 4, 'INTP': 3, 'ENTJ': 3, 'ENFP': 4, 'ISFP': 3, 'ISTP': 4, 'ESFP': 4, 'ESTP': 4, 'ESFJ': 4, 'ESTJ': 3, 'ISFJ': 4, 'ISTJ': 3, 'INFP': 4, 'ENFJ': 4},
        'ISTP': {'INTJ': 2, 'ENTP': 3, 'INFJ': 3, 'INTP': 4, 'ENTJ': 3, 'ENFP': 3, 'ISFP': 4, 'ISTP': 3, 'ESFP': 3, 'ESTP': 4, 'ESFJ': 3, 'ESTJ': 4, 'ISFJ': 3, 'ISTJ': 3, 'INFP': 3, 'ENFJ': 4},
        'ESFP': {'INTJ': 1, 'ENTP': 3, 'INFJ': 3, 'INTP': 3, 'ENTJ': 3, 'ENFP': 4, 'ISFP': 4, 'ISTP': 3, 'ESFP': 3, 'ESTP': 4, 'ESFJ': 4, 'ESTJ': 4, 'ISFJ': 3, 'ISTJ': 2, 'INFP': 3, 'ENFJ': 4},
        'ESTP': {'INTJ': 1, 'ENTP': 3, 'INFJ': 3, 'INTP': 3, 'ENTJ': 3, 'ENFP': 4, 'ISFP': 4, 'ISTP': 4, 'ESFP': 4, 'ESTP': 3, 'ESFJ': 3, 'ESTJ': 4, 'ISFJ': 3, 'ISTJ': 3, 'INFP': 3, 'ENFJ': 4},
        'ESFJ': {'INTJ': 2, 'ENTP': 2, 'INFJ': 4, 'INTP': 2, 'ENTJ': 3, 'ENFP': 4, 'ISFP': 4, 'ISTP': 3, 'ESFP': 4, 'ESTP': 3, 'ESFJ': 3, 'ESTJ': 4, 'ISFJ': 5, 'ISTJ': 4, 'INFP': 4, 'ENFJ': 5},
        'ESTJ': {'INTJ': 2, 'ENTP': 2, 'INFJ': 3, 'INTP': 2, 'ENTJ': 4, 'ENFP': 3, 'ISFP': 3, 'ISTP': 4, 'ESFP': 4, 'ESTP': 4, 'ESFJ': 4, 'ESTJ': 3, 'ISFJ': 4, 'ISTJ': 5, 'INFP': 3, 'ENFJ': 4},
        'ISFJ': {'INTJ': 3, 'ENTP': 2, 'INFJ': 5, 'INTP': 3, 'ENTJ': 3, 'ENFP': 4, 'ISFP': 4, 'ISTP': 3, 'ESFP': 3, 'ESTP': 3, 'ESFJ': 5, 'ESTJ': 4, 'ISFJ': 3, 'ISTJ': 4, 'INFP': 5, 'ENFJ': 5},
        'ISTJ': {'INTJ': 4, 'ENTP': 3, 'INFJ': 4, 'INTP': 3, 'ENTJ': 4, 'ENFP': 3, 'ISFP': 3, 'ISTP': 3, 'ESFP': 2, 'ESTP': 3, 'ESFJ': 4, 'ESTJ': 5, 'ISFJ': 4, 'ISTJ': 3, 'INFP': 3, 'ENFJ': 4},
        'INFP': {'INTJ': 3, 'ENTP': 4, 'INFJ': 5, 'INTP': 4, 'ENTJ': 4, 'ENFP': 5, 'ISFP': 4, 'ISTP': 3, 'ESFP': 3, 'ESTP': 3, 'ESFJ': 4, 'ESTJ': 3, 'ISFJ': 5, 'ISTJ': 3, 'INFP': 3, 'ENFJ': 5},
        'ENFJ': {'INTJ': 4, 'ENTP': 5, 'INFJ': 5, 'INTP': 4, 'ENTJ': 5, 'ENFP': 5, 'ISFP': 4, 'ISTP': 4, 'ESFP': 4, 'ESTP': 4, 'ESFJ': 5, 'ESTJ': 4, 'ISFJ': 5, 'ISTJ': 4, 'INFP': 5, 'ENFJ': 3}
    }
    return compatibility_matrix.get(mbti1, {}).get(mbti2, 0)

# Adjust columns to match script expectations
def adjust_columns(data):
    column_mapping = {
        "Name": "Name",
        "What's your favourite Hobbies?": "Hobbies",
        "What Social Activities you like ?": "Social Activities",
        "What are you looking for ?": "Looking For",
        "What is your preferred energy level in a partner?": "Energy Level",
        "What’s your ideal way to spend a Friday night": "Friday Night",
        "Choose your favourite beverage": "Favorite Beverage",
        "Describe your sense of humour?": "Sense of Humor",
        "MBTI": "MBTI",
        "Gender": "Gender",
        "Sexuality ": "Sexuality"  #
    }
    return data.rename(columns=column_mapping)

def calculate_score(participant1, participant2):
    score = 0

    # Gender and sexuality matching
    if participant1['Sexuality'] == 'Homosexual':
        if participant1['Gender'] != participant2['Gender']:
            return 0
    elif participant1['Sexuality'] == 'Heterosexual':
        if participant1['Gender'] == participant2['Gender']:
            return 0
    elif participant1['Sexuality'] == 'Bisexual':
        pass  # Bisexual can match with anyone
    else:
        return 0  # Invalid sexuality case

    # Check if the second participant's sexuality is compatible with the first
    if participant2['Sexuality'] == 'Homosexual':
        if participant2['Gender'] != participant1['Gender']:
            return 0
    elif participant2['Sexuality'] == 'Heterosexual':
        if participant2['Gender'] == participant1['Gender']:
            return 0
    elif participant2['Sexuality'] == 'Bisexual':
        pass  # Bisexual can match with anyone

    # If gender and sexuality align, calculate compatibility
    # Check MBTI compatibility (scaled 0 to 5 points)
    score += mbti_compatibility_score(participant1['MBTI'], participant2['MBTI'])

    # Check hobbies (1 point per match, max 3 points)
    hobbies1 = set(participant1['Hobbies'].split(", "))
    hobbies2 = set(participant2['Hobbies'].split(", "))
    shared_hobbies = hobbies1.intersection(hobbies2)
    score += min(3, len(shared_hobbies))

    # Check social activities (1 point per match, max 3 points)
    activities1 = set(participant1['Social Activities'].split(", "))
    activities2 = set(participant2['Social Activities'].split(", "))
    shared_activities = activities1.intersection(activities2)
    score += min(3, len(shared_activities))

    # Check what they are looking for (3 points)
    if participant1['Looking For'] == participant2['Looking For']:
        score += 3

    # Check preferred energy level (3 points)
    if participant1['Energy Level'] == participant2['Energy Level']:
        score += 3

    # Fun compatibility questions (1 point each)
    if participant1['Friday Night'] == participant2['Friday Night']:
        score += 1
    if participant1['Favorite Beverage'] == participant2['Favorite Beverage']:
        score += 1
    if participant1['Sense of Humor'] == participant2['Sense of Humor']:
        score += 1

    return score


# Perform matchmaking
def matchmaking(data):
    matches = []
    for p1, p2 in itertools.combinations(data.to_dict('records'), 2):
        score = calculate_score(p1, p2)
        if score > 0:  # Only include valid matches
            matches.append({
                'Participant 1': p1['Name'],
                'Participant 2': p2['Name'],
                'Compatibility Score': score
            })

    matches_df = pd.DataFrame(matches)
    matches_df = matches_df.sort_values(by='Compatibility Score', ascending=False)
    return matches_df

# Function to create a diverse round-robin schedule for all matches
def create_diverse_schedule(matches_df):
    rounds = []  # List to hold rounds
    assigned_pairs = set()  # To track already assigned pairs

    for round_num in range(4):  # 4 rounds for matchmaking
        current_round = []
        used_participants = set()

        for _, match_row in matches_df.iterrows():
            p1, p2, score = match_row['Participant 1'], match_row['Participant 2'], match_row['Compatibility Score']
            pair = tuple(sorted((p1, p2)))

            if pair not in assigned_pairs and p1 not in used_participants and p2 not in used_participants:
                current_round.append((p1, p2, score))
                assigned_pairs.add(pair)
                used_participants.add(p1)
                used_participants.add(p2)

        rounds.append(current_round)

    return rounds


def assign_tables(schedule, max_tables=25):
    """
    Assign participants to designated tables for each round.
    If there are fewer participants than max_tables, some tables will remain unused.
    """
    table_assignments = []
    for round_num, round_pairs in enumerate(schedule, start=1):
        round_tables = {}
        table_number = 1

        for pair in round_pairs:
            if table_number > max_tables:  # Ensure we don't exceed the number of tables
                break
            round_tables[table_number] = f"{pair[0]} - {pair[1]} (Score: {pair[2]})"
            table_number += 1

        # Fill empty tables with "Unused"
        while table_number <= max_tables:
            round_tables[table_number] = "Unused"
            table_number += 1

        table_assignments.append(round_tables)

    return table_assignments

def generate_participant_match_list(schedule, participants):
    """
    Generate a list of matches for each participant across all rounds.
    If a participant does not have a match in a round, it will be marked as 'No Date'.
    """
    participant_matches = {participant: ["No Date"] * len(schedule) for participant in participants}

    for round_num, round_pairs in enumerate(schedule):
        for pair in round_pairs:
            participant1, participant2 = pair[0], pair[1]
            participant_matches[participant1][round_num] = participant2
            participant_matches[participant2][round_num] = participant1

    # Prepare data for output
    output_data = []
    for participant, matches in participant_matches.items():
        output_data.append({
            "Participant": participant,
            "Round 1": matches[0],
            "Round 2": matches[1] if len(matches) > 1 else "No Date",
            "Round 3": matches[2] if len(matches) > 2 else "No Date",
            "Round 4": matches[3] if len(matches) > 3 else "No Date",
        })

    return pd.DataFrame(output_data)

def main():
    file_path = r"C:\Users\hooba\PycharmProjects\PythonProject\NSA.xlsx"  # Replace with your file path
    output_file_schedule = r"C:\Users\hooba\PycharmProjects\PythonProject\all_participants_schedule.xlsx"
    output_file_participants = r"C:\Users\hooba\PycharmProjects\PythonProject\participant_matches.xlsx"

    data = load_data(file_path)
    data.columns = data.columns.str.strip()  # Normalize column names
    adjusted_data = adjust_columns(data)

    # Perform matchmaking for all participants
    matches_df = matchmaking(adjusted_data)

    if matches_df.empty:
        print("No valid matches found. Exiting.")
        return

    # Create the diverse schedule
    schedule = create_diverse_schedule(matches_df)

    # Assign tables for each round
    max_tables = 25  # You can adjust the number of available tables
    table_assignments = assign_tables(schedule, max_tables=max_tables)

    # Prepare table schedule DataFrame
    output_data_schedule = []
    for round_num, tables in enumerate(table_assignments, start=1):
        for table, assignment in tables.items():
            output_data_schedule.append({
                "Round": round_num,
                "Table": table,
                "Assignment": assignment
            })

    schedule_df = pd.DataFrame(output_data_schedule)

    # Generate participant match list
    participants = adjusted_data['Name'].tolist()
    participant_matches_df = generate_participant_match_list(schedule, participants)

    # Save both outputs to Excel
    schedule_df.to_excel(output_file_schedule, index=False)
    participant_matches_df.to_excel(output_file_participants, index=False)

    print(f"Schedule with table assignments saved to {output_file_schedule}")
    print(f"Participant matches saved to {output_file_participants}")


if __name__ == "__main__":
    main()