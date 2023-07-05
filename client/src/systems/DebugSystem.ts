// DebugSystem.ts

import * as PIXI from 'pixi.js';
import { ethers } from "ethers";
import {
  getComponentValue,
} from '@latticexyz/recs';
import { terrainTypes, TerrainType } from "../terrainTypes";

import { SetupResult } from "../mud/setup";
import { World } from "../world/World";

export async function setup(ctx: SetupResult, world: World) {
  const {
    components: { MapConfig },
    singletonEntity,
  } = ctx;

  const mapConfig = getComponentValue(MapConfig, singletonEntity);

  if (mapConfig == null) {
    throw new Error(
      "game config not set or not ready, only use this hook after loading state === LIVE"
    );
  }
 
  const { width, height, terrain } = mapConfig;
  const terrainValues = Array.from(ethers.utils.toUtf8Bytes(terrain)).map(
    (value, index) => ({
      x: index % width,
      y: Math.floor(index / width),
      value,
      type: value in TerrainType ? terrainTypes[value as TerrainType] : null,
    })
  );

  for (let x=0; x<width; x++) {
    for (let y=0; y<height; y++) {
      const terrain = terrainValues.find(
        (t) => t.x === x && t.y === y
      )?.type;

      if (terrain?.emoji) {
        const rectangle = new PIXI.Graphics();
        rectangle.beginFill(0xFF0000, 0.5); // 设置填充颜色为红色，透明度为50%
        rectangle.drawRect(x*world.TileWidth, y*world.TileHeight, world.TileWidth, world.TileHeight); // 在(20, 20)位置绘制一个宽度为100，高度为50的矩形
        rectangle.endFill();

        world.EntityLayer.addChild(rectangle)
      }
    }
  }
}
