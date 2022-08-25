
import armatureModel as AM


class MediapipeRetarget():
    def __init__(self):
        pass

    def retarget(self, poseLandmarks, armatureModel):
        #still gotta figure out bone offsets


        poseLmks = poseLandmarks #this is just here because I dont remember if I need to index into the landmark object to get the arary of landmark coords

        pL = []
        #convert to vector object
        for _, p in enumerate(poseLmks):
            pL.append(AM.Vec3(p.x, p.y, p.z))
        
        
        #interpolating to find a point that represents the base of the neck
        baseOfNeck= AM.Vec3(pL[12].x - pL[11].x, 
            ((pL[12].y - pL[11].y)/2) + min(pL[11].y, pL[12].y), 
            ((pL[12].z - pL[11].z)/2) + min(pL[11].z, pL[12].z))

        limbs = {
            "hip": pL[23] - pL[22],
            "head": pL[0] - baseOfNeck,
            "rForearm": pL[15] - pL[13],
            "rArm": pL[13] - pL[11],
            "rHand": (((pL[19] - pL[17]) / 2) + pL[17]) - pL[15],
            "rSpine": pL[23] - pL[11],
            "rThigh": pL[25] - pL[23],
            "rCalf": pL[27] - pL[25],
            "rFoot": pL[29] - pL[31],
            "lForearm": pL[16] - pL[14],
            "lArm": pL[14] - pL[12],
            "lHand": (((pL[20] - pL[18]) / 2) + pL[18]) - pL[16],
            "lSpine": pL[24] - pL[12],
            "lThigh": pL[26] - pL[24],
            "lCalf": pL[28] - pL[26],
            "lFoot": pL[30] - pL[32]
        }
        
        #loop through the limb dict and use the keys to index into the armature model to revise the bone vectors
        for key, val in enumerate(limbs.items()):
            if(armatureModel.getBoneByName(key) == None):
                print(f"Unable to retarget bone: {key}")

            #retarget
            armatureModel.getBoneByName(key).setBone(val)

        #return a ref to that retargeted model
        return armatureModel





