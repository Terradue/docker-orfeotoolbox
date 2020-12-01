from urllib.parse import urlparse
from pystac import *
import otbApplication

def fix_asset_href(uri):
    #print('-', uri)
    parsed = urlparse(uri)
    
    if parsed.scheme.startswith('http'):
        
        return '/vsicurl/{}'.format(uri)
    
    else:
        
        return uri

def get_asset(item, band_name):
    
    asset = None
    
    eo_item = extensions.eo.EOItemExt(item)
    
    print(eo_item)
    #print(eo_item)
    
    # Get bands
    if (eo_item.bands) is not None:
        print('in')
        for index, band in enumerate(eo_item.bands):
            #print(index, band, band.common_name, band.name) # eg --> 1 <Band name=B02> blue B02
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
    
    asset, asset_href = get_asset(item, 'red')
    
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

    app.SetParameterString('out', '{}.tif'.format(common_band_name))

    app.SetParameterString("milli", '0')
    app.SetParameterString("clamp", '0')

    #app.SetParameterOutputImagePixelType("out", otbApplication.ImagePixelType_int16)
    
    app.ExecuteAndWriteOutput()

    return '{}.tif'.format(common_band_name)