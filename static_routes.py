from config import app

class StaticRouter:
    @staticmethod
    def index():
        return render_template('index.html', is_home = 'true')

    @staticmethod
    def about():
        return render_template('about.html')

    @staticmethod
    def breweries():
        return render_template('breweries.html')

    @staticmethod
    def beers():
        return render_template('beers.html')

    @staticmethod
    def styles():
        return render_template('styles.html')
