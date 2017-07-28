from django.contrib.sites.models import Site


class UtilsMixin(object):

    def get_map_screen(self, location):
        lat, lng = self.get_position(location)
        return "https://maps.googleapis.com/maps/api/staticmap?zoom=15&size=500x250&markers=color:red%7Clabel:S%7C" + str(
            lat) \
               + "," + str(lng) + "&key=AIzaSyBwHPJ6_aVyk9QNkzMIPRoC22QFnvnHjME"

    def get_map_url(self, location):
        lat, lng = self.get_position(location)
        return "https://maps.google.com/maps?q=" + str(lat) + "," + str(lng)

    def get_position(self, location):
        geo = str(location).split(",")
        return geo[0], geo[1]

    def get_url(self, url):
        site = Site.objects.get_current()
        return "%s/%s" % (site.domain, url)