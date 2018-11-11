This is a basic Django app _without a web interface_ to query the LineageOS
device list with SQL.

# Requirements

* Python (not sure about the version, works with 3.7.1, but should work with >3)

# Setup

Create a virtualenv and install necessary packages:

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

and run migrations:

    ./manage.py migrate

Checkout the LineageOS Wiki repository which contains the device data:

    git clone https://github.com/LineageOS/lineage_wiki.git

and import device data into our database:

    ./manage.py import_devices lineage_wiki/_data/devices

# Usage

Now, you can query the database in the Django shell:

    $ ./manage.py shell
    Python 3.7.1 (default, Oct 22 2018, 10:41:28)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.1.1 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: list(Device.objects
                .filter(ram_variants__value__gt=2, battery_removable=True, versions__name='15.1')
                .order_by('screen_mm')
                .values_list('vendor', 'name', 'ram', 'cpu_cores', 'screen_mm', 'versions__name'))
    Out[1]: [('Samsung', 'Galaxy S5 LTE-A', '3 GB', '4', Decimal('130.0'), '15.1')]

which outputs devices with over 2 GB of RAM, removable battery and LineageOS
available at version 15.1.

For availabl fields, take a look at `apps/devices/models.py`. For some fields,
different variants of the device are available with different specs, namely
these are storage, RAM and SoC. This is why you need to use a filter like
`storage_variants__value__gt=16` for example.

# Development

This is only a very basic app, as you can see, but feel free to make a complete
web app out of it. I’d be pleased :)

# License

See the file `LICENSE.md`.


