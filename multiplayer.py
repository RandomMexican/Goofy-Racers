from ursinanetworking import *
from ursina import Entity,Vec3,color,destroy
from testPlayer import Player,PlayerRep

# its 1:38 am and I forgot what this does but pretty sure it manages the server
class Multiplayer(Entity):
    def __init__(self, player):
        
        print("THIS SHOULD BE FUCKING RUNNING")
        self.player = player
        
        if str(self.player.IP) != "IP" and str(self.player.PORT) != "PORT":
            self.client = UrsinaNetworkingClient("localhost", 55555)
            self.easy = EasyUrsinaNetworkingClient(self.client)

            self.players = {}
            self.players_target_pos = {}
            self.players_target_rot = {}
            self.players_target_model = {}
            self.players_target_tex = {}
            

            self.selfid = -1

            @self.client.event
            def GetId(id):
                self.selfid = id
                print(f"My ID is : {self.selfid}")

            
            @self.easy.event
            def onReplicatedVariableCreated(variable):
                """
                    When a client/player joins this helps the other client/player see them in real time
                """
                print(f"rep var created: {variable}")
                variable_name = variable.name
                

                self.players_target_pos[variable_name] = Vec3(-80,-30,15)
                self.players_target_rot[variable_name] = Vec3(0,90,0)

                self.players_target_model[variable_name] = "Low_Poly_Car.obj"
                self.players_target_tex[variable_name] = "grass.png"
                self.players[variable_name] = PlayerRep(self.player, (-80, -30, 15), (0, 90, 0))

                if self.selfid == int(variable.content["id"]):
                    self.players[variable_name].color = color.red
                    self.players[variable_name].visible = False
            
            # updates when the player moves or rotates 
            @self.easy.event
            def onReplicatedVariableUpdated(variable):
                """
                    Whenever the variables below change on the player it sends a message
                    to the server and updates the values there
                """
                print("updating rep var")
                self.players_target_pos[variable.name] = variable.content["position"]
                self.players_target_rot[variable.name] = variable.content["rotation"]
                self.players_target_model[variable.name] = variable.content["model"]
                self.players_target_tex[variable.name] = variable.content["texture"]

            # removes the player from everything on disconnect
            @self.easy.event
            def onReplicatedVaribaleRemoved(variable):
                """
                    Whenever a client/player leaves the server the list of players updates
                    to remove the player from it using the ID
                """
                variable_name = variable.name
                
                destroy(self.players[variable_name])
                del self.player[variable_name]
            

    # Updates the player for the server
    def update_Multiplayer(self):
        print("updating multiplayer")
        for p in self.players:
            self.players[p].position += (Vec3(self.players_target_pos[p]) - self.players[p].position)/25
            self.players[p].rotation += (Vec3(self.players_target_rot[p]) - self.players[p].rotation)/25
            self.players[p].model = f"{self.players_target_model[p]}"
            self.players[p].texture = f"{self.players_target_tex[p]}"



        self.easy.process_net_events()