class Sample:
    def __init__(self, sampleID, date, layers, materials, magPower, growthTimes, gasses, backgroundPressure, period, gamma, bias, comments, specularpath, offspecularpath, mappath):
        #self.internalID = internalID
        self.sampleID = sampleID
        self.date = date
        self.backgroundpressure = backgroundPressure
        self.layers = layers
        self.materials = materials
        self.magPower = magPower
        self.growthTimes = growthTimes
        self.gasses = gasses
        self.period = period
        self.gamma = gamma
        self.bias = bias
        self.comments = comments
        self.specularpath = specularpath
        self.offspecularpath = offspecularpath
        self.mappath = mappath