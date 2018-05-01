from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

import time

#Functions
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_SPAWN_OVERLORD = actions.FUNCTIONS.Train_Overlord_quick.id
_SPAWN_ZERGLING = actions.FUNCTIONS.Train_Zergling_quick.id
_BUILD_SPAWNING_POOL = actions.FUNCTIONS.Build_SpawningPool_screen.id

#Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

#Unit Id's
_ZERG_DRONE = 104
_ZERG_ZERGLING = 105
_ZERG_LARVA = 151
_ZERG_HATCHERY = 86

# Parameters
_PLAYER_SELF = 1
_NOT_QUEUED = [0]
_QUEUED = [1]

class SimpleAgent(base_agent.BaseAgent):
    base_top_left = None
    overlord_spawned = False
    drone_selected = False
    larva_selected = False;
    hatchery_selected = False
    spawningPool_built = False
    
    
    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]
    
        return [x + x_distance, y + y_distance]
    
    def step(self, obs):
        super(SimpleAgent, self).step(obs)
        
        time.sleep(0.5)
        
        if self.base_top_left is None:
            player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base_top_left = player_y.mean() <= 31
        
        if not self.overlord_spawned:
            if not self.larva_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _ZERG_LARVA).nonzero()
            
                target = [unit_x[0], unit_y[0]]
            
                self.larva_selected = True
                
                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])
            elif _SPAWN_OVERLORD in obs.observation["available_actions"]:
                return actions.FunctionCall(_SPAWN_OVERLORD, [_QUEUED])
            
        
        return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])