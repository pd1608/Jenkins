from napalm import get_network_driver
def ping_from_router():
    driver = get_network_driver("ios")
    router = driver(
        '198.51.100.12',
        'lab',
        'lab123')
    
    router.open()

    result = router.ping('10.1.5.1')
    router.close()

    return isinstance(result,dict)
    
        
ping_from_router()