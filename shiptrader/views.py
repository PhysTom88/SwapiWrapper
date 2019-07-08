
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from shiptrader.formatters import ship_to_dict, listing_to_dict
from shiptrader.models import Starship, Listing


class ShipsView(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request):
        ships = Starship.objects.all()
        data = [ship_to_dict(ship) for ship in ships]

        return Response(status=HTTP_200_OK, data=data)


class ShipListingsView(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request):
        sort_by = request.GET.get("sort_by", "listed_date")
        starship_class = request.GET.get("starship_class")
        if not starship_class:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": "No startship_class given"})

        if sort_by not in ["listed_date", "price"]:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": "Sort by must be by price or time of listing"})

        listings = Listing.objects.filter(
            ship_type__starship_class=starship_class,
            active=True
        ).order_by(sort_by)

        data = [listing_to_dict(l) for l in listings]

        return Response(status=HTTP_200_OK, data={"listings": data})


class ShipSaleView(APIView):

    def post(self, request):
        starship_class = request.data.get("starship_class")
        manufacturer = request.data.get("manufacturer")
        price = request.data.get("price")
        name = request.data.get("name")

        try:
            starship = Starship.objects.get(
                manufacturer=manufacturer,
                starship_class=starship_class
            )
        except Starship.DoesNotExist:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": "starship class not found"})

        try:
            clean_price = int(price)
        except (TypeError, ValueError):
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": "Invalid price format"})

        if not name or Listing.objects.filter(name=name).exists():
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": "Name must be supplied and be unique"})

        listing = Listing.objects.create(
            name=name,
            price=clean_price,
            ship_type_id=starship.id
        )

        data = listing_to_dict(listing=listing)

        return Response(status=HTTP_201_CREATED, data={"listing": data})

    def put(self, request):
        name = request.data.get("name")
        if not name:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": "Name must be supplied"})

        try:
            listing = Listing.objects.get(
                name=name
            )
        except Listing.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND, data={"error": "listing not found"})
        else:
            listing.active = not listing.active
            listing.save()

            data = listing_to_dict(listing=listing)

        return Response(status=HTTP_200_OK, data={"listing": data})
