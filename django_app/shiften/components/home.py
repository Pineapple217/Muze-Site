from django_unicorn.components import UnicornView
from shiften.models import Shiftlijst

class HomeView(UnicornView):
    shiftlists = Shiftlijst.objects.none()

    def mount(self):
        self.load_shiftlists()

    def load_shiftlists(self):
        if self.request.user.has_perm('shiften.change_shiftlijst'):
            self.shiftlists = Shiftlijst.objects.all()
        else:
            self.shiftlists = Shiftlijst.objects.filter(is_active=True)
        self.shiftlists = self.shiftlists.order_by('date')
    