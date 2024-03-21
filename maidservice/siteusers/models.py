
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    is_houseresident = models.BooleanField(default=False)
    is_flatresident = models.BooleanField(default=False)
    is_housemaid = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # Add any other custom fields you need for your user model

    def __str__(self):
        return self.username
class House_Resident(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)

    def save(self, *args, **kwargs):
        # Set is_houseresident to True when saving the House_Resident instance
        self.user.is_houseresident = True
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username



class Flat_Resident(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)
    flat_name = models.CharField(max_length=10, blank=True, null=True)
    caretaker_email = models.EmailField(null=True, blank=True)

    # New field for flat number

    def save(self, *args, **kwargs):

        self.user.is_flatresident = True
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Service_Category(models.Model):
    category = models.CharField(max_length=30, null=True)
    desc = models.CharField(max_length=100, null=True)
    image = models.FileField(null=True)
    total=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.category
class City(models.Model):
    city = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.city

class Status(models.Model):
    status = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.status

class ID_Card(models.Model):
    card = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.card
class Housemaid(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    doj = models.DateField(null=True)
    dob = models.DateField(null=True)
    id_type = models.CharField(max_length=100, null=True)
    service_name = models.ForeignKey(Service_Category,on_delete=models.CASCADE,null=True)
    experience = models.CharField(max_length=100, null=True)
    id_card = models.FileField(null=True)
    image = models.FileField(null=True)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        self.user.is_housemaid = True
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
class Notification(models.Model):

    message = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    is_read = models.BooleanField(default=False)

class CaretakerApproval(models.Model):
    caretaker_approval = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.caretaker_approval
class Work(models.Model):
    work = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.work
class Paid(models.Model):
    paid = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.paid

class Order(models.Model):
    report_status = models.CharField(max_length=100, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Housemaid, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(House_Resident, on_delete=models.CASCADE, null=True,blank=True)
    flat_resident = models.ForeignKey(Flat_Resident, on_delete=models.CASCADE, null=True, blank=True)

    book_date = models.DateField(null=True)
    book_days = models.IntegerField(null=True)  # Number of days
    book_hours = models.IntegerField(null=True)  # Number of hours
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    work_completed = models.ForeignKey(Work, on_delete=models.CASCADE, null=True)
    paid=models.ForeignKey(Paid, on_delete=models.CASCADE, null=True)
    caretaker_approval = models.ForeignKey(CaretakerApproval, on_delete=models.CASCADE, null=True,blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
class Contact(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    message = models.CharField(max_length=500, default="")
    timestamp = models.DateTimeField(default=timezone.now)
    replied = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# class Contact(models.Model):
#         status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
#         name = models.CharField(max_length=100, null=True)
#         message1 = models.CharField(max_length=200, null=True)
#         email = models.EmailField(null=True)
#
#         def __str__(self):
#             return self.name

    # def calculate_payment_amount(self):
    #     if self.book_days is not None and self.book_hours is not None and self.service is not None:
    #         # Assuming self.service has a rate_per_hour field
    #         rate_per_hour_str = str(self.service.rate_per_hour)
    #         rate_per_hour = Decimal(rate_per_hour_str) if rate_per_hour_str.replace('.', '').isdigit() else Decimal(0)
    #         return self.book_days * self.book_hours * rate_per_hour
    #     return Decimal(0)
    #
    # def save(self, *args, **kwargs):
    #     # Calculate payment amount before saving the order
    #     self.payment_amount = self.calculate_payment_amount()
    #     super().save(*args, **kwargs)
    #
    # def __str__(self):
    #     return f"Order #{self.id} - {self.customer} - {self.service} - ${self.payment_amount}"
class Payment(models.Model):
    cardholder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiration_date = models.CharField(max_length=7)  # Format: MM/YYYY
    cvv = models.CharField(max_length=3)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        # Get the latest Order associated with this Payment
        latest_order = Order.objects.filter(payment=self).order_by('-id').first()

        # Check if there is a valid Order and payment_amount is not None
        if latest_order and latest_order.payment_amount is not None:
            self.amount_received = latest_order.payment_amount

        super(Payment, self).save(*args, **kwargs)
    def __str__(self):
        return self.cardholder_name