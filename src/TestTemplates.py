class TestTemplates :

    def __init__( self ) :

        self.test_templates    = {
            'template_1' : { 
                'question' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '110',
                    'prompt' : """Consider the following list of frames as defined by FrameNet: 
{}

Generate frames relevant for answering the following question. Make sure that the output frames are from the list above. 

Question: {}

""",
                },
                'fact' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '110',
                    'prompt' : """Consider the following list of frames as defined by FrameNet: 
{}

Generate frames relevant to the following factoid. Make sure that the output frames are from the list above. 

Factoid: {}

""",
                },
            },
            'template_2' : { 
                'question' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Generate frames relevant for answering the following question. Make sure that the output frames are from FrameNet. Only include frams from FrameNet. Do not include any frames not in FrameNet. 

Question: {}

""",
                },
                'fact' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Generate frames relevant to the following factoid. Make sure that the output frames are from FrameNet. Only include frams from FrameNet. Do not include any frames not in FrameNet. 

Factoid: {}

""",
                },
            },
            'template_3' : { 
                'question' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Generate frames relevant for answering the question provided. The output frames must be from FrameNet. Only include frams from FrameNet. Do not include any frames not in FrameNet. Do not include frames about answering questions or reasoning, that is implied. The frames must be useful in retriving factoids that are indexed by frames. Generate frames similar to the example provided in json format. 

Example 1:
Question 1: A population of small, plant-eating beetles lives in a forest. About half of the beetles are light brown and the others are dark green. If years of drought cause the area to become dry with few trees, what would the beetle population most likely look like after several generations?
Frames 1: [
  {{
    "frame": "Surviving",
    "explanation": "Crucial for understanding the adaptive strategies the beetles might employ to cope with the changing environmental conditions."
  }},
  {{
    "frame": "Becoming_dry",
    "explanation": "This frame is relevant because the question describes a change in the environment due to drought, resulting in the area becoming dry."
  }},
  {{
    "frame": "Animals",
    "explanation": "This frame pertains to the beetles as living organisms, which are the subject of the question, focusing on their survival and adaptation."
  }},
  {{
    "frame": "Food",
    "explanation": "Since the beetles are plant-eaters, this frame is relevant due to potential changes in food availability affecting the beetle population."
  }},
  {{
    "frame": "Color",
    "explanation": "Pertinent to the possible changes in the physical appearance of the beetles, particularly if there is a shift in the dominance of color traits (light brown or dark green) due to natural selection."
  }}
]


Question: {}

""",
                },
                'fact' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Generate frames relevant to the following factoid. Make sure that the output frames are from FrameNet. Only include frams from FrameNet. Do not include any frames not in FrameNet. 

Factoid: {}

""",
                },
            },
            'template_4' : { 
                'explore' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Generate frames relevant for answering the question provided. The output frames must be from FrameNet. Do not include frames about answering questions or reasoning, that is implied. The frames must be useful in retriving factoids that are indexed by frames. Make the frames as conceptual as possible. Do not include frames which are metaphorical.

Example 1:
Question 1: A population of small, plant-eating beetles lives in a forest. About half of the beetles are light brown and the others are dark green. If years of drought cause the area to become dry with few trees, what would the beetle population most likely look like after several generations?
Frames 1: [
  {{
    "frame": "Surviving",
    "explanation": "Crucial for understanding the adaptive strategies the beetles might employ to cope with the changing environmental conditions."
  }},
  {{
    "frame": "Becoming_dry",
    "explanation": "This frame is relevant because the question describes a change in the environment due to drought, resulting in the area becoming dry."
  }},
  {{
    "frame": "Animals",
    "explanation": "This frame pertains to the beetles as living organisms, which are the subject of the question, focusing on their survival and adaptation."
  }},
  {{
    "frame": "Food",
    "explanation": "Since the beetles are plant-eaters, this frame is relevant due to potential changes in food availability affecting the beetle population."
  }},
  {{
    "frame": "Color",
    "explanation": "Pertinent to the possible changes in the physical appearance of the beetles, particularly if there is a shift in the dominance of color traits (light brown or dark green) due to natural selection."
  }}
]

Only output the json in the following format and be sure to output between 5 and 10 frames and sort them by importance to answering the question in descending order:

[
  {{
    "frame": "<<Name Of Frame>>",
    "explanation": "Explanation of why the frame is relevant",
  }},
... 
]


Question: {}

""",
                },
                'question' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '011',
                    'prompt' : """Generate frames relevant for answering the question provided. The output frames must be from FrameNet. Only include frams from FrameNet. Do not include any frames not in FrameNet. Do not include frames about answering questions or reasoning, that is implied. The frames must be useful in retriving factoids that are indexed by frames. Do not include frames which are metaphorical.

Generate frames similar to the example provided in json format. 

Example 1:
Question 1: A population of small, plant-eating beetles lives in a forest. About half of the beetles are light brown and the others are dark green. If years of drought cause the area to become dry with few trees, what would the beetle population most likely look like after several generations?
[
  {{
    "frame": "Surviving",
    "explanation": "Crucial for understanding the adaptive strategies the beetles might employ to cope with the changing environmental conditions."
  }},
  {{
    "frame": "Becoming_dry",
    "explanation": "This frame is relevant because the question describes a change in the environment due to drought, resulting in the area becoming dry."
  }},
  {{
    "frame": "Animals",
    "explanation": "This frame pertains to the beetles as living organisms, which are the subject of the question, focusing on their survival and adaptation."
  }},
  {{
    "frame": "Food",
    "explanation": "Since the beetles are plant-eaters, this frame is relevant due to potential changes in food availability affecting the beetle population."
  }},
  {{
    "frame": "Color",
    "explanation": "Pertinent to the possible changes in the physical appearance of the beetles, particularly if there is a shift in the dominance of color traits (light brown or dark green) due to natural selection."
  }}
]


Question: {}

All frames output must be in the following list of availableFrames:

availableFrames = [ {} ]

Only output the json in the following format and be sure to output between 5 and 10 frames and sort them by importance to answering the question in descending order:

[
  {{
    "frame": "<<Name Of Frame>>",
    "explanation": "Explanation of why the frame is relevant",
  }},
... 
]

""",
                },
                
                'explore_fact' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Generate frames relevant to the following factoid. Make sure that the output frames are from FrameNet. Only include frams from FrameNet. Do not include any frames not in FrameNet. Do not include frames about answering questions or reasoning, that is implied. The frames must be useful in retriving factoids that are indexed by frames. Do not include frames which are metaphorical. Make sure that the frames generated a most likely to be related to the factoid even in the most general sense of the frame.

Factoid: {}

Only output the json in the following format and be sure to output between 5 and 10 frames and sort them by importance to answering the question in descending order. The output should include nothing but the json. Do not include any formatting information. Input only the json:

[
  {{
    "frame": "<<Name Of Frame>>",
    "explanation": "Explanation of why the frame is relevant",
  }},
... 
]

""",
                },
                
                'fact' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '011',
                    'prompt' : """Generate frames relevant to the following factoid. Make sure that the output frames are from FrameNet. Only include frams from FrameNet. Do not include any frames not in FrameNet. Do not include frames about answering questions or reasoning, that is implied. The frames must be useful in retriving factoids that are indexed by frames. Do not include frames which are metaphorical. Make sure that the frames generated a most likely to be related to the factoid even in the most general sense of the frame.

Factoid: {}

All frames output must be in the following list of availableFrames:

availableFrames = [ {} ]

Only output the json in the following format and be sure to output between 5 and 10 frames and sort them by importance to answering the question in descending order. The output should include nothing but the json. Do not include any formatting information. Input only the json:

[
  {{
    "frame": "<<Name Of Frame>>",
    "explanation": "Explanation of why the frame is relevant",
  }},
... 
]

""",
                },
            },

            'template_5' : { 
                'explore' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Generate frames relevant for answering the question provided. Do not include frames about answering questions or reasoning, that is implied. The frames must be useful in retriving factoids that are indexed by frames. Make the frames as conceptual as possible. Do not include frames which are metaphorical.

Only output the json in the following format and be sure to output between 5 and 10 frames and sort them by importance to answering the question in descending order:

[
  {{
    "frame": "<<Name Of Frame>>",
    "explanation": "Explanation of why the frame is relevant",
  }},
... 
]


Question: {}

""",
                },
                
                'explore_fact' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Generate frames relevant to the following factoid. Do not include any frames not in FrameNet. Do not include frames about answering questions or reasoning, that is implied. The frames must be useful in retriving factoids for answering questions. Do not include frames which are metaphorical. Make sure that the frames generated a most likely to be related to the factoid even in the most general sense of the frame.

Factoid: {}

Only output the json in the following format and be sure to output between 5 and 10 frames and sort them by importance to answering the question in descending order. The output should include nothing but the json. Do not include any formatting information. Input only the json:

[
  {{
    "frame": "<<Name Of Frame>>",
    "explanation": "Explanation of why the frame is relevant",
  }},
... 
]

""",
                },
            },
            'template_6' : { 
                'explore' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """What is the single most important frame, based on the theory of frame semantics, relevant for answering the question below. 
Do not include frames about answering questions or reasoning, that is implied. 
Do not include frames which are metaphorical.

Ensure the the name of the frame is as descriptive as possible.
Output a single frame and join words in the frame by underscores. Output nothing but the name of the frame.

Examples: 
Question 1:  How does the appearance of a constellation change during the night?
Answer 1: celestial_motion

Question 2: Students want to plant a lemon tree at their school, but the cold winter temperatures in Massachusetts would kill the tree. Which of the following is the best solution to this problem?
Answer 2: temperature_regulation

Question 3: A student pushes a wooden block across a sheet of sandpaper. Which characteristic of the block increases?
Answer 3: surface_friction

Problem: 
Question Problem: {}
Answer Problem:""",
                },

                'frame_check_question' : { 
                    'style' : 'ChatCompletion' ,
                    'fields' : '0111',
                    'prompt' : """
The following question has been tagged with the single frame listed. Is this frame significantly different from existing frames listed and should it be added as a new frame? Respond with True if it is significantly different otherwise False. Respond with True and False only.
Examples: 
Example Question 1: How does the appearance of a constellation change during the night?
Example Tagged Frame 1:celestial_motion
Example Existing Frames 1: celestial_motion
Example Answer 1: False

Example Question 2: From Earth, the Sun appears brighter than any other star because the Sun is the
Example Tagged Frame 2:proximity
Example Existing Frames 2: celestial_motion
Example Answer 2: True

Example Question 3: In New York State, the longest period of daylight occurs during which month?
Example Tagged Frame 3:seasonal_variation
Example Existing Frames 3: celestial_motion, celestial_brightness, proximity
Example Answer 3: True

Problem:
Question Problem: {}
Tagged Frame Problem:{}
Existing Frames Problem: {}
Answer Problem:""",
                },
                
                'frame_check_fact' : { 
                    'style' : 'ChatCompletion' ,
                    'fields' : '0111',
                    'prompt' : """
The following fact has been tagged with the single frame listed. Is this frame significantly different from existing frames listed and should it be added as a new frame? Respond with True if it is significantly different otherwise False. Respond with True and False only.
Examples: 
Example Input 1: How does the appearance of a constellation change during the night?
Example Tagged Frame 1:celestial_motion
Example Existing Frames 1: celestial_motion
Example Answer 1: False

Example Input 2: From Earth, the Sun appears brighter than any other star because the Sun is the
Example Tagged Frame 2:proximity
Example Existing Frames 2: celestial_motion
Example Answer 2: True

Example Input 3: In New York State, the longest period of daylight occurs during which month?
Example Tagged Frame 3:seasonal_variation
Example Existing Frames 3: celestial_motion, celestial_brightness, proximity
Example Answer 3: True

Problem:
Input Problem: {}
Tagged Frame Problem:{}
Existing Frames Problem: {}
Answer Problem:""",
                },
                
                'classify_fact' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Classify the following sentences in to one of the following possible classes: question, causation, generalisaation, fact-common, fact-scientific. Output exactly one word corresponding to the corresponding class.                                   
