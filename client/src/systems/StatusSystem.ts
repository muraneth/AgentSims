// StatusSystem.ts

import * as PIXI from 'pixi.js';
import {
  defineSystem,
  Has,
  getComponentValue,
} from '@latticexyz/recs';

import { SetupResult } from "../mud/setup";
import { World } from "../world/World";

import { contractComponents } from "../mud/components"

const Agent = contractComponents.Agent;
const Position = contractComponents.Position;
const Status = contractComponents.Status;

const marginWidth = 8
const StatusComponentName = "status";

export async function setup(ctx: SetupResult, world: World) {
  const spritesheet = await PIXI.Assets.load(`${ctx.publicURL}/assets/chat/chat.json`) as PIXI.Spritesheet;
  console.log("ChatSystem init spritesheet:", spritesheet)

  await spritesheet.parse();

  let chatBgLeft = spritesheet.textures["Medium_01.png"]
  let chatBgMid = spritesheet.textures["Medium_03.png"]
  let chatBgRight = spritesheet.textures["Medium_02.png"]

  const createBackground = (width: number) => {
    const background = new PIXI.Container();
  
    const leftEdge = new PIXI.Sprite(chatBgLeft);
    const middle = new PIXI.Sprite(chatBgMid);
    const rightEdge = new PIXI.Sprite(chatBgRight);
  
    middle.width = width - leftEdge.width - rightEdge.width;
    middle.scale.x = middle.width / chatBgMid.width;
    middle.x = leftEdge.width;
  
    rightEdge.x = leftEdge.width + middle.width;
  
    background.addChild(leftEdge);
    background.addChild(middle);
    background.addChild(rightEdge);
  
    return background;
  }

  const createStatus = (name: string, textContent: string)=>{
    const billboard = new PIXI.Container();

    const nameStyle = new PIXI.TextStyle({
      fontFamily: "Helvetica",
      fontSize: 7,
      fill: "#ff9300",
    });

    
    const contentStyle = new PIXI.TextStyle({
      fontFamily: "Helvetica",
      fontSize: 7,
      fill: "black"
    });
  
    const nameText = new PIXI.Text(name, nameStyle);
    const contentText = new PIXI.Text(textContent, contentStyle);

    let backgroupWidth = Math.max(contentText.width, nameText.width)
    contentText.x = marginWidth + (backgroupWidth-contentText.width)/2;
    contentText.y = 17
    nameText.x = marginWidth + (backgroupWidth-nameText.width)/2;
    nameText.y = 8;

    const background = createBackground(backgroupWidth + marginWidth*2);
    billboard.addChild(background);
    billboard.addChild(nameText);
    billboard.addChild(contentText);

    return billboard;
  }

  defineSystem(ctx.world, [Has(Position), Has(Status)], (update) => {
    const entity = world.getOrCreateEntity(update.entity)
    const position = getComponentValue(Position, update.entity);
    const status = getComponentValue(Status, update.entity);
    const agent = getComponentValue(Agent, update.entity);

    if (agent && position && status) {
      let statusTips = createStatus(agent.name, status.value)
      statusTips.name = StatusComponentName
      statusTips.x = -statusTips.width/2;
      statusTips.y = -statusTips.height-16;

      let oldStatus = entity.getChildByName(StatusComponentName)
      if (oldStatus) {
        oldStatus.removeAllListeners();
        oldStatus.removeFromParent()
      }

      statusTips.zIndex = 100;
      statusTips.interactive = true;
      statusTips.cursor = "pointer";

      statusTips.on('pointerdown', (e: any) => {
        console.log("statusTips pointerdown:", e)

        world.emit("status_click", {
          targetEntity: update.entity,
          agent: agent,
          position: position,
          status: status,
          rawEvent: e,
        })
      });

      entity.addChild(statusTips);
    }
  });
}
