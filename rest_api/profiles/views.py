from django.shortcuts import get_object_or_404, redirect, reverse

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from profiles.models import Profile, ProfileGeolocation
from .serializers import CreateProfileSerializers, UpdateProfileSerializers, ProfileSerializer
from utils.utils import coordinates_calculation


class CreateProfileView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializers

    def create(self, request, *args, **kwargs):
        try:
            instance = request.data
            super(CreateProfileView, self).create(request, *args, **kwargs)
            lat_cal, lng_cal = coordinates_calculation(
                '',
                instance.__getitem__('postal_code'),
                instance.__getitem__('city'),
                instance.__getitem__('country')
            )
            profile = Profile.objects.get(user=self.request.user)
            ProfileGeolocation.objects.create(profile=profile, lat=lat_cal, lng=lng_cal)
            return Response({'redirect': reverse('homepage')})
        except Exception as e:
            err = e.__dict__.get('detail')
            if not err:
                return Response({'redirect': reverse('homepage')})
            err = {k: ' '.join(err[k]) for k in err.keys()}
            err.update({'err': True})
            return Response(err)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EditProfileView(RetrieveUpdateAPIView):
    serializer_class = UpdateProfileSerializers
    queryset = Profile.objects.all()

    def get_queryset(self):
        user = self.request.user
        qs = Profile.objects.all()
        user_profile = qs.filter(user=user)
        return user_profile

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        try:
            instance = request.data
            lat_cal, lng_cal = coordinates_calculation(
                number='',
                street=instance.get('street', ''),
                postal_code=instance.get('postal_code', ''),
                city=instance.get('city', ''),
                country=instance.get('country', '')
            )
            response = super(EditProfileView, self).update(request, *args, **kwargs)
            if lat_cal == -1 and lng_cal == -1:
                return response
            profile = Profile.objects.get(user=self.request.user)
            geo = ProfileGeolocation.objects.get(profile=profile)
            geo.lat = lat_cal
            geo.lng = lng_cal
            geo.save()
            return response
        except Exception as e:
            print(e)
            return

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ProfileViewSet(ReadOnlyModelViewSet):
    queryset = Profile.objects.all().order_by('id')
    serializer_class = ProfileSerializer
