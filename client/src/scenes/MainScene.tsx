// MainScene.tsx

import * as PIXI from 'pixi.js';
import { useRef, useEffect } from 'react';
import { Viewport } from 'pixi-viewport';
import {TiledLoader} from '../pixi/tiled/TiledLoader'

import { config } from "../mud/config";
import { SetupResult } from "../mud/setup"
import { useMUD } from "../MUDContext";

import { World } from "../world/World";

import { setup as setupMoveSystem } from "../systems/MoveSystem"
import { setup as setupAgentSimpleAnimationSystem } from "../systems/AgentSimpleAnimationSystem";
import { setup as setupPlayerSystem } from "../systems/PlayerSystem";
import { setup as setupStatusSystem } from "../systems/StatusSystem";
import { setup as setupInteractionSystem } from "../systems/InteractionSystem";
import { setup as setupDebugSystem } from "../systems/DebugSystem";
import { setup as setupFollowUpSystem } from "../systems/FollowUpSystem";

const showLoading = (app: PIXI.Application):PIXI.DisplayObject=>{
  const loadingText = new PIXI.Text('Map loading...', {
      fontFamily: 'Arial',
      fontSize: 24,
      fill: 'white',
  });

  loadingText.anchor.set(0.5);
  loadingText.x = app.screen.width/2;
  loadingText.y = app.screen.height/2;

  app.stage.addChild(loadingText);

  return loadingText
}

const loadMap = async (ctx: SetupResult, app: PIXI.Application): Promise<[Viewport, PIXI.Container]> => {
    let loader = new TiledLoader();

    // Adjust the path to your actual map file and its assets
    let layer = await loader.load(`${ctx.publicURL}/assets/map3/Dunhuang_map.json`)

    console.log("layer width:", layer.width, "height:", layer.height);

    const viewport = new Viewport({
      screenWidth: app.view.width,
      screenHeight: app.view.height,
      worldWidth: layer.width, // Set to your map dimensions
      worldHeight: layer.height,
      events: app.renderer.events,
    });

    // activate plugins
    viewport
      .drag()
      .pinch()  
      .wheel()
      .decelerate()

    // center map
    viewport.moveCenter(layer.width/2, layer.height/2);
    
    viewport.addChild(layer);
    app.stage.addChild(viewport);

    loader.on("tile_click", (e: any)=>{
      layer.emit("click", e)
    })
    
    return [viewport, layer]
}

const setupGame = async (ctx: SetupResult, app: PIXI.Application, ready: (world: World)=>void):Promise<void>=> {
  let loading = showLoading(app)

  try {
    // load map
    let [viewport, map] = await loadMap(ctx, app)
    let world = new World(ctx.world, viewport, map, app.ticker, 32, 32)

    // setup sytems
    await setupMoveSystem(ctx, world)
    await setupPlayerSystem(ctx, world)
    await setupAgentSimpleAnimationSystem(ctx, world)
    await setupStatusSystem(ctx, world)
    await setupInteractionSystem(ctx, world)
    await setupFollowUpSystem(ctx, world)

    if (config.devMode) {
      await setupDebugSystem(ctx, world)
    }

    if (ready) {
      ready(world)
    }
  } finally {
    loading.removeFromParent()
  }
}

interface MainSceneProps {
  ready: (world: World)=>void
}

const MainScene = ({ready}:MainSceneProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const ctx = useMUD();

  useEffect(() => {
    const parentWidth = canvasRef.current!.parentElement!.clientWidth;
    const parentHeight = canvasRef.current!.parentElement!.clientHeight;

    const app = new PIXI.Application({
      view: canvasRef.current!,
      width: parentWidth,
      height: parentHeight,
      backgroundColor: "#438F53",
      autoStart: false, // 关闭自动渲染
      antialias: false,
      autoDensity: true // 确保渲染器大小与画布大小相同
    });

    // Scale mode for all textures, will retain pixelation
    PIXI.settings.SCALE_MODE = PIXI.SCALE_MODES.NEAREST;

    app.start();

    setupGame(ctx, app, ready)

    return () => {
      app.destroy(true);
    };
  }, []);

  return (
    <div style={{ width: "100%", height: "100%" }}>
      <canvas ref={canvasRef} />
    </div>
  );
};

export default MainScene;
