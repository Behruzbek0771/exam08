from django.db import transaction

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.db.models import Count, Q


from .models import Event,Registration
from rest_framework.permissions import IsAuthenticated

from .serilaziers import EventSerializers,EventRegistrSerailizers

class EventListView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializers


from .models import Event, Registration


class EventRegisterViews(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        try:
            event = Event.objects.select_for_update().get(pk=pk)
        except Event.DoesNotExist:
            raise ValidationError("Event topilmadi")

        if event.capacity == 0:
            raise ValidationError("Ro‘yxatga olish yopiq")

        active_count = event.registrations.filter(
            status=Registration.Status.REGISTERED
        ).count()

        if active_count >= event.capacity:
            raise ValidationError("Event to‘lib bo‘lgan")

        registration, created = Registration.objects.get_or_create(
            user=request.user,
            event=event,
            defaults={"status": Registration.Status.REGISTERED}
        )

        if not created:
            if registration.status == Registration.Status.CANCELLED:
                registration.status = Registration.Status.REGISTERED
                registration.save()
            else:
                raise ValidationError("Siz allaqachon ro‘yxatdan o‘tgansiz")

        return Response(
            {
                "message": "Muvaffaqiyatli ro‘yxatdan o‘tildi",
                "event_id": event.id,
                "user_id": request.user.id,
                "status": registration.status,
            },
            status=status.HTTP_201_CREATED
        )

class EventStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise ValidationError("Event topilmadi")

        registered_count = event.registrations.filter(
            status=Registration.Status.REGISTERED
        ).count()

        available_slots = max(event.capacity - registered_count, 0)

        return Response({
            "event_id": event.id,
            "registered_users": registered_count,
            "available_slots": available_slots,
            "capacity": event.capacity
        })
    
class TopEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = (
            Event.objects
            .annotate(
                total_registrations=Count(
                    "registrations",
                    filter=Q(registrations__status=Registration.Status.REGISTERED)
                )
            )
            .order_by("-total_registrations")[:5]
        )

        data = []
        for event in events:
            data.append({
                "event_id": event.id,
                "title": event.title,
                "registered_users": event.total_registrations,
                "capacity": event.capacity
            })

        return Response(data)