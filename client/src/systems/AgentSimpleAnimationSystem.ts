// RotationSystem.ts

import * as PIXI from 'pixi.js';
import {
  defineSystem,
  Has,
  getComponentValue,
} from '@latticexyz/recs';

import { SetupResult } from "../mud/setup";
import { World } from "../world/World";

import { contractComponents } from "../mud/components"
import { State as StateType } from "../mud/components/State";

const Agent = contractComponents.Agent;
const Position = contractComponents.Position;

const CompomentName = "animation";

export async function setup(ctx: SetupResult, world: World) {
  const tileWidth = world.TileWidth;
  const tileHeight = world.TileHeight;
  const spritesheet = await PIXI.Assets.load(`${ctx.publicURL}/assets/characters/Paker.json`) as PIXI.Spritesheet;
  console.log("FightResultSystem init spritesheet:", spritesheet)

  await spritesheet.parse();

  const createAnimation = (actor: string, _state: number)=>{
    let frames = spritesheet.animations[actor];
    if (!frames) {
      throw new Error(`not found animation for ${actor}`);
    }

    let animation = new PIXI.AnimatedSprite(
      spritesheet.animations[actor],
    );

    animation.anchor.set(0.5);
    animation.animationSpeed = 0.05;
    animation.play();

    return animation
  }

  const calState = (player: PIXI.Container<PIXI.DisplayObject>, targetPos: {x: number, y: number}):number=>{
    let currentPos = {
      x: Math.round((player.x-tileWidth/2)/tileWidth),
      y: Math.round((player.y-tileHeight/2)/tileHeight),
    }

    if (currentPos.x == targetPos.x) {
      if (targetPos.y > currentPos.y) {
        return StateType.WalkForwards
      } else if (targetPos.y < currentPos.y){
        return StateType.WalkBackwards
      }
    } else if (targetPos.y == currentPos.y) {
      if (targetPos.x > currentPos.x) {
        return StateType.WalkEastwards
      } else if (targetPos.x < currentPos.x){
        return StateType.WalkWestwards
      }
    }

    return StateType.Idle
  }

  defineSystem(ctx.world, [Has(Agent), Has(Position)], (update) => {
    const entity = world.getOrCreateEntity(update.entity);

    const agent = getComponentValue(Agent, update.entity);
    const position = getComponentValue(Position, update.entity);

    if (agent && position) {
      let state = calState(entity, {x: position.x, y: position.y})
      let animation = createAnimation(agent.model, state);
      animation.name = CompomentName
      
      entity.x = position.x * tileWidth + tileWidth/2;
      entity.y = position.y * tileHeight + tileHeight/2;

      let old = entity.getChildByName(CompomentName)
      if (old) {
        old.removeAllListeners();
        old.removeFromParent();
      }

      animation.zIndex = 100;
      animation.interactive = true;
      animation.cursor = "pointer";
      
      animation.on('pointerdown', (e: any) => {
        console.log("agent animation pointerdown:", e)

        world.emit("agent_click", {
          targetEntity: update.entity,
          agent: agent,
          position: position,
          rawEvent: e,
        })
      });

      entity.addChild(animation);
    }
  });
}

