# Define dictionaries for each material with their respective parameter values
reservoir_params = {
    'E': 1.0e+07,
    'nu': 0.25,
    'K': 1.6722408e-6,
    'gw': 10.0,
    'Pht': 0.10,
    'Bp': 1.0e-25,
    'Kww': 2.2e6,
    'Kss': 1.0e-25,
    'uf': 5.98e-7,
    'h': 1.0,
    'rhob': 2260.0,
    'gr': 10.0,
    'materialType': 'poroElastic',
}

capRock_params = {
    'E': 1.0e+07,
    'nu': 0.25,
    'K': 1.6722408e-12,
    'gw': 10.0,
    'Pht': 0.01,
    'Bp': 1.0e-25,
    'Kww': 2.2e6,
    'Kss': 1.0e-25,
    'uf': 5.98e-7,
    'h': 1.0,
    'rhob': 2260.0,
    'gr': 10.0,
    'materialType': 'poroElastic',
}

upperAquifer_params = {
    'E': 1.0e+07,
    'nu': 0.25,
    'K': 1.6722408e-7,
    'gw': 10.0,
    'Pht': 0.10,
    'Bp': 1.0e-25,
    'Kww': 2.2e6,
    'Kss': 1.0e-25,
    'uf': 5.98e-7,
    'h': 1.0,
    'rhob': 2260.0,
    'gr': 10.0,
    'materialType': 'poroElastic',
}

basalAquifer_params = {
    'E': 1.0e+07,
    'nu': 0.25,
    'K': 1.6722408e-9,
    'gw': 10.0,
    'Pht': 0.01,
    'Bp': 1.0e-25,
    'Kww': 2.2e6,
    'Kss': 1.0e-25,
    'uf': 5.98e-7,
    'h': 1.0,
    'rhob': 2260.0,
    'gr': 10.0,
    'materialType': 'poroElastic',
}

faultAquifer_params = {
    'Kn': 5.0e9,
    'Ks': 5.0e9,
    'Cf': 0.0,
    'Phif': 25.0,
    'Psif': 20.0,
    'Tcut': 0.0,
    'Gap': 1.0e-07,
    'uf': 5.98e-7,
    'Lkt': 1.0e-9,
    'Lkb': 1.0e-9,
    'h': 1.0,
    'Iopen': 1,
    'materialType': 'elasticInterface',
}

faultReservoirCapRock_params = {
    'Kn': 5.0e9,
    'Ks': 5.0e9,
    'Cf': 0.0,
    'Phif': 25.0,
    'Psif': 20.0,
    'Tcut': 0.0,
    'Gap': 1.0e-07,
    'uf': 5.98e-7,
    'Lkt': 1.0e-9,
    'Lkb': 1.0e-9,
    'h': 1.0,
    'Iopen': 1,
    'materialType': 'poroInterfaceMC',
}

# Create a dictionary to hold the dictionaries for each material
problemMaterials = {
    'reservoir': reservoir_params,
    'capRock': capRock_params,
    'upperAquifer': upperAquifer_params,
    'basalAquifer': basalAquifer_params,
    'fault1': faultAquifer_params,
    'fault2': faultAquifer_params,
    'faultReservoirCapRock': faultReservoirCapRock_params
}