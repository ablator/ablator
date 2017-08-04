import random


name_spaces = {
    'default': [
        [
            'Hefty',
            'Weary',
            'Faulty',
            'Structural',
            'Nice',
            'Cute',
            'Fantastic',
            '',
        ],
        [
            'Reaction Control',
            'Engine',
            'Dissipator',
            'Radiator',
            'Antenae',
            'Cupola',
        ]
    ]
}


def generate_name(name_space='default') -> str:
    parts = []
    for part in name_spaces[name_space]:
        parts.append(random.choice(part))
    return ' '.join(parts)

