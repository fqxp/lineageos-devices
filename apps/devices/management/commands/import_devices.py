from django.core.management.base import BaseCommand
from apps.devices.models import (
    Device, Camera, Channel, Maintainer, Model, Network, Peripheral, Version,
    RamVariant, SocVariant, StorageVariant)
from termcolor import colored
from decimal import Decimal
import os
import os.path
import re
import yaml


class Command(BaseCommand):

    help = 'Import/update devices from checked-out LineageOS wiki git repo'

    def add_arguments(self, parser):
        parser.add_argument(
            'devices_dir',
            type=str,
            help='directory to import device info from')
        pass

    def handle(self, *args, **options):
        devices_dir = os.path.abspath(options['devices_dir'])

        for filename in os.listdir(devices_dir):
            codename = self._codename(filename)

            print(colored('Updating {} ...'.format(codename), 'green'))

            data = self.update_device(os.path.join(devices_dir, filename))
            self.update_db(codename, data)

    def update_device(self, filename):
        with open(filename, 'r') as fp:
            return yaml.load(fp.read())

    def update_db(self, codename, data):
        assert data['codename'] == codename

        try:
            device = Device.objects.get(codename=codename)
        except Device.DoesNotExist:
            device = Device(codename=codename)

        device.architecture = data['architecture']
        battery = self._parse_battery(data['battery'])
        device.battery_removable = battery['removable']
        device.battery_capacity = battery['capacity']
        device.battery_tech = battery['tech']
        device.carrier = data.get('carrier') or ''
        device.cpu = data['cpu']
        device.cpu_cores = data['cpu_cores']
        device.current_branch = data['current_branch']
        device.depth_mm = self._parse_mm(data.get('depth'))
        device.gpu = data['gpu']
        device.height_mm = self._parse_mm(data.get('height'))
        # device.image = models.ImageField()
        device.install_method = data['install_method']
        device.kernel = data['kernel']
        device.name = data['name']
        device.ram = data['ram']
        device.recovery_boot = data['recovery_boot']
        device.release = data['release']
        device.screen_mm = self._parse_mm(data['screen'])
        device.screen_ppi = self._parse_screen_ppi(data['screen_ppi'])
        device.screen_res_x, device.screen_res_y = self._parse_screen_res(data['screen_res'])
        device.screen_tech = data.get('screen_tech') or ''
        device.sdcard = data.get('sdcard') or ''
        device.sdcard_max_gb = self._parse_sdcard_max_gb(data['sdcard'])
        device.storage = data.get('storage') or ''
        device.tree = data['tree']
        device.type = data['type']
        device.vendor = data['vendor']
        device.vendor_short = data['vendor_short']
        device.width = self._parse_mm(data.get('width'))
        device.wifi = data['wifi']

        device.save()

        for camera in data['cameras']:
            device.cameras.add(self._get_camera(camera))

        for channel in data['channels']:
            device.channels.add(self._get_channel(channel))

        for maintainer in data['maintainers']:
            device.maintainers.add(self._get_maintainer(maintainer))

        for model in data.get('models', []):
            device.models.add(self._get_model(model))

        for network in data.get('networks', []):
            device.networks.add(self._get_network(
                network['tech'],
                network['bands']))

        for peripheral in data['peripherals']:
            device.peripherals.add(self._get_peripheral(peripheral))

        for version in data['versions']:
            device.versions.add(self._parse_version(version))

        for ram_variant in self._parse_ram_variants(data['ram']):
            device.ram_variants.add(ram_variant)

        for soc_variant in self._parse_soc_variants(data['soc']):
            device.soc_variants.add(soc_variant)

        for storage_variant in self._parse_storage_variants(data.get('storage')):
            device.storage_variants.add(storage_variant)

    def _codename(self, filename):
        return os.path.basename(filename).split('.')[0]

    def _parse_battery(self, battery_field):
        battery = {'removable': None, 'capacity': None, 'tech': ''}

        if type(battery_field) == dict:
            battery['removable'] = bool(battery_field['removable'])
            battery['capacity'] = int(battery_field['capacity'])
            battery['tech'] = battery_field.get('tech', '')

        return battery

    def _get_camera(self, camera_field):
        return Camera.objects.get_or_create(
            flash=camera_field['flash'],
            info=camera_field['info'])[0]

    def _get_channel(self, channel_field):
        return Channel.objects.get_or_create(name=channel_field)[0]

    def _parse_mm(self, mm_field):
        if not mm_field:
            return None

        # might happen that there is one device description file for two devices.
        # we're arbitrarily picking the first in list, as this happens
        # seldomly anyway.
        if type(mm_field) is list:
            mm_field = list(mm_field[0].values())[0]

        mm_field = mm_field.strip()

        mo = re.match(r'^(\d+(\.\d+)?) *mm.*$', mm_field)
        if mo:
            return Decimal(mo.group(1))
        else:
            mo = re.match(r'^(\d+(\.\d+)?) *in.*$', mm_field)
            if mo:
                return Decimal(mo.group(1)) * Decimal(25.4)

        return None

    def _get_maintainer(self, name):
        return Maintainer.objects.get_or_create(name=name)[0]

    def _get_model(self, name):
        return Model.objects.get_or_create(name=name)[0]

    def _get_network(self, tech, bands):
        return Network.objects.get_or_create(tech=tech, bands=bands)[0]

    def _get_peripheral(self, name):
        return Peripheral.objects.get_or_create(name=name)[0]

    def _parse_ram_variants(self, ram_field):
        return [
            RamVariant.objects.get_or_create(
                value=(
                    Decimal(re.match('^(\d+(\.\d)?)', variant.strip()).group(1))
                    if variant.strip() else None))[0]
            for variant in re.split('r[,/]', ram_field)]

    def _parse_screen_ppi(self, screen_ppi_field):
        mo = re.match(r'~?(\d+)', str(screen_ppi_field).strip())

        if mo:
            return int(mo.group(1))
        else:
            return None

    def _parse_screen_res(self, screen_res_field):
        if not screen_res_field:
            return (None, None)

        mo = re.match(r'^(\d)+x(\d+)$', screen_res_field)
        if mo:
            return (int(mo.group(1)), int(mo.group(2)))
        else:
            return (None, None)

    def _parse_sdcard_max_gb(self, sdcard_field):
        if not sdcard_field:
            return None

        mo = re.match('up to (\d+)', sdcard_field)
        return int(mo.group(1)) if mo else None

    def _parse_soc_variants(self, soc_field):
        return [
            SocVariant.objects.get_or_create(
                name=variant.strip())[0]
            for variant in soc_field.split('/')]

    def _parse_storage_variants(self, storage_field):
        if not storage_field:
            return []

        if storage_field.strip():
            return [
                StorageVariant.objects.get_or_create(
                    value=int(re.match('^(\d)+', variant.strip()).group(1)))[0]
                for variant in re.split(r'[,/]', storage_field)]
        else:
            return []

    def _parse_version(self, version_field):
        return Version.objects.get_or_create(name=str(version_field))[0]
