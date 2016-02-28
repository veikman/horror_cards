# -*- coding: utf-8 -*-
'''Location-based Wound card generator.

This module generates specifications for the content of the larger Wound
decks in the game: Blunt, Cut and Ballistic Wounds.

The specifics are generated programmatically because there are strong
patterns in the distribution of hit locations etc. between the decks.

@author: Viktor Eikman <viktor.eikman@gmail.com>

'''


import collections
import logging
import os
import yaml

import horror_cards.card
import horror_cards.tags


FATALITY = [horror_cards.markup.fatality.produce()]  # Markup for replacement.
BLACKOUT = [horror_cards.markup.blackout.produce()]  # Markup for replacement.

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
    '''Relative probabilities of hitting various parts of the body.

    Generator of specifications for one deck.

    Abstract base class.

    '''

    class UnmappedError(ValueError):
        pass

    def __init__(self, tag, head, neck, torso, arm, leg):
        self.tag = tag
        self[HEAD] = head
        self[TORSO] = torso
        for location, value in zip(ARM, arm):
            self.side(location, value)
        for location, value in zip(LEG, leg):
            self.side(location, value)

    def side(self, location, value):
        self['Right {}'.format(location)] = value
        self['Left {}'.format(location)] = value

    def describe(self, location, number):
        '''Describe a numbered injury to a particular location.'''

        tags = ['wound', self.tag.key]
        crunch = None
        days = 4

        if location == HEAD:
            crunch = ['When you gain this: Draw 1 Head Wound.']
        if location == TORSO:
            crunch = ['When you gain this: Draw 1 Torso Wound.']

        try:
            details = self.details(location, number, tags, crunch)
        except self.UnmappedError:
            s = 'Too many cards requested for {}, {}: {}.'
            logging.error(s.format(self.tag, location, number))
            raise

        title, fluff, crunch, days = details

        if days and horror_cards.tags.TORMENT.key not in tags:
            threshold = 55
            if location in (HEAD, TORSO):
                threshold = 40
            elif HAND in location:
                threshold = 80
            if days >= threshold:
                tags.append(horror_cards.tags.TORMENT.key)

        if horror_cards.tags.TORMENT.key in tags:
            if crunch:
                crunch = crunch + BLACKOUT
            else:
                crunch = BLACKOUT

        if isinstance(crunch, list):
            crunch = tuple(crunch)  # Hashable.

        return tuple(tags), title, fluff, crunch, days

    def details(self, location, number, tags, crunch):
        raise NotImplementedError

    def is_limb(self, location):
        return self.is_leg(location) or self.is_arm(location)

    def is_arm(self, location):
        return any(map(lambda detail: detail in location, ARM))

    def is_leg(self, location):
        return any(map(lambda detail: detail in location, LEG))

    def name_limb_type(self, location):
        if self.is_arm(location):
            return 'arm'
        elif self.is_leg(location):
            return 'leg'
        else:
            raise ValueError('Not on a limb: {}'.format(location))

    def name_limb(self, location):
        side = self.name_side(location)
        limb_type = self.name_limb_type(location)
        return ' '.join((side, limb_type))

    def name_side(self, location):
        if 'Right' in location:
            return 'right'
        elif 'Left' in location:
            return 'left'
        else:
            raise ValueError('Not on a side: {}.'.format(location))

    def dex_loss(self, location):
        s = '-1 Dexterity (-1 in total for {}).'
        return s.format(self.name_limb(location))

    def specification(self, folder):
        '''Write YAML.'''

        def generate():
            for location in self:
                for number in range(self[location]):
                    yield self.describe(location, number)

        def structure(copies, tags, title, fluff, crunch, recovery):
            python = {title:
                      {'metadata': {'copies': copies},
                       'data': {'tags': list(tags)}}
                      }
            if fluff:
                python[title]['data']['fluff'] = fluff
            if recovery:
                python[title]['data']['recovery'] = recovery
            if crunch:
                python[title]['data']['crunch'] = list(crunch)
            return python

        path = os.path.join(folder, 'auto_{}.yaml'.format(self.tag))
        with open(path, mode='w', encoding='utf-8') as f:
            f.write('---\n\n#: Generated by a program. Do not edit.\n\n')

            python = {'metadata': {'game': 'Horror Cards',
                                   'title': self.tag.full_name,
                                   'defaults': {'copies': 1}}}
            f.write(yaml.dump(python))

            for data, copies in collections.Counter(generate()).items():
                f.write(yaml.dump(structure(copies, *data)))
                f.write('\n')

            f.write('...')


