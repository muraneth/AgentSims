// RotationSystem.ts

import * as PIXI from 'pixi.js';
import {
  defineQuery,
  defineSystem,
  defineRxSystem,
  Has,
  getComponentValue,
  removeComponent,
  setComponent,
} from '@latticexyz/recs';

import { SetupResult } from "../mud/setup";
import { World } from "../world/World";

import { clientComponents, contractComponents } from "../mud/components"
import { State as StateType } from "../mud/components/State";

const Agent = contractComponents.Agent;
const Position = contractComponents.Position;
const Movement = clientComponents.Movement;

const CompomentName = "animation";

export async function setup(ctx: SetupResult, world: World) {
  const tileWidth = world.TileWidth;
  const tileHeight = world.TileHeight;
  const spritesheet = await PIXI.Assets.load(`${ctx.publicURL}/assets/characters/characters&GUI.json`) as PIXI.Spritesheet;
  console.log("FightResultSystem init spritesheet:", spritesheet)

  await spritesheet.parse();

  const createAnimation = (actor: string, state: number)=>{
    let textures = new Array<PIXI.Texture>();

    switch (state) {
      case StateType.Idle:
        textures.push(spritesheet.textures[`${actor}_walk_forwards/${actor}_walk_forwards_02.png`])
        break;
      case StateType.WalkBackwards:
        textures = spritesheet.animations[`${actor}_walk_backwards/${actor}_walk_backwards`]
        break;
      case StateType.WalkEastwards:
        textures = spritesheet.animations[`${actor}_walk_eastwards/${actor}_walk_eastwards`]
        break;
      case StateType.WalkForwards:
        textures = spritesheet.animations[`${actor}_walk_forwards/${actor}_walk_forwards`]
        break;
      case StateType.WalkWestwards:
        textures = spritesheet.animations[`${actor}_walk_Westwards/${actor}_walk_Westwards`]
        break;
    }

    let animation = new PIXI.AnimatedSprite(
      textures,
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
      
      if (entity.x>0 && entity.y>0) {
        setComponent(Movement, update.entity, {
          targetX: position.x * tileWidth + tileWidth/2,
          targetY: position.y * tileHeight + tileHeight/2,
          speed: 0.4,
        })
      } else {
        entity.x = position.x * tileWidth + tileWidth/2;
        entity.y = position.y * tileHeight + tileHeight/2;
      }

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

  defineRxSystem(ctx.world, world.$update, (delta: number)=>{
    let query = defineQuery([Has(Movement)], { runOnInit: true })
    let entities = query.matching;

    for (let entityIndex of entities) {
      const entity = world.getOrCreateEntity(entityIndex);
      const movement = getComponentValue(Movement, entityIndex);

      if (entity && movement) {
        const dx = movement.targetX - entity.x;
        const dy = movement.targetY - entity.y;
        
        const distance = Math.sqrt(dx * dx + dy * dy);
        const step = movement.speed * delta;
  
        if (distance > step) {
          entity.x = entity.x + (dx / distance) * step;
          entity.y = entity.y + (dy / distance) * step;
        } else {
          entity.x = movement.targetX;
          entity.y = movement.targetY;

          removeComponent(Movement, entityIndex)
          setComponent(Position, entityIndex, {
            x: Math.round((entity.x-tileWidth/2)/tileWidth),
            y: Math.round((entity.y-tileHeight/2)/tileHeight),
          })
        }
      }
    }
  })
}