Examples:                                                                                                                              
Example Input 1: Early scientists most likely saw a discharge of electricity for the first time when observing a
Example Output 1: question
Example Input 2: the amount of daylight is greatest in the summer
Example Output 2:  fact-scientific
Example Input 3: apparent motion is when an object appears to move relative to another object 's position
Example Output 3:  fact-scientific
Example Input 4: if a spoon is used to stir a liquid then that spoon is touching that liquid
Example Output 4: fact-common
Example Input 4: replacing something decreases that something
Example Output 4: fact-common
Example Input 5: weather phenomenon can be observed
Example Output 5: fact-common
Example Input 6: pliers are made of two levers for gripping
Example Output 6: fact-common
Example Input 7 : if something has a definite volume , then its volume will not change when transferred into a different container
Example Output 7: fact-scientific
Example Input 7 : a line graph is a kind of graph of connected data points
Example Output 7: generalisaation
Example Input 7 : fruit salad is a kind of salad
Example Output 7: generalisaation
Example Input 8: microscope is a kind of optical tools for observing small things
Example Output 9: fact-scientific
Example Input 10:  sugar causes food to taste sweet
Example Output 10:  causation

Problem:
Problem Input : {}
Problem Output: """,
                },

                'explore_fact' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """What are the 2 most important frames, based on the theory of frame semantics, relevant to the fact below.
