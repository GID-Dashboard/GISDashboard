from DataDashboard.models import Student, TeachingGroup, SIMSTeacher, SIMSSummativeData

ROUTED_MODELS = [Student, TeachingGroup, SIMSTeacher, SIMSSummativeData]

class SimsRouter(object):

    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        if model in ROUTED_MODELS:
            return 'sims'
        return None

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        if model in ROUTED_MODELS:
            return 'sims'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in ROUTED_MODELS:
            return False
        return None
