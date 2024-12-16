from datetime import datetime


def get_current_fiscal_year():
    current_date = datetime.now()
    current_year = current_date.year
    fiscal_year_start_month = 10

    if current_date.month >= fiscal_year_start_month:
        fiscal_year = current_year + 1
    else:
        fiscal_year = current_year
    return fiscal_year


CURRENT_FY: str = get_current_fiscal_year()
CURRENT_FY_END_DATE: str = f'{CURRENT_FY}-09-30'
NEXT_FY: str = CURRENT_FY + 1


# PLAN TYPES
PLAN_0: str     = 'PLAN_TYPE'
PLAN_1 : str    = 'PLAN_TYPE'
PLAN_2 : str    = 'PLAN_TYPE'
PLAN_3 : str    = 'PLAN_TYPE'
PLAN_4: str     = 'PLAN_TYPE'


LONG_TERM_PLANS: tuple[str,...] = (PLAN_0,PLAN_1)
TEMPORARY_PLANS: tuple[str,...] = (PLAN_2,PLAN_3)


class Consultants:
    CONSULTANT_0: str = 'HRC_NAME'
    CONSULTANT_1: str = 'HRC_NAME'
    CONSULTANT_2: str = 'HRC_NAME'
    CONSULTANT_3: str = 'HRC_NAME'
HRC: Consultants = Consultants()


class Liaisons:
    CONSULTANT_0: str  = 'LIAISON_NAME'
    CONSULTANT_1: str  = 'LIAISON_NAME'
    CONSULTANT_2: str  = 'LIAISON_NAME'
    CONSULTANT_3: str  = 'LIAISON_NAME'
    LIAISON_4: str  = 'LIAISON_NAME'
    LIAISON_5: str  = 'LIAISON_NAME'
    LIAISON_6: str  = 'LIAISON_NAME'
    LIAISON_7: str  = 'LIAISON_NAME'
    LIAISON_8: str  = 'LIAISON_NAME'
    LIAISON_9: str  = 'LIAISON_NAME'
    LIAISON_10: str = 'LIAISON_NAME'
    LIAISON_11: str = 'LIAISON_NAME'
    LIAISON_12: str = 'LIAISON_NAME'
    LIAISON_13: str = 'LIAISON_NAME'
    LIAISON_14: str = 'LIAISON_NAME'
    LIAISON_15: str = 'LIAISON_NAME'
    LIAISON_16: str = 'LIAISON_NAME'
    LIAISON_17: str = 'LIAISON_NAME'
    LIAISON_18: str = 'LIAISON_NAME'
    LIAISON_19: str = 'LIAISON_NAME'
    LIAISON_20: str = 'LIAISON_NAME'
    LIAISON_21: str = 'LIAISON_NAME'
    LIAISON_22: str = 'LIAISON_NAME'
    LIAISON_23: str = 'LIAISON_NAME'
    LIAISON_24: str = 'LIAISON_NAME'
    LIAISON_25: str = 'LIAISON_NAME'
    LIAISON_26: str = 'LIAISON_NAME'
HRL: Liaisons   = Liaisons()


ORG_MAPPING: dict[str,tuple] = {
    'ORG_0':    (HRC.CONSULTANT_0,  HRL.LIAISON_14),
    'ORG_1':    (HRC.CONSULTANT_0,  HRL.LIAISON_17),
    'ORG_2':    (HRC.CONSULTANT_0,  f'{HRL.LIAISON_9};      {HRL.CONSULTANT_1}'),
    'ORG_3':    (HRC.CONSULTANT_1,  HRL.CONSULTANT_3),
    'ORG_4':    (HRC.CONSULTANT_1,  HRL.LIAISON_8),
    'ORG_5':    (HRC.CONSULTANT_0,  HRL.CONSULTANT_1),
    'ORG_6':    (HRC.CONSULTANT_2,  f'{HRL.LIAISON_24};     {HRL.LIAISON_4}'),
    'ORG_7':    (None,              None),
    'ORG_8':    (HRC.CONSULTANT_1,  HRL.LIAISON_15),
    'ORG_9':    (HRC.CONSULTANT_2,  HRL.LIAISON_5),
    'ORG_10':   (HRC.CONSULTANT_2,  HRL.LIAISON_26),
    'ORG_11':   (HRC.CONSULTANT_3,  HRL.CONSULTANT_2),
    'ORG_12':   (HRC.CONSULTANT_1,  HRL.CONSULTANT_3),
    'ORG_13':   (HRC.CONSULTANT_1,  HRL.CONSULTANT_3),
    'ORG_14':   (HRC.CONSULTANT_3,  HRL.LIAISON_18),
    'ORG_15':   (HRC.CONSULTANT_1,  HRL.LIAISON_11),
    'ORG_16':   (HRC.CONSULTANT_1,  HRL.LIAISON_23),
    'ORG_17':   (HRC.CONSULTANT_2,  HRL.LIAISON_21),
    'ORG_18':   (HRC.CONSULTANT_1,  HRL.LIAISON_6),
    'ORG_19':   (HRC.CONSULTANT_2,  HRL.LIAISON_10),
    'ORG_20':   (HRC.CONSULTANT_1,  f'{HRL.CONSULTANT_3};   {HRL.LIAISON_22}'),
    'ORG_21':   (HRC.CONSULTANT_2,  f'{HRL.LIAISON_20};     {HRL.LIAISON_13}'),
    'ORG_22':   (HRC.CONSULTANT_3,  HRL.LIAISON_19),
    'ORG_23':   (HRC.CONSULTANT_3,  HRL.LIAISON_25),
    'ORG_24':   (HRC.CONSULTANT_1,  HRL.LIAISON_7),
    'ORG_25':   (HRC.CONSULTANT_3,  HRL.LIAISON_16),
    'ORG_26':   (HRC.CONSULTANT_3,  HRL.LIAISON_25),
}


ACTION_MAPPING: dict[int,str] = {
    100: ('Career Appt',                    PLAN_1),
    101: ('Career-Cond Appt',               PLAN_1),
    130: ('Transfer',                       PLAN_1),
    140: ('Reins-Career',                   PLAN_1),
    141: ('Reins-Career-Cond',              PLAN_1),
    142: ('SES Career Appt',                PLAN_0),
    170: ('Exc Appt',                       PLAN_1),
    171: ('Exc Appt NTE',                   PLAN_1),
    301: ('Retirement-Disability',          PLAN_4),
    302: ('Retirement-Voluntary',           PLAN_4),
    317: ('Resignation',                    PLAN_4),
    330: ('Removal',                        PLAN_4),
    352: ('Termination-Appt in',            PLAN_4),
    355: ('Termination-Exp of Appt',        PLAN_4),
    385: ('Term. during prob/trialperiod',  PLAN_4),
    452: ('Suspension-Indefinite',          PLAN_4),
    500: ('Conv to Career Appt',            PLAN_1),
    501: ('Conv to Career-Cond Appt',       PLAN_1),
    542: ('Conv to SES Career Appt',        PLAN_0),
    570: ('Conv to Exc Appt',               PLAN_1),
    702: ('Promotion',                      PLAN_1),
    703: ('Promotion NTE',                  PLAN_3),
    721: ('Reassignment',                   PLAN_1),
    930: ('Detail NTE',                     PLAN_2),
}
