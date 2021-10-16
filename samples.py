from dataclasses import dataclass


@dataclass
class Sample:
    sampleID: str = ""
    date: str = ""
    backgroundPressure: str = ""
    layers: str = ""
    materials: str = ""
    magPower: str = ""
    growthTimes: str = ""
    gasses: str = ""
    period: str = ""
    gamma: str = ""
    bias: str = ""
    comments: str = ""
    specularpathXray: str = ""
    offspecularpathXray: str = ""
    specularpathNeutron: str = ""
    offspecularpathNeutron: str = ""
    superAdamMapPath: str = ""