class Ballistic(BodyMap):
    def __init__(self):
        super().__init__(horror_cards.tags.BALLISTIC,
                         3, 1, 9,
                         (1, 2, 2, 1),
                         (3, 1, 2, 0))

    def details(self, location, number, tags, crunch):
        fluff = None
        days = 3 * MONTH

        if number in (0, 4):
            title = 'Bullet in the {}'.format(location)
            fluff = "It's still in there."
            days = 4 * MONTH

            if self.is_limb(location):
                crunch = [self.dex_loss(location)]

            if location == HEAD:
                fluff = "It's in the brain."
                crunch = ['-1 Physique.'] + crunch + FATALITY
            elif KNEE in location:
                title = 'Shattered {}'.format(location)
                fluff = "The bullet fragmented the kneecap."
            elif UPPER_ARM in location or LOWER_LEG in location:
                fluff = "You need to dig it out."
            elif LOWER_ARM in location:
                fluff = "No grip. Nerve damage."
            elif HAND in location:
                crunch = None
                title = 'Finger Blown Off {}'.format(location)
                fluff = "It's gone."
                days = 2 * MONTH

        elif number == 1:
            title = 'Grazed {}'.format(location)
            fluff = "It barely hit you."
            crunch = None
            days = 6 * WEEK

            if location == HEAD:
                title = 'Bullet Through the Jaw'
                fluff = ("You are drinking your own blood.")
                days = 3 * MONTH
            elif location == TORSO:
                fluff = "It left a long but shallow gash."
                days = 5 * WEEK
            elif SHOULDER in location or LOWER_ARM in location:
                fluff = "It just winged you."
                days = 4 * WEEK
            elif KNEE in location:
                fluff = "It must have bounced off the bone."
                days = 10 * WEEK
            elif UPPER_LEG in location:
                new_location = location.replace(UPPER_LEG, 'Thigh')
                title = 'Torn Inner {}'.format(new_location)
                fluff = "Your pants are slick with blood."

        elif number in (2, 8):
            title = 'Shot Through the {}'.format(location)

            if self.is_limb(location):
                crunch = [self.dex_loss(location)]

            if location == HEAD:
                fluff = "You don't always see it coming."
                crunch = ['You are dead.']
                days = None
            elif location == TORSO:
                tags.append(horror_cards.tags.TORMENT.key)
                title = 'Gutshot'
                fluff = "You're going to die, and it won't be fast."
                crunch = ['Draw one Torso Wound per hour.']
                days = None
            elif SHOULDER in location:
                fluff = "The clavicle shattered."
            elif UPPER_ARM in location:
                fluff = "The humerus shattered."
                days = 6 * MONTH
            elif HAND in location or FOOT in location:
                fluff = "The exit wound is the size of a dime."
            elif UPPER_LEG in location:
                fluff = "The exit wound is the size of a golf ball."
                days = 5 * MONTH
            else:
                fluff = "The exit wound is as big as a quarter."
                days = 4 * MONTH

        elif number in (3, 6):
            title = 'Fragmented Bullet in the {}'.format(location)
            fluff = "It hit the bone and broke up."

        elif number in (5, 7):
            title = 'Clean Shot Through the {}'.format(location)
            days = 2 * MONTH
            if location == HEAD:
                crunch = crunch + FATALITY
                days = 6 * MONTH
        else:
            raise self.UnmappedError()

        return title, fluff, crunch, days


class Cut(BodyMap):
    def __init__(self):
        super().__init__(horror_cards.tags.CUT,
                         3, 1, 8,
                         (2, 3, 4, 2),
                         (3, 1, 2, 0))

    def details(self, location, number, tags, crunch):
        fluff = None
        days = 2 * MONTH

        if location == TORSO:
            if number in (0, 1):
                title = 'Wicked Chest Cut'
                days = 3 * MONTH
                crunch = crunch + FATALITY
            elif number == 2:
                tags.append(horror_cards.tags.TORMENT.key)
                title = 'Stomach Cut Open'
                fluff = "Yards of slippery rope."
                crunch = ['Draw one Torso Wound per minute.']
                days = None
            elif number == 3:
                title = 'Stabbed in the Back'
                fluff = "Feels deep."
            elif number == 4:
                title = 'Stabbed Between the Ribs'
                crunch = crunch + FATALITY
                days = 6 * MONTH
            elif number == 5:
                title = 'Slashed Pelvis'
                crunch = None
            elif number == 6:
                title = 'Lacerated Armpit'
                fluff = 'There will be scars.'
                days = 10
            elif number == 7:
                title = 'Slashed Left Abdomen'
                crunch = None
            elif number == 7:
                title = 'Slashed Right Abdomen'
                crunch = None
            else:
                raise self.UnmappedError()

        else:
            if number == 0:
                title = 'Lacerated {}'.format(location)
                if KNEE in location or LOWER_ARM in location:
                    fluff = "You'll want to disinfect that."

            elif number in (1, 4):
                title = 'Slashed {}'.format(location)
                days = 3 * MONTH

                if self.is_limb(location):
                    crunch = [self.dex_loss(location)]

            elif number == 2:
                title = '{} Gash'.format(location)
                if KNEE in location:
                    title = 'Raked {}'.format(location)
                    days = 3 * WEEK
                elif FOOT in location:
                    fluff = "There's blood in your tracks."

            elif number == 3:
                title = 'Ragged {}'.format(location)
                fluff = "Like a wild animal attack."
                days = 4 * MONTH

                if self.is_limb(location):
                    crunch = [self.dex_loss(location)]

            else:
                raise self.UnmappedError()

        return title, fluff, crunch, days


