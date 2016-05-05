class SearchRoutes:
    @staticmethod
    def search(terms):
        return render_template('search.html', terms = terms)

    @staticmethod
