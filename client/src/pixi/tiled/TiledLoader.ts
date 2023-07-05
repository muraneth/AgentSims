import * as PIXI from "pixi.js";

export class TiledLoader extends PIXI.utils.EventEmitter{
  private texturesCache: { [key: string]: PIXI.Texture[] } = {};

  private async getTilesetTexture(tilesetId: number, tilesets: any[], basePath: string): Promise<PIXI.Texture> {
    const tileset = tilesets.find((tileset) => tileset.firstgid <= tilesetId && tilesetId < (tileset.firstgid + tileset.tilecount));
  
    if (!tileset) {
      throw new Error(`Tileset for tile id ${tilesetId} not found.`);
    }
  
    const textureKey = basePath + tileset.image;
    let textures: PIXI.Texture[] = [];

    if (this.texturesCache[textureKey]) {
      textures = this.texturesCache[textureKey];
    } else {
      const textureUrl = basePath + tileset.image;

      let texture = await PIXI.Assets.load(textureUrl);
      if (texture && texture.baseTexture) {
        texture.baseTexture.scaleMode = PIXI.SCALE_MODES.NEAREST;
      }

      const tilesPerRow = Math.floor((tileset.imagewidth - tileset.margin) / (tileset.tilewidth + tileset.spacing));
      const numRows = Math.ceil(tileset.tilecount / tilesPerRow);
    
      for (let row = 0; row < numRows; row++) {
        for (let col = 0; col < tilesPerRow; col++) {
          const x = tileset.margin + col * (tileset.tilewidth + tileset.spacing);
          const y = tileset.margin + row * (tileset.tileheight + tileset.spacing);
          const rect = new PIXI.Rectangle(x, y, tileset.tilewidth, tileset.tileheight);
          textures.push(new PIXI.Texture(texture.baseTexture, rect));
        }
      }

      this.texturesCache[textureKey] = textures;
    }
    
    return textures[tilesetId - tileset.firstgid];
  }
  
  private processTileId(_tileId: number): { tileId: number, flippedHorizontally: boolean, flippedVertically: boolean, flippedDiagonally: boolean, rotatedHexagonal120: boolean } {
    const FLIPPED_HORIZONTALLY_FLAG = 0x80000000;
    const FLIPPED_VERTICALLY_FLAG = 0x40000000;
    const FLIPPED_DIAGONALLY_FLAG = 0x20000000;
    const ROTATED_HEXAGONAL_120_FLAG = 0x10000000;
  
    const flippedHorizontally = (_tileId & FLIPPED_HORIZONTALLY_FLAG) !== 0;
    const flippedVertically = (_tileId & FLIPPED_VERTICALLY_FLAG) !== 0;
    const flippedDiagonally = (_tileId & FLIPPED_DIAGONALLY_FLAG) !== 0;
    const rotatedHexagonal120 = (_tileId & ROTATED_HEXAGONAL_120_FLAG) !== 0;
  
    // 清除所有翻转标志
    const tileId = _tileId & ~(FLIPPED_HORIZONTALLY_FLAG | FLIPPED_VERTICALLY_FLAG | FLIPPED_DIAGONALLY_FLAG);
  
    return { tileId, flippedHorizontally, flippedVertically, flippedDiagonally, rotatedHexagonal120  };
  }

