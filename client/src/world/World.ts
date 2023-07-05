import * as PIXI from 'pixi.js';
import { EntityID, EntityIndex } from '@latticexyz/recs';
import { Viewport } from 'pixi-viewport';
import { MudWorld } from '../mud/world';
import { Observable } from "rxjs";

export class World extends PIXI.utils.EventEmitter{
  private name: string;
  private description: string;
  private mudWorld: MudWorld;
  private entities: Map<EntityID, PIXI.Container>
  private viewport: Viewport;
  private mapLayer: PIXI.Container;
  private entityLayer: PIXI.Container;
  private ticker: PIXI.Ticker
  private tileWidth: number;
  private tileHeight: number;
  private selectedEntity: EntityIndex|undefined;

  public constructor(mudWorld: MudWorld, viewport: Viewport, map: PIXI.Container, ticker: PIXI.Ticker, tileWidth: number, tileHeight: number){
    super()

    this.name = "Anyoung AItown";
    this.description = "Anyoung AItown is An interactive sandbox game.Merge techs like openai-gpt4,latticexyz-mud to create a world for ai agents and allow human players to give prompt to agents."
    this.mudWorld = mudWorld;
    this.ticker = ticker;
    this.tileWidth = tileWidth;
    this.tileHeight = tileHeight;
    this.entityLayer = new PIXI.Container();
    this.entities = new Map<EntityID, PIXI.Container>();

    this.viewport = viewport;
    this.mapLayer = map;
    this.setupMapEvents()

    this.entityLayer.x = 0;
    this.entityLayer.y = 0;
    this.viewport.addChild(this.entityLayer)

    this.selectedEntity = undefined
  }

  private setupMapEvents() {
    this.MapLayer.on("click", (e: any)=>{
      if (e.type == "tile_click") {
        this.emit("tile_click", e)
      }
    })
  }

  public get Name() {
    return this.name
  }

  public get Description() {
    return this.description
  }

  public get Viewport () {
    return this.viewport
  }

  public get MapLayer () {
    return this.mapLayer
  }

  public get EntityLayer () {
    return this.entityLayer
  }

  public get TileWidth () {
    return this.tileWidth
  }

  public get TileHeight () {
    return this.tileHeight
  }

  public get SelectedEntity () {
    return this.selectedEntity
  }

  public set SelectedEntity (entityIndex: EntityIndex|undefined) {
    this.selectedEntity = entityIndex;
    
    this.emit("entity_selected", {
      entityIndex: entityIndex
    })
  }

  public get $update ():Observable<number> {
    const source = new Observable<number>((subscriber) => {
      this.ticker.add((ts:number)=>{
        subscriber.next(ts);
      })
    });

    return source
  }

  public getOrCreateEntity(index: EntityIndex): PIXI.Container {
    let entityId = this.mudWorld.entities[index]
    let entity = this.entities.get(entityId)

    if (!entity) {
      entity = new PIXI.Container()
      entity.x = 0;
      entity.y = 0;
      entity.sortableChildren = true;
      
      this.entityLayer.addChild(entity)
      this.entities.set(entityId, entity)
    }

    return entity;
  }
}