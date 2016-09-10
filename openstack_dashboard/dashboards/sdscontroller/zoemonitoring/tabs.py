from django.utils.translation import ugettext_lazy as _

from horizon import tabs


class ZoeAppTab(tabs.TableTab):
    name = _("Zoe App")
    slug = "zoe_app_plots"
    template_name = "horizon/sdscontroller/zoemonitoring/_app_plots.html"


class ZoeStatusTab(tabs.TableTab):
    name = _("Zoe Status")
    slug = "zoe_plots"
    template_name = "horizon/sdscontroller/zoemonitoring/_zoe_plots.html"


class MypanelTabs(tabs.TabGroup):
    slug = "zoe_monitoring_tabs"
    tabs = (ZoeAppTab, ZoeStatusTab,)
    sticky = True

