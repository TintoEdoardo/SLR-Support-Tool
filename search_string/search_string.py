"""

"""


class Search_String:
    population   = []
    intervention = []
    comparison   = []
    outcome      = []
    context      = []

    def __init__ (self,
                  population   = None,
                  intervention = None,
                  comparison   = None,
                  outcome      = None,
                  context      = None):

        if population is None:
            population   = []
        if intervention is None:
            intervention = []
        if comparison is None:
            comparison   = []
        if context is None:
            context      = []
        if outcome is None:
            outcome      = []

        self.population   = population
        self.intervention = intervention
        self.comparison   = comparison
        self.outcome      = outcome
        self.context      = context

    def To_String (self):
        """

        """
        population_string   = " OR ".join (self.population)
        intervention_string = " OR ".join (self.intervention)
        comparison_string   = " OR ".join (self.comparison)
        outcome_string      = " OR ".join (self.outcome)
        context_string      = " OR ".join (self.context)

        result      = ""
        AND_missing = False
        if len (self.population) > 0:
            result     += "(" + population_string + ")"
            AND_missing = True
        if len(self.intervention) > 0:
            if AND_missing:
                result += " AND "
            result += "(" + intervention_string + ")"
            AND_missing = True
        if len (self.comparison) > 0:
            if AND_missing:
                result += " AND "
            result += "(" + comparison_string + ")"
            AND_missing = True
        if len (self.outcome) > 0:
            if AND_missing:
                result += " AND "
            result += "(" + outcome_string + ")"
            AND_missing = True
        if len (self.context) > 0:
            if AND_missing:
                result += " AND "
            result += "(" + context_string + ")"

        return result
