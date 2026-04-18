import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

# --- Templates for each class ---

# Hate Speech (label=0): targets protected groups
hate_templates = [
    "All {group} are {negative_adj} and should be {action}",
    "{group} don't deserve to live in this country",
    "I hate {group} they are ruining everything",
    "We need to get rid of all {group} from our society",
    "{group} are inferior to us in every way",
    "Every single {group_member} I've met is {negative_adj}",
    "The world would be better without {group}",
    "{group} are nothing but {slur} and should know their place",
    "Why do we let {group} into our country they are all {negative_adj}",
    "These {group} are the reason our country is failing",
    "Ban all {group} from entering our borders",
    "{group} are subhuman and deserve nothing",
    "I wish all {group} would just disappear",
    "No {group_member} should be allowed to {activity}",
    "{group} are genetically {negative_adj} it's a fact",
    "Death to all {group} they are a plague on society",
    "Every {group_member} is a criminal waiting to happen",
    "{group} should be shipped back where they came from",
    "Real people don't associate with {group}",
    "The problem with this world is too many {group}",
    "Keep {group} away from our children",
    "{group} are destroying our culture and values",
    "There is no place for {group} in civilized society",
    "I can't stand being around {group} they disgust me",
    "All {group} should be locked up permanently",
    "{group} contribute nothing positive to society",
    "Our ancestors fought to keep {group} out for good reason",
    "{group} are the enemy of decent people everywhere",
    "Someone needs to teach {group} a lesson",
    "Pure {negative_adj} behavior from {group} as usual",
]

groups = [
    "immigrants", "foreigners", "refugees", "minorities", "outsiders",
    "those people", "them", "these people", "that community", "their kind",
]

group_members = [
    "immigrant", "foreigner", "refugee", "outsider", "one of them",
]

negative_adjs = [
    "disgusting", "worthless", "pathetic", "terrible", "horrible",
    "lazy", "stupid", "dangerous", "violent", "inferior",
    "useless", "barbaric", "primitive", "filthy", "vile",
]

actions = [
    "removed", "deported", "banned", "eliminated", "expelled",
    "punished", "silenced", "excluded", "isolated", "destroyed",
]

slurs = [
    "trash", "scum", "parasites", "vermin", "animals",
    "savages", "cockroaches", "pests", "filth", "garbage",
]

activities = [
    "vote", "work here", "attend school", "own property", "have rights",
    "speak in public", "hold office", "get education", "walk freely", "exist peacefully",
]

# Offensive (label=1): rude/profane but not targeting protected groups
offensive_templates = [
    "You're such a {insult} I can't believe it",
    "Shut the {expletive} up nobody cares",
    "What a {insult} thing to say you {insult}",
    "Go {expletive} yourself you piece of {expletive}",
    "You're the biggest {insult} I've ever seen",
    "That's the dumbest {expletive} thing I've ever heard",
    "This is complete {expletive} and everyone knows it",
    "You have no {expletive} clue what you're talking about",
    "I don't give a {expletive} about your opinion",
    "What a load of {expletive} you're spewing",
    "Get the {expletive} out of here with that nonsense",
    "You're a complete waste of {expletive} space",
    "Nobody likes you because you're a {insult}",
    "Stop being such a {insult} all the time",
    "This {expletive} sucks so bad it's unbelievable",
    "You don't know {expletive} about anything",
    "That was the most {insult} performance ever",
    "I'm so {expletive} tired of this {expletive}",
    "Your opinion is {expletive} garbage",
    "Why are you so {insult} all the time",
    "Can you be any more {insult} seriously",
    "You {insult} stop wasting everyone's time",
    "That's absolutely {insult} behavior from you",
    "Screw you and your {insult} attitude",
    "You make me want to {expletive} scream",
    "This is the worst {expletive} thing I've seen today",
    "You're acting like a total {insult} right now",
    "I hate dealing with {insult} people like you",
    "Your {insult} comments are so annoying",
    "How {insult} can one person possibly be",
]

insults = [
    "stupid", "idiotic", "moronic", "pathetic", "ridiculous",
    "dumb", "brainless", "clueless", "incompetent", "dense",
    "obnoxious", "annoying", "disgusting", "terrible", "awful",
]

