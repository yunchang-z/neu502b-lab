living_thing = {
    ('isa', 'living thing'),
    ('is', 'living'),
    ('can', 'grow'),
}

plant = {
    ('isa', 'plant'),
    ('has', 'roots'),
    ('has', 'leaves'),
} | living_thing

tree = {
    ('isa', 'tree'),
    ('has', 'bark'),
    ('has', 'branches'),
} | plant

oak = {
    ('isa', 'oak'),
    ('is', 'big'),
} | tree

pine = {
    ('isa', 'pine'),
    ('is', 'green'),
} | tree - {
    ('has', 'leaves'),
}

flower = {
    ('isa', 'flower'),
} | plant

rose = {
    ('isa', 'rose'),
    ('is', 'red'),
} | flower

daisy = {
    ('isa', 'daisy'),
    ('is', 'yellow'),
} | flower

animal = {
    ('isa', 'animal'),
    ('has', 'skin'),
    ('can', 'move'),
} | living_thing

bird = {
    ('isa', 'bird'),
    ('has', 'feathers'),
    ('has', 'wings'),
    ('can', 'fly'),
} | animal

canary = {
    ('isa', 'canary'),
    ('can', 'sing'),
    ('is', 'yellow'),
} | bird

robin = {
    ('isa', 'robin'),
    ('is', 'red'),
} | bird

fish = {
    ('isa', 'fish'),
    ('has', 'gills'),
    ('can', 'swim'),
    ('has', 'scales'),
} | animal

salmon = {
    ('isa', 'salmon'),
    ('is', 'red'),
} | fish

sunfish = {
    ('isa', 'sunfish'),
    ('is', 'yellow'),
} | fish
