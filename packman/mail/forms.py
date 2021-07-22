from django import forms

from .models import Attachment, Message, MessageDistribution, MessageRecipient


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ("filename",)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("subject", "body")


class MessageDistributionForm(forms.ModelForm):
    class Meta:
        model = MessageDistribution
        fields = ("delivery", "distribution_list")


class MessageRecipientForm(forms.ModelForm):
    class Meta:
        model = MessageRecipient
        fields = ("delivery", "recipient")