expletives = [
    "damn", "freaking", "bloody", "effing", "flipping",
    "frigging", "blasted", "crappy", "lousy", "stinking",
]

# Clean (label=2): normal social media posts
clean_templates = [
    "Just had an amazing {meal} at {place} today",
    "I love spending time with my {relation} on weekends",
    "The weather is so {weather_adj} today perfect for {outdoor_activity}",
    "Just finished reading {book_type} and it was incredible",
    "Can't wait for the {event} this {time_period}",
    "My {pet} did the funniest thing today",
    "Started a new {hobby} and I'm really enjoying it",
    "Great game by {team} tonight what a performance",
    "Just got back from {travel_place} and it was amazing",
    "Working on a new {project_type} project really excited about it",
    "Happy birthday to my wonderful {relation}",
    "Beautiful sunset today the sky was {color} and {color}",
    "Spent the day {indoor_activity} and it was so relaxing",
    "So proud of my {relation} for their achievements",
    "Trying out a new {food_type} recipe tonight wish me luck",
    "The new {entertainment} is absolutely worth watching",
    "Had a productive day at {workplace} feeling accomplished",
    "Morning {drink} and a good {book_type} perfect start to the day",
    "Grateful for all the wonderful people in my life",
    "Just signed up for a {course_type} course so excited to learn",
    "The {season} vibes are real and I'm here for it",
    "Love how the {place} looks during {season}",
    "My {relation} surprised me with {gift} today so sweet",
    "Finally mastered {skill} after weeks of practice",
    "This {food_type} turned out better than expected",
    "Enjoying a quiet {time_period} at home with {relation}",
    "The community event was such a great experience today",
    "Just completed my first {achievement} feeling amazing",
    "Nature walks are the best therapy change my mind",
    "Positive vibes only today has been absolutely wonderful",
    "Learning something new every day keeps life interesting",
    "The {entertainment} concert was mind blowing last night",
    "Volunteering at the {place} was so rewarding",
    "So happy with how my {project_type} project turned out",
    "Can't believe how fast this {time_period} went by",
    "Thankful for good health good friends and good {food_type}",
    "The sunrise this morning was breathtaking",
    "Just adopted a {pet} and I'm already in love",
    "Spent the day helping my {relation} with their {project_type}",
    "This is the best {season} we've had in years",
]

meals = ["breakfast", "lunch", "dinner", "brunch", "snack"]
places = ["the park", "downtown", "the mall", "the beach", "the cafe", "the library", "the museum", "the garden"]
relations = ["family", "friends", "mom", "dad", "sister", "brother", "kids", "grandparents", "partner", "best friend"]
weather_adjs = ["beautiful", "sunny", "warm", "pleasant", "gorgeous", "lovely", "mild", "perfect", "crisp", "clear"]
outdoor_activities = ["hiking", "biking", "walking", "swimming", "running", "fishing", "gardening", "picnicking"]
book_types = ["a mystery novel", "a sci-fi book", "a biography", "a self-help book", "a thriller", "a classic novel"]
events = ["concert", "festival", "game", "workshop", "conference", "exhibition", "carnival", "marathon"]
time_periods = ["weekend", "evening", "afternoon", "morning", "week", "month", "summer", "holiday"]
pets = ["dog", "cat", "puppy", "kitten", "bunny", "parrot", "hamster"]
hobbies = ["painting", "cooking", "photography", "yoga", "guitar", "pottery", "coding", "sketching"]
teams = ["the home team", "our squad", "the champions", "the underdogs", "the legends"]
travel_places = ["the mountains", "the coast", "a road trip", "Europe", "Japan", "a national park"]
project_types = ["coding", "art", "DIY", "science", "music", "writing", "home improvement"]
colors = ["orange", "pink", "purple", "golden", "red", "blue"]
indoor_activities = ["reading", "cooking", "baking", "gaming", "watching movies", "journaling", "meditating"]
food_types = ["pasta", "sushi", "pizza", "salad", "curry", "stir fry", "soup", "dessert", "smoothie"]
entertainments = ["movie", "TV show", "album", "documentary", "podcast", "series", "anime"]
workplaces = ["work", "the office", "the studio", "the lab", "the shop", "school"]
drinks = ["coffee", "tea", "juice", "smoothie", "hot chocolate"]
course_types = ["photography", "coding", "cooking", "language", "fitness", "design", "writing"]
seasons = ["spring", "summer", "autumn", "winter", "fall"]
gifts = ["flowers", "a book", "a surprise party", "a handmade card", "breakfast in bed", "tickets"]
skills = ["cooking pasta", "playing guitar", "solving puzzles", "parallel parking", "public speaking"]
achievements = ["5K run", "marathon", "certification", "semester", "painting", "half marathon"]


