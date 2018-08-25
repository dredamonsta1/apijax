from __future__ import unicode_literals
from django.db import models
from datetime import datetime,date
from ..exam_practice.models import User


class TripManager(models.Manager):
    def tripvalidate(self, form):
        today=date.today()
        errors = []

        if not form['new_destination']:
            errors.append("Destination is required")
        if not form['new_description']:
            errors.append("Description is required")
        if not form['trip_start']:
            errors.append("Travel Start Date is required")

        else:
            try:
                trip_start= datetime.strptime(form['trip_start'],'%Y-%m-%d')
                if trip_start.date() < today:
                    errors.append('Cannot book date from past')
            except:
                errors.append('Please enter a valid date')

        if not form['trip_end']:
            errors.append('Travel End Date is required')

        else:
            try:
                trip_end= datetime.strptime(form['trip_end'],'%Y-%m-%d')
                if trip_end.date() < today:
                    errors.append('Cannot book date from past')
            except:
                errors.append('Please enter a valid date')

        try:
            if trip_start.date() >= trip_end.date():
                errors.append('End date must be after Start date')

        except:
            pass

        return errors


class Trip(models.Model):
    planner = models.ForeignKey(User)
    joiner = models.ManyToManyField(User, related_name='joined_trips')
    new_destination = models.CharField(max_length=45)
    new_description = models.CharField (max_length=100)
    trip_start = models.DateField()
    trip_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
