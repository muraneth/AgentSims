// PlayerSystem.ts

import {
  Has,
  getComponentValue,
  EntityIndex
} from '@latticexyz/recs';

import { defineQuery } from "@latticexyz/recs";
import { SetupResult } from "../mud/setup";
import { World } from "../world/World";

import { setComponent } from "@latticexyz/recs";

export async function setup(ctx: SetupResult, world: World) {
  const {
    components: { Position, Player, Agent, Status },
    api: { joinGame },
    playerEntity,
  } = ctx;

  const playerPosition = getComponentValue(Position, playerEntity);
  const canJoinGame = getComponentValue(Player, playerEntity)?.value !== true;

  // new player
  if (canJoinGame) {
    world.on("tile_click", (e: any)=>{
      console.log("tile click:", e)
  
      if (canJoinGame) {
        joinGame(e.tile_x, e.tile_y)
      } else {
        console.log("Already joined!")
      }
    })
  }

  // current player
  if (!canJoinGame && playerPosition) {
    console.log("playerPosition:", playerPosition)

    setComponent(Status, playerEntity, {value: "Eat"})
    setComponent(Agent, playerEntity, {
      name: "Player",
      age: 13,
      occupation: "The human player",
      model: "merchant/merchant"
    })
    
    let playerWorldPos = {
      x: world.EntityLayer.x + playerPosition.x*world.TileWidth + world.TileWidth/2,
      y: world.EntityLayer.y + playerPosition.y*world.TileHeight + world.TileHeight/2,
    }
    world.Viewport.moveCenter(playerWorldPos)
  }

  // others players
  const handleOtherPlayers = (entiyIndexs: EntityIndex[])=>{
    for (let playerEntity of entiyIndexs) {
      const agent = getComponentValue(Agent, playerEntity);
      const position = getComponentValue(Position, playerEntity);
      
      if (agent && position) {
        console.log("agent:", agent?.name, " online, position:", position.x, position.y)
      }
    }
  }

  let query = defineQuery([Has(Player), Has(Agent), Has(Position)], { runOnInit: true })
  handleOtherPlayers([...query.matching])
}
