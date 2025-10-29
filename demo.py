from topo_creator.topo_generator import gen_topos


def main_test():
    p = {
        "SRO": {
            "gpkg_path": "./gpkg/SRO.gpkg",
            "layer_name": "elj_qae_sro"
        },
        "BOX": {
            "gpkg_path": "./gpkg/BOX.gpkg",
            "layer_name": "elj_qae_boite_optique"
        },
        "CABLE": {
            "gpkg_path": "./gpkg/CABLE.gpkg",
            "layer_name": "elj_qae_cable_optique"
        }
    }
    print(gen_topos(p, './'))

if __name__ == '__main__':
    main_test()