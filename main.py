if __name__ == '__main__':
    import sys
    import json
    from audnauseum.data_models.complex_encoder import ComplexEncoder
    from audnauseum.state_machine.looper import Looper

    # create Looper
    L = Looper()

    # Load a Loop project from json file
    L.load_loop('resources/json/cd_test2.json')

    # check that it loaded (only reason we imported ComplexEncoder)
    print(json.dumps(L.loop, cls=ComplexEncoder, indent=4))

    # Write loop to another JSON file
    L.write_loop('resources/json/cd_test4.json')
