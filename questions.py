"""
The fermi-estimation question bank is stored here. The bank is under the functions.
"""
import math


def by_category(category):
    """Return all questions in a given category."""
    return [q for q in QUESTIONS if q["category"] == category]


def categories():
    """Return the sorted set of category names."""
    return sorted({q["category"] for q in QUESTIONS})

def get_score(question, low, high, k):
    """
    Converts user's entered range into a scaled interval score.
    The higher the user's range, the lower their score is since precision is what's being rewarded. 
    The smaller the range, the higher their score because they were more confident.
    The score also increases if the correct answer was included in the range.
    If the answer does not fall within range, ranges that are further off will 
    have lower scores than ranges that are closer. The constant k determines the intensity
    of this effect, meaning how much users should be punished based on how far their guesses
    were from the actual numbers.
    When calculating, the raw score follows "lower is better", then gets normalized to higher is better.

    """
    answer = question["answer"]
    hit = low <= answer <= high
    width = math.log10(high / low) #  if low > 0 and high > 0 else float("inf")
    #^^^ this gets the range using a proportion
    # log function compresses differences in high ranges, but intensifies them at lower ranges.
        #meaning (100, 105) and (100, 110) are more significantly different than (1, 9000) and (1, 10,000)
    # (for clarification, a lower final score is better)
    score = 0
    a = 10 / k # used as multiplier, so lower k makes scoring harsher
    if not hit: # only increase score if answer was missed (lower score is better)
        if answer > high: # if upper bound was closer 
            score = width + a * math.log10(answer / high)
        else: # if lower bound was closer 
            score = width + a * math.log10(low / answer)
    else: # if answer was in range, score should just be based on width (no extra added)
        score = width

    norm_score = 100 / (1 + score) 
    #^^^ normalizing score so that higher is better
    #if 'score' was 0, then final score would be 100
        # this is because it means the user's range was just 1 number that was correct, so they got the perfect score.
    
    return norm_score, hit, width

"""
Fermi-estimation question bank.

Each question has a single numerical answer. Intended for a calibration game
where the player submits a (low, high) range and scores if the true answer falls
inside it. The score also changes based on how wide or narrow the range was.
Scoring is done by the score() function above. 

Fields:
    id       - stable slug id (lowercase words joined by underscores)
    question - the prompt text
    answer   - the accepted true value as a float
    display  - human-readable answer string
    unit     - unit of measure
    category - loose topic grouping
"""

