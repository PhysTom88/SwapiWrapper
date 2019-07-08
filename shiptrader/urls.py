from django.conf.urls import url

from shiptrader.views import ShipsView, ShipListingsView, ShipSaleView


urlpatterns = [
    url(
        r'ships/$', ShipsView.as_view(), name="ships"
    ),
    url(
        r'listings/$', ShipListingsView.as_view(), name="ship_listings"
    ),
    url(
        r'listing/$', ShipSaleView.as_view(), name="ship_listing"
    )
]
