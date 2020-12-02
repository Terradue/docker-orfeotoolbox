import os
os.environ['LD_LIBRARY_PATH'] = '/opt/anaconda/envs/env_opt_calibration/lib'
from urllib.parse import urlparse
from pystac import *
import otbApplication
import gdal
import logging
import sys 
import numpy as np
from time import sleep

os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 
                                          'conda-otb/share/proj/' )
    

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

def fix_asset_href(uri):
    #print('-', uri)
    parsed = urlparse(uri)
    
    if parsed.scheme.startswith('http'):
        
        return '/vsicurl/{}'.format(uri)
    
    else:
        
        return uri

    
def get_bands(item):
    
    eo_item = extensions.eo.EOItemExt(item)
    
    bands = None
    
    if (eo_item.bands) is not None:
    
        bands = [band.common_name for band in eo_item.bands]
    
    return bands
    
def get_asset(item, band_name):
    
    asset = None
    
    eo_item = extensions.eo.EOItemExt(item)
    
    print(eo_item)
    #print(eo_item)
    
    # Get bands
    if (eo_item.bands) is not None:
  
        for index, band in enumerate(eo_item.bands):

            if band.common_name in [band_name]: 
                asset = item.assets[band.name]
                asset_href = fix_asset_href(asset.get_absolute_href())
                break
    
    return (asset, asset_href)

def get_asset_property(asset, prop):
    
    if prop in asset.properties['eo:bands'][0].keys():
        
        return asset.properties['eo:bands'][0][prop]

    else:
        
        return None

def get_calibration_parameter(asset):
    
    f = open('gainbias.txt', 'w')
    f.write('{}\n'.format(get_asset_property(asset, 'scale')))
    f.write('{}'.format(get_asset_property(asset, 'offset')))
    f.close()


    f = open('solarillumination.txt', 'w')
    f.write('{}'.format(get_asset_property(asset, 'eai')))
    f.close()
    
    return 'gainbias.txt', 'solarillumination.txt'


def get_item_property(item, prop):
    
    if prop in item.properties.keys():
        
        return item.properties[prop]

    else:
        
        return None
    
    
def get_sun_elevation(item):
    
    return get_item_property(item, 'view:sun_elevation')

def get_sun_azimuth(item):
    
    return get_item_property(item, 'view:sun_azimuth')

def otb_opt_calibration(item, common_band_name, level='toa'):
    
    os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 
                                          'conda-otb/share/proj/')
    
    logging.info(os.environ['PROJ_LIB'])
    
    asset, asset_href = get_asset(item, 'red')
    
    get_calibration_parameter(asset)
    
    app = otbApplication.Registry.CreateApplication('OpticalCalibration')

    app.SetParameterString('in', asset_href)
    app.SetParameterString("level", level)
    app.SetParameterInt('ram', 4096)

    app.SetParameterString('acqui.gainbias', 
                                'gainbias.txt')

    app.SetParameterString('acqui.solarilluminations',
                                'solarillumination.txt')

    app.SetParameterFloat('acqui.sun.elev',
                          get_sun_elevation(item))

    app.SetParameterFloat('acqui.sun.azim',
                          get_sun_azimuth(item))

    app.SetParameterInt('acqui.minute', item.datetime.minute)
    app.SetParameterInt('acqui.hour', item.datetime.hour)
    app.SetParameterInt('acqui.day', item.datetime.day)
    app.SetParameterInt('acqui.month', item.datetime.month)
    app.SetParameterInt('acqui.year', item.datetime.year)

    app.SetParameterString('atmo.aerosol', 'noaersol')

    app.SetParameterString('out', 'f_{}.tif'.format(common_band_name))

    app.SetParameterString("milli", '0')
    app.SetParameterString("clamp", '1')

    #app.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_int16)
    
    app.ExecuteAndWriteOutput()

    rescale('f_{}.tif'.format(common_band_name), 
            '{}.tif'.format(common_band_name))
    
    os.remove('f_{}.tif'.format(common_band_name))
    
    os.remove('gainbias.txt')
    os.remove('solarillumination.txt')
    
    return '{}.tif'.format(common_band_name)

def rescale(in_tif, out_tif):
    
    scaling_factor = 10000
    
    ds = gdal.Open(in_tif)
    
    width = ds.RasterXSize
    height = ds.RasterYSize

    input_geotransform = ds.GetGeoTransform()
    input_georef = ds.GetProjectionRef()
    
    in_band = ds.GetRasterBand(1)
    
    in_arr = in_band.ReadAsArray()
    
    driver = gdal.GetDriverByName('GTiff')

    output = driver.Create(out_tif, 
                           width, 
                           height, 
                           1, 
                           gdal.GDT_Int16)

    output.SetGeoTransform(input_geotransform)
    output.SetProjection(input_georef)

    logging.info('Converting band to Int16')

    band = output.GetRasterBand(1)

    band.WriteArray((in_arr * scaling_factor).astype(np.intc))

    output.FlushCache()

    band = None

    output = None

    sleep(5)
    
    del(ds)
    del(output)
    
    in_band = None
    ds = None
    del(ds)
    
    return True