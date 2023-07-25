from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django import six


class CustomUserActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(
            str(user.pk) + str(timestamp) +
            str(user.email)
        )
    
user_activation_token = CustomUserActivationTokenGenerator()



# class CustomUserChangePasswordTokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return(
#             str(user.pk) + str(timestamp) +
#             str(user.email)
#         )