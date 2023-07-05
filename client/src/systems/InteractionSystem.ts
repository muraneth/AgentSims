// InteractionSystem.ts

import * as PIXI from 'pixi.js';
import {
  defineQuery,
  defineSystem,
  defineRxSystem,
  Has,
  getComponentValue,
  removeComponent,
  setComponent,
  EntityIndex
} from '@latticexyz/recs';
import { SetupResult } from "../mud/setup";
import { World } from "../world/World";

const CompomentName = "selected_outline";

export async function setup(ctx: SetupResult, world: World) {
  const {
    components: {Position, Agent, Selected, OutlineEffect},
  } = ctx;

 
  world.on("tile_click", (e: any)=>{
    console.log("tile click:", e)

    if (world.SelectedEntity) {
      setComponent(Selected, world.SelectedEntity, {
        value: false,
      })
    }

    world.SelectedEntity = undefined;
  })

  world.on("status_click", (e: any)=>{
    console.log("status click:", e)

    if (world.SelectedEntity) {
      setComponent(Selected, world.SelectedEntity, {
        value: false,
      })
    }

    world.SelectedEntity = e.targetEntity as EntityIndex;
    setComponent(Selected, e.targetEntity, {
      value: true,
    })
  })

  world.on("agent_click", (e: any)=>{
    console.log("agent click:", e)

    if (world.SelectedEntity) {
      setComponent(Selected, world.SelectedEntity, {
        value: false,
      })
    }

    world.SelectedEntity = e.targetEntity as EntityIndex;
    setComponent(Selected, e.targetEntity, {
      value: true,
    })
  })

  const originalLineWidth = 16;
  const radius = 4;

  const addBreathEffect = ():PIXI.DisplayObject => {
    const outline = new PIXI.Graphics();
    
    outline.lineStyle(originalLineWidth, 0x0000AA, 1);
    outline.drawEllipse(0, 0, radius, radius/4);
    outline.x = 0;
    outline.y = 0;

    return outline
  }

  defineSystem(ctx.world, [Has(Agent), Has(Position), Has(Selected)], (update) => {
    const entity = world.getOrCreateEntity(update.entity);

    const agent = getComponentValue(Agent, update.entity);
    const position = getComponentValue(Position, update.entity);
    const selected = getComponentValue(Selected, update.entity);

    if (agent && position && selected) {
      if (selected.value) {
        let outline = entity.getChildByName(CompomentName)
        if (outline) {
          outline.removeAllListeners();
          outline.removeFromParent();
        }

        outline = addBreathEffect()
        outline.name = CompomentName;
        outline.zIndex = 99;
        entity.addChild(outline);
  
        setComponent(OutlineEffect, update.entity, {
          speed: 0.005,
          scaleFactor: 1,
        })
      } else {
        let outline = entity.getChildByName(CompomentName)
        if (outline) {
          outline.removeAllListeners();
          outline.removeFromParent();
        }

        removeComponent(OutlineEffect, update.entity)
      }
    }
  });

  defineRxSystem(ctx.world, world.$update, (_delta: number)=>{
    let query = defineQuery([Has(OutlineEffect)], { runOnInit: true })
    let entities = query.matching;

    for (let entityIndex of entities) {
      const entity = world.getOrCreateEntity(entityIndex);
      const effect = getComponentValue(OutlineEffect, entityIndex);

      if (entity && effect) {
        let comp = entity.getChildByName(CompomentName)
        if (comp) {
          let outline = comp as PIXI.Graphics;
          let scaleFactor = effect.scaleFactor + effect.speed;

          // 限制呼吸效果的缩放范围
          if (scaleFactor > 1.1 || scaleFactor < 0.9) {
            setComponent(OutlineEffect, entityIndex, {
              speed : -effect.speed,
              scaleFactor: scaleFactor,
            })
          } else {
            setComponent(OutlineEffect, entityIndex, {
              speed : effect.speed,
              scaleFactor: scaleFactor,
            })
          }
  
          // 更新轮廓的缩放和透明度
          outline.scale.set(scaleFactor * 2); // 将轮廓的缩放设置为精灵尺寸的两倍
          outline.alpha = 1.3 - scaleFactor;
  
          // 更新轮廓的线宽
          const newLineWidth = originalLineWidth * scaleFactor;
          outline.clear();
          outline.lineStyle(newLineWidth, 0x0000AA, 1);
          outline.drawEllipse(0, 0, radius, radius/4);
        }
      }
    }
  })
  
}
