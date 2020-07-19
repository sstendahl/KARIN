"""
MultiLayer with correlated roughness
"""
import bornagain as ba
import numpy
from bornagain import deg, angstrom, nm


phi_f_min, phi_f_max = -0.1, 0.1
alpha_f_min, alpha_f_max = 0.0, 15.0
alpha_i_min, alpha_i_max = 0.0, 15.0  # incoming beam


def get_sample(bilayers, interfacewidth, crosscorrlength, lattcorrlength):
    """
    Returns a sample with two layers on a substrate, with correlated roughnesses.
    """
    # defining materials
    m_ambience = ba.HomogeneousMaterial("ambience", 0.0, 0.0)
    m_Ni = ba.MaterialBySLD("Ni", -1.9493e-06, 0.0)
    m_Ti = ba.MaterialBySLD("Ti", 9.4245e-06, 0.0)
    m_substrate = ba.MaterialBySLD("Substrate", 2.0704e-06, 0.0)

    # defining layers
    l_ambience = ba.Layer(m_ambience)
    l_Ni = ba.Layer(m_Ni, 22 * angstrom)
    l_Ti = ba.Layer(m_Ti, 26 * angstrom)
    l_substrate = ba.Layer(m_substrate)

    roughness = ba.LayerRoughness()
    roughness.setSigma(interfacewidth * angstrom)
    roughness.setHurstParameter(0.8)
    roughness.setLatteralCorrLength(lattcorrlength * angstrom)
    my_sample = ba.MultiLayer()
    # adding layers
    my_sample.addLayer(l_ambience)

    n_repetitions = bilayers;
    for i in range(n_repetitions):
        my_sample.addLayerWithTopRoughness(l_Ni, roughness)
        my_sample.addLayerWithTopRoughness(l_Ti, roughness)
    my_sample.addLayerWithTopRoughness(l_substrate, roughness)
    my_sample.setCrossCorrLength(crosscorrlength * angstrom)

    print(my_sample.treeToString())

    return my_sample


def get_simulation():
    """
    Returns an off-specular simulation with beam and detector defined.
    """
    print("Getting simulation")
    simulation = ba.OffSpecSimulation()
    simulation.setDetectorParameters(1, phi_f_min * deg, phi_f_max * deg,
                                     400, alpha_f_min * deg, alpha_f_max * deg)
    # define the beam with alpha_i varied between alpha_i_min and alpha_i_max
    alpha_i_axis = ba.FixedBinAxis("alpha_i", 400, alpha_i_min * deg, alpha_i_max * deg)
    simulation.setBeamParameters(5.23 * angstrom, alpha_i_axis, 0.0 * deg)
    # setBeamParameters(wavelength, alpha_i, phi_i)
    simulation.setBeamIntensity(1e11)
    return simulation


def run_simulation(bilayers, interfacewidth, crosscorrlength, lattcorrlength):
    """
    Runs simulation and returns intensity map.
    """
    sample = get_sample(bilayers, interfacewidth, crosscorrlength, lattcorrlength)
    print("Running simulation")
    simulation = get_simulation()
    simulation.setSample(sample)
    simulation.runSimulation()
    arr = simulation.result().array()
#    numpy.savetxt("crossinf_Latt10000_H080_N52_s08.txt", arr)
 #   ba.plot_simulation_result(result, intensity_min=0.1)
    return simulation.result()


if __name__ == '__main__':
    result = run_simulation()
    print(result)
    ba.plot_simulation_result(result, intensity_min=0.1)
