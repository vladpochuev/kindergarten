class Extractor:
    def __init__(self, form):
        self.form = form

    def extract(self, name):
        return self.form[name]
