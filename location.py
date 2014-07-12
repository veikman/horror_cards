# -*- coding: utf-8 -*-
'''Wound cards for initial hits, by type of trauma and hit location.'''

import yaml
import collections

import cardtypes
import hctags


FILENAME = 'locations'
FATALITY = ' ' + str(cardtypes.FATALITY)  # Markup for replacement.
BLACKOUT = ' ' + str(cardtypes.BLACKOUT)  # Markup for replacement.

HEAD = 'Head'
NECK = 'Neck'
TORSO = 'Torso'

SHOULDER = 'Shoulder'
UPPER_ARM = 'Upper Arm'
LOWER_ARM = 'Lower Arm'
HAND = 'Hand'

UPPER_LEG = 'Upper Leg'
KNEE = 'Knee'
LOWER_LEG = 'Lower Leg'
FOOT = 'Foot'

ARM = (SHOULDER, UPPER_ARM, LOWER_ARM, HAND)
LEG = (UPPER_LEG, KNEE, LOWER_LEG, FOOT)


WEEK = 7
MONTH = 30


class BodyMap(dict):
    library = []

    def __init__(self, violence, head, neck, torso, arm, leg):
        self.violence = violence
        self[HEAD] = head
        self[TORSO] = torso
        for location, value in zip(ARM, arm):
            self.side(location, value)
        for location, value in zip(LEG, leg):
            self.side(location, value)
        self.__class__.library.append(self)

    def side(self, location, value):
        self['Right {}'.format(location)] = value
        self['Left {}'.format(location)] = value


BALLISTIC = BodyMap(hctags.VIOLENCE_BALLISTIC,
                    3, 1, 9,
                    (1, 2, 2, 1),
                    (3, 1, 2, 0))
CUT = BodyMap(hctags.VIOLENCE_CUT,
              3, 1, 8,
              (2, 3, 4, 2),
              (3, 1, 2, 0))
BLUNT = BodyMap(hctags.VIOLENCE_BLUNT,
                3, 1, 7,
                (2, 3, 3, 3),
                (3, 3, 3, 1))


