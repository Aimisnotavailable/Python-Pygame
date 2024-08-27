from scripts.utils import load_sound, load_sounds
from scripts.assets import Assets
class SoundMixer:

    def __init__(self, payload={}):
        self.assets = {}
        for load in payload:
            self.assets.update(Assets().fetch(payload={'sfx' : {load : payload[load]}}))

    def play(self, s_type, variant=0, loop=-1, vol=1.0):
        self.assets[s_type][variant].play(loop)
        self.assets[s_type][variant].set_volume(vol)
    
    def stop(self, s_type='', variant=0, stop_all=False):
        if stop_all:
            if s_type != '':
                sfx = self.assets[s_type]
                for i in range(len(sfx)):
                    sfx[i].stop()
            else:
                for sound_type in self.assets:
                    sfx = self.assets[sound_type]
                    for i in range(len(sfx)):
                        sfx[i].stop()
        else:
            self.assets[s_type][variant].stop()