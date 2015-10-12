import datetime as dt
import random as rn
from pprint import pprint

from faker import Factory
from faker.providers import BaseProvider

from inspectors.extensions import db

from inspectors.registration.serializers import user_schema
from inspectors.inspections.models import Inspection

def chance(prob):
    return rn.random() < prob

class FakeUserProvider(BaseProvider):
    """This provider class generates fake users
    """

    fields = (
            'permit_number',
            'date_registered',
            'email',
            'phone_number',
            'active',
            )

    def contact_info(self):
        prob = rn.random()
        phone = self.generator.phone_number()
        email = self.generator.email()
        phone = phone.split('x')[0][-15:]
        if prob < 0.4:
            return {
                    "email": email
                    }
        elif prob < 0.9:
            return {
                    "phone_number": phone
                    }
        else:
            return {
                    "email": email,
                    "phone_number": phone
                    }

    def is_active(self):
        return chance(0.9)

    def date_registered(self):
        delta = dt.timedelta(days=rn.randint(-30,0), minutes=rn.randint(-700,
            700))
        now = dt.datetime.now()
        date = now + delta
        return date.isoformat()

    def permit_numbers(self, n=1):
        count = range(n)
        permit_numbers = []
        if db.session:
            query = db.session.query(
                    Inspection.permit_number.distinct().label("permit_number")
                    )
            numbers = [row.permit_number for row in query.all()]
            if numbers:
                for i in range(n):
                    permit_numbers.append(rn.choice(numbers))
        if not db.session or not permit_numbers:
            fmt = "20##0#####"
            gen = lambda x: fake.bothify(fmt)
            permit_numbers = map(count, gen)
        return permit_numbers

    def inspections_users(self, n=1, save=False, permit_numbers=None):
        """make `n` fake users, and possibly `save` them
        """
        count = range(n)
        fake = self
        user_data = []
        if not permit_numbers:
            permit_numbers = self.permit_numbers(n)
        for i in count:
            data = {
                'permit_number': permit_numbers[i],
                'date_registered': self.date_registered(),
                'active': self.is_active(),
                    }
            data.update(self.contact_info())
            user_data.append(data)
        users, errors = user_schema.load(user_data, many=True)
        if not errors:
            map(lambda u: db.session.add(u), users)
        else:
            pprint(errors)
            pprint(user_data)
        return users

def make_generator():
    fake = Factory.create('en_US')
    fake.add_provider(FakeUserProvider)
    return fake

def run():
    fake = make_fake()
    pprint(fake.inspections_users(5))

if __name__ == '__main__':
    run()
