import os
os.environ['LD_LIBRARY_PATH'] = '/usr/lib64'
import sys
import logging
import click
import shutil
from pystac import Item, Catalog, CatalogType, extensions

from .optcal import otb_opt_calibration, get_bands, get_asset
from .stac import get_item

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command()
@click.option('--input_reference', '-i', 'input_reference', help='')
def main(input_reference):

    os.environ['LD_LIBRARY_PATH'] = '/usr/lib64'
    os.environ['PROJ_LIB'] = os.path.join(os.environ['PREFIX'], 
                                          'conda-otb/share/proj/' )
    
    logging.info(os.path.join(input_reference, 'catalog.json'))

    item = get_item(os.path.join(input_reference, 'catalog.json')) 
    
    os.mkdir(item.id)
    
    bands = get_bands(item)
    
    #cal_assets = []
    
    out_item = Item(id=item.id,
                   geometry=item.geometry,
                   bbox=item.bbox,
                   datetime=item.datetime,
                   properties=item.properties)
    for band in bands: 
        
        asset, asset_href = get_asset(item, band)
        
        if band == 'pan':
                        
            shutil.copy(asset_href, os.path.join(item.id, 'pan.tif'))
            
            asset.href = 'pan.tif'
            
            out_item.add_asset(band, asset)
            
        else:
            
            cal_tif = otb_opt_calibration(item, band)
            
            shutil.move(cal_tif, os.path.join(item.id, cal_tif))
    
            asset.href = cal_tif
            dir(asset)
            out_item.add_asset(band, asset)
            
            #cal_assets.append(asset)
      
    eo_item = extensions.eo.EOItemExt(item)
    
    eo_bands = []

    for band in eo_item.bands: 

        band.name = band.common_name

        eo_bands.append(band)
        
    eo_item.apply(eo_bands)
    
    # to STAC
    logging.info('STAC')
    cat = Catalog(id=item.id,
                  description="Calibrated optical product") 

    cat.add_items([out_item])
    
    cat.normalize_and_save(root_href='./',
                           catalog_type=CatalogType.SELF_CONTAINED)
     
    logging.info('Done!')
    
if __name__ == '__main__':
    main()
