# All the constant values and default values/names in the same file

# World stats
worldWidth = 960
worldHeight = 540
distFromGround = int(worldHeight-0.14*worldHeight)


# Players stats
playerSpeed = 3
playerInventorySize = 8
startingCash = 1000


# Item stats: images, stack size, food, drink
itemStats = {'cardboard box': ('images/item/cardboard.png', 5, 0, 0), # PIC TBA
             'empty bottle': ('images/item/emptybottle.png', 5, 0, 0),
             'water bottle': ('images/item/waterbottle.png', 5, 0, 6),
             'fizzy drink': ('images/item/fizzydrink.png', 5, 0, 8),
             'food ration': ('images/item/foodration.png', 10, 8, 0),
             'ice cream': ('images/item/icecream.png', 5, 4, 0),
             'onion': ('images/item/onion.png', 16, 1, 0),
             'potato': ('images/item/potato.png', 16, 2, 0),
             'apple': ('images/item/apple.png', 10, 4, 0),
             'watermelon': ('images/item/watermelon.png', 1, 10, 3)}

# Research Center availability
upgradeExpansions = [['small container', 'small study', 'small solar panel', 'small room'],
                     ['small water tank', 'small science instrument'],
                     ['medium container', 'docking system'],
                     ['medium solar panel', 'small satellite dish'],
                     ['medium study', 'long room'],
                     ['framework', 'medium water tank'],
                     ['medium science instrument', 'medium room',],
                     ['medium satellite dish', 'small greenhouse'],
                     ['large container'],
                     ['large study'],
                     ['water recycler'],
                     ['large solar panel'],
                     ['shaped corridor', 'long framework'],
                     ['medium greenhouse'],
                     ['large satellite dish'],
                     ['large water tank']]

# Kitchens selection of buyable foods with name, amount and cost
kitchenSelection = [['onion', 16, 10],
                    ['potato', 16, 16],
                    ['apple', 10, 20],
                    ['watermelon', 1, 8],
                    ['ice cream', 5, 12],
                    ['food ration', 10, 40],
                    ['fizzy drink', 5, 10],
                    ['water bottle', 5, 7]]