QUESTIONS = [
    {
        "id": "un_member_states",
        "question": "How many member states does the United Nations have?",
        "answer": 193,
        "display": "193",
        "unit": "countries",
        "category": "geography",
    },
    {
        "id": "active_satellites",
        "question": "How many active satellites are currently orbiting Earth?",
        "answer": 11_000,
        "display": "~11,000",
        "unit": "satellites",
        "category": "tech",
    },
    {
        "id": "youtube_upload_rate",
        "question": "How many hours of video are uploaded to YouTube every "
                    "minute?",
        "answer": 500,
        "display": "~500",
        "unit": "hours per minute",
        "category": "tech",
    },
    {
        "id": "walmart_stores",
        "question": "How many Walmart stores are there in the United States?",
        "answer": 4_600,
        "display": "~4,600",
        "unit": "stores",
        "category": "business",
    },
    {
        "id": "daily_blinks",
        "question": "How many times does the average person blink per day?",
        "answer": 17_000,
        "display": "~15,000-20,000",
        "unit": "blinks",
        "category": "body",
    },
    {
        "id": "quarter_ridges",
        "question": "How many ridges are on the edge of a US quarter?",
        "answer": 119,
        "display": "119",
        "unit": "ridges",
        "category": "objects",
    },
    {
        "id": "us_counties",
        "question": "How many counties (and county equivalents) are in the "
                    "United States?",
        "answer": 3_143,
        "display": "3,143",
        "unit": "counties",
        "category": "geography",
    },
    {
        "id": "mcdonalds_locations",
        "question": "How many McDonald's locations are there worldwide?",
        "answer": 43_500,
        "display": "~43,500",
        "unit": "locations",
        "category": "business",
    },
    {
        "id": "minnesota_lakes",
        "question": "How many lakes of 10 acres or more are in Minnesota?",
        "answer": 11_842,
        "display": "11,842",
        "unit": "lakes",
        "category": "geography",
    },
    {
        "id": "hen_eggs_per_year",
        "question": "How many eggs does a commercial laying hen produce per "
                    "year?",
        "answer": 280,
        "display": "~280",
        "unit": "eggs",
        "category": "food",
    },
    {
        "id": "everest_height",
        "question": "How tall is Mount Everest, in feet?",
        "answer": 29_032,
        "display": "29,032 ft (8,849 m)",
        "unit": "feet",
        "category": "geography",
    },
    {
        "id": "wikipedia_articles",
        "question": "How many articles are in the English-language Wikipedia?",
        "answer": 7_000_000,
        "display": "~7 million",
        "unit": "articles",
        "category": "tech",
    },
    {
        "id": "gas_stations",
        "question": "How many gas stations are there in the United States?",
        "answer": 145_000,
        "display": "~145,000",
        "unit": "stations",
        "category": "business",
    },
    {
        "id": "body_cells",
        "question": "How many cells are in the human body?",
        "answer": 30_000_000_000_000,
        "display": "~30 trillion",
        "unit": "cells",
        "category": "body",
    },
    {
        "id": "observable_galaxies",
        "question": "How many galaxies are in the observable universe?",
        "answer": 2_000_000_000_000,
        "display": "~2 trillion",
        "unit": "galaxies",
        "category": "space",
    },
    {
        "id": "milky_way_stars",
        "question": "How many stars are in the Milky Way?",
        "answer": 200_000_000_000,
        "display": "~100-400 billion",
        "unit": "stars",
        "category": "space",
    },
    {
        "id": "starbucks_locations",
        "question": "How many Starbucks locations are there worldwide?",
        "answer": 40_000,
        "display": "~40,000",
        "unit": "locations",
        "category": "business",
    },
    {
        "id": "cars_in_use",
        "question": "How many cars and light trucks are in use worldwide?",
        "answer": 1_500_000_000,
        "display": "~1.5 billion",
        "unit": "vehicles",
        "category": "tech",
    },
    {
        "id": "daily_flights",
        "question": "How many commercial flights take off worldwide each day?",
        "answer": 100_000,
        "display": "~100,000",
        "unit": "flights",
        "category": "geography",
    },
    {
        "id": "windows_per_house",
        "question": "How many windows are in the average American house?",
        "answer": 23,
        "display": "~23",
        "unit": "windows",
        "category": "objects",
    },
    {
        "id": "beach_sand_grains",
        "question": "How many grains of sand are on all the beaches on Earth?",
        "answer": 7_500_000_000_000_000_000,
        "display": "~7.5 quintillion (7.5 x 10^18)",
        "unit": "grains",
        "category": "nature",
    },
    {
        "id": "daily_google_searches",
        "question": "How many Google searches happen per day?",
        "answer": 8_500_000_000,
        "display": "~8.5 billion",
        "unit": "searches",
        "category": "tech",
    },
    {
        "id": "nyc_subway_riders",
        "question": "How many people ride the New York City subway on an "
                    "average weekday?",
        "answer": 4_000_000,
        "display": "~4 million",
        "unit": "riders",
        "category": "geography",
    },
    {
        "id": "empire_state_bricks",
        "question": "How many bricks were used to build the Empire State "
                    "Building?",
        "answer": 10_000_000,
        "display": "~10 million",
        "unit": "bricks",
        "category": "objects",
    },
    {
        "id": "world_languages",
        "question": "How many languages are spoken in the world today?",
        "answer": 7_150,
        "display": "~7,150",
        "unit": "languages",
        "category": "nature",
    },
    {
        "id": "us_paved_roads",
        "question": "How many miles of paved road are in the United States?",
        "answer": 2_800_000,
        "display": "~2.8 million",
        "unit": "miles",
        "category": "geography",
    },
    {
        "id": "philippines_islands",
        "question": "How many islands does the Philippines have?",
        "answer": 7_641,
        "display": "7,641",
        "unit": "islands",
        "category": "geography",
    },
    {
        "id": "spotify_tracks",
        "question": "How many songs (tracks) are on Spotify?",
        "answer": 100_000_000,
        "display": "~100 million",
        "unit": "tracks",
        "category": "tech",
    },
    {
        "id": "smartphones_sold_yearly",
        "question": "How many smartphones are sold worldwide each year?",
        "answer": 1_200_000_000,
        "display": "~1.2 billion",
        "unit": "phones",
        "category": "tech",
    },
    {
        "id": "humans_ever_lived",
        "question": "How many humans have ever lived?",
        "answer": 117_000_000_000,
        "display": "~117 billion",
        "unit": "people",
        "category": "nature",
    },
    {
        "id": "golf_ball_dimples",
        "question": "How many dimples are on a typical golf ball?",
        "answer": 336,
        "display": "~336",
        "unit": "dimples",
        "category": "objects",
    },
    {
        "id": "earth_trees",
        "question": "How many trees are on Earth?",
        "answer": 3_000_000_000_000,
        "display": "~3 trillion",
        "unit": "trees",
        "category": "nature",
    },
    {
        "id": "great_wall_length",
        "question": "How long is the Great Wall of China, in miles?",
        "answer": 13_171,
        "display": "~13,171 miles",
        "unit": "miles",
        "category": "geography",
    },
    {
        "id": "piano_keys",
        "question": "How many keys are on a standard piano?",
        "answer": 88,
        "display": "88",
        "unit": "keys",
        "category": "objects",
    },
    {
        "id": "pizza_slices_per_second",
        "question": "How many slices of pizza do Americans eat per second?",
        "answer": 350,
        "display": "~350",
        "unit": "slices per second",
        "category": "food",
    },
    {
        "id": "card_deck_shuffles",
        "question": "How many distinct ways can a standard 52-card deck be "
                    "shuffled?",
        "answer": 8.07e+67,
        "display": "52! = about 8.07 x 10^67",
        "unit": "arrangements",
        "category": "objects",
    },
    {
        "id": "eiffel_tower_rivets",
        "question": "How many rivets hold the Eiffel Tower together?",
        "answer": 2_500_000,
        "display": "~2.5 million",
        "unit": "rivets",
        "category": "objects",
    },
    {
        "id": "brain_neurons",
        "question": "How many neurons are in the human brain?",
        "answer": 86_000_000_000,
        "display": "~86 billion",
        "unit": "neurons",
        "category": "body",
    },
    {
        "id": "us_zip_codes",
        "question": "How many ZIP codes are there in the United States?",
        "answer": 41_700,
        "display": "~41,700",
        "unit": "ZIP codes",
        "category": "geography",
    },
    {
        "id": "earth_ants",
        "question": "How many ants are alive on Earth at any given moment?",
        "answer": 20_000_000_000_000_000,
        "display": "~20 quadrillion",
        "unit": "ants",
        "category": "nature",
    },
    {
        "id": "head_hairs",
        "question": "How many hairs are on an average human head?",
        "answer": 100_000,
        "display": "~100,000",
        "unit": "hairs",
        "category": "body",
    },
    {
        "id": "tokyo_population",
        "question": "What is the population of the Tokyo metropolitan area?",
        "answer": 37_000_000,
        "display": "~37 million",
        "unit": "people",
        "category": "geography",
    },
    {
        "id": "small_intestine_length",
        "question": "How long is the human small intestine?",
        "answer": 20,
        "display": "~20 feet (6 m)",
        "unit": "feet",
        "category": "body",
    },
    {
        "id": "cell_dna_length",
        "question": "If you uncoiled the DNA in a single human cell, how long "
                    "would it be?",
        "answer": 6,
        "display": "~6 feet (2 m)",
        "unit": "feet",
        "category": "body",
    },
    {
        "id": "tootsie_pop_licks",
        "question": "How many licks does it take to reach the center of a "
                    "Tootsie Pop, according to the Purdue University study?",
        "answer": 364,
        "display": "364",
        "unit": "licks",
        "category": "food",
    },
    {
        "id": "strawberry_seeds",
        "question": "How many seeds are on the outside of an average "
                    "strawberry?",
        "answer": 200,
        "display": "~200",
        "unit": "seeds",
        "category": "food",
    },
    {
        "id": "daily_emails",
        "question": "How many emails are sent worldwide each day?",
        "answer": 360_000_000_000,
        "display": "~360 billion",
        "unit": "emails",
        "category": "tech",
    },
    {
        "id": "eiffel_tower_steps",
        "question": "How many steps are there to the top of the Eiffel Tower?",
        "answer": 1_665,
        "display": "1,665",
        "unit": "steps",
        "category": "objects",
    },
    {
        "id": "human_bones",
        "question": "How many bones are in the adult human body?",
        "answer": 206,
        "display": "206",
        "unit": "bones",
        "category": "body",
    },
    {
        "id": "daily_heartbeats",
        "question": "How many times does an average human heart beat per day?",
        "answer": 100_000,
        "display": "~100,000",
        "unit": "beats",
        "category": "body",
    },
    {
        "id": "moon_distance",
        "question": "How far is the Moon from Earth, in miles?",
        "answer": 238_900,
        "display": "~238,900 miles (384,400 km)",
        "unit": "miles",
        "category": "space",
    },
]

