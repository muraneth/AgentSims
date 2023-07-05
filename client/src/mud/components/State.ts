import { defineComponent, Metadata, Type, World } from "@latticexyz/recs";

export enum State {
  Idle = 0,
  WalkWestwards = 1,
  WalkBackwards = 2,
  WalkEastwards = 3,
  WalkForwards = 4,
}

const StateType = {
  value: Type.Number,
} as const;

export function defineStateComponent<M extends Metadata>(
  world: World,
  options?: { id?: string; metadata?: M; indexed?: boolean }
) {
  return defineComponent<typeof StateType, M>(world, {
    value: Type.Number,
  }, options);
}