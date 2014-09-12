# The code bounces around a lot, but I'll try to explain
# everything in a way that makes sense.  I've put the script together from
# both the Hypatia catalog class as well as the smaller class I wrote
# for the workshop abundances.

# Each star is it's own class, having been put through the "Star" class
# and gaining attributes as a result.  The hipList, is a giant list
# of all of those star-classes, which are accessed by their HIP-number (hip).

hipList = []

# This is where I define the attributes to be used later as part of the
# overall class, these are just the definitions.  I've tried to show a couple
# of examples where the first is sort of normal but with a bit of
# calculation, the second has a string as its output, and the third
# has place holders for null values.

def calcDist(hip):
    line = hipparcos.where(hipparcos.HIP==hip)
    par = line.PARX
    # parallax angle in milliarcseconds converted to distance in parsecs
    dist = 1./(float(par) * 0.001)
    return [dist]

def thickOrthin(hip):
    if (not uxux(hip)[0]=='' and not vxvx(hip)[0]=='' and not wxwx(hip)[0]==''):
        hips_u = uxux(hip)[0]
        hips_v = vxvx(hip)[0]
        hips_w = wxwx(hip)[0]
        kd = 1./((2.*pi)**1.5*35.*20.*16.)  #Calculations from Benbsy et al. (2003)
        ktd = 1./((2.*pi)**1.5*67.*38.*35.)
        ud = (hips_u)**2./(2.*35.**2.)
        vd = ((hips_v+15.)**2.)/(2.*20.**2.)
        wd = (hips_w)**2./(2.*16.**2.)
        ffd = kd*exp(-ud-vd-wd)
        #
        utd = (hips_u)**2./(2.*67.**2.)
        vtd = ((hips_v+36.)**2.)/(2.*38.**2.)
        wtd = (hips_w)**2./(2.*35.**2.)
        fftd = ktd*exp(-utd-vtd-wtd)
        #
        td_d = ((0.18/0.82)*(fftd/ffd))  #Value changed to match Adibekyan et al. (2013)
        if td_d > 10.:
            disk = "thick"
        else:
            disk = "thin"
    else:
        disk = "N/A"
    return disk

def tee(hip):
    line = exo.where(hip.HIPP==str(hip))
    if len(line.TEFF)==0:
        ttt = 9999.
    elif line.TEFF[0]=='':
        ttt= 9999.
    else:
        ttt = float(line.TEFF[0]) #[0][5]
    return [ttt]

# End of the attributes.

# This is the actual class structure.  Like a definition, it is
# general and then gets filled in depending on the input.  My main
# class is called Star.
class Star():
    def __init__(self,hip):  #You must always define the self, here with
        self.hip = hip      # the attribute of the only input "hip".
        self.dist = calcDist(hip)  #The three attributes accessed.
        self.disk = thickOrthin(hip)
        self.teff = tee(hip)
        self.abundances = []   #A call to a smaller class, used as a sub-class
                                # which is defined below.

# This defines the output of the output for self.hip.  So if I say
# "print hipList[0]" the result is "Star: hip=400"
# Notice that this is still part of the main Star class.
    def __str__(self):
        description = "Star: hip=%d"%self.hip  #print star by name


# A more descriptive feature that will print out some of the details
# when you tell it. At the end of compiling Hypatia, I have it output
# everything for every star, just to check it and make sure it's right,
# - namely: "for star in hipList: print star.longDescription()".
# You can also type, "print hipList[0].longDescription()" to look at one
# particular entry.  This is also still part of the main Star class.
    def longDescription(self):
        description = "hip = %s\n" % self.hip
        description += ("dist (pc) = %.2f \n" % self.dist[0] )
        for b in self.abundances:
            description += b.__str__() + "\n"
        return description

# This is the smaller sub-class referenced above (note how the indenting is
# different since it's not part of the Star class.  This is how I actually
# go through and compile the abundances for the catalog.

class AbundanceData():
    def __init__(self,name,value,err,ref): #Define self and the 4 input values.
        self.name = name    #The attributes as determined by the inputs,
        self.value = value  #since no definitions or calculations are required.
        self.err = err
        self.ref = ref
    def __str__(self):
        return "%s %g (%g) [%s]" % (self.name, self.value, self.err, self.ref)

# Since I'm compiling data on a star-by-star basis and not just entering
# whatever data comes my way, I need to check to see if the star name has
# already been entered into the hipList, i.e. whether it was found already
# to exist or its class needs to be created.
def findOrCreate1(hip):
    starSearch = [x for x in hipList if x.hip==hip]
    if len(starSearch)==1:  #star exists
        star=starSearch[0]
    else:              #new star
        star = Star(hip=hip)  #This is where the main class is called.
        hipList.append(star)  # Make a list of the Star-classes for each star.
    return star

#----------------------------BEGIN DATASETS--------------------------------#

# This is a super simple version of how the data is manipulated, where the data
# was coming from a table called "blanco" - which is someone's last name -
# who has a catalog with 6 elements measured. So first I step through each
# row in the blanco-table, then I cycle through the elements I know are
# measured in this table. Finally, I check to see if the hip-number or
# blanco.Star[ii] is already in the hipList or needs to be created. When
# the class for sure exists, such that the main attributes (like
# calcDist, thickOrthin, and teff) have been defined, I then fill in the abundance
# information using the sub-class.  Notice that because the sub-class has unique
# data every time, I don't check to see if information already exists, like I
# have to do with the main class.
for ii in range(len(blanco)):
    for jj, name in enumerate("NaH","SiH","TiH","FeH","NiH"):
        star = findOrCreate1(blanco.Star[ii])
        star.abundances.append(AbundanceData(name, blanco[ii][jj+2], blanco[ii][jj+41], "Blanco"))

