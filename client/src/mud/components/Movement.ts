import { defineComponent, Metadata, Type, World } from "@latticexyz/recs";

const Movement = {
  speed : Type.Number,
  targetX: Type.Number,
  targetY: Type.Number
} as const;

export function defineMovementComponent<M extends Metadata>(
  world: World,
  options?: { id?: string; metadata?: M; indexed?: boolean }
) {
  return defineComponent<typeof Movement, M>(world, {
    speed : Type.Number,
    targetX: Type.Number,
    targetY: Type.Number
  }, options);
}