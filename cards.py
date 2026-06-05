"""Card and clue data for the 30 Seconds-style AI mini-project.

The AI learns which actual clue works best for each card and round.
Round 1 uses full sentence clues, round 2 uses one-word clues, and round 3
uses action clues.
"""

ROUND_CLUES = {
    "Shark cage diving": {
        1: [
            "People go underwater in a cage to see sharks.",
            "This ocean activity lets tourists safely watch great whites.",
            "A metal cage protects you while you are near dangerous sea animals.",
        ],
        2: ["Sharks", "Cage", "Ocean"],
        3: [
            "Pretend to lower yourself into water and look around.",
            "Hold invisible bars, then act scared of something swimming past.",
            "Pretend to put on goggles and point at a shark.",
        ],
    },
    "Robben Island": {
        1: [
            "This island near Cape Town was used as a prison.",
            "Nelson Mandela was imprisoned at this famous place.",
            "Visitors take a ferry there to learn about South African history.",
        ],
        2: ["Mandela", "Island", "Prison"],
        3: [
            "Pretend to row across water, then point to an island.",
            "Hold your wrists together like a prisoner, then look across the sea.",
            "Pretend to board a ferry and look at a distant place.",
        ],
    },
    "Koe'sister": {
        1: [
            "This is a spiced Cape Malay sweet treat.",
            "It is a small doughnut-like snack often covered in coconut.",
            "People eat this soft, sweet South African pastry.",
        ],
        2: ["Sweet", "Coconut", "Pastry"],
        3: [
            "Pretend to eat a small sweet snack.",
            "Pretend to roll food in coconut and take a bite.",
            "Rub your stomach after eating a small pastry.",
        ],
    },
    "Constitution Hill": {
        1: [
            "This Johannesburg landmark is linked to law and history.",
            "It has an old prison and South Africa's Constitutional Court.",
            "People visit this site to learn about justice and democracy.",
        ],
        2: ["Court", "Justice", "Constitution"],
        3: [
            "Pretend to read an important law document.",
            "Act like a judge using a gavel.",
            "Point to a hill, then hold up a serious document.",
        ],
    },
    "Gautrain": {
        1: [
            "This is a fast train system in Gauteng.",
            "People use it to travel between Johannesburg, Pretoria, and the airport.",
            "This modern rail service has gold-coloured branding.",
        ],
        2: ["Train", "Gauteng", "Rail"],
        3: [
            "Pretend to hold a rail handle while moving fast.",
            "Act like you are waiting on a platform and entering a train.",
            "Move your arm forward like a train speeding along tracks.",
        ],
    },
    "Durban beachfront": {
        1: [
            "This is the beach area along Durban's coast.",
            "People swim, walk, and visit restaurants near this warm ocean place.",
            "This coastal strip is known for sand, waves, and holiday crowds.",
        ],
        2: ["Beach", "Durban", "Ocean"],
        3: [
            "Pretend to swim in the sea.",
            "Pretend to spread a towel on the sand.",
            "Act like you are walking beside waves.",
        ],
    },
    "Karoo": {
        1: [
            "This is a dry inland region with wide open spaces.",
            "It is known for small towns, sheep farms, and hot weather.",
            "This semi-desert area covers a large part of South Africa.",
        ],
        2: ["Dry", "Desert", "Sheep"],
        3: [
            "Pretend to wipe sweat in a hot dry place.",
            "Shield your eyes and look across a flat empty landscape.",
            "Pretend to walk slowly through heat and dust.",
        ],
    },
    "Orlando Towers": {
        1: [
            "These colourful twin towers are in Soweto.",
            "People can bungee jump between these painted towers.",
            "This landmark used to be part of a power station.",
        ],
        2: ["Bungee", "Towers", "Soweto"],
        3: [
            "Pretend to jump from a high place.",
            "Point up at two tall towers, then act scared.",
            "Hold an invisible rope and leap forward.",
        ],
    },
    "Rooibos tea": {
        1: [
            "This is a red herbal tea from South Africa.",
            "It is a caffeine-free drink made from a local plant.",
            "People often drink this warm red bush tea.",
        ],
        2: ["Tea", "Red", "Herbal"],
        3: [
            "Pretend to sip from a cup.",
            "Stir an invisible mug and drink slowly.",
            "Pretend to pour tea, then hold up a cup.",
        ],
    },
    "Cradle of Humankind": {
        1: [
            "This heritage site is famous for ancient human fossils.",
            "It is linked to the study of where early humans came from.",
            "This area has caves and discoveries about human origins.",
        ],
        2: ["Fossils", "Origins", "Caves"],
        3: [
            "Pretend to dig carefully for bones.",
            "Hold a pretend baby, then point to the ground.",
            "Act like an archaeologist brushing dust off a fossil.",
        ],
    },
    "Big Five": {
        1: [
            "This is the famous group of five safari animals.",
            "It includes lion, leopard, rhino, elephant, and buffalo.",
            "Tourists hope to see this animal group on game drives.",
        ],
        2: ["Safari", "Five", "Animals"],
        3: [
            "Hold up five fingers and look for animals.",
            "Pretend to take photos from a safari vehicle.",
            "Act like a lion, then hold up five fingers.",
        ],
    },
    "Sardine run": {
        1: [
            "This is a huge movement of sardines along the coast.",
            "Many fish swim together and attract birds, sharks, and dolphins.",
            "This ocean event happens when a large school of small fish travels.",
        ],
        2: ["Fish", "Sardines", "Run"],
        3: [
            "Move your hands like a school of fish swimming.",
            "Pretend to run, then make fish movements.",
            "Point at water and show many small fish moving together.",
        ],
    },
    "Bunny chow": {
        1: [
            "This is curry served inside a hollowed-out loaf of bread.",
            "It is a famous Durban street food.",
            "You eat this spicy meal from a bread bowl.",
        ],
        2: ["Curry", "Bread", "Durban"],
        3: [
            "Pretend to scoop food from bread.",
            "Hold a loaf shape and eat curry from the middle.",
            "Pretend your mouth burns from spicy food.",
        ],
    },
    "Union Buildings": {
        1: [
            "These government buildings are in Pretoria.",
            "The president's offices are linked to this famous landmark.",
            "This place has large gardens and official state events.",
        ],
        2: ["Pretoria", "Government", "President"],
        3: [
            "Pretend to make a serious speech.",
            "Stand formally and wave like a president.",
            "Point to a large building, then salute.",
        ],
    },
    "Tsitsikamma": {
        1: [
            "This is a forest and coastal area on the Garden Route.",
            "It is known for bridges, trees, and adventure activities.",
            "Visitors go there for nature, hiking, and ocean views.",
        ],
        2: ["Forest", "Bridge", "Coast"],
        3: [
            "Pretend to walk through trees.",
            "Act like you are crossing a high bridge.",
            "Pretend to zipline through a forest.",
        ],
    },
    "Hout Bay": {
        1: [
            "This harbour area is near Cape Town.",
            "People visit this bay for boats, seafood, and mountain views.",
            "This coastal place is known for its harbour and seals.",
        ],
        2: ["Harbour", "Bay", "Seals"],
        3: [
            "Pretend to steer a small boat.",
            "Act like a seal clapping near the water.",
            "Point at a bay, then pretend to catch a fish.",
        ],
    },
    "Maropeng": {
        1: [
            "This is the visitor centre at the Cradle of Humankind.",
            "People go there to learn about human origins.",
            "This museum-style place explains fossils and early humans.",
        ],
        2: ["Origins", "Museum", "Fossils"],
        3: [
            "Pretend to walk through an exhibition.",
            "Point at a display, then act amazed.",
            "Pretend to find and show an ancient fossil.",
        ],
    },
    "Comrades Marathon": {
        1: [
            "This is a famous long-distance race in South Africa.",
            "Runners travel between Durban and Pietermaritzburg in this event.",
            "This ultra-marathon is known for being very difficult.",
        ],
        2: ["Running", "Marathon", "Comrades"],
        3: [
            "Pretend to run while very tired.",
            "Wipe sweat and keep jogging slowly.",
            "Act like you cross a finish line after a long race.",
        ],
    },
    "Pilanesberg": {
        1: [
            "This is a game reserve in an ancient volcanic area.",
            "People go on safari there to see wild animals.",
            "This wildlife park is near Sun City.",
        ],
        2: ["Safari", "Reserve", "Volcano"],
        3: [
            "Pretend to look at animals from a game vehicle.",
            "Act like you are using binoculars on safari.",
            "Point at wildlife, then drive slowly.",
        ],
    },
    "District Six": {
        1: [
            "This Cape Town area is remembered for forced removals.",
            "It is linked to apartheid history and a famous museum.",
            "Many families were moved from this neighbourhood.",
        ],
        2: ["Six", "Apartheid", "Museum"],
        3: [
            "Hold up six fingers, then point around a neighbourhood.",
            "Pretend to pack boxes and leave a home.",
            "Point to an area, then show sadness and memory.",
        ],
    },
}


def get_cards():
    """Return a copy of the card list."""
    return list(ROUND_CLUES)


def get_clues_for_round(card, round_number):
    """Return the allowed clues for one card and round."""
    return ROUND_CLUES[card][round_number].copy()


def get_all_clues():
    """Return every possible clue action used by the Q-learning agent."""
    clues = []

    for card_rounds in ROUND_CLUES.values():
        for round_clues in card_rounds.values():
            for clue in round_clues:
                if clue not in clues:
                    clues.append(clue)

    return clues
