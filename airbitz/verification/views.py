from django.shortcuts import render

from recaptcha.client import captcha


def verify(veriy_id):
	return render(veriy_id, 'verification/index.html')

# class verifyAPI(serializers.Serializer):
#     claimed = serializers.BooleanField(required=True)

#     def restore_object(self, attrs, instance=None):
#         if instance is not None:
#             instance.claimed = attrs.get('claimed', instance.claimed)
#             return instance
#         return HBitsClaimedPost(**attrs)

# Create more views here.
