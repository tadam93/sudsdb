class DetailRouter:
    @staticmethod
    def beer(beer):
        return render_template('/beer-details.html')

    @staticmethod
    def brewery(brewery):
        return render_template('/brewery-details.html')

    @staticmethod
    def style(style):
        return render_template('/style-details.html')
