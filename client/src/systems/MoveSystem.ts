// MoveSystem.ts

import { SetupResult } from "../mud/setup";
import { World } from "../world/World";

export async function setup(ctx: SetupResult, _world: World) {
  const {
    api: { moveBy },
  } = ctx;

  const listener = (e: KeyboardEvent) => {
    if (e.key === "ArrowUp") {
      moveBy(0, -1);
    }
    if (e.key === "ArrowDown") {
      moveBy(0, 1);
    }
    if (e.key === "ArrowLeft") {
      moveBy(-1, 0);
    }
    if (e.key === "ArrowRight") {
      moveBy(1, 0);
    }
  };

  window.addEventListener("keydown", listener);
}
