import os
import sys
import logging
import click
from .optcal import otb_opt_calibration
from .stac import get_item

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')


@click.command()
@click.option('--input_reference', '-i', 'input_reference', help='')
def main(input_reference):

    os.environ['PROJ_LIB'] = '/opt/anaconda/envs/env_opt_calibration/conda-otb/share/proj/'
    
    logging.info(os.path.join(input_reference, 'catalog.json'))

    item = get_item(os.path.join(input_reference, 'catalog.json')) 
    
    otb_opt_calibration(item, 'red')
    
    
if __name__ == '__main__':
    main()
