from django.utils.translation import ugettext_lazy as _

from horizon import tabs


# class ProxyTab(tabs.TableTab):
#     name = _("Proxy System")
#     slug = "proxy_plots"
#     template_name = "horizon/sdscontroller/storagemonitoring/system/_system_plots2.html"


class ZoeAppTab(tabs.TableTab):
    name = _("Zoe App")
    slug = "zoe_plots"
    template_name = "horizon/sdscontroller/zoemonitoring/_zoe_plots.html"

class MypanelTabs(tabs.TabGroup):
    slug = "zoe_monitoring_tabs"
    tabs = (ZoeAppTab,) # ZoeStatusTab,)
    sticky = True

