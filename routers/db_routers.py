class blogsRouter:
    route_app_labels = ['blogs']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'blogs'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'blogs'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in ['blogs', 'sentiment', 'auth', 'contenttypes', 'sessions', 'admin', 'users'] or
                obj2._meta.app_label in ['blogs', 'sentiment', 'auth', 'contenttypes', 'sessions', 'admin', 'users']
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'blogs'
        return None


class sentiment:
    route_app_labels = ['sentiment']

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'sentiment'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'sentiment'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'sentiment'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in ['blogs', 'sentiment', 'auth', 'contenttypes', 'sessions', 'admin', 'users'] or
                obj2._meta.app_label in ['blogs', 'sentiment', 'auth', 'contenttypes', 'sessions', 'admin', 'users']
        ):
            return True
        return None