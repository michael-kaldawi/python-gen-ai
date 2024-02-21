from time import sleep
import sys
import random
from io import BytesIO
import os
from openai import OpenAI
import webbrowser
import requests
from PIL import Image
import types


def custom_print(text): 
    slow_print(text) if slow_print_opt else print(text)

def slow_print(text):
    for c in text:
        print(c, end="")
        sleep(.03)
    sleep(.5)


### Generative AI client

SECRET_KEY = "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"

client = OpenAI(api_key=SECRET_KEY)

################## Text Answers ###################

# results = lambda: None
# results.cube_a = ""
# results.ladder_a = ""
# results.horse_a = ""
# results.flower_a = ""
# results.storm_a = ""
# results.name = ""

################ Updated Text Answers (image gen) #

results = types.SimpleNamespace()
results.cube = types.SimpleNamespace()
results.ladder = types.SimpleNamespace()
results.horse = types.SimpleNamespace()
results.flower = types.SimpleNamespace()
results.storm = types.SimpleNamespace()

results.name = ""

results.cube.size = ""
results.cube.madeof = ""
results.cube.location = ""
results.cube.appearance = ""

results.ladder.madeof = ""
results.ladder.size = ""
results.ladder.location = ""
results.ladder.appearance = ""

results.horse.location = ""
results.horse.activity = ""
results.horse.direction = ""
results.horse.appearance = ""

results.flower.count = ""
results.flower.appearance = ""
results.flower.location = ""

results.storm.location = ""
results.storm.direction = ""
results.storm.effect = ""
results.storm.appearance = ""

################## Text Constants #################

intro = """Playing the Desert Game is a fun one to me. It goes like this:

The Desert Game

I’m going to share a game with you. This game will reveal incredible traits about whoever plays it; surprise, shock and delight complete strangers, and has kickstarted more friendships than I know how to count. Play along and you’ll see.

I want you to imagine a desert, stretching out as far as your eyes can see.

"""

# Questions

cube_q = """In this desert is a cube. Your first task is to describe the cube. What does it look like? How large is it? What is it made of? Where exactly is it? There are no right answers here, only your answers. Take a moment before you continue – the detail is important.

"""

cube_q_appearance = "What does the cube look like?\n"
cube_q_size = "Describe the size of the cube\n"
cube_q_madeof = "What is the cube made of?\n"
cube_q_location = "Where exactly is the cube (in the desert)?\n"

ladder_q = """As you look at the desert and your cube, you notice there is also a ladder. Your second task \(there are just five\) is to describe the ladder. What is it made of? How big is it? Where is it, in relation to the cube?

"""

ladder_q_madeof = "What is the ladder made of?\n"
ladder_q_size = "How big is it?\n"
ladder_q_location = "Where is it, in relation to the cube?\n"
ladder_q_appearance = "Describe any additional details about the ladder\n"

horse_q = """Now imagine that in the scene there is a horse. (Yes, horse. I didn't say this desert made sense\).

Your third task: describe the horse. Most importantly: where is the horse, and what is it doing? Where, if anywhere, is it going? We’re nearly there now.

"""

horse_q_location = "Where is the horse? (in relation to the cube)\n"
horse_q_activity = "What is the horse doing?\n"
horse_q_direction = "What direction is the horse moving? (if moving)\n"
horse_q_appearance = "Describe the horse: \n"


flower_q = """In the scene before you are flowers. Your penultimate task: describe the flowers. How many are there? What do they look like? Where are they, in relation to the horse, cube, ladder and sand?

"""

flower_q_count = "How many flowers are there? (feel free to be specific or vague; examples: 3, many, countless, scattered, etc.)\n"
flower_q_appearance = "Describe the flowers:\n"
flower_q_location = "Where are they, in relation to the horse, cube, ladder, and sand?"

storm_q = """Final question. In the desert there is a storm. Describe the storm. What type of storm is it? Is it near, or far? What direction is it headed? Does it affect the horse, flowers, cube or ladder?

"""

storm_q_location = "Where is the storm?\n"
storm_q_direction = "What direaction is the storm headed?\n"
storm_q_effect = " Does the storm affect the horse, flowers, cube or ladder?\n"
storm_q_appearance = "Describe the storm's appearance.\n"

results_pretext = """If you've been playing along, this is going to be fun. If you didn’t, I must warn you: the next part ruins your ability to play this game ever again. If you won’t want to ruin it forever, go back now. Trust me.

 """

