from pystac import Catalog

def get_item(catalog):
    
    cat = Catalog.from_file(catalog) 
    
    try:
        
        collection = next(cat.get_children())
        item = next(collection.get_items())
        
    except StopIteration:

        item = next(cat.get_items())
        
    return item