def describe(violence, location, number):
    error = 'Too many cards requested for {}, {}: {}.'
    error = error.format(violence, location, number)
    torment = hctags.TORMENT.string.string

    tags = ['wound']
    description = 'Seek medical attention.'
    crunch = None
    days = 4

    if location == HEAD:
        crunch = 'Draw 1 Head Wound.'
    if location == TORSO:
        crunch = 'Draw 1 Torso Wound.'

    if violence == hctags.VIOLENCE_BALLISTIC:
        tags.append(hctags.VIOLENCE_BALLISTIC)
        days = 3 * MONTH
        if number in (0, 4):
            title = 'Bullet in the {}'.format(location)
            description = "It's still in there."
            days = 4 * MONTH
            if location == HEAD:
                description = "It's in the brain."
                crunch = '-1 Physique. ' + crunch + FATALITY
            elif KNEE in location:
                title = 'Shattered {}'.format(location)
                description = "The bullet fragmented the kneecap."
            elif UPPER_ARM in location or LOWER_LEG in location:
                description = "You need to dig it out."
            elif LOWER_ARM in location:
                description = "No grip. Nerve damage."
            elif HAND in location:
                title = 'Finger Blown Off {}'.format(location)
                description = "It's gone."
                days = 2 * MONTH
        elif number == 1:
            title = 'Grazed {}'.format(location)
            description = "It barely hit you."
            crunch = None
            days = 6 * WEEK
            if location == HEAD:
                title = 'Bullet Through the Jaw'
                description = ("You are drinking your own blood.")
                days = 3 * MONTH
            elif location == TORSO:
                description = "It left a long but shallow gash."
                days = 5 * WEEK
            elif SHOULDER in location or LOWER_ARM in location:
                description = "It just winged you."
                days = 4 * WEEK
            elif KNEE in location:
                description = "It must have bounced off the bone."
                days = 10 * WEEK
            elif UPPER_LEG in location:
                new_location = location.replace(UPPER_LEG, 'Thigh')
                title = 'Torn Inner {}'.format(new_location)
                description = "Your pants are slick with blood."
        elif number in (2, 8):
            title = 'Shot Through the {}'.format(location)
            if location == HEAD:
                description = "You don't always see it coming."
                crunch = 'You are dead.'
                days = None
            elif location == TORSO:
                tags.append(torment)
                title = 'Gutshot'
                description = "You're going to die, and it won't be fast."
                crunch = 'Draw one card per hour from the Torso Wound deck.'
                days = None
            elif SHOULDER in location:
                description = "The clavicle shattered."
            elif UPPER_ARM in location:
                description = "The humerus shattered."
                days = 6 * MONTH
            elif HAND in location or FOOT in location:
                description = "The exit wound is the size of a dime."
            elif UPPER_LEG in location:
                description = "The exit wound is the size of a golf ball."
                days = 5 * MONTH
            else:
                description = "The exit wound is as big as a quarter."
                days = 4 * MONTH
        elif number in (3, 6):
            title = 'Fragmented Bullet in the {}'.format(location)
            description = "It hit the bone and broke up."
        elif number in (5, 7):
            title = 'Clean Shot Through the {}'.format(location)
            days = 2 * MONTH
            if location == HEAD:
                crunch = crunch + FATALITY
                days = 6 * MONTH
        else:
            raise ValueError(error)

    elif violence == hctags.VIOLENCE_CUT:
        tags.append(hctags.VIOLENCE_CUT)
        days = 2 * MONTH
        if location == TORSO:
            if number in (0, 1):
                title = 'Wicked Chest Cut'
                days = 3 * MONTH
                crunch = crunch + FATALITY
            elif number == 2:
                tags.append(torment)
                title = 'Stomach Cut Open'
                description = "Yards of slippery rope."
                crunch = 'Draw one card per minute from the Torso Wound deck.'
                days = None
            elif number == 3:
                title = 'Stabbed in the Back'
                description = "Feels deep."
            elif number == 4:
                title = 'Stabbed Between the Ribs'
                crunch = crunch + FATALITY
                days = 6 * MONTH
            elif number == 5:
                title = 'Slashed Pelvis'
                crunch = None
            elif number == 6:
                title = 'Lacerated Armpit'
                description = 'There will be scars.'
                days = 10
            elif number == 7:
                title = 'Slashed Left Abdomen'
                crunch = None
            elif number == 7:
                title = 'Slashed Right Abdomen'
                crunch = None
            else:
                raise ValueError(error)

        else:
            if number == 0:
                title = 'Lacerated {}'.format(location)
                if KNEE in location or LOWER_ARM in location:
                    description = "You'll want to disinfect that."
            elif number in (1, 4):
                title = 'Slashed {}'.format(location)
                days = 3 * MONTH
            elif number == 2:
                title = '{} Gash'.format(location)
                if KNEE in location:
                    title = 'Raked {}'.format(location)
                    days = 3 * WEEK
                elif FOOT in location:
                    description = "There's blood in your tracks."
            elif number == 3:
                title = 'Ragged {}'.format(location)
                description = "Like a wild animal attack."
                days = 4 * MONTH
            else:
                raise ValueError(error)

    elif violence == hctags.VIOLENCE_BLUNT:
        tags.append(hctags.VIOLENCE_BLUNT)
        days = 3 * WEEK
        if location == TORSO:
            if number == 0:
                title = 'Smashed-up Chest'
                days = 6 * WEEK
                crunch = crunch + FATALITY
            elif number == 1:
                tags.append(torment)
                title = 'Battered Stomach'
            elif number == 2:
                title = 'Wrenched Back'
                description = "It hurts more when you're upright."
                crunch = None
                days = 5 * WEEK
            elif number == 3:
                title = 'Genital Abrasion'
                crunch = None
            elif number == 4:
                title = 'Pulled a Muscle in Your Back'
                description = 'The swelling will go down.'
                crunch = None
                days = 1 * WEEK
            elif number == 5:
                tags.append(torment)
                title = 'Battered Left Abdomen'
            elif number == 6:
                tags.append(torment)
                title = 'Battered Right Abdomen'
            else:
                raise ValueError(error)

        else:
            if number in (0, 5):
                title = 'Smashed {}'.format(location)
                days = 6 * WEEK
                if location == HEAD:
                    title = 'Lump on the {}'.format(location)
                    description = "Swollen and sore."
                    days = 1 * WEEK
                elif location == NECK:
                    title = 'Smashed Larynx'
                    description = "You can't breathe."
                    days = 3 * WEEK
                elif SHOULDER in location:
                    title = 'Dislocated {}'.format(location)
                    description = "Feels weird."
                    days = 2 * WEEK
                elif HAND in location:
                    description = "You can barely move your fingers."
                    days = 5 * WEEK
                elif KNEE in location:
                    title = 'Busted {}'.format(location)
                    description = "Keep your weight off it."
                    days = 8 * WEEK
            elif number == 1:
                title = 'Bruised {}'.format(location)
                description = 'Ugly, but no deeper than the muscle.'
                days = 1 * WEEK
                if location == HEAD:
                    title = 'Battered Face'
                    description = 'A black eye.'
                elif HAND in location:
                    description = 'The joints are sore.'
                elif KNEE in location:
                    title = 'Scraped {}'.format(location)
                    description = 'It hurts when it bends.'
                    days = 2 * WEEK
                elif FOOT in location:
                    title = 'Stubbed Toes on {}'.format(location)
                    description = "You're going to lose that nail."
            elif number == 2:
                title = 'Crushed {}'.format(location)
                days = 3 * MONTH
                if location == HEAD:
                    title = 'Compound Skull Fracture'
                    description = "Cracked like an egg."
                    crunch = "You are dead."
                    days = None
                elif UPPER_ARM in location:
                    new_location = location.replace(UPPER_ARM, 'Elbow')
                    title = 'Twisted {}'.format(new_location)
                    days = 4
                elif LOWER_ARM in location:
                    new_location = location.replace(LOWER_ARM, 'Wrist')
                    title = 'Twisted {}'.format(new_location)
                    description = "Badly sprained."
                    days = 6
                elif UPPER_LEG in location:
                    new_location = location.replace(UPPER_LEG, 'Thigh')
                    title = 'Pulled {} Muscle'.format(new_location)
                    description = 'A little bruised.'
                    days = 4
                elif KNEE in location:
                    title = 'Twisted {}'.format(location)
                    days = 2 * WEEK
                elif LOWER_LEG in location:
                    title = 'Sprained {}'.format(location)
                    description = "The tendon might be OK."
                    days = 2 * WEEK
                elif FOOT in location:
                    description = "You can't move your toes."
            elif number == 3:
                title = 'Broken {}'.format(location)
                days = 10 * WEEK
            elif number == 4:
                title = 'Welts on the {}'.format(location)
                description = 'Just needs time to heal.'
                days = 2 * WEEK
            else:
                raise ValueError(error)

    else:
        raise ValueError('Unknown location.')

    if days and torment not in tags:
        threshold = 55
        if location in (HEAD, TORSO):
            threshold = 40
        elif HAND in location:
            threshold = 80
        if days >= threshold:
            tags.append(torment)

    if torment in tags:
        if crunch:
            crunch = crunch + BLACKOUT
        else:
            crunch = BLACKOUT.strip()

    return tuple(tags), title, description, crunch, days


def generate(folder):
    '''Write YAML.'''
    path = folder + '/' + FILENAME + '.yaml'
    with open(path, mode='w', encoding='utf-8') as f:
        f.write('---\n\n#: Generated by a program. Do not edit.\n\n')

        python = {'DECK METADATA': {'GAME': 'Horror Cards',
                                    'TITLE': 'generic wound location cards',
                                    'DEFAULTS': {'copies': 1}}}
        f.write(yaml.dump(python))

        contents = list()
        for bodymap in BodyMap.library:
            for location in bodymap:
                for number in range(bodymap[location]):
                    text = describe(bodymap.violence, location, number)
                    contents.append(text)
        for data, copies in collections.Counter(contents).items():
            f.write(yaml.dump(writeup(copies, *data)))


def writeup(copies, tags, title, description, crunch, recovery):
    python = {title:
              {'copies': copies,
               'data':
               {'tags': tags,
                'lead': description}
               }
              }
    if recovery:
        python[title]['data']['recovery'] = recovery
    if crunch:
        python[title]['data']['crunch'] = crunch
    return python