Do not include frames about answering questions or reasoning, that is implied.
Do not include frames which are metaphorical.
Ensure the the name of the frame is as descriptive as possible.
Ensure that the frame is not about causation, generalisation.
Output a list of 2 relevant frames and join words in the frame by underscores. Output nothing but the frames separated by commas.

Examples:
Example Fact 1: the earth rotates on its tilted axis
Example Output 1: earth_rotation , orbital_period
Example Fact 2: the earth revolves around the sun
Example Output 2: earth_rotation, orbital_period
Example Fact 3: as a source of light becomes closer , the light will appear brighter
Example Output 3: relative_luminosity, distance_effect
Example Fact 4: venus is covered in highly reflective clouds
Example Output 4: planetary_brightness, reflectivity

Problem: 
Problem Fact: {}
Problem Output:""",
                },
            
                'frame_relations' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '011',
                    'prompt' : """Listed below is a single frame relevant to a question. List those frames which are most likely to be associated with the facts required for answer this question. These frames are  based on the theory of frame semantics.
Do not include frames about answering questions or reasoning, that is implied.
Do not include frames which are metaphorical.
Ensure the the name of the frame is as descriptive as possible.
Ensure that the frame is not about causation, generalisation.
Output a list relevant frames and join words in the frame by underscores. Output nothing but the frames separated by commas.