class Blunt(BodyMap):
    def __init__(self):
        super().__init__(horror_cards.tags.BLUNT,
                         3, 1, 7,
                         (2, 3, 3, 3),
                         (3, 3, 3, 1))

    def details(self, location, number, tags, crunch):
        fluff = None
        days = 3 * WEEK

        if location == TORSO:
            if number == 0:
                title = 'Smashed-up Chest'
                days = 6 * WEEK
                crunch = crunch + FATALITY
            elif number == 1:
                tags.append(horror_cards.tags.TORMENT.key)
                title = 'Battered Stomach'
            elif number == 2:
                title = 'Wrenched Back'
                fluff = "It hurts more when you're upright."
                crunch = None
                days = 5 * WEEK
            elif number == 3:
                title = 'Genital Abrasion'
                crunch = None
            elif number == 4:
                title = 'Pulled a Muscle in Your Back'
                fluff = 'The swelling will go down.'
                crunch = None
                days = 1 * WEEK
            elif number == 5:
                tags.append(horror_cards.tags.TORMENT.key)
                title = 'Battered Left Abdomen'
            elif number == 6:
                tags.append(horror_cards.tags.TORMENT.key)
                title = 'Battered Right Abdomen'
            else:
                raise self.UnmappedError()

        else:
            if number in (0, 5):
                title = 'Smashed {}'.format(location)
                days = 6 * WEEK

                if self.is_limb(location):
                    crunch = [self.dex_loss(location)]

                if location == HEAD:
                    title = 'Lump on the {}'.format(location)
                    fluff = "Swollen and sore."
                    days = 1 * WEEK
                elif location == NECK:
                    title = 'Smashed Larynx'
                    fluff = "You can't breathe."
                    days = 3 * WEEK
                elif SHOULDER in location:
                    title = 'Dislocated {}'.format(location)
                    fluff = "Feels weird."
                    days = 2 * WEEK
                elif HAND in location:
                    fluff = "You can barely move your fingers."
                    days = 5 * WEEK
                elif KNEE in location:
                    title = 'Busted {}'.format(location)
                    fluff = "Keep your weight off it."
                    days = 8 * WEEK

            elif number == 1:
                title = 'Bruised {}'.format(location)
                fluff = 'Ugly, but no deeper than the muscle.'
                days = 1 * WEEK
                if location == HEAD:
                    title = 'Battered Face'
                    fluff = 'A black eye.'
                elif HAND in location:
                    fluff = 'The joints are sore.'
                elif KNEE in location:
                    title = 'Scraped {}'.format(location)
                    fluff = 'It hurts when it bends.'
                    days = 2 * WEEK
                elif FOOT in location:
                    title = 'Stubbed Toes on {}'.format(location)
                    fluff = "You're going to lose that nail."

            elif number == 2:
                title = 'Crushed {}'.format(location)
                days = 3 * MONTH

                if self.is_limb(location):
                    crunch = [self.dex_loss(location)]

                if location == HEAD:
                    title = 'Compound Skull Fracture'
                    fluff = 'Cracked like an egg.'
                    crunch = ['You are dead.']
                    days = None
                elif UPPER_ARM in location:
                    new_location = location.replace(UPPER_ARM, 'Elbow')
                    title = 'Twisted {}'.format(new_location)
                    crunch = None
                    days = 4
                elif LOWER_ARM in location:
                    new_location = location.replace(LOWER_ARM, 'Wrist')
                    title = 'Twisted {}'.format(new_location)
                    fluff = "Badly sprained."
                    crunch = None
                    days = 6
                elif UPPER_LEG in location:
                    new_location = location.replace(UPPER_LEG, 'Thigh')
                    title = 'Pulled {} Muscle'.format(new_location)
                    fluff = 'A little bruised.'
                    days = 4
                elif KNEE in location:
                    title = 'Twisted {}'.format(location)
                    days = 2 * WEEK
                elif LOWER_LEG in location:
                    title = 'Sprained {}'.format(location)
                    fluff = "The tendon might be OK."
                    crunch = None
                    days = 2 * WEEK
                elif FOOT in location:
                    fluff = "You can't move your toes."
                    crunch = [self.dex_loss(location)]
            elif number == 3:
                title = 'Broken {}'.format(location)
                days = 10 * WEEK

                if self.is_limb(location):
                    crunch = [self.dex_loss(location)]

            elif number == 4:
                title = 'Welts on the {}'.format(location)
                fluff = 'Just needs time to heal.'
                days = 2 * WEEK

            else:
                raise self.UnmappedError()

        return title, fluff, crunch, days
