from django.db.models import (
    Model as DjangoModel, CharField, IntegerField, ManyToManyField, ImageField,
    BooleanField, DecimalField)


class Device(DjangoModel):
    architecture = CharField(max_length=255)
    battery_removable = BooleanField(null=True)
    battery_capacity = IntegerField(null=True)
    battery_tech = CharField(max_length=255, blank=True)
    cameras = ManyToManyField('Camera')
    carrier = CharField(max_length=255, blank=True)
    channels = ManyToManyField('Channel')
    codename = CharField(max_length=255, unique=True)
    cpu = CharField(max_length=255)
    cpu_cores = CharField(max_length=255)
    current_branch = CharField(max_length=255)
    depth_mm = DecimalField(max_digits=10, decimal_places=1, null=True)
    gpu = CharField(max_length=255)
    height_mm = DecimalField(max_digits=10, decimal_places=1, null=True)
    image = ImageField()
    install_method = CharField(max_length=255)
    kernel = CharField(max_length=255)
    maintainers = ManyToManyField('Maintainer')
    models = ManyToManyField('Model')
    name = CharField(max_length=255)
    networks = ManyToManyField('Network')
    peripherals = ManyToManyField('Peripheral')
    ram = CharField(max_length=255)
    ram_variants = ManyToManyField('RamVariant')
    release = CharField(max_length=255)
    screen_mm = DecimalField(null=True, max_digits=10, decimal_places=1)
    screen_ppi = IntegerField(null=True)
    screen_res_x = IntegerField(null=True)
    screen_res_y = IntegerField(null=True)
    screen_tech = CharField(max_length=255, blank=True)
    sdcard = CharField(max_length=255, blank=True)
    sdcard_max_gb = IntegerField(null=True)
    soc_variants = ManyToManyField('SocVariant')
    storage = CharField(max_length=255, blank=True)
    storage_variants = ManyToManyField('StorageVariant')
    tree = CharField(max_length=255, blank=True)
    type = CharField(max_length=255)
    vendor = CharField(max_length=255, blank=True)
    vendor_short = CharField(max_length=255, blank=True)
    versions = ManyToManyField('Version')
    width = DecimalField(max_digits=10, decimal_places=1, null=True)
    wifi = CharField(max_length=255)


class Camera(DjangoModel):
    flash = CharField(max_length=255)
    info = CharField(max_length=255)


class Channel(DjangoModel):
    name = CharField(max_length=255)


class Maintainer(DjangoModel):
    name = CharField(max_length=255)


class Model(DjangoModel):
    name = CharField(max_length=255)


class Network(DjangoModel):
    tech = CharField(max_length=255)
    bands = CharField(max_length=255)


class Peripheral(DjangoModel):
    name = CharField(max_length=255)


class Version(DjangoModel):
    name = CharField(max_length=255)


class RamVariant(DjangoModel):
    value = DecimalField(max_digits=10, decimal_places=2, null=True)


class SocVariant(DjangoModel):
    name = CharField(max_length=255, blank=True)


class StorageVariant(DjangoModel):
    value = IntegerField(null=True)