Examples:
Example Question 1: Stars are organized into patterns called constellations. One constellation is named Leo. Which statement best explains why Leo appears in different areas of the sky throughout the year?
Example Question Frame 1: celestial_motion
Example Output Frames 1: constellation_classification, star_classification, celestial_motion
Example Question 2: From Earth, the Sun appears brighter than any other star because the Sun is the
Example Question Frame 2: celestial_proximity
Example Output Frames 2: stellar_properties, planetary_brightness, source_provider
Example Question 3: Many stars can be seen in the sky at night. Which statement best explains why the Sun appears brighter than the stars seen in the night sky?
Example Question Frame 3: relative_brightness
Example Output Frames 3: celestial_proximity, planetary_brightness, stellar_properties, source_provider
Example Question 4: In an accurate diagram of the solar system, which object would be shown closest to Earth?
Example Question Frame 4: solar_movement
Example Output Frames 4: solar_system_astronomy, celestial_proximity, celestial_body_membership
Example Question 5: Which of the following statements best explains why the tilt of Earth on its axis causes summer to be warmer than winter in the Northern Hemisphere?
Example Question Frame 5: seasonal_change
Example Output Frames 5: hemisphere_tilt, hemisphere_orientation, sunlight_exposure

Problem Question : {}
Problem Question Frame :  {}
Problem Output Frames:""",
                },

                'search_terms' : {
                    'style' : 'ChatCompletion' ,
                    'fields' : '010',
                    'prompt' : """Listed below is a single question. Generate search terms appropriate for extracting intermediary reasoning steps. Output nothing but the search terms separated by questions.

Examples:
Example Question 1: When the Northern Hemisphere is tilted toward the Sun, what season is occurring in Australia?
Example Search Terms 1: Australia, hemisphere
Example Question 2: About how many Earth days does it take the Moon to travel around Earth?
Example Search Terms 2: earth, month
Example Question 3: Which of the following statements best explains why the tilt of Earth on its axis causes summer to be warmer than winter in the Northern Hemisphere?
Example Search Terms 3: hemisphere, sunlight
Example Question 4: Approximately how long does Earth take to complete its orbit around the Sun?
Example Search Terms 4: revolution, sun, earth

Problem Question : {}
Problem Search Terms :""",
                },
            },

        }
                