def generate_hate_speech(n):
    texts = []
    for _ in range(n):
        template = random.choice(hate_templates)
        text = template.format(
            group=random.choice(groups),
            group_member=random.choice(group_members),
            negative_adj=random.choice(negative_adjs),
            action=random.choice(actions),
            slur=random.choice(slurs),
            activity=random.choice(activities),
        )
        # Add random social media noise
        if random.random() < 0.3:
            text = text.upper()
        if random.random() < 0.2:
            text += " " + random.choice(["!!!", "!!", "...", "smh", "tbh", "fr fr", "no cap"])
        if random.random() < 0.15:
            text = random.choice(["RT: ", "@user ", "replying to @user "]) + text
        texts.append(text)
    return texts


def generate_offensive(n):
    texts = []
    for _ in range(n):
        template = random.choice(offensive_templates)
        text = template.format(
            insult=random.choice(insults),
            expletive=random.choice(expletives),
        )
        if random.random() < 0.25:
            text = text.upper()
        if random.random() < 0.2:
            text += " " + random.choice(["lmao", "smh", "bruh", "ffs", "ugh", "jfc"])
        if random.random() < 0.1:
            text = random.choice(["RT: ", "@user "]) + text
        texts.append(text)
    return texts


def generate_clean(n):
    texts = []
    for _ in range(n):
        template = random.choice(clean_templates)
        text = template.format(
            meal=random.choice(meals),
            place=random.choice(places),
            relation=random.choice(relations),
            weather_adj=random.choice(weather_adjs),
            outdoor_activity=random.choice(outdoor_activities),
            book_type=random.choice(book_types),
            event=random.choice(events),
            time_period=random.choice(time_periods),
            pet=random.choice(pets),
            hobby=random.choice(hobbies),
            team=random.choice(teams),
            travel_place=random.choice(travel_places),
            project_type=random.choice(project_types),
            color=random.choice(colors),
            indoor_activity=random.choice(indoor_activities),
            food_type=random.choice(food_types),
            entertainment=random.choice(entertainments),
            workplace=random.choice(workplaces),
            drink=random.choice(drinks),
            course_type=random.choice(course_types),
            season=random.choice(seasons),
            gift=random.choice(gifts),
            skill=random.choice(skills),
            achievement=random.choice(achievements),
        )
        if random.random() < 0.15:
            text += " " + random.choice(["#blessed", "#love", "#happy", "#grateful", "#life", "#vibes"])
        if random.random() < 0.1:
            text += " " + random.choice(["<3", ":)", "xo", "yay"])
        texts.append(text)
    return texts


def main():
    n_hate = 3000       # 20%
    n_offensive = 3750  # 25%
    n_clean = 8250      # 55%

    hate_texts = generate_hate_speech(n_hate)
    offensive_texts = generate_offensive(n_offensive)
    clean_texts = generate_clean(n_clean)

    data = []
    for text in hate_texts:
        data.append({"text": text, "label": 0})
    for text in offensive_texts:
        data.append({"text": text, "label": 1})
    for text in clean_texts:
        data.append({"text": text, "label": 2})

    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Add 5% label noise for realism
    noise_idx = np.random.choice(len(df), size=int(0.05 * len(df)), replace=False)
    for idx in noise_idx:
        original = df.at[idx, "label"]
        choices = [l for l in [0, 1, 2] if l != original]
        df.at[idx, "label"] = random.choice(choices)

    df.to_csv("hate_speech_data.csv", index=False)
    print(f"Dataset generated: {len(df)} rows")
    print(f"  Hate Speech (0): {len(df[df['label'] == 0])}")
    print(f"  Offensive (1):   {len(df[df['label'] == 1])}")
    print(f"  Clean (2):       {len(df[df['label'] == 2])}")
    print("Saved to hate_speech_data.csv")


if __name__ == "__main__":
    main()
