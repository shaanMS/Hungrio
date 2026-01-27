from django.db import models

class UserProfileManager(models.Manager):

    def completion_count(self, user):
        """
        Kitni optional fields filled hain
        """
        try:
            profile = self.get(user=user)
        except self.model.DoesNotExist:
            return 0

        optional_fields = [
            "phone",
            "address_line1",
            "city",
            "state",
            "pincode",
            "country",
        ]

        filled = 0
        for field in optional_fields:
            value = getattr(profile, field)
            if value not in [None, "", 0]:
                filled += 1

        return filled

    def completion_percentage(self, user):
        total = 7
        filled = self.completion_count(user)
        return int((filled / total) * 100)

    def is_profile_complete(self, user):
        return self.completion_percentage(user) >= 80
