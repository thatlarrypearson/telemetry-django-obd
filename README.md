# Django Lightroom Classic Catalog Image File Loader

This [Django](https://www.djangoproject.com/) application contains a number of [Custom Management Commandds](https://docs.djangoproject.com/en/3.0/howto/custom-management-commands/) to:

- Extract image file data from Adobe Lightroom Classic catalogs and load that data into a database.
- Compare image file data to file system data in order to identify missing image files.
- Find missing image files on backups and create scripts to copy the files from backups to appropriate directories in Lightroom directories.

## ```get_lightroom_catalog```

The Django management program, ```get_lightroom_catalog```, extracts image file data from Lightroom Classic databases and writes that data into a database.  Additionally, the catalog data can be browsed in the Django administrative interface.

### USAGE

## Installation

### Dependencies

### Developer Mode Install

Developers who wish to modify the code can clone from ```github``` and install with pip.  This enables changes made in the code to appear immediately as though they were happening in the library.

```bash
python3.8 -m pip install pip --upgrade
python3.8 -m pip install setuptools --upgrade
python3.8 -m pip install wheel --upgrade
git clone hhttps://gitub.com/thatlarrypearson/Django-Lightroom-Classic-Catalog-Image-File-Loader.git
cd Django-Lightroom-Classic-Catalog-Loader
python3.8 setup.py build
python3.8 -m pip install -e .
```

### Check Installation

## ```get_lightroom_catalog```

### USAGE

## Example Linux/Mac Shell Commands To Find All Image File Names Contained in Multiple Lightroom Classic Catalogs

