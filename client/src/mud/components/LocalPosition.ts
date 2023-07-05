import { defineComponent, Metadata, Type, World } from "@latticexyz/recs";

const LocalPosition = {
  x: Type.Number,
  y: Type.Number,
} as const;

export function defineLocalPositionComponent<M extends Metadata>(
  world: World,
  options?: { id?: string; metadata?: M; indexed?: boolean }
) {
  return defineComponent<typeof LocalPosition, M>(world, {
    x : Type.Number,
    y: Type.Number,
  }, options);
}