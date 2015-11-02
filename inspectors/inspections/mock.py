import datetime as dt
import random as rn
from pprint import pprint

from faker import Factory
from faker.providers import BaseProvider

from inspectors.app import create_app
from inspectors.inspections.serializers import (
        SOCRATA_DATE_FMT,
        supervisor_schema,
        inspector_schema,
        inspection_schema
    )

def chance(prob):
    return rn.random() < prob

class FakeSocrataProvider(BaseProvider):
    """This provider class generates fake data similar to the data that comes
    from Socrata.
    """

    fields = (
            'date',
            'inspection_description',
            'disp_description',
            'permit_type',
            'permit_number',
            'job_site_address',
            'inspector_id',
            'last_name',
            'first_name',
            'photo',
            'super_email',
            'super_name',
            )

    def date(self):
        delta = dt.timedelta(days=rn.randint(-10,6))
        now = dt.datetime.now()
        date = now + delta
        return date.strftime(SOCRATA_DATE_FMT)

    def inspection_description(self):
        return rn.choice((
            "FOUNDATION GROUNDING", "FINAL ZONING", "FRAMING/FIRE STOPPING WINDOWS",
            "BEFORE ANCHOR SHEET IS COVERED", "WORK WITH",
            "CANCELLATION REQ/VERIFY WORK", "TEMPORARY C.O.",
            "TEMPORARY FOR CONSTRUCTION", "SLAB", "FENCE FOUNDATION", "SOLAR ROUGH",
            "BUCK AND FASTENER", "POOL PIPING", "NOT INSPECTED", "GROUND ROUGH",
            "FINAL ZONING AND LANDSCAPE", "TIME OF INSTALLATION",
            "USER(OWNER) REQUESTED", "VERIFY COMPLETION OF EVENT", "ANNUAL",
            "FOUNDATION/MONOLITHIC SLAB", "ROUGH/SLAB", "EXPIRED PERMIT CHECK",
            "TIE BEAM/REINFORCING", "PRESSURE TEST", "TEMPORARY FOR TESTING",
            "ROOF TRUSS/PERM BRACING/SHEATH", "SOLAR FINAL",
            "LATHING/FIREWALL/DRYWALL INSPE", "TILE PLACING (INTERMEDIATE)",
            "POOL BARRIER", "FINAL", "UNDERGROUND", "SEWER AND RELAY/WATER SERVICE",
            "STEEL & MAIN DRAIN", "ROUGH", "CAP SHEET INSTALLATION",
            ))

    def disp_description(self):
        return rn.choice(("PARTIAL APPROVE COMPLX STRUCT","CANCELLATION BY INTRNET",
            "REJECTED MULTI INSPECTED BLDG", "INSPECTION FOR QTY ASSURANCE",
            "REJECTED REVISE PLANS REQ", "APPROVED", "REJECTED NOT ACCESSIBLE",
            "REJECTED PLAN & PERMIT MISSING", "REJECTED WORK CONCEALED",
            "CORRECTIONS REQUIRED", "FIELD CHECK ONLY",
            "REJECTED SUPPLEMENT PERMIT REQ", "COMPLETED", "REJECTED NOT TO CODE",
            "NOT READY FOR INSPECTION", "REFERRED TO REGULATION", "NOT INSPECTED",
            "INSPECTION CANCELLATION", "APPRVD PARTIAL/EXTRA INSP REQ",
            "UNABLE TO LOCATE/ADD/APT/SPACE", "REJECTED APPROVED PLANS REQ.",
            "REJECTED, NOTICE COMMENCEMENT", "WORK REMOVED", "APPROVED PARTIAL"))

    def permit_type(self):
        return rn.choice(( "ZONE", "BLDG", "MECH", "boil", "PLUM", "ELEC",
            "ROOF"))

    def permit_number(self):
        yr = rn.randint(1980, 2017)
        number = rn.randint(1, 99999)
        alt = rn.randint(100, 9999)
        template = "{year}{number}"

    def job_site_address(self):
        return rn.choice(( "5945 SW 50 TER", "6055 SW 74 AVE", "6100 SW 104 AVE",
            "6201 SW 85 AVE", "6205 BLUE LAGOON DR          600",
            "6205 NW 27 AVE", "6212 S WATERWAY DR", "6231 SW 22 ST",
            "6350 SW 27 ST", "6374 SW 22 ST", "6420 BIRD RD", "6475 SW 82 ST",
            "6528 SW 27 ST"))

    def inspector_id(self):
        key = rn.choice(( "A666", "ALNUNO", "ARMMART", "BARRIOS", "BLAYLC",
            "BURNS", "CAICEDO", "CJSM", "DEXTER", "DOBSOS", "DUJULIO", "E217138",
            "E312568", "E312792", "E312793", "E312964", "E313999",))
        if chance(0.08):
            key = key.lower()
        return key

    def last_name(self):
        return rn.choice(("Rojas", "Loiseau", "Winter", "Perez", "Roy", "Andrade",
            "Copenhaver", "Folorunsho", "Silva", "Paula", "Seijas", "Webb", "Carr",
            "Pradenas", "Maldonado", "Barrington", "Dobson", "Santos" ))

    def first_name(self):
        return rn.choice(("Alberto", "Donald", "Jose E.", "Willie", "Jorge R.",
            "Jordan", "Luigi", "Santana", "Jaselyn", "Sydney", "Carlos", "John R.",
            "James", "German", "Clifton", "Miguel", "Saleem", "Javier", "Julio",
            "Gilberto", "Vincent", "Felix", "Manuel", "Jerry", "Leo", "Joel",
            "Everildo", "Kevin", "Timothy", "David", "Dexter", "Orlando",
            "Robert A.", "Juan", "Mufatau", "Freddy", "Israel"))

    def photo(self, name=None):
        if not name:
            name = self.first_name()
        template = "images\\jpg\\{name}.{ext}"
        ext = "jpg"
        if chance(0.1):
            ext = ext.upper()
        return template.format(name=name, ext=ext)

    def super_email(self, name=None):
        if not name:
            name = self.first_name()
        addr = name.upper()[:6]
        template = "{addr}@miamidade.gov"
        return template.format(addr=addr)

    def super_name(self):
        return " ".join([self.first_name(), self.last_name()])

    def socrata_row(self):
        row = {}
        for key in self.fields:
            gen_method = getattr(self, key)
            row[key] = gen_method()
        return row


def make_fake():
    fake = Factory.create('en_US')
    fake.add_provider(FakeSocrataProvider)
    return fake

def run():
    fake = make_fake()
    pprint(fake.socrata_row())

if __name__ == '__main__':
    run()