  private async processLayers(parent: PIXI.Container, mapData: any, layers: any[], tilesets: any[], basePath: string): Promise<PIXI.Container[]> {
    const containers: PIXI.Container[] = [];

    for (const layer of layers) {
      if (layer.type === "tilelayer") {
        const tileLayerContainer = new PIXI.Container();

        if (layer.chunks) {
          for (const chunk of layer.chunks) {
            const data = chunk.data as number[];

            for (let y = 0; y < chunk.height; y++) {
              for (let x = 0; x < chunk.width; x++) {
                const tileIdWithFlags  = data[y * chunk.width + x];
                const { tileId, flippedHorizontally, flippedVertically, flippedDiagonally  } = this.processTileId(tileIdWithFlags);

                if (tileId !== 0) {
                  const tileTexture = await this.getTilesetTexture(tileId, tilesets, basePath);
                  const sprite = new PIXI.Sprite(tileTexture);

                  // 将精灵的锚点设置为中心
                  sprite.anchor.set(0.5, 0.5);
                  sprite.x = (x + chunk.x) * mapData.tilewidth + mapData.tilewidth / 2;
                  sprite.y = (y + chunk.y) * mapData.tileheight + mapData.tileheight / 2;

                  // 根据翻转标志设置精灵的缩放和旋转
                  sprite.scale.x = flippedHorizontally ? -1 : 1;
                  sprite.scale.y = flippedVertically ? -1 : 1;
                  if (flippedDiagonally) {
                    sprite.rotation = Math.PI / 2;
                    sprite.scale.x *= -1;
                  }

                  sprite.interactive = true;
                  sprite.cursor = "pointer"

                  sprite.on('pointerdown', (e: any) => {
                    this.handleTileClick(parent, mapData, e);
                  });

                  sprite.on("mousedown", (e: any)=>{
                    e.target.cursor = "grab"
                  })
              
                  sprite.on("mouseup", (e: any)=>{
                    e.target.cursor = "pointer"
                  })

                  tileLayerContainer.addChild(sprite);
                }
              }
            }
          }
        } else {
          const data = layer.data as number[];

          for (let y = 0; y < layer.height; y++) {
            for (let x = 0; x < layer.width; x++) {
              const tileIdWithFlags  = data[y * layer.width + x];
              const { tileId, flippedHorizontally, flippedVertically, flippedDiagonally  } = this.processTileId(tileIdWithFlags);

              if (tileId !== 0) {
                const tileTexture = await this.getTilesetTexture(tileId, tilesets, basePath);
                const sprite = new PIXI.Sprite(tileTexture);

                // 将精灵的锚点设置为中心
                sprite.anchor.set(0.5, 0.5);
                sprite.x = x * mapData.tilewidth + mapData.tilewidth / 2;
                sprite.y = y * mapData.tileheight + mapData.tileheight / 2;


                // 根据翻转标志设置精灵的缩放和旋转
                sprite.scale.x = flippedHorizontally ? -1 : 1;
                sprite.scale.y = flippedVertically ? -1 : 1;
                if (flippedDiagonally) {
                  sprite.rotation = Math.PI / 2;
                  sprite.scale.x *= -1;
                }

                sprite.interactive = true;
                sprite.cursor = "pointer"

                sprite.on('pointerdown', (e: any) => {
                  this.handleTileClick(parent, mapData, e);
                });

                sprite.on("mousedown", (e: any)=>{
                  e.target.cursor = "grab"
                })
            
                sprite.on("mouseup", (e: any)=>{
                  e.target.cursor = "pointer"
                })

                tileLayerContainer.addChild(sprite);
              }
            }
          }
        }

        containers.push(tileLayerContainer);
      } else if (layer.type === "group") {
        const groupContainers = await this.processLayers(parent, mapData, layer.layers, tilesets, basePath);
        containers.push(...groupContainers);
      }
    }

    return containers;
  }

  private handleTileClick(_parent:PIXI.Container, mapData:any, e:any) {
    console.log("source event:", e)

    this.emit("tile_click", {
      type: "tile_click",
      tile_x: Math.round(e.target.x/mapData.tilewidth),
      tile_y: Math.round(e.target.y/mapData.tileheight)
    })
  }

  public async load(url: string): Promise<PIXI.Container> {
    const mapData = await PIXI.Assets.load(url);
    const basePath = new URL(url).origin + new URL(url).pathname.split('/').slice(0, -1).join('/') + '/';
    const container = new PIXI.Container();

    // Add map dimensions to the container
    container.width = mapData.width * mapData.tilewidth;
    container.height = mapData.height * mapData.tileheight;

    const layers = await this.processLayers(container, mapData, mapData.layers, mapData.tilesets, basePath);

    for (const layer of layers) {
      container.addChild(layer);
    }

    return container;
  }
}