results_text = """The cube is yourself.

The size is ostensibly your ego: a large cube means you’re pretty sure of yourself, a small cube less so. The vertical placement of the cube is how grounded you are. Resting on the sand? You’re probably pretty down to earth. Floating in the sky? Your head is in the clouds. The cube’s material conveys how open you are: transparent cubes belong to transparent people, opaque cubes are more protective of their minds. Glowing? You’re likely a positive person, who aims to raise the spirits of others. Made of granite? You’re likely protective and resilient.

The trick here is that when asked to describe a blank, abstract entity – a cube – your imagination will tend to project its own identity onto it. This trick is as old as time, but it’s about to get more interesting.

The ladder represents your friends. Are your friends leaning on the cube? Your friends depend on you, and are close. Is the ladder frail, or robust? Tall or short? Does it lead inside the cube? Or is it cast to one side, lying unloved on the sand? By now you should be able to draw your own conclusions.

The horse represents your dream partner. The type of horse reveals a lot about what you yearn for in a partner. Some people see a steady brown workhorse, others a shining pegasus or unicorn. Make of these people what you will. Is your horse nuzzling your cube affectionately, or taking a bite out of it? Is it far from your cube, or walking away? This can represent a current partner, or an aspirational one, but the results are often a mix of touching and hilarious.

The flowers represent children. The number of flowers relates to how many you imagine having. Some people see just a single, withered daisy; others a resplendent garden covering the cube and desert beneath. (Guys: watch out for those). The colour and vitality of the flowers can speak to their health and presumed prosperity. The placement – particularly in relation to the cube – can reveal interesting relations; I met one woman whose horse was eating their flowers.

Finally, the storm represents threat. This speaks to the current state of the person, and how they perceive risk in their life. Some may see a distant storm, on the lip of the horizon, fading from sight. Others may view themselves in the midst of a thunderous apocalypse, hailstones the size of tennis balls pelting their fragile cube and horse. Chances are those people have some immediate trauma in their life.

Now is this all correct? Of course it isn’t. You won’t be reading any peer-reviewed journals on the soothsaying properties of horses and ladders. This is a game, albeit one that has endured in various forms for thousands of years. But if you play along – and I encourage you to try this on others – you will find it appears to have an uncanny sense of reliability to it. There might be many reasons: people seem to project themselves onto abstract objects (the cube), and their affections onto animals (the horse). Our nurturing of flowers bears some resemblance to that of children, a storm is a signal of environmental danger that taps into our sense of unease, and a ladder is something we find supporting. Maybe it’s all just wishful psychobabble. But I’ll tell you what. It’s an incredible tool for getting to know someone. In five minutes you’re able to discuss a stranger’s character, friends, partner, children, risks, dreams and aspirations. You will stand out as someone memorable, and you probably had a right laugh too.

"""

### slow print option 
# slow_print("\nType 1 to go through all of the dialogue quickly! Or press Enter to continue at a normal pace.\n")

# slow_a = input()
slow_print_opt = 1

# if(slow_a == "1"):
#     # don't slow print
#     slow_print_opt = 0

### Intro and questions
custom_print(intro)
input("Press Enter to continue... \n")

custom_print("Please enter your name: ")
results.name = input()
print("\n")

### Collect Results

# cube
custom_print(cube_q)
custom_print(cube_q_size)
results.cube.size = input()
custom_print(cube_q_location)
results.cube.location = input()
custom_print(cube_q_madeof)
results.cube.madeof = input()
custom_print(cube_q_appearance)
results.cube.appearance = input()
#results.cube_a = input()

custom_print(ladder_q)
custom_print(ladder_q_size)
results.ladder.size = input()
custom_print(ladder_q_location)
results.ladder.location = input()
custom_print(ladder_q_madeof)
results.ladder.madeof = input()
custom_print(ladder_q_appearance)
results.ladder.appearance = input()
# results.ladder_a = input()

custom_print(horse_q)
custom_print(horse_q_location)
results.horse.location = input()
custom_print(horse_q_activity)
results.horse.activity = input()
custom_print(horse_q_appearance)
results.horse.appearance = input()
custom_print(horse_q_direction)
results.horse.direction = input()
# results.horse_a = input()

custom_print(flower_q)
custom_print(flower_q_count)
results.flower.count = input()
custom_print(flower_q_appearance)
results.flower.appearance = input()
custom_print(flower_q_location)
results.flower.location = input()
# results.flower_a = input()

custom_print(storm_q)
custom_print(storm_q_location)
results.storm.location = input()
custom_print(storm_q_appearance)
results.storm.appearance = input()
custom_print(storm_q_direction)
results.storm.direction = input()
custom_print(storm_q_effect)
results.storm.effect = input()
# results.storm_a = input()


### Results
custom_print("\nYour Results: \n")
custom_print(vars(results))

input("Press Enter to continue... ")

custom_print(results_text)

### Write results to file. 
# filename = results.name + str(random.randrange(1,10000000,1)) + ".txt"
# file = open(filename, "w")
# file.write("Results:\n")
# file.write("Name: " + results.name + "\n")
# file.write("Cube: " + results.cube_a + "\n")
# file.write("Ladder: " + results.ladder_a + "\n")
# file.write("Horse: " + results.horse_a + "\n")
# file.write("Flower: " + results.flower_a + "\n")
# file.write("Storm: " + results.storm_a + "\n\n")

# file.close()

### Pass Results to generative AI for a visualization!

# construct the prompt
prompt_descriptor = "In a vast desert landscape, stretching out as far as the eye can see, lies a " + results.cube.size + " " + results.cube.madeof + " cube at " + results.cube.location + ". The cube looks like: " + results.cube.appearance + "." + "There is a " + results.ladder.size + " ladder, made of " + results.ladder.madeof + " which is " + results.ladder.location + " The ladder looks like: " + results.ladder.appearance + ". There is a " + results.horse.appearance + " horse " + results.horse.activity + ". The horse is " + results.horse.location + ", and " + results.horse.direction + ". There are " + results.flower.count + " " + results.flower.appearance + " flowers. The flowers are " + results.flower.location + ". A " + results.storm.appearance + " storm is " + results.storm.location + ", and " + results.storm.direction + ". The storm affects the cube, flowers, ladder, and horse in the following way: " + results.storm.effect + "."

response = client.images.generate(
  model="dall-e-3",
  prompt=prompt_descriptor,
  size="1024x1024",
  quality="standard",
  n=1
)
image_url = response.data[0].url

webbrowser.open(image_url)

# write the image to a file
image = requests.get(image_url).content

f = open(str("img" + str(random.randrange(1,10000000)) + ".png"), 'wb')
f.write(image)
f.close()

### Ending

input("""Thank you for playing! Your results have been saved. Press enter to continue. """)